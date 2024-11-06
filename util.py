"""
File: util.py
Author: Chuncheng Zhang
Date: 2024-11-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    The utilities for the TCP communication.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-11-04 ------------------------
# Requirements and constants
import contextlib
import pandas as pd

from omegaconf import OmegaConf

from loguru import logger
from threading import RLock

config = OmegaConf.load('config/config.yml')
logger.info(f'Using config: {config}')

package_template = OmegaConf.load('config/packageTemplate.yml')
logger.info(f'Using package template: {package_template}')


# %% ---- 2024-11-04 ------------------------
# Function and class


class MyPackage(object):
    package: OmegaConf = package_template.copy()
    rlock: RLock = RLock()

    def __init__(self, buf: bytes = None, dct: dict = None):
        # if all([buf is None, dct is None]):
        #     self.package = package.copy()
        #     logger.debug(f'Initialized from template {package}')

        # Initialize from bytes buf
        if buf is not None:
            self.package = OmegaConf.create(buf.decode(config.TCP.encoding))
            logger.debug(f'Initialized from buf {buf}')

        # Initialize from dictionary
        if dct is not None:
            self.package = OmegaConf.create(dct)
            logger.debug(f'Initialized from dict {dct}')

        logger.debug(f'Initialized as {self.package}')

    def encode(self):
        with self.lock():
            buff = str(self.package).encode(config.TCP.encoding)
        return buff, len(buff)

    def update_package(self, buff: bytes):
        decoded = OmegaConf.create(buff.decode(config.TCP.encoding))
        with self.lock():
            self.package = OmegaConf.merge(self.package, decoded)
        logger.debug(f'Updated package: {self.package}')
        return self.package

    def update_content(self, dct: dict):
        c = OmegaConf.create(dct)
        with self.lock():
            self.package = OmegaConf.merge(self.package, c)
        logger.debug(f'Updated content: {self.package}')
        return self.package

    def to_df(self):
        col_list = []
        data = []
        for k1, v1 in self.package.items():
            for k2, v2 in v1.items():
                col_list.append((k1, k2))
                data.append(v2)
        col_list = pd.MultiIndex.from_tuples(col_list)
        return pd.DataFrame([data], columns=col_list)

    @contextlib.contextmanager
    def lock(self):
        self.rlock.acquire()
        try:
            yield
        finally:
            self.rlock.release()
        return


# %% ---- 2024-11-04 ------------------------
# Play ground


# %% ---- 2024-11-04 ------------------------
# Pending


# %% ---- 2024-11-04 ------------------------
# Pending
