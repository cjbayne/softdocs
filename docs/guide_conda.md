# Conda

## Contents

- [Create Environment](#create-environment)
- [Delete Environment or Packages](#delete-environment-or-packages)
- [Activate or Deactive Environment ](#activate-or-deactive-environment)
- [Export Environment to File](#export-environment-to-file)
- [Change Directory to Different Drive in Anaconda Prompt](#change-directory-to-different-drive-in-anaconda-prompt)

---

## Create Environment 

### Args
- `-c, --channel CHANNEL`: Additional channel to search for packages. The default channel_alias is https://conda.anaconda.org/. Channel most recommended is  `conda-forge`.
- `-f, --file FILE`: Environment definition file (default: environment.yml). 
- `-n, --name ENVIRONMENT`: Name of environment.
- `-p, --prefix PATH`: Full path to environment location (i.e. prefix).
- Additional keywords are names of package to install during creation. Common packages include `python`, `spyder`, `jupyter_core`, `matplotlib-base`, and `ipykernel`. These packages can be installed later as well.
	- To specify the version, append `==VER` with the version number. If the version number is not specified, the newest version will be downloaded.

### Examples

Create environment from file

    conda env create -f /path/to/environment.yml

Create environment from file and specify virtual environment location

    conda env create -f /path/to/requirements.txt -p /home/user/envname

Create environment from scratch

    conda create -n myenv -c conda-forge python

## Delete Environment or Packages

### Args
- `-n, --name ENVIRONMENT`: Name of environment.
- `--all`: Remove all packages, i.e., the entire environment.

### Examples

Remove the package 'scipy' from the currently-active environment

    conda remove scipy

Remove a list of packages from an environment 'myenv'

    conda remove -n myenv scipy curl wheel

Remove all packages from environment `myenv` and the environment itself

    conda remove -n myenv --all

Remove all packages from the environment `myenv` but retain the environment

    conda remove -n myenv --all --keep-env


## Activate or Deactive Environment 

### Args
- `ENVIRONMENT`: name of environment.
- `-f, --file FILE`: Environment definition file (default: environment.yml).

### Examples

Activate environment

	conda activate ENVIRONMENT

Deactivate environment

	conda deactivate

## Export Environment to File

- Export an enviroment for sharing, etc.

### Args
- `-f, --file FILE`: Environment definition file (default: environment.yml).

### Examples

Export the current environment into a .yml file 

	conda env export -f environment.yml


## Change Directory to Different Drive in Anaconda Prompt

- If changing the current working directory (cwd) to a different drive in an Anaconda Prompt window, need additional argument.

### Args
- `/d`: specifies a different drive is going to be used.
- `PATH`: new absolute path to change the current directory to.

### Examples

Change the cwd from the C drive to a location in the B drive (PATH = B:)

	cd /d PATH