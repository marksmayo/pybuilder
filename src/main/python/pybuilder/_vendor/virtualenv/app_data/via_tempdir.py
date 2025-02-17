import logging
from tempfile import mkdtemp

from ..util.path import safe_delete
from .via_disk_folder import AppDataDiskFolder


class TempAppData(AppDataDiskFolder):
    transient = True
    can_update = False

    def __init__(self):
        super().__init__(folder=mkdtemp())
        logging.debug("created temporary app data folder %s", self.lock.path)

    def reset(self):
        """this is a temporary folder, is already empty to start with"""

    def close(self):
        logging.debug("remove temporary app data folder %s", self.lock.path)
        safe_delete(self.lock.path)

    def embed_update_log(self, distribution, for_py_version):  # noqa: U100
        raise NotImplementedError


__all__ = [
    "TempAppData",
]
