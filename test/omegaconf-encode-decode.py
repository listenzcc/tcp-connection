"""
File: omegaconf-encode-decode.py
Author: Chuncheng Zhang
Date: 2024-11-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Encoding and decoding recovery by OmegaConf

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-11-04 ------------------------
# Requirements and constants
from omegaconf import OmegaConf
from rich import print


# %% ---- 2024-11-04 ------------------------
# Function and class


# %% ---- 2024-11-04 ------------------------
# Play ground
if __name__ == "__main__":
    d = dict(a=1, b=dict(c='a', d=2))
    print(f'Dict: {d}')

    config = OmegaConf.create(d)
    print(f'Config: {config}')

    encoded = str(config).encode("utf-8")
    print(f'Encoded: {encoded}')

    decoded = OmegaConf.create(encoded.decode("utf-8"))
    print(f'Decoded: {decoded}')

    config_1 = OmegaConf.create({'b': {'d': 5}})
    merged = OmegaConf.merge(config, config_1)
    print(f'Merging: {config_1} -> merged: {merged}')


# %% ---- 2024-11-04 ------------------------
# Pending


# %% ---- 2024-11-04 ------------------------
# Pending
