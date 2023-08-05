import logging
import subprocess
import os
import sys
import shlex

from ..exceptions import NonZeroRetcode, RunnerError, ConfigException
from .pyutils import PackageManager, glob_command, grab_from


# TODO: Handle config like PyPiConfig
class PythonRunner:
    def __init__(self, config) -> None:
        logging.info("[PythonRunner] Initializing")
        self.workdir = config["workdir"]
        self.virtual_dir = os.path.abspath(os.path.join(self.workdir, "venv"))
        self.config = config
        PackageManager.getInstance().ensure("virtualenv")
        self.__init_venv()

    # TODO: Detect if the prev venv is the same OS type
    def __init_venv(self):
        if os.name == "nt":  # Windows
            self.vpython = os.path.join(self.virtual_dir, "Scripts", "python.exe")
        else:  # Linux & Mac
            self.vpython = os.path.join(self.virtual_dir, "bin", "python")

        if not os.path.exists(self.vpython):
            logging.debug(f"[PythonRunner] Venv not found at {self.vpython}")
            logging.info("[PythonRunner] Initializing venv")
            output = []
            with subprocess.Popen([sys.executable, "-m", "virtualenv", self.virtual_dir],
                                  stdout=subprocess.PIPE) as p:
                p.wait()
                for line in p.stdout:
                    output.append(line.decode('utf8').strip())
                if p.returncode != 0:
                    print("\n".join(output))
                    raise RunnerError("[PythonRunner] Could not create virtualenv")
                else:
                    logging.info(f"[PythonRunner] Virtualenv initialized at {self.virtual_dir}")
        else:
            logging.info(f"[PythonRunner] Found virtualenv at {self.virtual_dir}")
        dependencies = self.config.get("dependencies", [])
        if len(dependencies) > 0:
            logging.info(f"[PythonRunner] Ensuring dependencies:  {', '.join(dependencies)}")
            command = [self.vpython, "-m", "pip", "install"] + dependencies
            if logging.root.isEnabledFor(logging.DEBUG):
                with subprocess.Popen(command) as p:
                    p.wait()
                    if p.returncode != 0:
                        raise(RunnerError(f"[PythonRunner] Could not install dependencies: {dependencies} ({p.returncode})"))
            else:
                output = []
                with subprocess.Popen(command, stdout=subprocess.PIPE) as p:
                    for line in p.stdout:
                        output.append(line.decode('utf8').strip())
                    p.wait()
                    if p.returncode != 0:
                        print("\n".join(output))
                        raise(RunnerError(f"[PythonRunner] Could not install dependencies: {dependencies} ({p.returncode})"))
            logging.info("[PythonRunner] Installation done")

    # Executes the given job in the one and only venv
    # parameter is the raw jobscpec
    def run(self, job_spec):
        if "workdir" in job_spec:
            pwd = os.path.abspath(os.path.join(self.workdir, job_spec["workdir"]))
        else:
            pwd = self.workdir
        run_env = {}
        for k, v in self.config["env"].items():
            if isinstance(v, str):
                run_env[k] = v
            else:
                run_env[k] = grab_from(v)
        if "env" in job_spec:
            for env_var in job_spec["env"]:
                if isinstance(env_var["value"], str):
                    run_env[env_var["name"]] = env_var["value"]
                else:
                    run_env[env_var["name"]] = grab_from(env_var["value"])
        if "commands" in job_spec:
            commands = job_spec["commands"]
            for command in commands:
                logging.debug(f"[PythonRunner] Raw command: {command}")
                # TODO: only split if command is not an array
                if "*" in command:
                    run_command = glob_command(shlex.split(command), pwd)
                else:
                    run_command = shlex.split(command)
                logging.info(f"[PythonRunner] Command to execute: {run_command}")
                logging.debug(f"[PythonRunner] Workdir: {pwd}")
                if os.path.isdir(pwd):
                    with subprocess.Popen([self.vpython] + run_command, cwd=pwd, env=run_env) as p:
                        p.wait()
                        if p.returncode != 0:
                            raise NonZeroRetcode(f"Command {command} returned code {p.returncode}")
                else:
                    raise RunnerError(f"[PythonRunner] Invalid path for shell command: {pwd}")
        else:
            raise ConfigException(f"[PythonRunner] No commands specified in step {job_spec['name']}")
