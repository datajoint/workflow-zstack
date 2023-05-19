# DataJoint Workflow for ZStack Imaging

The DataJoint Workflow for ZStack Imaging combines five DataJoint Elements for
volume cell segmentation - Elements Lab, Animal, Session, Calcium Imaging, and
ZStack. DataJoint Elements collectively standardize and automate data collection
and analysis for neuroscience experiments. Each Element is a modular pipeline for data 
storage and processing with corresponding database tables that can be combined with
other Elements to assemble a fully functional pipeline. This repository also provides 
a tutorial environment and notebook to learn the pipeline.

## Experiment Flowchart

![flowchart](https://raw.githubusercontent.com/datajoint/element-zstack/main/images/flowchart.svg)

## Data Pipeline Diagram

![pipeline](https://raw.githubusercontent.com/datajoint/element-zstack/main/images/pipeline.svg)

## Getting Started

+ [Interactive tutorial](#interactive-tutorial)

+ Install Element ZStack from PyPI

     ```bash
     pip install element-zstack
     ```

+ [Documentation](https://datajoint.com/docs/elements/element-zstack)

## Support

+ If you need help getting started or run into any errors, please contact our team by email at support@datajoint.com.

## Interactive Tutorial

### Launch Environment

+ Local Environment
  + Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  + Install [VSCode](https://code.visualstudio.com/)
  + Install [Conda](https://docs.conda.io/en/latest/miniconda.html)
  + Configure a database.  See [here](https://tutorials.datajoint.org/setting-up/local-database.html) for details.
  + `git clone` the code repository and open it in VSCode
  + Install the repository with `pip install -e .`
  + Setup a `dj_local_conf.json` with the `database.prefix` and `volume_root_data_dir`. See [User Guide](https://datajoint.com/docs/elements/user-guide/) for details.
  + Add your example data to the `volume_root_data_dir`.

### Instructions

1. To upload data to BossDB, [create an account](https://api.bossdb.io) to
   access the BossDB API and generate an API token. Please contact the team at [BossDB](https://bossdb.org)
   to ensure you have `resource-manager` permissions for your account. 
2. Follow the instructions below to set up the
   [intern](https://github.com/jhuapl-boss/intern) REST API locally. 
   + Create a new folder `.intern` in your root directory.
   + Create a configuration file `intern.cfg` within the `.intern` folder. The
     path to this file should be `~/.intern/intern.cfg`. 
   + The `intern.cfg` file should contain the following exactly as shown below:
   ```bash
    # ~/.intern/intern.cfg
    [Default]
    protocol = https
    host = api.bossdb.io
    token = <your-api-key>
   ```
3. Use the instructions above to set up a local environment.
4. Navigate to the `notebooks` directory. Execute the cells in the notebooks to begin your walk through of the tutorial.