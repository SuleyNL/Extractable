from enum import Enum


class Filetype(str, Enum):
    EXCEL = 'xlsx'
    LATEX = 'tex'
    PARQUET = 'parquet'
    PDF = 'pdf'
    IMG = 'img'
    XML = 'xml'
    JSON = 'json'
    CSV = 'csv'
    HTML = 'html'
    YAML = 'yaml'
