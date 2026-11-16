import pandas as pd
from pathlib import Path
import yaml

from . import steps
import importlib
importlib.reload(steps)

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


env: Environment | None = None  # Will be initialized by caller

def init_environment(template_dirs: Path):
    global env    
    """
    template_dirs: list of filesystem paths
    """
    loader = FileSystemLoader(template_dirs)
    env = Environment(loader=loader)


def generate_text_from_templates(
    project_config_path: Path
) -> str:
    # Load YAML config
    config = load_yaml(project_config_path)

    blocks_to_include = config.get("include_blocks", [])
    final_text_parts = []

    for block_name in blocks_to_include:
        template_filename = f"{block_name}.j2"

        try:
            template = env.get_template(template_filename)
        except TemplateNotFound as e:
            raise FileNotFoundError(
                f"Template block '{block_name}' not found via Jinja loader"
                f" (expected '{template_filename}')."
            ) from e

        # template_path = TEMPLATE_DIR / template_filename

        # if not template_path.exists():
        #     raise FileNotFoundError(
        #         f"Template block '{block_name}' not found at {template_path}"
        #     )

        # template = env.get_template(template_filename)
        rendered_text = template.render(**config)
        final_text_parts.append(rendered_text)

    # Combine into single output text
    return "\n\n".join(final_text_parts)


def create_paths_from_dict(root, paths_key):
    """Create every path from dictionary from given paths key.

    Args:
        root (Path object): Root path.
        paths_key (dict): Dictonary of paths.

    Returns:
        dict: Dictionary of paths appended from config to root.
    """
    return {k: root / v for k, v in paths_key.items()}


def generate_text(paths, export_path, text_type):
    file = paths["configs"] / f"{text_type}.yaml"
    text = generate_text_from_templates(file)
    export_text(text, export_path=paths[export_path]  / f"{text_type}.md", mode="w")


def export_text(text, export_path, mode):    
    with open(export_path, mode) as f:
        f.write(text)


# Remove function after verifying not in use
# def load_affordability_data(path, keep_default_na=False):
#     """Load in the affordability datasheet.
# 
#     Args:
#         path (Path): Path to file.
# 
#     Returns:
#         DataFrame: Contains content of file as pandas DataFrame.
#     """
#     return pd.read_csv(
#         path,
#         keep_default_na=keep_default_na
#     )


def load_standalone_tables(path):
    """Load tables not in star schema, which standalone.

    Args:
        path (Path): Path to file.

    Returns:
        DataFrame: Contains content of file as pandas DataFrame.
    """
    return pd.read_csv(path)


