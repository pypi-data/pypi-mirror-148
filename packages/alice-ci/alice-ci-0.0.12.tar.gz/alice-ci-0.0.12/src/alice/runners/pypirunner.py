from distutils.command.config import config
from distutils.log import debug
import json
import logging
from ntpath import join
import os
import re
import subprocess
import sys
from pkg_resources import parse_version
from requests import get
from requests.auth import HTTPBasicAuth
from os import environ, path
from html.parser import HTMLParser
from alice.runners.pyutils import PackageManager, glob, grab_from
from alice.exceptions import ConfigException, RunnerError
import hashlib
from pathlib import Path


def md5_update_from_file(filename, hash):
    assert Path(filename).is_file()
    with open(str(filename), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash


def md5_file(filename):
    return md5_update_from_file(filename, hashlib.md5()).hexdigest()


def md5_update_from_dir(directory, hash, exclude_dirs, exclude_extensions, exclude_dirs_wildcard):
    assert Path(directory).is_dir()
    for _path in os.listdir(directory):
        path = os.path.join(directory, _path)        
        if os.path.isfile(path) :
            hash.update(_path.encode())
            logging.debug(f"[PyPiRunner][Hash] File: {path}")
            hash = md5_update_from_file(path, hash)
        elif os.path.isdir(path):
            skip = False
            for name in exclude_dirs:
                if name in os.path.basename(_path):
                    skip = True
            if not skip:
                hash = md5_update_from_dir(path, hash, exclude_dirs, exclude_extensions, exclude_dirs_wildcard)
    return hash


def md5_dir(directory, exclude_dirs=[], exclude_extensions=[], exclude_dirs_wildcard=[]):
    return md5_update_from_dir(directory, hashlib.sha1(), exclude_dirs, exclude_extensions, exclude_dirs_wildcard).hexdigest()


def get_uri(config, default):
    url = config.get("repo", {}).get("uri", default)
    if url is not None:
        if not isinstance(url, str):
            url = grab_from(url)
        if not re.match('(?:http|ftp|https)://', url):
            url = f"https://{url}"
    return url


def get_user(config, default):
    if "repo" in config:
        if "username" in config["repo"]:
            data = config["repo"]["username"]
            if isinstance(data, str):
                return data
            else:
                return grab_from(data)
    return default


def get_pass(config, default):
    if "repo" in config:
        if "password" in config["repo"]:
            data = config["repo"]["password"]
            if isinstance(data, str):
                return data
            else:
                return grab_from(data)
    return default


class SimpleRepoParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.packages = []

    def handle_data(self, data):
        re_groups = re.findall("(\d*\.\d*\.\d*)", data)
        if len(re_groups) == 1:
            file_version = re_groups[0]
            if file_version not in self.packages:
                self.packages.append(file_version)


# Parses and stores the config from yaml
class PypiConfig:
    def __init__(self, config={}) -> None:
        self.workdir = path.abspath(config.get("workdir", "."))
        self.repo_uri = get_uri(config, None)
        self.repo_user = get_user(config, None)
        self.repo_pass = get_pass(config, None)
        self.packages = set(config.get("packages", []))
        self.upload = config.get("upload", False)
        self.fail_if_exists = config.get("fail_if_exists", False)

    # returns a PyPiConfig with merged values
    def copy(self, job_config={}):
        p = PypiConfig()
        p.workdir = path.abspath(path.join(self.workdir, job_config.get("workdir", ".")))
        p.repo_uri = get_uri(job_config, self.repo_uri)
        p.repo_user = get_user(job_config, self.repo_user)
        p.repo_pass = get_pass(job_config, self.repo_pass)
        job_pkg_set = set(job_config["packages"])
        job_pkg_set.update(self.packages)
        p.packages = job_pkg_set
        p.upload = job_config.get("upload", self.upload)
        p.fail_if_exists = job_config.get("fail_if_exists", self.fail_if_exists)
        return p


# TODO: Refactor to something sensible, more flexible
class PackageMeta:
    def __init__(self):
        self.conf_dir = path.join(os.getcwd(), ".alice", "pypirunner")
        self.metafile = path.join(self.conf_dir, "packagemeta.json")
        if not path.isdir(self.conf_dir):
            os.mkdir(self.conf_dir)
        if path.isfile(self.metafile):
            with open(self.metafile) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
            self.__save()

    def __save(self):
        with open(self.metafile, 'w') as f:
            json.dump(self.metadata, f)

    def get(self, package, key):
        return self.metadata.get(package, {}).get(key, "")

    def set(self, package, key, value):
        if package not in self.metadata:
            self.metadata[package] = {}
        self.metadata[package][key] = value
        self.__save()


# TODO: consider "--skip-existing" flag for twine
class PyPiRunner():
    def __init__(self, config) -> None:
        logging.info("[PyPiRunner] Initializing")
        self.workdir = config["workdir"]
        self.config = PypiConfig(config)
        self.metadata = PackageMeta()

    def __versions(self, config, pkg_name):
        repo = config.repo_uri
        if repo is None:
            repo = "https://pypi.python.org/pypi"

        if config.repo_pass is not None and config.repo_user is not None:
            logging.info(f"[PyPiRunner][Versions] Set auth headers from config")
            logging.debug(f"[PyPiRunner][Versions] Auth: {config.repo_user}:{config.repo_pass}")
            auth = HTTPBasicAuth(config.repo_user, config.repo_pass)
        else:
            logging.info(f"[PyPiRunner][Versions] No auth headers in config, skip")
            logging.debug(f"[PyPiRunner][Versions] Auth: {config.repo_user}:{config.repo_pass}")
            auth = None

        try:
            if repo.endswith("pypi"):
                url = f'{repo}/{pkg_name}/json'
                logging.info(f"[PyPiRunner][Versions] Trying JSON API at {url}")
                response = get(url, auth=auth)
                if response.status_code == 200:
                    releases = json.loads(response.text)["releases"]
                    return sorted(releases, key=parse_version, reverse=True)
                else:
                    logging.info(f"[PyPiRunner][Versions] JSON failed: [{response.status_code}]")
                    logging.debug(response.text)
                    repo = f"{repo}/simple"
            url = f"{repo}/{pkg_name}"
            logging.info(f"[PyPiRunner][Versions] Trying Simple API at {url}")
            response = get(url, auth=auth)
            if response.status_code == 200:
                parser = SimpleRepoParser()
                parser.feed(response.text)
                return sorted(parser.packages, key=parse_version, reverse=True)
            if response.status_code == 404:
                return []
            else:
                logging.info(f"[PyPiRunner][Versions] Simple failed: [{response.status_code}]")
                logging.debug(response.text)
                raise Exception("Failed to fetch available versions")
            
        except Exception as e:
            raise RunnerError(f"{url}: {e}")        

    def build(self, config, package):
        print(f"[PyPiRunner] Building {package}")
        pkg_path = path.join(config.workdir, package)
        if not path.isdir(pkg_path):
            raise ConfigException(f"Path does not exists: {pkg_path}")
        PackageManager.getInstance().ensure("build")
        command = [sys.executable, "-m", "build", package]
        if logging.root.isEnabledFor(logging.DEBUG):
            with subprocess.Popen(command, cwd=config.workdir) as p:
                p.wait()
                if p.returncode != 0:
                    raise RunnerError(f"[PyPiRunner] Failed to build {package}")
        else:
            with subprocess.Popen(command, cwd=config.workdir, stdout=subprocess.PIPE) as p:
                p.wait()
                if p.returncode != 0:
                    raise RunnerError(f"[PyPiRunner] Failed to build {package}")
        print(f"[PyPiRunner] Package {package} built")

    def find_unuploaded(self, config, file_list, pkg_name):
        versions = self.__versions(config, pkg_name)
        unuploaded = []
        for file in file_list:
            # flake8: noqa W605
            re_groups = re.findall("(\d*\.\d*\.\d*)", file)
            if len(re_groups) < 1:
                raise RunnerError(f"Unable to determine version of file {file}")
            file_version = re_groups[0]
            if file_version not in versions:
                unuploaded.append(file)
            else:
                print(f"[PyPiRunner] File already uploaded: {os.path.basename(file)}")
        print(f"[PyPiRunner] Packages to publish: {', '.join(unuploaded) if len(unuploaded) > 1 else 'None'}")
        return unuploaded

    def upload_command(self, config, package, _command, to_upload):
        unregistered = False
        command = _command + to_upload
        with subprocess.Popen(command, cwd=config.workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            p.wait()
            if p.returncode != 0:
                for line in map(lambda x: x.decode('utf8').strip(), p.stderr):
                    if "405 Method Not Allowed" in line:
                        unregistered = True
                if not unregistered:
                    print("STDOUT:")
                    sys.stdout.buffer.write(p.stdout.read())
                    print("STDERR:")
                    sys.stdout.buffer.write(p.stderr.read())
                    raise RunnerError(f"[PyPiRunner] Failed to upload {package} ({p.returncode})")
        if unregistered:
            print("[PyPiRunner] Registering package")
            register_command = [sys.executable, "-m", "twine", "register", "--verbose", "--non-interactive"]
            if config.repo_uri is not None:
                register_command.append("--repository-url")
                register_command.append(config.repo_uri)
            if config.repo_user is not None and config.repo_pass is not None:
                register_command.append("-u")
                register_command.append(config.repo_user)
                register_command.append("-p")
                register_command.append(config.repo_pass)
            register_command.append(to_upload[0])
            with subprocess.Popen(register_command, cwd=config.workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
                p.wait()
                if p.returncode != 0:
                    print("STDOUT:")
                    sys.stdout.buffer.write(p.stdout.read())
                    print("STDERR:")
                    sys.stdout.buffer.write(p.stderr.read())
                    raise RunnerError(f"[PyPiRunner] Failed to register {package} ({p.returncode})")
            self.upload_command(config, package, _command, to_upload)

    def upload(self, config, package, current_version):
        print(f"[PyPiRunner] Uploading {package}")
        PackageManager.getInstance().ensure("twine")
        command = [sys.executable, "-m", "twine", "upload", "--verbose", "--non-interactive"]
        if config.repo_uri is not None:
            command.append("--repository-url")
            command.append(config.repo_uri)
        if config.repo_user is not None and config.repo_pass is not None:
            command.append("-u")
            command.append(config.repo_user)
            command.append("-p")
            command.append(config.repo_pass)
        else:
            raise RunnerError("[PyPiRunner] Can't upload without credentials!")
        
        dist_path = os.path.abspath(os.path.join(config.workdir, package, "dist"))
        _files = glob(os.path.join(dist_path, "*"), config.workdir)
        files = []
        for file in _files:
            if current_version in os.path.basename(file):
                files.append(file)
                print(f"[PyPiRunner] Found: {file}")
            else:
                logging.info(f"[PyPiRunner] Dropped: {file} doesn't match current version: {current_version}")

        to_upload = self.find_unuploaded(config, files, package)
        if len(to_upload) == 0:
            return
        #command += to_upload
        self.upload_command(config, package, command, to_upload)
        print(f"[PyPiRunner] Uploaded {package}")

    def package_version(self, config, package):
        cfg_path = path.join(config.workdir, package, "setup.cfg")
        with open(cfg_path) as f:
            for line in f:
                if line.startswith("version"):
                    re_groups = re.findall("(\d*\.\d*\.\d*)", line)
                    if len(re_groups) < 1:
                        raise RunnerError(f"Unable to determine version of package:  |{line}|")
                    return re_groups[0]

    def run(self, job_spec):
        job_config = self.config.copy(job_spec)
        
        for package in job_config.packages:
            pkg_dir = path.join(job_config.workdir, package)
            pkg_hash = md5_dir(pkg_dir, exclude_dirs=["pycache", "pytest_cache", "build", "dist", "egg-info"])
            logging.debug(f"[PyPiRunner] {package} hash: {pkg_hash}")
            pkg_version = self.package_version(job_config, package)
            logging.debug(f"[PyPiRunner] {package} local version: {pkg_version}")
            repo_versions = self.__versions(job_config, package)
            logging.debug(f"[PyPiRunner] {package} remote version: {repo_versions}")

            if pkg_version not in repo_versions:
                print(f"[PyPiRunner] {package} not found in repo")
                self.build(job_config, package)
                self.metadata.set(package, pkg_version, pkg_hash)
            else:
                if pkg_hash != self.metadata.get(package, pkg_version):
                    self.build(job_config, package)
                    self.metadata.set(package, pkg_version, pkg_hash)
                else:
                    print(f"[PyPiRunner] {package} Unchanged since last build")

            if job_config.upload:
                self.upload(job_config, package, pkg_version)
            else:
                print(f"[PyPiRunner] Upload disabled, skipping")
