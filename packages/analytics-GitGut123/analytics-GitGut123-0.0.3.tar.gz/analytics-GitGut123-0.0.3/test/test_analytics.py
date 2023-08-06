"""This file contains tests for analytics.py."""

import pandas as pd
import numpy as np
import pytest
from src.example_package import analytics


@pytest.mark.parametrize("df_input", [
    # Test with none values as strings
    pd.DataFrame({"A": ["a", "b", "a", "a", "b", "b", "b", "a"],
                  "B": ["AXA", "BZB", "CYC", "BZB", "AXA", "CYC", "None", "AXA"],
                  "C": [13.00000, 123.12000, 3.40000, 4.41332,
                        54.00000, 6.12000, 612.10000, "NaN"],
                  "D": ["djasd8", "7123hy", "h6as7d", "Naisd871a",
                        "dashd77", "mdas7gg", "masf7gg", "jdasd765ad"]}),
    # Test with none values as None and np.nan
    pd.DataFrame({"A": ["a", "b", "a", "a", "b", "b", "b", "a"],
                  "B": ["AXA", "BZB", "CYC", "BZB", "AXA", "CYC", None, "AXA"],
                  "C": [13.00000, 123.12000, 3.40000, 4.41332,
                        54.00000, 6.12000, 612.10000, np.nan],
                  "D": ["djasd8", "7123hy", "h6as7d", "Naisd871a",
                        "dashd77", "mdas7gg", "masf7gg", "jdasd765ad"]})
])
def test_remove_null_values(df_input):
    """Test the analytics.py function remove_null_values, with info found from comments in /exercise_3/exercise_3.py.

    Args:
        df_input (pd.DataFrame): Input dataframe to test the function with.
    """
    df_expected: pd.DataFrame = pd.DataFrame({"A": ["a", "b", "a", "a", "b", "b"],
                                              "B": ["AXA", "BZB", "CYC", "BZB", "AXA", "CYC"],
                                              "C": [13.00000, 123.12000, 3.40000, 4.41332, 54.00000, 6.12000],
                                              "D": ["djasd8", "7123hy", "h6as7d", "Naisd871a", "dashd77", "mdas7gg"]})

    # Run the function under test
    df_result = analytics.Ops().remove_null_values(df_input)

    # Assert
    pd.testing.assert_frame_equal(df_result, df_expected)


def test_rotate():
    """Test the analytics.py function rotate, with info found from comments in /exercise_3/exercise_3.py."""
    df_input: pd.DataFrame = pd.DataFrame({"A": ["a", "b", "a", "a", "b", "b", "b", "a"],
                                           "B": ["AXA", "BZB", "CYC", "BZB", "AXA", "CYC", "None", "AXA"],
                                           "C": [13.00000, 123.12000, 3.40000, 4.41332,
                                                 54.00000, 6.12000, 612.10000, "NaN"],
                                           "D": ["djasd8", "7123hy", "h6as7d", "Naisd871a",
                                                 "dashd77", "mdas7gg", "masf7gg", "jdasd765ad"]})

    # Create expected dataframe
    df_expected: pd.DataFrame = pd.DataFrame(data={"AXA": [13.0, 54.00000],
                                                   "BZB": [4.41332, 123.12000],
                                                   "CYC": [3.40, 6.12]},
                                             index=["a", "b"])
    df_expected.index.name = "A"
    df_expected.columns.name = "B"

    # Run the function under test
    df_result = analytics.Ops().rotate(df=df_input, xx='A', yy='B', scalars='C')

    # Assert
    pd.testing.assert_frame_equal(df_result, df_expected)
