def test_generate_pipeline(pipeline):
    subject = pipeline["subject"]
    session = pipeline["session"]
    scan = pipeline["scan"]
    volume = pipeline["volume"]
    bossdb = pipeline["bossdb"]

    # Test connection from Subject to Session
    assert subject.Subject.full_table_name in session.Session.parents()

    # Test connection from Session to Scan and Scan to Volume
    assert session.Session.full_table_name in scan.Scan.parents()
    assert scan.Scan.full_table_name in volume.Volume.parents()
    assert "mask_npix" in (volume.Segmentation.Mask.heading.secondary_attributes)

    assert all(
        [
            bossdb.VolumeUploadTask.full_table_name in bossdb.VolumeUpload.parents(),
            volume.Segmentation.full_table_name in bossdb.VolumeUploadTask.parents(),
        ]
    )

    assert "web_address" in (bossdb.VolumeUpload.WebAddress.heading.secondary_attributes)
