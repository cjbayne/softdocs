import numpy as np
import pandas as pd

def alphabetize_columns(df, config):
    df = df.sort_index(axis=1)
    return df


def columns_uppercase(df, config):

    df.columns = df.columns.str.upper()
    return df


def create_boolean_flag(
    df: pd.DataFrame,
    config: dict,
) -> pd.DataFrame:
    """
    Create boolean columns based on a condition.

    Supported conditions:
        - contains
        - equals
        - numeric
        - null
        - not_null
    """

    source_column = config["source_column"]
    output_column = config["output_column"]
    condition = config.get("condition", None)
    value = config.get("value")

    case = config.get(
        "case",
        False,
    )

    if condition == "contains":
        mask = df[source_column].str.contains(
            value,
            case=case,
            na=False,
        )

    elif condition == "equals":

        mask = df[source_column].eq(value)

    elif condition == "numeric":

        mask = pd.to_numeric(
            df[source_column],
            errors="coerce",
        ).notna()

    elif condition == "null":
        mask = df[source_column].isna()

    elif condition == "not_null":
        mask = df[source_column].notna()

    else:

        raise ValueError(
            f"Unsupported condition: {condition}"
        )

    df[output_column] = mask

    return df

def create_conditional_column(
    df: pd.DataFrame,
    cfg: dict,
) -> pd.DataFrame:
    """
    Create derived columns based on a configurable condition.

    Supported conditions:
        - numeric
        - null
        - not_null
        - empty
        - not_empty

    Parameters
    ----------
    df : pd.DataFrame
        Source dataframe.

    config : dict
        Example:

        {
            "columns": ["RATE_6HCF", "MHI"],
            "condition": "numeric",
            "true_value": "Reported",
            "suffix": "_STATUS"
        }

    Behavior
    --------
    If condition is True:
        output_column = true_value

    Otherwise:
        output_column = original value
    """

    source_column = cfg["source_column"]
    output_column = cfg["output_column"]

    condition = cfg.get(
        "condition",
        "numeric",
    )

    true_value = cfg.get(
        "true_value",
        "Reported",
    )
    false_value = cfg.get("false_value", None)

    if source_column not in df.columns:
        raise KeyError(
            f"Columns not found: {source_column}"
        )

    if condition == "numeric":

        mask = pd.to_numeric(
            df[source_column],
            errors="coerce",
        ).notna()

    elif condition == "null":

        mask = df[source_column].isna()

    elif condition == "not_null":

        mask = df[source_column].notna()

    elif condition == "empty":

        mask = (
            df[source_column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
        )

    elif condition == "not_empty":

        mask = (
            df[source_column]
            .fillna("")
            .astype(str)
            .str.strip()
            .ne("")
        )

    else:

        raise ValueError(
            f"Unsupported condition: {condition}"
        )

    # df[output_column] = np.where(
    #     mask,
    #     true_value,
    #     df[column],
    # )

    if false_value is None:
        df[output_column] = np.where(
            mask,
            true_value,
            df[source_column],
        )
    else:
        df[output_column] = np.where(
            mask,
            true_value,
            false_value,
        )

    return df

# import numpy as np
# def create_numeric_status(
#     df: pd.DataFrame,
#     config: dict,
# ) -> pd.DataFrame:
#     """
#     Create status columns based on whether source values are numeric.
# 
#     If a value can be converted to numeric, the corresponding status
#     is set to `reported_value`. Otherwise, the original source value
#     is retained.
# 
#     Example:
#         RATE -> RATE_STATUS
#         MHI       -> MHI_STATUS
#     """
# 
#     columns = config["columns"]
#     reported_value = config.get(
#         "reported_value",
#         "Reported",
#     )
#     suffix = config.get(
#         "suffix",
#         "_STATUS",
#     )
# 
#     missing_columns = [
#         column
#         for column in columns
#         if column not in df.columns
#     ]
# 
#     if missing_columns:
#         raise KeyError(
#             f"Columns not found: {missing_columns}"
#         )
# 
#     for column in columns:
#         output_column = f"{column}{suffix}"
# 
#         numeric_values = pd.to_numeric(
#             df[column],
#             errors="coerce",
#         )
# 
#         is_numeric = numeric_values.notna()
# 
#         df[output_column] = df[column].where(
#             ~is_numeric,
#             reported_value,
#         )
# 
#     return df

def fill_na_values(df, cfg):
    fill = cfg.get("fill", "n/a")
    return df.fillna({c: fill for c in cfg["columns"]})

def filter_dataset(df, cfg):
    # If an empty list should mean "select no rows/columns," use an explicit is None
    columns = cfg.get("columns")
    rows = cfg.get("rows")
    df = df.loc[
        slice(None) if rows is None else rows,
        slice(None) if columns is None else columns
    ]
    return df


def normalize_datetime(df, cfg):
    # Normalize dates, i.e., set times to 0:00
    columns = cfg.get("columns", [])
    df[columns] = df[columns].apply(
        lambda col: col.dt.normalize()
    )
    return df


def rename_columns(df, config):

    df = df.rename(columns=config["mapping"])

    # Create columns if missing from clean column values
    missing = set(config["mapping"].values()) - set(df.columns)
    df[list(missing)] = None
    return df

def replace_by_key_values(
        df: pd.DataFrame, 
        columns: list, 
        mapping: dict):
    df[columns] = df[columns].replace(mapping)
    return df


def replace_text_patterns(df, config):

    columns = config["columns"]
    pattern = config["pattern"]
    repl = config.get("repl", "")
    regex = config.get("regex", True)

    df[columns] = df[columns].apply(
        lambda col: col.astype(str).str.replace(pattern, repl, regex=regex)
    )
    return df

def replace_exact_values(
    df: pd.DataFrame,
    cfg: dict,
) -> pd.DataFrame:
    """
    Replace values using a mapping.
    """

    columns = cfg["columns"]
    mapping = cfg["mapping"]

    df[columns] = df[columns].replace(mapping)

    return df

# May replace function below with create_numeric_status()
# def return_elements_by_condition(
#     df: pd.DataFrame,
#     columns: Sequence[str],
#     condition,
#     x,
#     y,
#     suffix: str = ""
# ) -> pd.DataFrame:
#     """
#     Create or overwrite columns based on a boolean condition.
# 
#     Parameters
#     ----------
#     df : pd.DataFrame
#         The input DataFrame to modify (in-place).
#     columns : Sequence[str]
#         Base column names to create. Suffix will be appended to each.
#     condition : Union[pd.Series, pd.DataFrame, np.ndarray, Sequence[bool]]
#         The boolean condition. Can be:
#         - 1-D (length == len(df)): applies to all target columns equally.
#         - 2-D (shape == (len(df), len(columns))): column-wise condition.
#     x, y : Any
#         Values to place where condition is True (x) and False (y).
#         Can be scalars or arrays; must broadcast with `condition`.
#     suffix : str, optional
#         Suffix to append to each target column name (default "").
# 
#     Returns
#     -------
#     pd.DataFrame
#         The same DataFrame, modified in place, also returned for chaining.
# 
#     Notes
#     -----
#     - When assigning to a list of columns (e.g., df[["A", "B"]]),
#       pandas expects a 2-D RHS with shape (n_rows, n_cols).
#     - If `condition` is 1-D (Series), `np.where` returns 1-D.
#       We explicitly reshape/replicate to 2-D so pandas accepts the assignment.
#     """
# 
#     # Build the final target column names (e.g., "X" -> "X_STATUS")
#     out_cols = [f"{c}{suffix}" for c in columns]
# 
#     # Convert condition to a NumPy array for predictable shape handling
#     cond = np.asarray(condition)
# 
#     # Basic sanity check: the first dimension must match number of rows in df
#     if cond.shape[0] != len(df):
#         raise ValueError(
#             f"`condition` length/rows ({cond.shape[0]})"
#             f" must equal len(df) ({len(df)})."
#         )
# 
#     # Compute values with np.where. Shape of `vals` follows shape of `cond`.
#     #    - If cond is 1-D (n_rows,), vals will be 1-D.
#     #    - If cond is 2-D (n_rows, k), vals will be 2-D with k columns.
#     vals = np.where(cond, x, y)
#     vals = np.asarray(vals)  # ensure ndarray for shape introspection
# 
#     # Normalize `vals` shape to what the LHS expects:
#     #    LHS: df[out_cols] expects 2-D with shape (n_rows, len(out_cols)).
#     n_rows = len(df)
#     n_out = len(out_cols)
# 
#     if vals.ndim == 1:
#         # Case: condition was 1-D ⇒ vals is 1-D of length n_rows.
#         # If assigning to a single column via list, reshape to (n_rows, 1).
#         # If assigning to multiple columns, replicate across columns.
#         if n_out == 1:
#             vals = vals.reshape(n_rows, 1)
#         else:
#             vals = np.column_stack([vals] * n_out)
# 
#     elif vals.ndim == 2:
#         # Case: condition was 2-D ⇒ vals is 2-D (n_rows, k).
#         # Make sure the number of columns matches the number of targets.
#         if vals.shape[0] != n_rows:
#             raise ValueError(
#                 f"RHS row count ({vals.shape[0]})"
#                 f" does not match df rows ({n_rows})."
#             )
#         if vals.shape[1] != n_out:
#             raise ValueError(
#                 f"RHS has {vals.shape[1]} columns,"
#                 f" but LHS expects {n_out} (targets: {out_cols})."
#                 " If you intended to broadcast the same values to all target"
#                 " columns, pass a 1-D condition or reshape/replicate."
#             )
#     else:
#         # Higher-dimensional arrays not supported in this assignment pattern.
#         raise ValueError("`condition`/RHS must be 1-D or 2-D.")
# 
#     # Perform the assignment. Because `vals` is now 2-D with the exact
#     #    number of target columns, pandas accepts it without errors.
#     df[out_cols] = vals
# 
#     return df



def set_dtypes(df, config):
    for col, dtype_config_value in config["mapping"].items():

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


def trim(df, config):
    for col in config["columns"]:
        df[col] = df[col].str.strip()
    return df