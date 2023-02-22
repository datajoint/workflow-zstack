from collections import Sequence
from typing import List

import datajoint as dj


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


def get_vol_root_data_dir() -> List[str]:
    """Return root directory for ephys from 'vol_root_data_dir' in dj.config

    Returns:
        path (any): List of path(s) if available or None
    """
    roots = dj.config.get("custom", {}).get("vol_root_data_dir", None)
    if not isinstance(roots, Sequence):
        roots = [roots]
    return roots
