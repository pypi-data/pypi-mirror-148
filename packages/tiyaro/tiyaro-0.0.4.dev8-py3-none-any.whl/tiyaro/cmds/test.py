import subprocess
import venv
import os
import shutil

import click

from ..api.status_update import (update_status_test_failed,
                                 update_status_test_passed)
from ..handler.cli_state import get_model_name_with_suffix
from ..common.constants import (HANDLER_MODEL_MANIFEST_FILE,
                                HANDLER_MODEL_MODEL_TEST_FILE, VERBOSE_HELP, TIYARO_TEST_VENV_PATH)
from ..common.utils import failed, success
from ..handler.model_manifest import get_requirements_file_path
from ..handler.utils import (validate_handler_exists,
                             validate_handler_test_file_exists)


@click.command()
@click.option('-p', '--pretrained', required=False, help=f'pretrained_file path or url.  default is value from {HANDLER_MODEL_MANIFEST_FILE}')
@click.option('-i', '--input', required=True, help=f'Valid JSON input string or file path')
@click.option('-v', '--verbose', is_flag=True, default=False, help=VERBOSE_HELP)
def test(pretrained, input, verbose):
    """
    - Test model locally
    """
    do_test(pretrained, input, verbose)


def do_test(pretrained, input, is_verbose):
    validate_handler_exists()
    validate_handler_test_file_exists()
    requirements_file_path = get_requirements_file_path()

    success(f'Creating VENV: {TIYARO_TEST_VENV_PATH}')
    venv.create(TIYARO_TEST_VENV_PATH, with_pip=True)

    os.system(
        f'{TIYARO_TEST_VENV_PATH}/bin/pip3 install -r {requirements_file_path}')

    if not pretrained:
        pretrained = 'from-config'

    p = subprocess.run(
        f'{TIYARO_TEST_VENV_PATH}/bin/python {HANDLER_MODEL_MODEL_TEST_FILE} {pretrained} {input}', shell=True)

    if (os.path.isdir(TIYARO_TEST_VENV_PATH)):
        success(f'Cleaning up VENV: {TIYARO_TEST_VENV_PATH}', is_verbose)
        shutil.rmtree(TIYARO_TEST_VENV_PATH)
        
    if p.returncode == 0:
        update_status_test_passed(get_model_name_with_suffix())
        success('Test successful !  You can push your model now.')
    else:
        update_status_test_failed(get_model_name_with_suffix())
        failed('Test failed !')
