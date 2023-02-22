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
#     display_name: ele
#     language: python
#     name: python3
# ---

# %% [markdown] tags=[]
# # DataJoint U24 - Workflow Volume
#

# %% [markdown]
# Change into the parent directory to find the `dj_local_conf.json` file.
#

# %% tags=[]
import os
import datajoint as dj
from pathlib import Path

# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")

# %%
from workflow_volume.pipeline import (
    imaging_report,
    volume,
    bossdb,
    imaging,
    scan,
    Device,
    session,
    subject,
    surgery,
    lab,
)

dj.config["safemode"] = True  # Set to false to turn off drop confirmation

# %% [markdown]
# ## Drop schemas
#
# - Schemas are not typically dropped in a production workflow with real data in it.
# - At the developmental phase, it might be required for the table redesign.
# - When dropping all schemas is needed, drop items starting with the most downstream.
#

# %%
# imaging_report.schema.drop()
# volume.schema.drop()
# bossdb.schema.drop()
# imaging.schema.drop()
# scan.schema.drop()
# Device.drop_quick()
# session.schema.drop()
# subject.schema.drop()
# surgery.schema.drop()
# lab.schema.drop()
