def test_export(pipeline):
    """Test export to BossDB.

    Please note that uploading data to BossDB via this pipeline requires an API
    token which can be obtained by creating an account at
    https://api.bossdb.io. You will also need resource manager permissions from the team at https://bossdb.org.
    """
    import datetime

    subject = pipeline["subject"]
    session = pipeline["session"]
    scan = pipeline["scan"]
    volume = pipeline["volume"]
    bossdb = pipeline["bossdb"]

    subject.Subject.insert1(
        dict(
            subject="subject2",
            sex="M",
            subject_birth_date="2023-01-01",
            subject_description="Cellpose segmentation of volumetric data."),
        skip_duplicates=True,
    )

    session_key = dict(
        subject="subject2",
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
        dict(session_key, session_dir="subject2"),
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
    volume.Volume.populate(session_key)
    key = (volume.Volume & "subject='subject2'").fetch1("KEY")
    volume.SegmentationParamSet.insert_new_params(
        segmentation_method="cellpose",
        paramset_idx=1,
        params=dict(
            diameter=None,
            min_size=2,
            do_3d=False,
            anisotropy=0.5,
            model_type="nuclei",
            channels=[[0, 0]],
            z_axis=0,
        ),
    )
    volume.SegmentationTask.insert1(dict(
        key,
        paramset_idx=1,
        task_mode="trigger",
        ),
    skip_duplicates=True,
    )
    segmentation_key = (volume.SegmentationTask & "subject='subject2'").fetch1("KEY")
    volume.Segmentation.populate(segmentation_key)
    volume.VoxelSize.insert1(
        dict(
            **session_key,
            scan_id=0,
            width=0.001,
            height=0.001,
            depth=0.001,
            )
        )
    col_name = "dataJointTestUpload"
    exp_name = "CaImagingFinal"
    chn_name = "test2"

    bossdb.VolumeUploadTask.insert1(
        dict(
            segmentation_key,
            collection_name=col_name,
            experiment_name=exp_name,
            channel_name=chn_name,
        ), skip_duplicates=True
    )

    bossdb.VolumeUpload.populate(segmentation_key)