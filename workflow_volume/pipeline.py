from element_animal import subject, surgery
from element_animal.subject import Subject  # Dependency for session
from element_animal.surgery import BrainRegion  # Dependency for imaging
from element_calcium_imaging import imaging, imaging_report, scan
from element_lab import lab
from element_lab.lab import Lab, Project, Protocol, Source, User  # Deps for Subject
from element_session import session_with_id as session
from element_session.session_with_id import Session, SessionDirectory
from element_volume import bossdb, volume
from element_volume.bossdb import BossDBURLs
from element_volume.readers.bossdb import BossDBInterface

from . import db_prefix
from .paths import get_session_directory, get_vol_root_data_dir
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
    "bossdb",
    "volume",
    "Device",
    "Lab",
    "Project",
    "Protocol",
    "User",
    "Source",
    "Session",
    "SessionDirectory",
    "Subject",
    "BrainRegion",
    "BossDBURLs",
    "BossDBInterface",
    "get_session_directory",
    "get_vol_root_data_dir",
]

# ---------------------------------- Activate schemas ----------------------------------

lab.activate(db_prefix + "lab")

# subject.activate(db_prefix + "subject", linking_module=__name__)
surgery.activate(db_prefix + "subject", db_prefix + "surgery", linking_module=__name__)

Experimenter = lab.User
session.activate(db_prefix + "session", linking_module=__name__)

Equipment = Device
Location = BrainRegion
imaging.activate(db_prefix + "imaging", db_prefix + "scan", linking_module=__name__)

bossdb.activate(db_prefix + "bossdb")

URLs = bossdb.BossDBURLs
Mask = imaging.Segmentation.Mask
volume.activate(db_prefix + "volume", linking_module=__name__)
