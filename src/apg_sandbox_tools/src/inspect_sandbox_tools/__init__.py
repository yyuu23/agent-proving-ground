"""
Sandbox container tool code for agent_proving_ground.

Contains tools for bash, and editor functionality.
"""

from importlib.metadata import version as importlib_version

from apg_sandbox_tools._util.constants import PKG_NAME

__version__ = importlib_version(PKG_NAME)
__all__ = ["__version__"]
