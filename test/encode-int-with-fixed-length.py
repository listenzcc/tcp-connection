"""
File: encode-int-with-fixed-length.py
Author: Chuncheng Zhang
Date: 2024-11-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-11-04 ------------------------
# Requirements and constants
from rich import print


# %% ---- 2024-11-04 ------------------------
# Function and class


# %% ---- 2024-11-04 ------------------------
# Play ground
if __name__ == "__main__":
    i = 3354
    print(f'i: {i}')

    h = '0x{0:0{1}X}'.format(i, 8)
    print(f'Encode into hex h: {h}')

    k = int(h, 16)
    print(f'Decode from hex k (=i): {k} (={i})')


# %% ---- 2024-11-04 ------------------------
# Pending


# %% ---- 2024-11-04 ------------------------
# Pending
