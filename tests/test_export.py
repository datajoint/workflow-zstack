def test_export(pipeline):
    """Test export to BossDB.

    Please note that uploading data to BossDB via this pipeline requires an API
    token which can be obtained by creating an account at
    https://api.bossdb.io. You will also need resource manager permissions from the team at https://bossdb.org.
    """
    
    scan = pipeline["scan"]
    bossdb = pipeline["bossdb"]

    scan_key = (scan.Scan & "subject = 'subject1'").fetch1("KEY")
    upload_key = dict(
        scan_key,
        paramset_idx=1,
    )
    col_name = "dataJointTestUpload"
    exp_name = "CaImagingFinal"
    chn_name = "test1"

    bossdb.VolumeUploadTask.insert1(
        dict(
            upload_key,
            collection_name=col_name,
            experiment_name=exp_name,
            channel_name=chn_name,
        ), skip_duplicates=True
    )

    bossdb.VolumeUpload.populate(upload_key)