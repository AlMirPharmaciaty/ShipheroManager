from enum import Enum


class ShipheroQueriesEnum(str, Enum):
    ORDERS = "Orders"


class ETLLogProcessessEnum(str, Enum):
    """List of etl log processes"""
    EXTRACTION = "Extraction"
    TRANSFORMATION = "Transformation"
    LOADING = "Loading"
