'''pysvn utilities module.
'''
import subprocess
from typing import List, Tuple
from pathlib import Path

def check_svn_installed() -> bool:
    """Check if the current system has the svn cli client installed.

    Returns:
        bool: True if svn is installed, otherwise False
    """
    try:
        subprocess.run('svn', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def get_longest_line_len(lines: List[str]) -> int:
    longest_len = 0
    for line in lines:
        if len(line) > longest_len:
            longest_len = len(line)
    return longest_len


def get_output(cmd: subprocess.Popen) -> Tuple[str, str]:
    """Get stdout and stderr from a finished process.

    Args:
        cmd (subprocess.Popen): process

    Returns:
        Tuple[str, str]: stdout, stderr
    """
    stdout = cmd.stdout.read().decode('utf-8').strip()
    stderr = cmd.stderr.read().decode('utf-8').strip()
    return stdout, stderr
