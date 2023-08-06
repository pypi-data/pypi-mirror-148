import os

import pandas as pd

from bln.pandas import extensions


def test_pandas_read():
    """Test the `read_bln` method."""
    assert extensions.read_bln
    assert pd.read_bln
    project_id = "UHJvamVjdDpiZGM5NmU1MS1kMzBhLTRlYTctODY4Yi04ZGI4N2RjMzQ1ODI="
    file_name = "ia.csv"
    tier = os.getenv("BLN_TEST_ENV", "dev")
    df = pd.read_bln(project_id, file_name, tier=tier)
    assert len(df) > 0
