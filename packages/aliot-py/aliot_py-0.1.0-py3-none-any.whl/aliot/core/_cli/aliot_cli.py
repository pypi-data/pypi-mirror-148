import json

import click
import requests
from subprocess import Popen
import os

import aliot.core._cli.cli_service as service
from aliot.core._config.constants import DEFAULT_FOLDER, CHECK_FOR_UPDATE_URL, CONFIG_FILE_NAME

from aliot.core._cli.utils import print_success, print_err, print_fail


@click.group()
def main():
    response = requests.get(CHECK_FOR_UPDATE_URL)
    if response.status_code != 200:
        return
    try:
        content = response.json()
    except json.JSONDecodeError:
        return
    latest_version = content.get("latest", None) or content.get("versions", [None])[-1]
    if latest_version is None:
        return
    # TODO finish the "auto-check for update" system


def print_result(success_msg: str, success: bool | None, err_msg: str) -> bool | None:
    if success:
        print_success(success_msg)
    elif success is None:
        print_err(err_msg)
    else:
        print_fail(err_msg)

    return success


@main.command()
@click.argument("folder", default=DEFAULT_FOLDER)
def init(folder: str):
    print_result(f"Your aliot project is ready to go!", *service.make_init(folder))


@main.command()
@click.argument("object-name")
# @click.option("-o", "mode", is_flag=True, help="Specify what you want to make")
def new(object_name: str):
    success = print_result(
        f"Object {object_name!r} config created successfully", *service.make_obj_config(object_name)
    )
    if success is None:
        return

    print_result(f"Object {object_name!r} created successfully", *service.make_obj(object_name))


@main.command()
@click.argument("object-name")
def run(object_name: str):
    if not os.path.exists(f"{DEFAULT_FOLDER}/{CONFIG_FILE_NAME}"):
        print_err(f"Could not find config file at '{DEFAULT_FOLDER}/{CONFIG_FILE_NAME}' (try running `aliot init`)")

    obj_path = f"{DEFAULT_FOLDER}/{object_name}/{object_name}.py"
    if not os.path.exists(obj_path):
        print_err(f"The object {object_name!r} doesn't exist. Make sure you wrote it correctly or create it using the"
                  f" `aliot new` command.")

    Popen(["python", obj_path]).communicate()


@main.group()
def check():
    """Group of commands to check the status of the aliot"""


@check.command(name="iot")
@click.option("--name", default=None)
def objects(name: str):
    """Look up all (or one) objects' id in the config.ini and validate them with the server"""
    if name is None:
        """Validate all the objects"""
    else:
        """Validate only the object with the name"""


@main.command()
@click.argument("name", default=None)
def update():
    """Update aliot with the latest version"""
