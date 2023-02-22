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

# %% [markdown] tags=[]
# ## Configure DataJoint

# %% [markdown] tags=[]
# - To run an Element workflow, we need to set up a DataJoint config file, called `dj_local_conf.json`, unique to each machine.
#
# - To upload to BossDB, you'd need to configure an `intern.cfg`.
#
# - These configs only need to be set up once. If you already have them, skip to [02-Workflow-Structure](./02-WorkflowStructure_Optional.ipynb).
#
# - By convention, we set a local config in the workflow directory. You may be interested in [setting a global config](https://docs.datajoint.org/python/setup/01-Install-and-Connect.html).

# %%
import os

# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")

# %% [markdown]
# ### Configure database host address and credentials

# %% [markdown]
# Now we can set up credentials following [instructions here](https://tutorials.datajoint.io/setting-up/get-database.html).

# %%
import datajoint as dj
import getpass

dj.config["database.host"] = "{YOUR_HOST}"
dj.config["database.user"] = "{YOUR_USERNAME}"
dj.config["database.password"] = getpass.getpass()  # enter the password securely

# %% [markdown]
# You should be able to connect to the database at this stage.

# %%
dj.conn()

# %% [markdown]
# ### Configure the `custom` field

# %% [markdown]
# #### Prefix

# %% [markdown]
# A schema prefix can help manage privelages on a server. Teams who work on the same schemas should use the same prefix.
#
# Setting the prefix to `neuro_` means that every schema we then create will start with `neuro_` (e.g. `neuro_lab`, `neuro_subject`, `neuro_model` etc.)

# %%
dj.config["custom"] = {"database.prefix": "neuro_"}

# %% [markdown]
# #### Root directory

# %% [markdown]
# `vol_root_data_dir` sets the root path(s) for the Element. Given multiple, the Element will always figure out which root to use based on the files it expects there. This should be the directory shared across all volumetric data.

# %%
dj.config["custom"] = {"vol_root_data_dir": ["/tmp/test_data/", "/tmp/example/"]}

# %% [markdown]
# ## Save the DataJoint config as a json
#
# Once set, the config can either be saved locally or globally. 
#
# - The local config would be saved as `dj_local_conf.json` in the workflow directory. This is usefull for managing multiple (demo) pipelines.
# - A global config would be saved as `datajoint_config.json` in the home directory.
#
# When imported, DataJoint will first check for a local config. If none, it will check for a global config.

# %%
dj.config.save_local()
# dj.config.save_global()

# %% [markdown]
# ## Configuring `intern`

# %% [markdown]
# Please refer [BossDB resources](https://www.youtube.com/watch?v=eVNr6Pzxoh8) for
# information on generating an account and configuring `intern`.
#
# Importantly, you'll need an `intern` config file at your root directory with your BossDB api token as follows:
#
# ```cfg
#     # ~/.intern/intern.cfg
#     [Default]
#     protocol = https
#     host = api.bossdb.io
#     token = <YOUR_TOKEN>
# ```
#

# %% [markdown]
# In the [next notebook](./02-WorkflowStructure_Optional.ipynb) notebook, we'll explore the workflow structure.
