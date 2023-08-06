# VERSION
def get_version():
    try:
        # Python >= 3.8
        from importlib import metadata

        return metadata.version("icartt")
    except ImportError:
        # Python <= 3.7
        import pkg_resources

        return pkg_resources.get_distribution("icartt").version


__version__ = get_version()
del get_version


# EXPORTED TYPES
from .dataset import (
    Dataset,
    StandardNormalComments,
    Variable,
    Formats,
    VariableType,
    DataStore1001,
    DataStore2110,
)

__all__ = (
    "Dataset",
    "StandardNormalComments",
    "Variable",
    "Formats",
    "VariableType",
    "DataStore1001",
    "DataStore2110",
)
