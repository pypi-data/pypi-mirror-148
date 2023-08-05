# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyafl_qemu_trace',
 'pyafl_qemu_trace.binaries',
 'pyafl_qemu_trace.events',
 'pyafl_qemu_trace.parse',
 'pyafl_qemu_trace.run']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0']

setup_kwargs = {
    'name': 'pyafl-qemu-trace',
    'version': '0.2.1',
    'description': 'A pip-installable distribution of afl-qemu-trace.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/pyafl-qemu-trace.svg)](https://badge.fury.io/py/pyafl-qemu-trace)\n# pyafl_qemu_trace\n\npip-installable afl-qemu-trace python package\n\n## Installation\n\n```\npython3 -m pip install pyafl-qemu-trace\n```\n\n## Building\n\nIf you would like to build this package, clone it and run `poetry build -f wheel`.\n\nYou will need to have `poetry`, `docker`, and `docker-compose` or `docker compose` (v2)\ninstalled.\n\n## Examples\n\n```python\nfrom pyafl_qemu_trace import qemu_path\n\n# Get the path to the tracer binary\ntracer = qemu_path("x86_64")\n\n# Run the tracer with the provided wrapper\nfrom pyafl_qemu_trace import TraceRunner\nfrom shutil import which\n\nretcode, stdout, stderr, log = TraceRunner.run(\n    "x86_64", \n    which("xxd"), \n    cwd="/tmp", \n    input_data="\\x41" * 400, \n    timeout=10\n)\n\n# Parse the output of the tracer into a programmatically\n# workable data structure result\nfrom pyafl_qemu_trace import TraceParser\n\nresult = TraceParser.parse(log)\n\nprint(f"The trace has {len(result.addrs)} instructions!")\n```\n\n## Requirements\n\nEither `docker-compose` or `docker compose` should be available at build time, but when\ninstalling, no dependencies are required, this basically just downloads a bunch of\nbinaries for you.\n\n## Targets\n\nSupported targets for `afl-qemu-trace` are as follows, but at the moment only `x86_64`\nand `aarch64` are built -- the infrastructure to generate the rest is already in place,\nhowever, I just need to enable it.\n\n```txt\naarch64-softmmu\nalpha-softmmu\narm-softmmu\navr-softmmu\ncris-softmmu\nhppa-softmmu\ni386-softmmu\nm68k-softmmu\nmicroblaze-softmmu\nmicroblazeel-softmmu\nmips-softmmu\nmips64-softmmu\nmips64el-softmmu\nmipsel-softmmu\nmoxie-softmmu\nnios2-softmmu\nor1k-softmmu\nppc-softmmu\nppc64-softmmu\nriscv32-softmmu\nriscv64-softmmu\nrx-softmmu\ns390x-softmmu\nsh4-softmmu\nsh4eb-softmmu\nsparc-softmmu\nsparc64-softmmu\ntricore-softmmu\nx86_64-softmmu\nxtensa-softmmu\nxtensaeb-softmmu\naarch64\naarch64_be\nalpha\narm\narmeb\ncris\nhexagon\nhppa\ni386\nm68k\nmicroblaze\nmicroblazeel\nmips\nmips64\nmips64el\nmipsel\nmipsn32\nmipsn32el\nnios2\nor1k\nppc\nppc64\nppc64le\nriscv32\nriscv64\ns390x\nsh4\nsh4eb\nsparc\nsparc32plus\nsparc64\nx86_64\nxtensa\nxtensaeb\n```',
    'author': 'novafacing',
    'author_email': 'rowanbhart@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/novafacing/pyafl_qemu_trace.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<=4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