def load_yaml(path):
    """Load yaml file

    Args:
        path (Path): Path of yaml file.

    Returns:
        dict: Dictionary of yaml file contents.
    """
    with open(path, "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as error:
            print(f"Error parsing YAML file: {error}")



def deep_merge(base: dict, override: dict):
    """Recursively merge two dicts. override wins."""
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def override_yaml(source_path, override_path):
    if not source_path.exists() and not override_path.exists():
        return "Neither yaml file exists" 

    # Use this yaml to override contents in shared yaml
    if source_path.exists():
        source = load_yaml(source_path)
        # If file contents is empty
        if not source:
            source = {}
    else:
        source = {}

    if override_path.exists():
        override = load_yaml(override_path)
        source = deep_merge(source, override)
    return source


def merge_datasets(path, export_path, filename, ext, keep_default_na=False):
    """_summary_

    Args:
        path (_type_): _description_
        export_path (_type_): _description_
        filename (_type_): _description_
        ext (_type_): _description_
        keep_default_na (bool, optional): Keeps default na values as is. 
            Argument needed because some source data contains na values
            that need to be kept as is. Defaults to False.

    Raises:
        FileNotFoundError: _description_

    Returns:
        _type_: _description_
    """
    paths = sorted(path.glob(f"**/{filename}_*.{ext}"), key=lambda p: p.name)

    if not paths:
        raise FileNotFoundError(
            f"No files found under {path} matching '{filename}*.csv'"
        )

    print("The following datasets will be merged into a single dataset:")
    for p in paths:
        print(f"- {p.name}")

    frames = []
    all_columns = set()

    # First pass: read each file, add metadata, and collect columns
    for p in paths:
        if ext == "csv":
            df = pd.read_csv(
                p, low_memory=False, keep_default_na=keep_default_na
            )
        elif ext == "xlsx":
            df = pd.read_excel(p, keep_default_na=keep_default_na)
        
        frames.append(df)
        all_columns.update(df.columns)

    # Create a stable, ordered set of columns:
    # put metadata first, then other columns alphabetically
    ordered_cols = sorted(all_columns)

    # Reindex each frame to the union of columns so concat aligns perfectly
    aligned = [f.reindex(columns=ordered_cols) for f in frames]

    # Outer union happens naturally with concat when columns are aligned
    stacked = pd.concat(aligned, axis=0, ignore_index=True)

    # Standardize to pandas’ nullable dtypes
    stacked = stacked.convert_dtypes()

    # Write out
    out_path = export_path / f"{filename}.csv"
    stacked.to_csv(out_path, index=False)
    print(f"\nFinal merged dataset: {out_path}")
    return stacked



# ==========================================
# File Loading
# ==========================================

def load_dataframe(filename, cfg, path_suffix=None):
    """Load file based on config file contents into pandas DataFrame.

    Args:
        filename (str): Filename.
        config (dict): Config file contents.

    Raises:
        ValueError: File extension not supported.

    Returns:
        pd.DataFrame: File contents as pandas DataFrame.
    """

    # Get file configuration
    file_cfg = cfg["files"][filename]

    # Get directory
    directory = cfg["settings"]["directories"][file_cfg["directory"]]
    if path_suffix:
        full_directory = path_suffix / directory
    else:
        full_directory = directory

    # Build full path
    file_path = Path(full_directory) / filename
    
    # Get loading parameters
    read_params = file_cfg.get("read_params", {})

    # Validate file
    if not file_path.exists():
            raise FileNotFoundError(file_path)

    # Determine file type
    extension = file_path.suffix.lower()
    if extension == ".csv":
        return pd.read_csv(file_path, **read_params)
    elif extension in [".xlsx", ".xls"]:
        return pd.read_excel(file_path, **read_params)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

# ==========================================
# Data Processing
# ==========================================

def clean_dataframe(
    df,
    column_mapping={},
    # all_columns_upper=False,
    columns_alphabetized=False,
    columns_uppercase=False,
    reset_index=True,
    # split_explode_columns=None,
):
    """_summary_

    Args:
        df (_type_): _description_
        column_mapping (dict, optional): _description_. Defaults to {}.
        split_explode_columns (list, optional): List of columns to apply split and explode to. Defaults to None.

    Returns:
        _type_: _description_
    """
    stage = "clean"

    # Copy df
    df = df.copy()

    # Convert all columns to uppercase
    # if all_columns_upper:
    if columns_uppercase:
        df.columns = df.columns.str.upper()

    # Fix column names
    params = get_step_params(column_mapping, "replace", stage)
    if params is not None:
#     replace_configs = column_mapping.get("replace")
#     if replace_configs:
        for replace_config in params:
            match = replace_config["match"]
            replacement = replace_config["replace"]
            columns = replace_config.get("columns")

            df.columns = [
                col.replace(match, replacement)
                if columns is None or col in columns
                else col
                for col in df.columns
            ]

    # Rename columns
    params = get_step_params(column_mapping, "rename", stage)
    if params is not None:
    # if column_mapping.get("clean"):
        df = df.rename(columns=column_mapping["clean"])

        # Create columns if missing from clean column values
        missing = set(column_mapping["clean"].values()) - set(df.columns)
        df[list(missing)] = None

    # Trim whitespaces
    params = get_step_params(column_mapping, "trim", stage)
    if params is not None:
    # if column_mapping.get("trim"):
        for col in params:
            df[col] = df[col].str.strip()

    # Set dtypes
    params = get_step_params(column_mapping, "set_dtypes", stage)
    if params is not None:
        df = set_dtypes(df, params)

    # is_valid = column_mapping.get("set_dtypes")
    # if is_valid:
    #     if is_valid.get("_clean"):
    #         df = set_dtypes(df, is_valid.get("_clean"))
    #     else:
    #         df = set_dtypes(df, column_mapping.get("set_dtypes"))

    # Drop specific rows
    params = get_step_params(column_mapping, "drop_rows", stage)
    if params is not None:
    # if column_mapping.get("drop_rows"):
        filters = column_mapping.get("drop_rows")
        drop_rows = []

        for rule in filters:
            mask = True
            for col, val in rule.items():
                mask = mask & (df[col] == val)

            drop_rows.extend(df[mask].index)

        drop_rows = list(set(drop_rows))
        df = df.drop(drop_rows)

    # # Explode values
    # if split_explode_columns:
    #     df[split_explode_columns] = df[split_explode_columns].apply(
    #         lambda col: col.str.split(",")
    #     )
    #     df = df.explode(split_explode_columns)


    # # Drop any possible duplicate rows
    # df = df.drop_duplicates()

    # Sort alphabetically
    if columns_alphabetized:
        df = df.sort_index(axis=1)

    # Reset index
    df = df.reset_index(drop=reset_index)

    return df

def get_step_params(config, step_name, stage):

    params = config.get(step_name)

    if params is None:
        return None

    stage_keys = {
        key for key in params
        if key.startswith("@")
    }

    if stage_keys:
        return params.get(f"@{stage}")

    return params




def set_dtypes(df, dtype_config):
    for col, dtype_config_value in dtype_config.items():

        if col not in df.columns:
            continue

        # Simple dtype: string, int, float, etc.
        if isinstance(dtype_config_value, str):
            dtype = dtype_config_value

            if dtype == "string":
                df[col] = df[col].astype("string")

            elif dtype == "int":
                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                ).astype("Int64")

            elif dtype == "float":
                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                ).astype("float64")

            else:
                df[col] = df[col].astype(dtype)

        # Dtype with additional configuration
        elif isinstance(dtype_config_value, dict):
            dtype = dtype_config_value.get("dtype")

            if dtype == "datetime":
                date_format = dtype_config_value.get("format")

                df[col] = pd.to_datetime(
                    df[col],
                    format=date_format,
                    errors="coerce"
                )
    return df

def run_stage(
    df,
    dataset_config,
    stage,
):

    # Copy df
    df = df.copy()

    stage_steps = dataset_config.get(
        stage,
        []
    )

    for step_config in stage_steps:

        step_name = step_config["step"]

        # getattr() is a built-in Python function that lets you retrieve an attribute from an object using a string.
        handler = getattr(
            steps,
            step_name,
            None,
        )

        if handler is None:
            raise ValueError(
                f"Unknown step: {step_name}"
            )

        df = handler(
            df,
            step_config,
        )

    return df