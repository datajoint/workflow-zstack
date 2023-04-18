from collections.abc import Sequence
from typing import List
import pathlib
import datajoint as dj
from element_interface.utils import find_full_path
from element_session import session_with_id as session


def get_session_directory(session_key: dict) -> str:
    """Return relative path from SessionDirectory table given key

    Args:
        session_key (dict): Key uniquely identifying a session

    Returns:
        path (str): Relative path of session directory
    """
    from .pipeline import session

    # NOTE: fetch (vs. fetch1) permits dir to not exist, may be the case when saving
    # slices directly from from BossDB into inferred dir based on BossDB structure
    session_dir = (session.SessionDirectory & session_key).fetch("session_dir")

    if len(session_dir) > 1:
        raise ValueError(
            f"Found >1 directory for this key:\n\t{session_key}\n\t{session_dir}"
        )
    elif len(session_dir) == 1:
        return session_dir[0]
    else:
        return None


def get_volume_root_data_dir() -> List[str]:
    """Return root directory for ephys from 'vol_root_data_dir' in dj.config

    Returns:
        path (any): List of path(s) if available or None
    """
    vol_root_dirs = dj.config.get("custom", {}).get("vol_root_data_dir", None)
    if not vol_root_dirs:
        return None
    elif not isinstance(vol_root_dirs, Sequence):
        return list(vol_root_dirs)
    else:
        return pathlib.Path(vol_root_dirs[0])


def _find_files_by_type(scan_key, filetype: str):
    """Uses roots + relative SessionDirectory, returns list of files with filetype"""
    sess_dir = find_full_path(
        get_volume_root_data_dir(),
        pathlib.Path((session.SessionDirectory & scan_key).fetch1("session_dir")),
    )
    return sess_dir, [fp.as_posix() for fp in sess_dir.rglob(filetype)]


def get_volume_tif_file(scan_key):
    """Retrieve the list of ScanImage files associated with a given Scan.

    Args:
        scan_key (dict): Primary key from Scan.

    Returns:
        path (list): Absolute path(s) of the scan files.

    Raises:
        FileNotFoundError: If the session directory or tiff files are not found.
    """
    # Folder structure: root / subject / session / .tif (raw)
    sess_dir, tiff_filepaths = _find_files_by_type(scan_key, "*_stitched.tif")
    if tiff_filepaths:
        return tiff_filepaths
    else:
        raise FileNotFoundError(f"No tiff file found in {sess_dir}")
