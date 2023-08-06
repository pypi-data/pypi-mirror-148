'''pysvn errors module.
'''

from typing import Dict
import re


RE_FILE_LOCK_PATTERN = re.compile("'(?!svn cleanup)(?!svn help cleanup)(?! to remove locks \(type \'svn help cleanup).*'")


class SVNError(Exception):
    pass

class SVNNotInstalledError(Exception):
    pass

class RepositoryDirDoesNotExistError(Exception):
    pass

class NoSuchRevisionError(Exception):
    pass

class RevisionSyntaxError(Exception):
    pass

class PreviousOperationNotFinishedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('previous operation has not finished')

class DatabaseDiskImageMalformedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('database disk image is malformed')

class CommitConflictError(Exception):
    pass

class FileLockedError(Exception):
    pass

class PristineTextChecksumNotFoundError(Exception):
    pass

class TargetsNotWorkingCopiesError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('none of the targets are working copies')

ERROR_CODES: Dict[str, Exception] = {
    'E155037': PreviousOperationNotFinishedError,
    'E200030': DatabaseDiskImageMalformedError,
    'E160006': NoSuchRevisionError,
    'E155015': CommitConflictError,
    'E155004': FileLockedError,
    'E205000': RevisionSyntaxError,
    'E155032': PristineTextChecksumNotFoundError,
    'E155007': TargetsNotWorkingCopiesError
}

def handle_stderr(stderr: str) -> None:
    error_cd_search = list(filter(lambda error_cd: error_cd in stderr, ERROR_CODES.keys()))
    if not error_cd_search:
        raise SVNError(str(stderr).replace('\n', ' '))
    
    error_cd = error_cd_search[0]
    error_cls = ERROR_CODES[error_cd]
    
    # special error code messages
    if error_cd == 'E160006':
        rev_num = stderr.split(' ')[-1]
        raise error_cls(f'no such revision {rev_num}')
    if error_cd == 'E205000':
        revision_search = re.findall("'.*'", stderr)
        if revision_search:
            raise error_cls(f"with great power comes great responsibility, {revision_search[0]} is not valid revision syntax")
    if error_cd == 'E155004':
        locked_files = set(RE_FILE_LOCK_PATTERN.findall(stderr))
        if locked_files:
            files = ', '.join(locked_files)
            raise error_cls(f'working copy {files} is locked')
    if error_cd == 'E155032':
        checksum_search = re.findall("'.*'", stderr)
        if checksum_search:
            raise error_cls(checksum_search[0].replace("'", '', 2))
    
    raise error_cls(stderr)
