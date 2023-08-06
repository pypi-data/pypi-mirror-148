from pathlib import Path
from typing import List

from ceader.adapters.file_disk_repo import FileDiskRepository
from ceader.app import Application


def new_application(
    files_dir: Path,
    header_path: Path,
    file_extensions: List[str],
    skip_hidden: bool,
    debug: bool,
) -> Application:
    file_repo = FileDiskRepository(
        dir_path=files_dir,
        header_path=header_path,
        skip_hidden=skip_hidden,
        extensions_to_get=file_extensions,
        debug=debug,
    )
    return Application(
        file_repo=file_repo,
        debug=debug,
    )
