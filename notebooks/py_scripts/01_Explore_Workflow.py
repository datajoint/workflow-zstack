# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: ele
#     language: python
#     name: python3
# ---

# DataJoint U24 - Workflow Volume
#

# ### Intro
#

# This notebook will describe the steps to use Element Volume for interacting with BossDB.
# Prior to using this notebook, please refer to documentation for
# [Element installation instructions](https://datajoint.com/docs/elements/user-guide/) and refer to [BossDB resources](https://www.youtube.com/watch?v=eVNr6Pzxoh8) for information on generating an account and configuring `intern`.
#
# Importantly, you'll need an `intern` config file, which should look like this:
#
# ```cfg
#     # ~/.intern/intern.cfg
#     [Default]
#     protocol = https
#     host = api.bossdb.io
#     token = <YOUR_TOKEN>
# ```
#

# +
import datajoint as dj
import os

if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")
dj.conn()

# +
dj.config["custom"]["database.prefix"] = "cbroz_wfboss_"
dj.config["custom"][
    "vol_root_data_dir"
] = "/Users/cb/Documents/data/U24_SampleData/boss/"
from workflow_volume.pipeline import volume, BossDBInterface, bossdb

# volume.Volume.delete_quick()
# -

volume.Volume()

# `BossDBInterface` works much like `intern.array`, but with additional functionality for managing records in your Element Volume schema. We can optionally link this dataset to a session in our pipeline via a session key.
#
# Note, however, that we'll have to change our notation slightly. Whereas we can directly index into a dataset to get slices, we'll need to either provide slices as a string or a tuple.
#

# ### Testing
#

data = BossDBInterface(
    "bossdb://takemura/takemura13/image", resolution=4, session_key={}
)

# Using `intern` notion, we can look at Z slice 300, from Y voxels 200-500, and X voxels 0 to 700.
#

data[300, 200:501, 0:701]

# The same data can be downloaded and loaded into Element Volume using either of the following commands.
#
# Without a session directory provided via `get_session_directory` in `workflow_volume.paths`, we will infer an output directory based on the BossDB path from `get_vol_root_data_dir`.
#

# data.download(slice_key=(300,slice(200,501),slice(0,701)))
data.download(slice_key="[300,200:501,0:701]")

# Our volume is stored in the `Volume`

volume.Volume()

# With `Slice` corresponding to slices

volume.Volume.Slice()

# Each BossDB resolution will have a unique entry in the `Resolution` table

volume.Resolution()

# And, the `Zoom` table retain information about the X/Y windows we use.

volume.Zoom()

# Changing any of these pieces of information would download different data.

data.download(slice_key=(slice(300, 311), slice(100, 401), slice(100, 401)))

# +
import logging
import numpy as np
from workflow_volume.pipeline import volume, bossdb, session, subject
from workflow_volume.paths import get_vol_root_data_dir
from element_volume.volume import *

# from workflow_volume.pipeline import BossDBInterface

# em_data = BossDBInterface("bossdb://Kasthuri/ac4/em", resolution=0)
# seg_data = BossDBInterface("bossdb://Kasthuri/ac4/neuron", resolution=0)
# em_data = BossDBInterface("bossdb://witvliet2020/Dataset_1/em", resolution=0)
# seg_data = BossDBInterface("bossdb://witvliet2020/Dataset_1/segmentation", resolution=0)

logger = logging.getLogger("datajoint")

volume_key = dict(volume_id="Thy1")


def drop_schemas():
    from datajoint_utilities.dj_search.lists import drop_schemas

    prefix = dj.config["custom"]["database.prefix"]
    drop_schemas(prefix, dry_run=False, force_drop=True)


def drop_tables():
    tables = [
        volume.Connectome,
        volume.ConnectomeTask,
        volume.ConnectomeParamset,
        volume.Segmentation,
        volume.Segmentation.Cell,
        volume.CellMapping,
        volume.SegmentationTask,
        volume.SegmentationParamset,
    ]
    for t in tables:
        t.drop_quick()


