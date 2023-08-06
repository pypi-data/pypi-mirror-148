"""acts.core.data package."""

from __future__ import annotations

import os
import re
import unicodedata

import pandas as pd


_FILEDIR = os.path.abspath(os.path.dirname(__file__))


__all__ = [
    # Function exports
    "load",
]


def load(name: str) -> pd.DataFrame:
    """Loads a parquet file from our datasets."""
    filename = f"{_slugify(name)}.parquet"
    filepath = os.path.join(_FILEDIR, "parquets", filename)
    return pd.read_parquet(filepath)


def _slugify(value: str, *, allow_unicode: bool = False) -> str:
    """Converts a string into a filename-safe version.

    Taken from github.com/django/django/blob/master/django/utils/text.py

    Convert to ASCII if `allow_unicode` is `False`. Convert spaces or
    repeated dashes to single dashes. Remove characters that aren't
    alphanumerics, underscores, or hyphens. Convert to lowercase. Also
    strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value)
        value = value.encode("ascii", "ignore").decode("ascii")

    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
