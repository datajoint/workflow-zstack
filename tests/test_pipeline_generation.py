def test_generate_pipeline(pipeline):
    session = pipeline["session"]
    volume = pipeline["volume"]

    volume_children = volume.volume.children()
    assert volume.Volume.full_table_name in volume_children
    assert session.Session.volume.full_table_name in volume_children

    # test connection Subject -> schema children
    session_children_links = session.Session.children()
    session_children_list = [
        volume.Volume,
    ]

    for child in session_children_list:
        assert (
            child.full_table_name in session_children_links
        ), f"session.Session.children() did not include {child.full_table_name}"
