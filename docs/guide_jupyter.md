# Guide to Jupyter

## Change Jupyter's default start directory

* Right-click Start Menu icon > More > Open file location
* Right-click shortcut > Properties
* In Target: X\python.exe X\cwp.py X\envs\E X\envs\E\python.exe X\envs\E\Scripts\jupyter-notebook-script.py "path"
- If this is for base environment, just remove all envs\E parts
- X = path to anaconda (e.g. C:\Users\10070015\AppData\Local\anaconda3)
- E = name of environment (e.g. env)
- path = path where Jupyter notebook will open
* Ok to keep Start in: as %HOMEPATH%

https://stackoverflow.com/questions/35254852/how-to-change-the-jupyter-start-up-folder

====================================

## Export Jupyter notebook without any code

https://stackoverflow.com/questions/34818723/export-notebook-to-pdf-without-code

* Activate relevant conda environment and enter command
conda activate [ENV]
jupyter nbconvert --no-input --to html [FULLPATH.ipynb]

- Change output location (default is same location as .ipynb)
--output-dir

- Change name of file
--output

====================================

## Create hyperlink within Jupyter code

* Create the hyperlink with the following:

```
[Hypertext](#link_id_no_spaces)
```

- [Hypertext] is the text which will be underlined and clickable
- (#link_id_no_spaces) is the unique link id assigned

* This is where the link will move to:

```
<a id='link_id_no_spaces'></a>
```

- 'link_id_no_spaces' is the matching unique link id

The following is a Python function that automatically creates a link using the copied text

```
def hyperlink():
    import pyperclip

    text = pyperclip.paste().replace('#', '').lstrip()
    text_edited = (
        text.replace(' ', '_')
        .replace('`', '')
        .lower())
    final = (f"- [{text}](#{text_edited})"
            f"\n<a id='{text_edited}'></a>")
    pyperclip.copy(final)
```

====================

## Add Jupyter notebook shortcut to desktop

https://stackoverflow.com/questions/62878573/is-there-a-way-to-make-a-desktop-shortcut-for-jupyter-notebook

* Right-click Desktop > create Shortcut
For base environment, copy and paste the following into the shortcut dialogue:

%PY_HOME%\python.exe %PY_HOME%\cwp.py %PY_HOME% %PY_HOME%\python.exe -m jupyter notebook

- Replace all %PY_HOME% text with location of anaconda (e.g. C:\Users\moba1\anaconda3)

For virtual environments, copy and paste the following into the shortcut dialogue:

%PY_HOME%\python.exe %PY_HOME%\cwp.py %PY_HOME%\envs\myenvironment %PY_HOME%\envs\myenvironment\python.exe -m jupyter notebook

- Replace all %PY_HOME% text with location of anaconda (e.g. C:\Users\moba1\anaconda3)
-- %USERPROFILE% can be used, which in the example above would equal C:\Users\moba1 (is shorter if the user name is > 4 characters)
-- ...or can set a system variable if the path is too long (e.g. %ANA% as C:\Users\me\AppData\Local\anaconda3)
- Replace all myenvironment text with env folder name (e.g. test)
- Can also add --ip XXX.X.X.X --port XXXX

* To change the default starting location, follow the steps above