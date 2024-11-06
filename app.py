"""
File: app.py
Author: Chuncheng Zhang
Date: 2024-11-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Application for TCP communication.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2024-11-04 ------------------------
# Requirements and constants
import time
import json
from util import MyPackage


# %% ---- 2024-11-04 ------------------------
# Function and class
if __name__ == '__main__':
    mp = MyPackage()
    t = time.time()
    mp.update_content(t, 'hello')
    buff, n = mp.encode()
    print(mp, buff, n)

    # p1 = dict(server={'recv': 100})
    # buf = json.dumps(p1).encode()
    # print(mp.update_package(buf))


# %% ---- 2024-11-04 ------------------------
# Play ground
from util import config, OmegaConf


# %% ---- 2024-11-04 ------------------------
# Pending


# %% ---- 2024-11-04 ------------------------
# Pending
pkg1 = OmegaConf.create(mp.package)
pkg2 = OmegaConf.create(dict(server={'recv': 100}))

pkg1.content.time = 3

print(pkg1)
print(pkg2)

pkg1.merge_with(pkg2)
print(pkg1)
print(pkg2)

# %%
