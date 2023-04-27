def test_export(pipeline):
    scan = pipeline["scan"]
    bossdb = pipeline["bossdb"]

    scan_key = (scan.Scan & "subject = 'subject1'").fetch1("KEY")
    col_name = "dataJointTestUpload"
    exp_name = "CaImagingFinal"
    chn_name = "test1"

    bossdb.VolumeUploadTask.insert1(
        dict(
            scan_key,
            collection_name=col_name,
            experiment_name=exp_name,
            channel_name=chn_name,
            upload_type="image",
        ), skip_duplicates=True
    )

    bossdb.BossDBURLs.populate(scan_key)