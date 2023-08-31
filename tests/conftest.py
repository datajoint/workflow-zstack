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


@pytest.fixture(scope="session")
def volume_segmentation_param_set(pipeline):
    volume = pipeline["volume"]
    key = (volume.Volume & "subject='subject1'").fetch1("KEY")
    volume.SegmentationParamSet.insert_new_params(
        segmentation_method="cellpose",
        paramset_idx=1,
        params=dict(
            diameter=8,
            min_size=2,
            do_3d=False,
            anisotropy=0.5,
            model_type="nuclei",
            channels=[[0, 0]],
            z_axis=0,
        ),
    )
    yield


@pytest.fixture(scope="session")
def volume_segmentation_task(pipeline):
    volume = pipeline["volume"]
    key = (volume.Volume & "subject='subject1'").fetch1("KEY")
    volume.SegmentationTask.insert1(dict(
        key,
        paramset_idx=1,
    ))
    yield


@pytest.fixture(scope="session")
def volume_segmentation(pipeline):
    volume = pipeline["volume"]
    key = (volume.Volume & "subject='subject1'").fetch1("KEY")
    volume.Segmentation.populate(key)
    yield


@pytest.fixture(scope="session")
def volume_voxel_size(pipeline):
    volume = pipeline["volume"]
    key = (volume.Volume & "subject='subject1'").fetch1("KEY")
    volume.VoxelSize.insert1(
        dict(
            key,
            width=0.001,
            height=0.001,
            depth=0.001,
            )
        )
    yield

@pytest.fixture(scope="session")
def bossdb_volume_upload_task(pipeline):
    bossdb = pipeline["bossdb"]
    volume = pipeline["volume"]
    key = (volume.Segmentation & "subject='subject1'").fetch1("KEY")
    col_name = "dataJointTestUpload"
    exp_name = "CaImagingFinal"
    chn_name = "test1"

    bossdb.VolumeUploadTask.insert1(
        dict(
            key,
            collection_name=col_name,
            experiment_name=exp_name,
            channel_name=chn_name,
        ), skip_duplicates=True
    )
    yield

@pytest.fixture(scope="session")
def bossdb_volume_upload(pipeline):
    bossdb = pipeline["bossdb"]
    bossdb.VolumeUpload.populate()
    yield