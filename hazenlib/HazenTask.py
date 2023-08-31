"""
HazenTask.py
"""

from pydicom import dcmread
from hazenlib.logger import logger
import pathlib
import os


class HazenTask:
    # ANSI escape codes for coloured text
    COLOR_CODES = {
        'red': '\033[91m',
        'green': '\u001b[32;1m',
        'yellow': '\u001b[33;1m',
        'reset': '\033[0m',
    }

    def __init__(self, data_paths: list, report: bool = False, report_dir: str = os.path.join(os.getcwd(), 'report')):
        self.data_paths = sorted(data_paths)
        self.report: bool = report
        self.report_path = os.path.join(report_dir, type(self).__name__)
        if report:
            pathlib.Path(self.report_path).mkdir(parents=True, exist_ok=True)
        else:
            pass
        self.report_files = []

    @property
    def data(self) -> list:
        return [dcmread(dicom)for dicom in self.data_paths]

    def key(self, dcm, properties=None) -> str:
        if properties is None:
            properties = ['SeriesDescription', 'SeriesNumber', 'InstanceNumber']
        try:
            metadata = [str(dcm.get(field)) for field in properties]
        except KeyError:
            logger.warning(f"Could not find one or more of the following properties: {properties}")
            metadata = [str(dcm.get(field)) for field in ['SeriesDescription', 'SeriesNumber']]

        key = f"{type(self).__name__}_" + '_'.join(metadata).replace(' ', '_')
        return key
