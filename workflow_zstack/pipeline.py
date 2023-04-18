from element_animal import subject, surgery
from element_calcium_imaging import imaging, imaging_report, scan
from element_lab import lab
from element_session import session_with_id as session
from element_zstack import volume
from element_zstack.export import bossdb

from . import db_prefix
from .paths import get_session_directory, get_volume_root_data_dir, get_volume_tif_file
from .reference import Device

__all__ = [
    "db_prefix",
    "lab",
    "scan",
    "imaging",
    "imaging_report",
    "session",
    "subject",
    "surgery",
    "volume",
    "bossdb",
    "Device",
    "get_session_directory",
    "get_volume_root_data_dir",
    "get_volume_tif_file",
]

# ---------------------------------- Activate schemas ----------------------------------

lab.activate(db_prefix + "lab")

# subject.activate(db_prefix + "subject", linking_module=__name__)
surgery.activate(db_prefix + "subject", db_prefix + "surgery", linking_module=__name__)

Experimenter = lab.User
session.activate(db_prefix + "session", linking_module=__name__)

Equipment = Device
imaging.activate(db_prefix + "imaging", db_prefix + "scan", linking_module=__name__)

Mask = imaging.Segmentation.Mask
Session = session.Session
SessionDirectory = session.SessionDirectory
Scan = scan.Scan
volume.activate(db_prefix + "volume", linking_module=__name__)
bossdb.activate(db_prefix + "bossdb", linking_module=__name__)
