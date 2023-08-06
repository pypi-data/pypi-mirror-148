import os
import shutil
import subprocess
import tarfile

import click
import requests

from ..api.status_update import update_status_init
from ..common.constants import *
from ..common.utils import failed, get_tiyaro_token, success, warn
from ..handler.cli_state import get_model_name_with_suffix, save_model_metadata, get_model_framework


@click.command()
@click.option('-f', '--force', is_flag=True, default=False, help=INIT_HELP)
@click.option('-v', '--verbose', is_flag=True, default=False, help=VERBOSE_HELP)
def init(force, verbose):
    """
    - Initializes model repo for Tiyaro Push
    """
    name = click.prompt('Please enter the name of your model', type=str)
    framework = get_framework(verbose)
    get_templates(force, verbose)
    save_model_metadata(name, framework, verbose)
    update_status_init(get_model_name_with_suffix(), get_model_framework())
    success(
        f'Created {TIYARO_HANDLER_DIR}, {HANDLER_MODEL_MODEL_TEST_FILE} templates successfully !')


def get_framework(is_verbose):
    framework_opt = '\n 1\t Pytorch\n 2\t Tensorflow\n 3\t JAX\n 4\t Other -specify\n'
    
    option = click.prompt(f'Please enter the framework of your model {framework_opt} \t\t\t', type=str)
    option = option.casefold()
    if option in ['1', 'Pytorch']:
        option = 'pytorch'
    elif option in ['2', 'Tensorflow']:
        option = 'tensorflow'
    elif option in ['3', 'JAX']:
        option = 'jax'
    elif option == '4':
        failed(f'For option 4, you must specify the framework name')
        exit(-1)
    success(f'DEBUG - use selected option is: {option}', is_verbose)
    return option

def get_templates(is_overwrite, is_verbose):

    if (os.path.isdir(TIYARO_HANDLER_DIR)):
        if not is_overwrite:
            warn(
                f'{TIYARO_HANDLER_DIR} already exists.  To force init, kindly use -f with your init command')
            exit(-1)
        else:
            if is_verbose:
                subprocess.run(f'tiyaro clear -f -v', shell=True)
            else:
                subprocess.run(f'tiyaro clear -f', shell=True)

    if (os.path.isfile(HANDLER_MODEL_MODEL_TEST_FILE)):
        if not is_overwrite:
            warn(f'{HANDLER_MODEL_MODEL_TEST_FILE} already exists.  To force init kindly use -f with your init command')
            exit(-1)
        else:
            subprocess.run(f'tiyaro clear -f', shell=True)

    token = get_tiyaro_token()
    resp = requests.get(
        f'{PUSH_SUPPORT_FILES_ENDPOINT}/{ARTIFACTS_FILE_NAME}',
        headers={
            'Authorization': token
        })
    if resp.status_code == 200:
        template_url = resp.content
    else:
        failed(resp.status_code)
        failed(resp.content)
        failed(
            f'Unable to get templates URL.  Is your {TIYARO_TOKEN} still valid ?')
        exit(-1)

    os.makedirs(ARTIFACTS_DOWNLOAD_DIR)
    downloaded_artifact = f'{ARTIFACTS_DOWNLOAD_DIR}/ARTIFACTS_FILE_NAME'

    resp = requests.get(template_url, stream=True)
    if resp.status_code == 200:
        with open(downloaded_artifact, 'wb') as f:
            f.write(resp.raw.read())
    else:
        failed(
            f'Unable to get templates.  Is your {TIYARO_TOKEN} still valid ?')
        exit(-1)

    def members(tf, sub_folder):
        l = len(sub_folder)
        for member in tf.getmembers():
            if member.path.startswith(sub_folder):
                member.path = member.path[l:]
                yield member

    tar = tarfile.open(downloaded_artifact)
    tar.extractall(path=TIYARO_HANDLER_DIR,
                   members=members(tar, ARTIFACTS_FILES_DIR))
    # move test file to project root for tiyaro test
    shutil.move(f'{TIYARO_HANDLER_DIR}/{HANDLER_MODEL_MODEL_TEST_FILE}',
                f'{HANDLER_MODEL_MODEL_TEST_FILE}')
    shutil.rmtree(ARTIFACTS_DOWNLOAD_DIR)
