import logging
import subprocess
import docker
from os.path import join, isdir
from os import getcwd, mkdir
import os
import requests
import platform
import time

from ..exceptions import RunnerError
from ..config import ConfigHolder


pipconf = """[global]
index-url = URL
trusted-host = BASE
               pypi.org
extra-index-url= http://pypi.org/simple"""


class RepoConfig:
    def __init__(self, config={}) -> None:
        self.port = config.get("port", 8888)
        self.enabled = config.get("enabled", True)
        self.container_name = config.get("container_name", "alice-pypiserver")

    def copy(self, job_config):
        r = RepoConfig()
        r.container_name = job_config.get("container_name", self.container_name)
        r.enabled = job_config.get("enabled", self.enabled)
        r.port = job_config.get("port", self.port)
        return r


class PypiRepoRunner:
    def __init__(self, config) -> None:
        logging.info("[PyPiRepo] Initializing")
        self.config = RepoConfig(config)
        self.client = docker.from_env()
        self.user = "alice"
        self.passwd = "alice"
        self.htpasswd = 'alice:{SHA}UisnajVr3zkBPfq+os1D4UHsyeg='

    def get_image(self):
        # TODO: remove when resolved:
        # Official Docker image support for ARM?
        # https://github.com/pypiserver/pypiserver/issues/364
        pypiserver = "https://github.com/pypiserver/pypiserver.git"
        if platform.machine() == "aarch64":
            tag = "alice.localhost/pypiserver:arm"
            try:
                self.client.images.get(tag)
                return tag
            except docker.errors.ImageNotFound:
                print("[PyPiRepo] Building PyPiServer ARM image, this could take a while")
                workdir = join(getcwd(), ".alice", "pypirepo", "source")
                if not os.path.isdir(workdir):
                    os.mkdir(workdir)
                git_command = ["git", "clone", pypiserver, "--branch=v1.3.2"]
                output = []
                with subprocess.Popen(git_command, cwd=workdir, stdout=subprocess.PIPE) as p:
                    for line in p.stdout:
                        output.append(line.decode('utf8').strip())
                    p.wait()
                    if p.returncode != 0:
                        print("\n".join(output))
                        raise(RunnerError("[PyPiRepo] Could not fetch pypiserver source"))
                source_path = os.path.join(workdir, "pypiserver")
                self.client.images.build(path=source_path, tag=tag)
                return tag
        else:
            return "pypiserver/pypiserver:latest"

    def run(self, job_spec):
        job_config = self.config.copy(job_spec)
        docker_host_ip = None
        for network in self.client.networks.list():
            if network.name == "bridge":
                try:
                    docker_host_ip = network.attrs["IPAM"]["Config"][0]["Gateway"]
                except KeyError:
                    docker_host_ip = network.attrs["IPAM"]["Config"][0]["Subnet"].replace(".0/16", ".1")
        if docker_host_ip is None:
            raise RunnerError("Unable to determine Docker host IP")

        if job_config.enabled:
            try:
                c = self.client.containers.get(job_config.container_name)
                print(f"[PyPiRepo] {job_config.container_name} already running")
            except docker.errors.NotFound:
                persistency_dir = join(getcwd(), ".alice", "pypirepo")
                if not isdir(persistency_dir):
                    mkdir(persistency_dir)

                package_dir = join(persistency_dir, "packages")
                if not isdir(package_dir):
                    mkdir(package_dir)

                htpasswd_file = join(persistency_dir, ".htpasswd")
                with open(htpasswd_file, 'w') as f:
                    f.write(self.htpasswd)

                c = self.client.containers.run(
                    name=job_config.container_name,
                    image=self.get_image(),
                    detach=True,
                    labels={"app": "alice"},
                    command=["--overwrite", "-P", ".htpasswd", "packages"],
                    ports={"8080/tcp": job_config.port},
                    volumes={
                        package_dir: {
                            "bind": "/data/packages",
                            "mode": "rw"
                        },
                        htpasswd_file: {
                            "bind": "/data/.htpasswd",
                            "mode": "ro"
                        }
                    },
                    restart_policy={
                        "Name": "unless-stopped"
                    }
                )
                print(f"[PyPiRepo] Started {job_config.container_name}")

            c.reload()
            logging.info(f"[PyPiRepo] {job_config.container_name} : {c.status}")
            if c.status != "running":
                raise RunnerError(f"[PyPiRepo] Repo container unstable: {c.status}")

            uri = f"http://localhost:{job_config.port}"
            unreachable = True
            attempts = 0
            while unreachable and attempts < 5:
                attempts += 1                
                try:
                    requests.get(uri)
                    unreachable = False
                except Exception as e:
                    logging.info(f"[PyPiRepo] {attempts} - Repo at {uri} is unavailable: {e}")
                    time.sleep(2)
            if unreachable:
                raise RunnerError(f"[PyPiRepo] Repo unreachable")


            cfgh = ConfigHolder.getInstance()
            cfgh.soft_set("PYPI_USER", self.user)
            cfgh.soft_set("PYPI_PASS", self.passwd)
            cfgh.soft_set("PYPI_REPO", uri)
            cfgh.soft_set("DOCKER_PYPI_USER", self.user)
            cfgh.soft_set("DOCKER_PYPI_PASS", self.passwd)
            cfgh.soft_set("DOCKER_PYPI_REPO", f"http://{docker_host_ip}:{job_config.port}")
            cfgh.commit()

            venv = join(os.getcwd(), "venv")
            if os.path.isdir(venv):
                netloc = f"localhost:{job_config.port}"
                url = f"http://{self.user}:{self.passwd}@{netloc}"
                conf = pipconf.replace("URL", url).replace("BASE", netloc)

                if os.name == "nt":  # Windows
                    filename = join(venv, "pip.ini")
                else:  # Linux & Mac
                    filename = join(venv, "pip.conf")
                with open(filename, 'w') as f:
                    f.write(conf)
                print(f"[PyPiRepo] pip conf written to {filename}")
