from collections.abc import Sequence
from typing import List
import pathlib
import datajoint as dj
from element_interface.utils import find_full_path
from element_session import session_with_id as session


def get_volume_root_data_dir() -> List[str]:
    """Return root directory for volumetric data in dj.config

    Returns:
        path (any): List of path(s) if available or None
    """
    vol_root_dirs = dj.config.get("custom", {}).get("volume_root_data_dir", None)
    if not vol_root_dirs:
        return None
    elif not isinstance(vol_root_dirs, Sequence):
        return list(vol_root_dirs)
    else:
        return pathlib.Path(vol_root_dirs)


def get_volume_tif_file(scan_key):
    """Retrieve the ScanImage file associated with a given Scan.

    Args:
        scan_key (dict): Primary key from Scan.

    Returns:
        path (str): Absolute path of the scan file.

    Raises:
        FileNotFoundError: If the tiff file(s) are not found.
    """
    # Folder structure: root / subject / session / .tif (raw)    
    sess_dir = find_full_path(
        get_volume_root_data_dir(),
        pathlib.Path((session.SessionDirectory & scan_key).fetch1("session_dir")),
    )
    
    tiff_filepaths = [fp.as_posix() for fp in sess_dir.rglob("*.tif")]

    if tiff_filepaths:
        assert len(tiff_filepaths) == 1, "More than 1 `.tif` file in file path. Please ensure the session directory contains only 1 image file."
        return tiff_filepaths[0]
    else:
        raise FileNotFoundError(f"No tiff file found in {sess_dir}")
