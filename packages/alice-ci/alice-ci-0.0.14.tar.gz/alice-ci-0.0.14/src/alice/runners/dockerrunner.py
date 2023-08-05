from enum import Enum
import json
import logging
from os import path, getcwd
import docker

from .pyutils import grab_from, gen_dict
from ..exceptions import ConfigException, NonZeroRetcode, RunnerError


class ImageSource(Enum):
    NONE = 1
    BUILD = 2
    PULL = 3


def get_user(config, default):
    if "credentials" in config:
        if "username" in config["credentials"]:
            data = config["credentials"]["username"]
            if isinstance(data, str):
                return data
            else:
                return grab_from(data)
    return default


def get_pass(config, default):
    if "credentials" in config:
        if "password" in config["credentials"]:
            data = config["credentials"]["password"]
            if isinstance(data, str):
                return data
            else:
                return grab_from(data)
    return default


def get_provider(config, default, default_type):
    if "image" in config:
        build = False
        pull = False
        candidate_type = default_type
        if "build" in config["image"]:
            build = True
            if default_type == ImageSource.BUILD:
                candidate = default.copy(config["image"]["build"])
            else:
                candidate = Builder(config["image"]["build"])
                candidate_type = ImageSource.BUILD
        elif "pull" in config["image"]:
            pull = True
            if default_type == ImageSource.PULL:
                candidate = default.copy(config["image"]["pull"])
            else:
                candidate = Puller(config["image"]["pull"])
                candidate_type = ImageSource.PULL

        if build and pull:
            raise ConfigException("[DockerRunner] Can't build and pull the same image!")

        return candidate, candidate_type
    return default, default_type


class Tagger:
    def __init__(self, config={}) -> None:
        self.name = config.get("name", None)
        self.username = get_user(config, None)
        self.password = get_pass(config, None)
        self.publish = config.get("publish", False)

    def copy(self, job_config):
        t = Tagger()
        t.name = job_config.get("name", self.name)
        t.username = get_user(job_config, self.username)
        t.password = get_pass(job_config, self.password)
        t.publish = job_config.get("publish", self.publish)
        return t

    def __str__(self) -> str:
        data = {
            "name": self.name,
            "publish": self.publish,
            "credentials": {
                "username": self.username,
                "password": self.password
            }
        }
        return f"{data}"

    def handle(self, client, image):
        if self.name is not None:
            if self.name not in image.tags and f"{self.name}:latest" not in image.tags:
                print(f"[DockerRunner] Tagging {image.tags[0]} as {self.name}")
                image.tag(self.name)
        if self.publish:
            print(f"[DockerRunner] Pushing {self.name}")
            client.push(self.name)


class Builder():
    def __init__(self, config) -> None:
        self.dir = path.abspath(config.get("dir", getcwd()))
        self.dockerfile = config.get("dockerfile", None)
        self.name = config.get("name", None)
        self.args = gen_dict(config.get("args", []))

    def copy(self, job_config):
        b = Builder({})
        b.dir = path.abspath(path.join(self.dir, job_config.get("dir", ".")))
        b.dockerfile = job_config.get("dockerfile", self.dockerfile)
        b.name = job_config.get("name", self.name)
        b.args = self.args.copy().update(gen_dict(job_config.get("args", [])))
        return b

    def __str__(self) -> str:
        data = {
            "type": "builder",
            "dir": self.dir,
            "dockerfile": self.dockerfile,
            "name": self.name,
            "args": self.args
        }
        return json.dumps(data)

    def prepare(self, client):
        print(f"[DockerRunner] Building image {self.name}")
        if self.dockerfile is None:
            self.dockerfile = "Dockerfile"
        try:
            image, log = client.images.build(path=self.dir,
                                             dockerfile=self.dockerfile,
                                             tag=self.name,
                                             buildargs=self.args,
                                             labels={"builder": "alice-ci"})
            for i in log:
                logging.debug(i)
            return image
        except docker.errors.BuildError as e:
            raise RunnerError(f"[DockerRunner] Build failed: {e}")
        except docker.errors.APIError as e:
            raise RunnerError(f"[DockerRunner] Error: {e}")


class Puller():
    def __init__(self, config={}) -> None:
        self.name = config.get("name", None)
        self.username = get_user(config, None)
        self.password = get_pass(config, None)

    def copy(self, job_config={}):
        p = Puller()
        p.name = job_config.get("name", self.name)
        p.username = get_user(job_config, self.username)
        p.password = get_pass(job_config, self.password)

    def __str__(self) -> str:
        data = {
            "name": self.name,
            "credentials": {
                "username": self.username,
                "password": self.password
            }
        }
        return f"{data}"

    def prepare(self, client):
        print(f"[DockerRunner] Pulling image {self.name}")
        return client.images.pull(self.name)


class DockerConfig:
    def __init__(self, config={}) -> None:
        self.username = get_user(config, None)
        self.password = get_pass(config, None)
        self.image_provider, self.provider_type = get_provider(config, None, ImageSource.NONE)
        self.tagger = Tagger(config.get("tag", {}))
        self.commands = config.get("commands", [])
        self.env = config.get("env", {})

    def copy(self, job_config={}):
        d = DockerConfig()
        d.username = get_user(job_config, self.username)
        d.password = get_pass(job_config, self.password)
        d.image_provider, d.provider_type = get_provider(job_config, self.image_provider, self.provider_type)
        d.tagger = self.tagger.copy(job_config.get("tag", {}))
        d.commands = self.commands.copy() + job_config.get("commands", [])
        d.env = self.env.copy()
        d.env.update(gen_dict(job_config.get("env", [])))
        return d

    def __str__(self) -> str:
        data = {
            "credentials": {
                "username": {self.username},
                "password": {self.password}
            },
            "image": self.image_provider.__str__(),
            "commands": self.commands,
            "tag": self.tagger.__str__()
        }
        return f"{data}"


class DockerRunner():
    def __init__(self, config) -> None:
        logging.info("[DockerRunner] Initializing")
        self.config = DockerConfig(config)
        self.client = docker.from_env()

    def run(self, job_spec):
        job_config = self.config.copy(job_spec)
        logging.debug(f"[DockerRunner] Job config: {job_config.__str__()}")
        if job_config.image_provider is None:
            raise RunnerError("[DockerRunner] No image provider configured!")
        image = job_config.image_provider.prepare(self.client)
        logging.info(f"[DockerRunner] Image: {image.tags} ({image.id})")

        if len(job_config.commands) > 0:
            if "PATH" in job_config.env:
                del job_config.env["PATH"]
            container = self.client.containers.run(image=image.id,
                                                   entrypoint=["sleep", "infinity"],
                                                   detach=True,
                                                   auto_remove=True)
            try:
                for i in job_config.commands:
                    command = ["/bin/sh", "-c", i]
                    logging.debug(f"[DockerRunner] Command array: {command}")
                    code, output = container.exec_run(cmd=command,
                                                      environment=job_config.env)
                    for line in output.decode("UTF-8").splitlines():
                        print(f"[{job_spec['name']}] {line}")
                    if code != 0:
                        raise NonZeroRetcode(f"Command {i} returned code {code}")
            finally:
                if container is not None:
                    container.stop()

        job_config.tagger.handle(self.client, image)
