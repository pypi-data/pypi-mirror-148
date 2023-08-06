"""Main file for the package."""
import pandas as pd
import numpy as np


class Ops():
    """Class for making operations on pd.DataFrames."""

    @staticmethod
    def remove_null_values(df: pd.DataFrame) -> pd.DataFrame:
        """Remove all rows containing null values in the dataframe.

        Args:
            df (pd.DataFrame): Dataframe to remove null rows from.

        Returns:
            pd.DataFrame: The input dataframe without any null values.
        """
        # Regex: (flags = case insensitive) matches "none" or "nan"
        df = df.replace(to_replace="(?i)none|nan", value=np.nan, regex=True).dropna()

        return df

    @staticmethod
    def rotate(df: pd.DataFrame, xx: str, yy: str, scalars: str) -> pd.DataFrame:
        """Remove missing values and rotate the dataframe using the pivot function.

        Args:
            df (pd.DataFrame): Dataframe to rotate.
            xx (str): Column to make frame's new index.
            yy (str): Column to make frame's new columns.
            scalars (str): Column to use for populating he new index.

        Returns:
            pd.DataFrame: reshaped dataframe.
        """
        df = Ops.remove_null_values(df=df)
        return df.pivot(index=xx, columns=yy, values=scalars)
