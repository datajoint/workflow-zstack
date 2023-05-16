import logging
import os
import pathlib
from pathlib import Path

import datajoint as dj
import pytest
from element_interface.utils import find_full_path

from workflow_zstack.paths import get_volume_root_data_dir

# ------------------- SOME CONSTANTS -------------------


logger = logging.getLogger("datajoint")


sessions_dirs = [
    "subject1",
]

# ---------------------- FIXTURES ----------------------


@pytest.fixture(scope="session")
def test_data():

    for p in sessions_dirs:
        try:
            find_full_path(get_volume_root_data_dir, p).as_posix()
        except FileNotFoundError as e:
            print(e)


@pytest.fixture(autouse=True, scope="session")
def pipeline():
    from workflow_zstack import pipeline

    yield {
        "subject": pipeline.subject,
        "lab": pipeline.lab,
        "session": pipeline.session,
        "scan": pipeline.scan,
        "volume": pipeline.volume,
        "volume_matching": pipeline.volume_matching,
        "bossdb": pipeline.bossdb,
    }


@pytest.fixture(scope="session")
def insert_upstream(pipeline):
    import datetime


    subject = pipeline["subject"]
    session = pipeline["session"]
    scan = pipeline["scan"]

    subject.Subject.insert1(
        dict(
            subject="subject1",
            sex="M",
            subject_birth_date="2023-01-01",
            subject_description="Cellpose segmentation of volumetric data."),
        skip_duplicates=True,
    )

    session_key = dict(
        subject="subject1",
        session_id=0,
    )
    session.Session.insert1(
        dict(
            session_key,
            session_datetime=datetime.datetime.now(),
        ),
        skip_duplicates=True,
    )

    session.SessionDirectory.insert1(
        dict(session_key, session_dir="subject1/session1"),
        skip_duplicates=True,
    )
    scan.Scan.insert1(
        dict(
            session_key,
            scan_id=0,
            acq_software="ScanImage",
        ),
        skip_duplicates=True,
    )

    yield


@pytest.fixture(scope="session")
def volume_volume(pipeline):
    volume = pipeline["volume"]

    volume.Volume.populate()

    yield
    