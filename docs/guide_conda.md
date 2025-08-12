# Conda

## Contents

- [Create Environment](#create-environment)
- [Delete Environment](#delete-environment)
- [Activate/Deactive Environment ](#activatedeactive-environment)
- [Export Environment to File (For Sharing, etc.)](#export-environment-to-file-for-sharing-etc)
- [Change Conda Directory to Different Drive](#change-conda-directory-to-different-drive)

---

## Create Environment 

Create from scratch

```
conda create --name ENV --channel conda-forge python==VER
```

...or create environment from yml file

```
conda env create --file environment.yml
```

**Args:**
- `ENV`: user set environment name
- `--channel`: specifies which channel to use to get packages. Channel most recommended is  `conda-forge`. 
- Any additional keywords are interpretted as the names of packages. Common packages include `spyder`, `jupyter_core`, `matplotlib-base`, and `ipykernel`.
	- `==VER`: for each package, if the version number is not specified, the newest version will be downloaded.
- `--file environment.yml`: load the file specified. Conventional to name file `environment.yml` but any location and name can be used.

## Delete Environment

```
conda remove --name ENV --all
```

**Args:**
- `ENV`: user set environment name

## Activate/Deactive Environment 

### Activate environment

```
conda activate ENV
```

**Args:**
- `ENV`: user set environment name

...or deactivate environment

```
conda deactivate
```

## Export Environment to File (For Sharing, etc.)

```
conda env export --file environment.yml
```

**Args:**
- `--file environment.yml`: load the file specified. Conventional to name file `environment.yml` but any location and name can be used.

## Change Conda Directory to Different Drive

```
cd /d PATH
```
**Args:**
- `/d`: specifies a different drive is going to be used.
- `PATH`: new absolute path to change the current directory to.