import logging
import docker
from os.path import join, isdir
from os import getcwd, mkdir
import os

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
        logging.info("[PythonRunner] Initializing")
        self.config = RepoConfig(config)
        self.client = docker.from_env()
        self.user = "alice"
        self.passwd = "alice"
        self.htpasswd = 'alice:{SHA}UisnajVr3zkBPfq+os1D4UHsyeg='

    def __is_running(self, name):
        try:
            self.client.containers.get(name)
            return True
        except docker.errors.NotFound:
            return False

    def run(self, job_spec):
        job_config = self.config.copy(job_spec)
        running = self.__is_running(job_config.container_name)
        print(f"[PyPiRepo] {job_config.container_name} running: {running}")

        persistency_dir = join(getcwd(), ".alice", "pypirepo")
        if not isdir(persistency_dir):
            mkdir(persistency_dir)

        package_dir = join(persistency_dir, "packages")
        if not isdir(package_dir):
            mkdir(package_dir)

        htpasswd_file = join(persistency_dir, ".htpasswd")
        with open(htpasswd_file, 'w') as f:
            f.write(self.htpasswd)

        docker_host_ip = None
        for network in self.client.networks.list():
            if network.name == "bridge":
                docker_host_ip = network.attrs["IPAM"]["Config"][0]["Gateway"]
        if docker_host_ip is None:
            raise RunnerError("Unable to determine Docker host IP")

        if job_config.enabled:
            if not running:
                c = self.client.containers.run(
                    name=job_config.container_name,
                    image="pypiserver/pypiserver:latest",
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
                c.reload()
                print(f"[PyPiRepo] {job_config.container_name} : {c.status}")
            cfgh = ConfigHolder.getInstance()
            cfgh.soft_set("PYPI_USER", self.user)
            cfgh.soft_set("PYPI_PASS", self.passwd)
            cfgh.soft_set("PYPI_REPO", f"http://localhost:{job_config.port}")
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
