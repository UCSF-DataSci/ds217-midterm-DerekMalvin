#!/usr/bin/env python3
# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.

    Args:
        filepath: Path to CSV file

    Returns:
        pd.DataFrame: Loaded data

    Example:
        >>> df = load_data('data/clinical_trial_raw.csv')
        >>> df.shape
        (10000, 18)
    """
    df = pd.read_csv(filepath)
    return df


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.

    Args:
        df: Input DataFrame
        remove_duplicates: Whether to drop duplicate rows
        sentinel_value: Value to replace with NaN (e.g., -999, -1)

    Returns:
        pd.DataFrame: Cleaned data

    Example:
        >>> df_clean = clean_data(df, sentinel_value=-999)
    """
    df_clean = df.copy()
    
    if sentinel_value is not None:
        df_clean = df_clean.replace(sentinel_value, np.nan)
    
    if remove_duplicates:
        df_clean = df_clean.drop_duplicates()
    
    return df_clean


def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.

    Args:
        df: Input DataFrame

    Returns:
        pd.Series: Count of missing values for each column

    Example:
        >>> missing = detect_missing(df)
        >>> missing['age']
        15
    """
    missing_counts = df.isna().sum()
    return missing_counts

def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.

    Args:
        df: Input DataFrame
        column: Column name to fill
        strategy: Fill strategy - 'mean', 'median', or 'ffill'

    Returns:
        pd.DataFrame: DataFrame with filled values

    Example:
        >>> df_filled = fill_missing(df, 'age', strategy='median')
    """
    df_filled = df.copy()
    if strategy == 'ffill':
        df_filled[column] = df_filled[column].ffill()
    elif strategy == 'median':
        median_value = df_filled[column].median()
        df_filled[column] = df_filled[column].fillna(median_value)
    elif strategy == 'mean':
        mean_value = df_filled[column].mean()
        df_filled[column] = df_filled[column].fillna(mean_value)
    
    return df_filled


def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.

    Args:
        df: Input DataFrame
        filters: List of filter dictionaries, each with keys:
                'column', 'condition', 'value'
                Conditions: 'equals', 'greater_than', 'less_than', 'in_range', 'in_list'

    Returns:
        pd.DataFrame: Filtered data

    Examples:
        >>> # Single filter
        >>> filters = [{'column': 'site', 'condition': 'equals', 'value': 'Site A'}]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Multiple filters applied in order
        >>> filters = [
        ...     {'column': 'age', 'condition': 'greater_than', 'value': 18},
        ...     {'column': 'age', 'condition': 'less_than', 'value': 65},
        ...     {'column': 'site', 'condition': 'in_list', 'value': ['Site A', 'Site B']}
        ... ]
        >>> df_filtered = filter_data(df, filters)
        >>>
        >>> # Range filter example
        >>> filters = [{'column': 'age', 'condition': 'in_range', 'value': [18, 65]}]
        >>> df_filtered = filter_data(df, filters)
    """
    result = df.copy()

    for filter_dict in filters:
        column_name = filter_dict['column']
        condition_type = filter_dict['condition']
        filter_value = filter_dict['value']
        
        if condition_type == 'equals':
            result = result[result[column_name] == filter_value]
        elif condition_type == 'in_list':
            result = result[result[column_name].isin(filter_value)]
        elif condition_type == 'greater_than':
            result = result[result[column_name] > filter_value]
        elif condition_type == 'less_than':
            result = result[result[column_name] < filter_value]
        elif condition_type == 'in_range':
            min_val = filter_value[0]
            max_val = filter_value[1]
            result = result[(result[column_name] >= min_val) & (result[column_name] <= max_val)]
    
    return result


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.

    Args:
        df: Input DataFrame
        type_map: Dict mapping column names to target types
                  Supported types: 'datetime', 'numeric', 'category', 'string'

    Returns:
        pd.DataFrame: DataFrame with converted types

    Example:
        >>> type_map = {
        ...     'enrollment_date': 'datetime',
        ...     'age': 'numeric',
        ...     'site': 'category'
        ... }
        >>> df_typed = transform_types(df, type_map)
    """
    df_result = df.copy()
    for col_name, new_type in type_map.items():
        if new_type == 'string':
            df_result[col_name] = df_result[col_name].astype(str)
        elif new_type == 'category':
            df_result[col_name] = df_result[col_name].astype('category')
        elif new_type == 'numeric':
            df_result[col_name] = pd.to_numeric(df_result[col_name], errors='coerce')
        elif new_type == 'datetime':
            df_result[col_name] = pd.to_datetime(df_result[col_name], errors='coerce')
    
    return df_result


def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().

    Args:
        df: Input DataFrame
        column: Column to bin
        bins: List of bin edges
        labels: List of bin labels
        new_column: Name for new binned column (default: '{column}_binned')

    Returns:
        pd.DataFrame: DataFrame with new binned column

    Example:
        >>> df_binned = create_bins(
        ...     df,
        ...     column='age',
        ...     bins=[0, 18, 35, 50, 65, 100],
        ...     labels=['<18', '18-34', '35-49', '50-64', '65+']
        ... )
    """
    if new_column is None:
        new_column = f"{column}_binned"
    
    df_binned = df.copy()
    df_binned[new_column] = pd.cut(df_binned[column], bins=bins, labels=labels)
    
    return df_binned

def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.

    Args:
        df: Input DataFrame
        group_col: Column to group by
        agg_dict: Dict of {column: aggregation_function(s)}
                  If None, uses .describe() on numeric columns

    Returns:
        pd.DataFrame: Grouped and aggregated data

    Examples:
        >>> # Simple summary
        >>> summary = summarize_by_group(df, 'site')
        >>>
        >>> # Custom aggregations
        >>> summary = summarize_by_group(
        ...     df,
        ...     'site',
        ...     {'age': ['mean', 'std'], 'bmi': 'mean'}
        ... )
    """
    if agg_dict is None:
        summary = df.groupby(group_col).describe()
    else:
        summary = df.groupby(group_col).agg(agg_dict)
    return summary


if __name__ == '__main__':
    # Optional: Test your utilities here
    print("Data utilities loaded successfully!")
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")
    
    # TODO: Add simple test example here
    # Example:
    # test_df = pd.DataFrame({'age': [25, 30, 35], 'bmi': [22, 25, 28]})
    # print("Test DataFrame created:", test_df.shape)
    # print("Test detect_missing:", detect_missing(test_df))
    sample_df = pd.DataFrame({
        'age': [25, 30, np.nan, 45, -999],
        'site': ['A', 'B', 'A', 'B', 'A']
    })

    print(f"Original DataFrame shape: {sample_df.shape}")
    
    cleaned_df = clean_data(sample_df, sentinel_value=-999)
    print(f"Missing values detected: {detect_missing(cleaned_df).sum()}")
    
    filled_df = fill_missing(cleaned_df, 'age', strategy='median')
    print(f"DataFrame after filling:\n{filled_df}")
    
    typed_df = transform_types(filled_df, {'site': 'category'})
    print(f"Data types:\n{typed_df.dtypes}")
    
    group_summary = summarize_by_group(typed_df, 'site')
    print(f"Summary by site:\n{group_summary}")