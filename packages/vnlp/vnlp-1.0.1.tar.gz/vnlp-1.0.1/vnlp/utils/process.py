import subprocess
import json
import logging


def run(command, only_if=None, fail_on_error=False):
    if only_if is None or only_if:
        try:
            out = subprocess.check_output(command).decode().strip()
            return out
        except Exception as e:
            if fail_on_error:
                raise e
            else:
                logging.error(e)
