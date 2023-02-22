def test_ingest_volume(pipeline, ingest_data):
    """Check length of various Volume schema tables"""
    volume = pipeline["Volume"]
    assert len(volume.Volume()) == 2, f"Check Volume: len={len(volume.Volume())}"
