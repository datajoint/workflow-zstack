# DataJoint Workflow for ZStack

The DataJoint Workflow for ZStack combines five DataJoint Elements for cell 
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

### Launch Environment

Here are some options that provide a great experience:

- Cloud-based Environment (*recommended*)
  - Launch using [GitHub Codespaces](https://github.com/features/codespaces) using the `+` option which will `Create codespace on main` in the codebase repository on your fork with default options. For more control, see the `...` where you may create `New with options...`.
  - Build time for a codespace is several minutes. This is done infrequently and cached for convenience.
  - Start time for a codespace is less than 1 minute. This will pull the built codespace from cache when you need it.
  - *Tip*: Each month, GitHub renews a [free-tier](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#monthly-included-storage-and-core-hours-for-personal-accounts) quota of compute and storage. Typically we run into the storage limits before anything else since codespaces consume storage while stopped. It is best to delete Codespaces when not actively in use and recreate when needed. We'll soon be creating prebuilds to avoid larger build times. Once any portion of your quota is reached, you will need to wait for it to be reset at the end of your cycle or add billing info to your GitHub account to handle overages.
  - *Tip*: GitHub auto names the codespace but you can rename the codespace so that it is easier to identify later.

- Local Environment
  - Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - Install [Docker](https://docs.docker.com/get-docker/)
  - Install [VSCode](https://code.visualstudio.com/)
  - Install the VSCode [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
  - `git clone` the codebase repository and open it in VSCode
  - Use the `Dev Containers extension` to `Reopen in Container` (More info is in the `Getting started` included with the extension.)

You will know your environment has finished loading once you either see a terminal open related to `Running postStartCommand` with a final message of `Done` or the `README.md` is opened in `Preview`.

### Instructions

1. We recommend you start by navigating to the `notebooks` directory on the left panel and go through the `tutorial.ipynb` Jupyter notebook. Execute the cells in the notebook to begin your walk through of the tutorial.

1. Once you are done, see the options available to you in the menu in the bottom-left corner. For example, in codespace you will have an option to `Stop Current Codespace` but when running Dev Container on your own machine the equivalent option is `Reopen folder locally`. By default, GitHub will also automatically stop the Codespace after 30 minutes of inactivity.  Once the codespace is no longer being used, we recommend deleting the codespace.
