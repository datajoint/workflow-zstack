# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3.9.13 ('ele')
#     language: python
#     name: python3
# ---

# %% [markdown] tags=[]
# # DataJoint U24 - Workflow Volume
#

# %% [markdown] tags=[]
# ## Interactively run the workflow
#

# %% [markdown]
# - If you haven't configured your set up, refer to [01-Configure](./01-Configure.ipynb).
# - For an overview of the schema, refer to [02-WorkflowStructure](02-WorkflowStructure_Optional.ipynb).
#

# %% [markdown]
# Let's change the directory to load the local config, `dj_local_conf.json`.
#

# %%
import os

# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")

# %% [markdown]
# `pipeline.py` activates the various schema and declares other required tables.
#

# %%
import datajoint as dj
from datetime import datetime
from workflow_volume.pipeline import (
    lab,
    subject,
    session,
    volume,
    bossdb,
    get_session_directory,
    get_vol_root_data_dir,
)

# %% [markdown] tags=[]
# ## Manually Inserting Entries
#

# %% [markdown]
# ### Upstream tables
#

# %% [markdown]
# We can insert entries into `dj.Manual` tables (green in diagrams) by providing values as a dictionary or a list of dictionaries.
#

# %%
subject.Subject.insert1(
    dict(subject="sub1", sex="M", subject_birth_date=datetime.now()),
    skip_duplicates=True,
)
session_key = (subject.Subject & "subject='sub1'").fetch1("KEY")
session.Session.insert1(
    dict(
        **session_key,
        session_id=1,
        session_datetime=datetime.now(),
    ),
    skip_duplicates=True,
)
session.SessionDirectory.insert1(
    dict(**session.Session.fetch1("KEY"), session_dir="<your-data-path>"),
    skip_duplicates=True,
)

# %% [markdown]
# `get_session_directory` will fetch your relative directory path form this `SessionDirectory` table.
#

# %%
from element_interface.utils import find_full_path

data_path = find_full_path(get_vol_root_data_dir(), get_session_directory(session_key))

# %% [markdown] tags=[]
# ### Element Volume Tables
#
# #### Uploading
#

# %% [markdown]
# The `Resolution` table keeps track details related to data collection, including units and size in each dimension. `downsampling` indicates number of times the dataset has been compressed by taking every other pixel. Within BossDB, resolution 3 data (here, `downsampling` 3) reflects every 8th pixel, for example.
#

# %%
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

# %% [markdown]
# BossDB operates with a hierarchy of collections, experiments, and channels. A collection spans multiple experiments. An experiment may collect one or more channels, including electron micrioscopy data, segmentation annotations, and connectome data. These form the portions of a BossDB URL.
#
# Here, we choose some example values. With the proper permissions, we can create a BossDB dataset right from our Python environment.
#

# %%
collection, experiment, volume, segmentation = (
    "DataJointTest",
    "test",
    "CalciumImaging",
    "Segmented",
)

bossdb.BossDBURLs.load_bossdb_info(
    collection=collection,
    experiment=experiment,
    volume=volume,
    segmentation=segmentation,
    skip_duplicates=True,
)
url_key = (
    bossdb.BossDBURLs.Volume & dict(collection_experiment=f"{collection}/{experiment}")
).fetch1()


# %% [markdown]
# The `load_sample_data` function below provides a template for loading a multi-page tif file and saving it into individual Z-axis images.
#
# In the next step, we can choose to upload to BossDB either with individual images in a directory or through an image volume in memory. To store the volume data in the table, replace the contents below with a function that loads your data.
#
# Note: BossDB only accepts image data as `uint8` or `uint16` numpy arrays.
#

# %%
def load_sample_data():
    from tifffile import TiffFile
    from PIL import Image
    from pathlib import Path

    root_dir = get_vol_root_data_dir()[0]
    image_fp = root_dir + "<your-data-path>/<your-file-name>.tif"
    png_fp = root_dir + "sample/Z%02d.png"  # Z-plane
    image_sample = TiffFile(image_fp).asarray()

    image_sample = image_sample.astype("uint16")
    if not Path(png_fp % 0).exists():
        for z in range(20):
            Image.fromarray(image_sample[z]).save(png_fp % z)
    return image_sample


# %% [markdown]
# Now, we can insert into the `Volume` table.

# %%
raw_data = load_sample_data()
raw_data_shape = raw_data.shape
volume_key = dict(volume_id="Thy1", resolution_id="990nm")
volume.Volume.insert1(
    dict(
        **volume_key,
        session_id=1,
        z_size=raw_data_shape[0],
        y_size=raw_data_shape[1],
        x_size=raw_data_shape[2],
        channel=volume,
        **url_key,
        volume_data=raw_data,
    ),
    skip_duplicates=True,
)

# %% [markdown]
# Finally, we can upload our data either from the data stored in the table or a path to images. If this entry is already associated with a `SessionDirectory` entry, we'll look for images in this path.
#

# %%
# For other optional parameters, see additional docstring info here:
# element_volume.export.bossdb.BossDBUpload
volume.Volume.upload(volume_key, upload_from="table")
# volume.Volume.upload(volume_key, upload_from="dir", data_extension="*pattern*.png")

# %% [markdown]
# #### Download

# %% [markdown]
# The `Volume` and `BossDBURLs` tables offer additional class methods for downloading BossDB data or returning objects for interacting with the data.
#

# %%
bossdb.BossDBURLs.load_bossdb_info(
    collection="Kasthuri",
    experiment="ac4",
    volume="em",
    segmentation="neuron",
    skip_duplicates=True,
)

# %%
# For other optional parameters, see additional docstring info here:
# element_volume.readers.bossdb.BossDBInterface.load_data_into_element
volume.Volume.download(
    "bossdb://witvliet2020/Dataset_1/em",
    downsampling=3,
    slice_key="[100:120,1000:1500,1000:1500]",
    save_images=True,
    save_ndarray=True,
    image_mode="P",
    skip_duplicates=True,
)
data = volume.Volume.return_bossdb_data(
    volume_key=dict(volume_id="witvliet2020/Dataset_1")
)

# %% [markdown]
# To load segmentation data, we can set the `task_mode` to load and add additional pararameters to the `SegmentationParamset` table.

# %%
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

# %% [markdown]
# In the [next notebook](./04-Drop.ipynb), we'll touch on how to drop these various schemas for development.
#
