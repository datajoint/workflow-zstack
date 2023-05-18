# DataJoint Workflow for ZStack Imaging

The DataJoint Workflow for ZStack Imaging combines five DataJoint Elements for cell 
segmentation, volume registration, and cell matching - Elements Lab, 
Animal, Session, Calcium Imaging, and ZStack.  DataJoint Elements collectively standardize and automate data collection and 
analysis for neuroscience experiments.  Each Element is a modular pipeline for data 
storage and processing with corresponding database tables that can be combined with
other Elements to assemble a fully functional pipeline.  This repository also provides 
a tutorial environment and notebook to learn the pipeline.

## Experiment Flowchart

![flowchart](https://raw.githubusercontent.com/datajoint/element-zstack/main/images/flowchart.svg)

## Data Pipeline Diagram

![pipeline](https://raw.githubusercontent.com/datajoint/element-zstack/main/images/pipeline.svg)

## Getting Started

+ [Interactive tutorial on GitHub Codespaces](#interactive-tutorial)

+ Install Element ZStack from PyPI

     ```bash
     pip install element-zstack
     ```

+ [Documentation](https://datajoint.com/docs/elements/element-zstack)

## Support

+ If you need help getting started or run into any errors, please contact our team by email at support@datajoint.com.

## Interactive Tutorial

+ The easiest way to learn about DataJoint Elements is to use the tutorial notebook within the included interactive environment configured using [Dev Container](https://containers.dev/).

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

1. We recommend you start by navigating to the `notebooks` directory. Execute the cells in the notebooks to begin your walk through of the tutorial.
