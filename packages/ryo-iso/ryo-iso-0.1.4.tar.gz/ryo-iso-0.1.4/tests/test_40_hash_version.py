import pytest
import os
import delegator
import shutil
import tempfile
import importlib
from pathlib import Path

def test_init(pytestconfig,request,data_path):
    import ryo_iso.cli

    with (data_path/'iso.yml').open('w') as f:
        f.write("""# test config file
image: ubuntu/20.04.1
arch: amd64
variant: desktop
apt:
  install:
    - git
    - python3-pip

pip:
  install:
    - doit
""")

    importlib.reload(ryo_iso.cli)
    ryo_iso.cli.cli(['_hash_version'])

    with (data_path/'.release_version').open('r') as f:
        image_version = f.read()
    assert(image_version == '20.04.1')

    with (data_path/'.hash').open('r') as f:
        image_hash = f.read()
    assert(image_hash == 'b45165ed3cd437b9ffad02a2aad22a4ddc69162470e2622982889ce5826f6e3d')
