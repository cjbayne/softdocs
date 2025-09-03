# Guide to X

This document is a guide to using the Python's `pathlib` built-in library. It is a "better" alternative to the `os` built-in library.

## Contents

- [`pathlib` Common Commands](#pathlib-common-commands)
- [`Path` Object Components](#path-object-components)
- [Rename `Path` Objects](#rename-path-objects)
- [Get File Metadata](#get-file-metadata)
- [Working With Files and Folders](#working-with-files-and-folders)

## `pathlib` Common Commands

Import `pathlib` library

```python
from pathlib import Path
```

Convert a string of a Windows path into a `WindowsPath` object

```python
# Convert string to path object
Path(r'C:\Users\me\py.data.py')

# Returns
WindowsPath('C:/Users/me/py/data.py')
```

Extend `Path` object

```python
# Add subdirectory and filename to path object
Path(r'C:\Users\me\python') / 'script' / 'data.py'

# Returns
WindowsPath('C:/Users/me/python/script/data.py')
```

- Returns a `WindowsPath` object with additional path elements
- Uses forward slashes (/) and can concatenate multiple elements

Get current working directory

```python
# The current working directory is set to C:/Users/me/py 
Path.cwd()

# Returns
WindowsPath('C:/Users/me/py')
```

- Returns a `WindowsPath` object representing the current working directory

Convert `Path` object to a string

```python
# Wrap path object with str function
str(Path(r'C:\Users\me\py.data.py'))

# Returns
'C:\\Users\\me\\py.data.py'
```

- `Path().__str__()` also works but is **not recommended** because `str()` already internally calls `__str__()` (breaks encapsulation), reduces code clarity, and may break code if `str()` changes in the future

Check if a path exists

```python
# Print message to user if path does not exist
if not Path().exists():
    print("File doesn't exist")

# Returns message if the file does not exist
"File doesn't exist"
```

- `Path().exists()` returns `True` if the `Path` object exists, otherwise `False`.

Create directory


```python
>>> Path().mkdir()
```
- Creates a directory **only if it does not already exist**.
- Argument `exist_ok` (default=`False`). If the directory exists, `FileExistsError` raised. If set to `True`, `FileExistsError` is ignored, and the directory is not overwritten

## `Path` Object Components

The following table shows how to get the components of the path:

`C:\Users\me\py\data.py`

| Path Component | Code            | Output                   | Suggested Variable |
|--------------- |-----            |-------                   | ------------------ |
| Full Path      | `str(Path())`   | `C:\Users\me\py\data.py` | `full_path`        |
| Parent of Path | `Path().parent` | `C:\Users\me\py`         | `parent_path`      |
| Root           | `Path().anchor` | `C:\`                    | `root`             |
| File Name      | `Path().name`   | `data.py`                | `filename`         |
| File Root      | `Path().stem`   | `data`                   | `file_root`        |
| File Extension | `Path().suffix` | `.py`                    | `ext`            |

### Extract Individual Parts of Path

- Returns a tuple containing every folder and filename.

```python
>>> Path().parts
```

**Example:**
```python
>>> Path(r'C:\Users\me\py\data.py').parts
('C:\\', 'Users', 'me', 'py', 'data.py')
```

### Get Relative Parts of a Path

- Returns the remaining path relative to another path (can be `Path` object or string).

```python
>>> Path().relative_to()
```

**Example:**
```python
>>> Path(r'C:\Users\me\py\data.py').relative_to(Path(r'C:\Users\me')) # Path object
WindowsPath('py/data.py')
>>> Path(r'C:\Users\me\py\data.py').relative_to(r'C:\Users\me') # string
WindowsPath('py/data.py')
```

---

## Rename `Path` Objects

### Rename Parts of `Path` Object

- Change parts of `Path` object.
- **None of these modifies the actual filename on the system.**
- **Warning:** Omitting the dot (`'.'`) in `.with_suffix()` raises `ValueError: Invalid suffix ''`.

```python
# change filename
>>> Path().with_name('newname.txt')
# change filename stem
>>> Path().with_stem('newname')
# change filename extension
>>> Path().with_suffix('.txt') 
```

**Example:**
```python
# change filename
>>> Path(r'C:\Users\me\py\data.py').with_name('newname.txt')
WindowsPath('C:/Users/me/py/newname.txt')

# change filename stem
>>> Path(r'C:\Users\me\py\data.py').with_stem('newname')
WindowsPath('C:/Users/me/py/newname.py')

# change filename extension
>>> Path(r'C:\Users\me\py\data.py').with_suffix('.txt')
WindowsPath('C:/Users/me/py/data.txt')
```

### Rename Actual Files in the System (Overwrite Prohibited)

- Renames or moves a file to a new path.
- Raises `FileExistsError` if the destination file already exists.

```python
>>> Path().rename()
```

**Example:**
```python
>>> Path(r'C:\Users\me\py\data.py').rename(Path(r'C:\Users\me\py\test.py'))
WindowsPath('C:/Users/me/py/test.py')
```

### Rename Actual Files in the System (Overwrite Permitted)

- Renames files, overwriting any existing file at the destination.

```python
>>> Path().replace()
```

**Example:**
```python
>>> Path(r'C:\Users\me\py\data.py').replace(r'C:\Users\me\py\test.py')
WindowsPath('C:/Users/me/py/test.py')
```

---

## Get File Metadata

### Get File Creation Date

```python
>>> from datetime import datetime
>>> datetime.fromtimestamp(Path().lstat().st_mtime)
```

**Example:**
```python
>>> datetime.fromtimestamp(Path().lstat().st_mtime)
datetime.datetime(2025, 1, 28, 13, 28, 46, 216162)
>>> print(datetime.fromtimestamp(Path().lstat().st_mtime))
'2025-01-28 13:28:46.216162'
```

---

## Working with Files and Folders

### Check If Path Object is Directory

- Return `True` if path points to a directory, `False` if it is another kind of file

```python
>>> Path().is_dir()
```

**Example:**
```python
>>> Path.cwd().is_dir()
True
```

### Check If Path Object is File

- Return `True` if path points to a directory, `False` if it is another kind of file

```python
>>> Path().is_file()
```

**Example:**
```python
>>> Path.cwd().is_file()
True
```

### Get All Folders and Files in Directory (Include Subdirectories)

- Creates a generator object with all folder and file paths in directory, including subdirectories.
- Common to use list comprehension to iterate over generator object.

```python
>>> Path().glob('**/*')
```

**Example:**
```python
# return all folder and file paths in directory, includes subdirectories
>>> [x for x in Path.cwd().glob('**/*')]

# return all file paths that begin with the string 'pandas' in the cwd's subfolder named '.ipynb'
>>> Path.cwd().glob('.ipynb/pandas*')

# return all file paths with extension '.py' in cwd's subfolder named '.ipynb'
>>> Path.cwd().glob('.ipynb/*.py')
# use .rglob() if there are multiple folders with the same name and/or are deeper than the first subfolder 
>>> Path.cwd().rglob('.ipynb/*.py')
```

### Get All Folders and Files in Directory (Not Including Subdirectories)

- Creates a generator object with all folder and file paths in directory, not including subdirectories.
- Common to use list comprehension to iterate over generator object.

```python
>>> Path().iterdir()
```

**Example:**
```python
# return all folder and file paths in directory, does not include subdirectories
>>> [x for x in Path.cwd().iterdir()]

# return all subfolder paths only in directory
>>> [x for x in Path.cwd().iterdir() if x.is_dir()]

# return all file paths in directory
>> [x for x in Path.cwd().iterdir() if x.is_file()]
```