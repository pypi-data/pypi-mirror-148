import os.path
import sys
import time
import urllib
import webbrowser

from ..model.build_pack import BuildPack
from ..output_callback import OutputCallBack
from ..util import execute


def deploy(
    build_pack: BuildPack, component, package_dir, build_dir, callback: OutputCallBack
):
    virtualenv = f"{build_dir}/virtualenv.pyz"
    if not os.path.isfile(virtualenv):
        callback.print_header("Going to download virtualenv")
        urllib.request.urlretrieve(
            "https://bootstrap.pypa.io/virtualenv.pyz", virtualenv
        )

    python_location = sys.executable

    venv = f"{build_dir}/venv"
    if not os.path.isdir(venv):
        callback.print_header("Going to create virtualenv")
        cmd = [python_location, virtualenv, venv]
        for path in execute(cmd):
            callback.print_line(path)

    callback.print_header("Going to install dependency")
    cmd = [f"{venv}/bin/pip", "install", "-r", f"{package_dir}/requirements.txt"]
    for path in execute(cmd):
        callback.print_line(path)

    callback.print_header("Going to run service")
    command = build_pack.local_run_command
    command = f"{venv}/bin/{command}"
    callback.print_line(f"Going to execute command {command}\n")
    cmd = command.split(" ")
    iterator = execute(cmd)

    time.sleep(5)
    url = f"http://127.0.0.1:{component['spec']['container']['ports'][0]['containerPort']}"
    callback.print_line(f"Service is up on {url}\n")
    webbrowser.open(url)
    for path in iterator:
        callback.print_line(path)
