"""Numbeo SDK - Python client for the Numbeo API.

This SDK provides a clean interface to interact with the Numbeo API,
which offers data on cost of living, property prices, and crime rates worldwide.
"""

__version__ = "0.1.0"

from .client import NumbeoClient

__all__ = ["NumbeoClient"]