class upload:
    @classmethod
    def manual_entry(cls):
        from datetime import datetime

        subject.Subject.insert1(
            dict(subject="sub1", sex="M", subject_birth_date=datetime.now()),
            skip_duplicates=True,
        )
        session.Session.insert1(
            dict(
                **(subject.Subject & "subject='sub1'").fetch1("KEY"),
                session_id=1,
                session_datetime=datetime.now(),
            ),
            skip_duplicates=True,
        )
        session.SessionDirectory.insert1(
            dict(**session.Session.fetch1("KEY"), session_dir="sample"),
            skip_duplicates=True,
        )
        volume.Resolution.insert1(
            dict(
                resolution_id="990nm",
                voxel_unit="micrometers",
                voxel_z_size=1,
                voxel_y_size=0.5,
                voxel_x_size=0.5,
                downsampling=0,
            ),
            skip_duplicates=True,
        )

        coll, exp, chann, seg = (
            "DataJointTest",
            "test",
            "CalciumImaging",
            "Segmentation",
        )

        bossdb.BossDBURLs.load_bossdb_info(
            collection=coll,
            experiment=exp,
            volume=chann,
            segmentation=seg,
            skip_duplicates=True,
        )
        url_key = (
            bossdb.BossDBURLs.Volume & dict(collection_experiment=f"{coll}/{exp}")
        ).fetch1()

        raw_data = cls.load_sample_data()
        raw_data_shape = raw_data.shape

        volume.Volume.insert1(
            dict(
                volume_id="Thy1",
                resolution_id="990nm",
                session_id=1,
                z_size=raw_data_shape[0],
                y_size=raw_data_shape[1],
                x_size=raw_data_shape[2],
                channel=chann,
                **url_key,
                volume_data=raw_data,
            ),
            skip_duplicates=True,
        )

    def load_sample_data():
        from tifffile import TiffFile
        from PIL import Image
        from pathlib import Path

        root_dir = get_vol_root_data_dir()[0]
        image_fp = root_dir + "sample/zstack_Gcamp_00001_00012.tif"
        png_fp = root_dir + "sample/Z%02d.png"
        image_sample = TiffFile(image_fp).asarray()[250:270, 1000:1246, :]
        if not Path(png_fp % 0).exists():
            for z in range(20):
                Image.fromarray(image_sample[z]).save(png_fp % z)
        return image_sample

    def upload_from_volume():
        volume.Volume.upload(volume_key)
        # Error uploading chunk 0-20: ndarray is not C-contiguous


class download:
    def add_manual_boss_url():
        bossdb.BossDBURLs.load_bossdb_info(
            collection="Kasthuri",
            experiment="ac4",
            volume="em",
            segmentation="neuron",
            skip_duplicates=True,
        )
        bossdb.BossDBURLs.load_bossdb_info(
            collection="witvliet2020",
            experiment="Dataset_1",
            volume="em",
            segmentation="segmentation",
            skip_duplicates=True,
        )

    def download_volume_via_classmeth():
        volume.Volume.download(
            url="bossdb://witvliet2020/Dataset_1/em",
            slice_key="[100:120,1000:1500,1000:1500]",
            save_images=True,
            save_ndarray=True,
            image_mode="P",
            skip_duplicates=True,
        )

    def download_seg_via_classmeth():
        volume.SegmentationParamset.insert_new_params(
            segmentation_method="bossdb",
            paramset_idx=1,
            params=dict(
                slice_key="[100:120,1000:1500,1000:1500]",
                save_images=True,
                save_ndarray=True,
                image_mode="P",
                skip_duplicates=True,
            ),
        )
        volume.SegmentationTask.insert1(
            dict(
                volume_id="witvliet2020/Dataset_1",
                resolution_id=0,
                task_mode="load",
                paramset_idx=1,
                **(
                    bossdb.BossDBURLs.Segmentation & "collection_experiment LIKE 'wit%'"
                ).fetch1(),
            )
        )
        volume.Segmentation.populate()

    @classmethod
    def run_all(cls):
        cls.add_manual_boss_url()
        cls.download_volume_via_classmeth()
        cls.download_seg_via_classmeth()

