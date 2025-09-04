# Guide to Pathlib

This document is a guide to using the Python"s `pathlib` built-in library. It is a "better" alternative to the `os` built-in library.

## Contents

- [`pathlib` Common Commands](#pathlib-common-commands)
- [`Path` Object Components](#path-object-components)
- [Renaming Objects](#renaming-objects)
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
Path(r"C:\Users\me\py.data.py")

# Returns
WindowsPath("C:/Users/me/py/data.py")
```

Extend `Path` object

```python
# Add subdirectory and filename to path object
Path(r"C:\Users\me\python") / "script" / "data.py"

# Returns
WindowsPath("C:/Users/me/python/script/data.py")
```

- Returns a `WindowsPath` object with additional path elements
- Uses forward slashes (/) and can concatenate multiple elements

Get current working directory

```python
# The current working directory is set to C:/Users/me/py 
Path.cwd()

# Returns
WindowsPath("C:/Users/me/py")
```

- Returns a `WindowsPath` object representing the current working directory

Convert `Path` object to a string

```python
# Wrap path object with str function
str(Path(r"C:\Users\me\py.data.py"))

# Returns
"C:\\Users\\me\\py.data.py"
```

- `Path().__str__()` also works but is **not recommended** because `str()` already internally calls `__str__()` (breaks encapsulation), reduces code clarity, and may break code if `str()` changes in the future

Check if a path exists

```python
# Print message to user if path does not exist
if not Path().exists():
    print("File doesn"t exist")

# Returns message if the file does not exist
"File doesn"t exist"
```

- `Path().exists()` returns `True` if the `Path` object exists, otherwise `False`.

Create directory

```python
# Make a directory of the path object
Path(Path.cwd() / "new").mkdir()
```

- Creates a directory **only if it does not already exist**
    - Argument `exist_ok` (default=`False`). If the directory exists, `FileExistsError` raised. If set to `True`, `FileExistsError` is ignored, and the directory is not overwritten

## `Path` Object Components

The following table shows how to get the components of the path:

`C:\Users\me\py\data.py`

| Path Component | Code            | Output                   |
|--------------- |-----            |-------                   |
| Full path      | `str(Path())`   | `C:\Users\me\py\data.py` |
| Parent of path | `Path().parent` | `C:\Users\me\py`         |
| Root           | `Path().anchor` | `C:\`                    |
| File name      | `Path().name`   | `data.py`                |
| File root      | `Path().stem`   | `data`                   |
| File extension | `Path().suffix` | `.py`                    |

Extract every individual parts of path

```python
# Get every individual part of path
Path(r"C:\Users\me\py\data.py").parts

# Returns
("C:\\", "Users", "me", "py", "data.py")
```

- Returns a tuple containing every folder and filename

Get relative parts of a path

```python
# Return the parts after the part passed to relative to
Path(r"C:\Users\me\py\data.py").relative_to(Path(r"C:\Users\me"))

# Returns
WindowsPath("py/data.py")
```

- Argument in `relative_to()` can be `Path` object or string

## Renaming Objects

Change the file name in the path object only

```python
# Change file name from data.py to newname.txt
Path(r"C:\Users\me\py\data.py").with_name("newname.txt")

# Returns
WindowsPath("C:/Users/me/py/newname.txt")
```

- This will **NOT** modify the actual files on the system

Change the file root in the path object only

```python
# Change file root from data to newname
Path(r"C:\Users\me\py\data.py").with_stem("newname")

# Returns
WindowsPath("C:/Users/me/py/newname.py")
```

- This will **NOT** modify the actual files on the system

Change the file extension in the path object only
```python
# Change file extenstion from .py to .txt
Path(r"C:\Users\me\py\data.py").with_suffix(".txt")

# Returns
WindowsPath("C:/Users/me/py/data.txt")
```

- This will **NOT** modify the actual files on the system
- **Warning:** Omitting the dot (`"."`) in `.with_suffix()` raises `ValueError: Invalid suffix ""`

Change the actual file name in the system (overwrite is prohibited)

```python
# Rename the actual file from data.py to test.py (keep the same location)
Path(r"C:\Users\me\py\data.py").rename(Path(r"C:\Users\me\py\test.py"))

# Returns
WindowsPath("C:/Users/me/py/test.py")
```

- If part of the directory is changed as well, the file will move to the new path
- Raises `FileExistsError` if the file already exists

Change the actual file name in the system (overwrite is permitted)

```python
# Rename the actual file from data.py to test.py (keep the same location)
Path(r"C:\Users\me\py\data.py").replace(r"C:\Users\me\py\test.py")

# Returns
WindowsPath("C:/Users/me/py/test.py")
```

- File is renamed and any existing file at the destination is overwritten

## Get File Metadata

Get file creation date

```python
# Get the file creation date
datetime.fromtimestamp(Path().lstat().st_mtime)

# Returns
datetime.datetime(2025, 1, 28, 13, 28, 46, 216162)
```

- Requires datetime import `from datetime import datetime`
- Pass through `print()` show in human readable version > `"2025-01-28 13:28:46.216162"`


## Working with Files and Folders

Check if path object is a directory

```python
# See if the current working directory is a directory
Path.cwd().is_dir()

# Returns
True
```

- Return `True` if path points to a directory, `False` if it is not

Check if path object is a file

```python
# See if the current working directory is a file
Path.cwd().is_file()

# Returns
True
```

- Return `True` if path points to a file, `False` if it is not

Get all folders and files in directory (include subdirectories)

```python
# Return a list of every file and folder in a directory, include subdirectory content
[x for x in Path.cwd().glob("**/*")]
```

- Creates a generator object with all folder and file paths in directory, including subdirectories
- Common to use list comprehension to iterate over generator object
- To return a list with only files or folders that begins with a string (e.g., `pandas`), replace `.glob("**/*")` with `.glob("**/pandas*")` 
    - The `*` after `pandas` means any other string can follow this
- To return a list with only files that end with a certain extension (e.g. `.py`), replace `.glob("**/*")` with `.glob("**/*.py")` 
- To return a list with only files that end with a certain extension in a direct subdirectory (e.g. `.py` files in directory `docs`), replace `.glob("**/*")` with `.glob("docs/*.py")`

Get all folders and files in directory (exclude subdirectories)

```python
# Return a list of every file and folder in a directory, exclude subdirectory contents
[x for x in Path.cwd().iterdir()]
```

- Creates a generator object with all folder and file paths in directory, not including subdirectories
- Common to use list comprehension to iterate over generator object
- Add `if x.is_dir()` at the end to only return folders
- Add `if x.is_file()` at the end to only return files
