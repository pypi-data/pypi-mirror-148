# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['microfpga', 'microfpga._tests']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'microfpga',
    'version': '3.1.0',
    'description': 'FPGA-based platform for the electronic control of microscopes.',
    'long_description': '<a href="https://mufpga.github.io/"><img src="https://raw.githubusercontent.com/mufpga/mufpga.github.io/main/img/logo_title.png" alt="Overview"/>\n\n</a>\n\n![version](https://img.shields.io/badge/version-3.1.0-blue)[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)\n\n\n\n# Overview\n\nMicroFPGA is an FPGA-based platform for the electronic control of microscopes. It aims at using affordable FPGA to generate or read signals from a variety of devices, including cameras, lasers, servomotors, filter-wheels, etc. It can be controlled via [Micro-Manager](https://micro-manager.org/MicroFPGA), or its [Java](https://github.com/mufpga/MicroFPGA-java), [Python](https://github.com/mufpga/MicroFPGA-py) and [LabView](https://github.com/mufpga/MicroFPGA-labview) communication libraries, and comes with optional complementary [electronics](https://github.com/mufpga/MicroFPGA-electronics).\n\nDocumentation and tutorials are available on [https://mufpga.github.io/](https://mufpga.github.io/).\n\n\n\n<img src="https://raw.githubusercontent.com/mufpga/mufpga.github.io/main/img/figs/G_overview.png" alt="Overview"/>\n\n## Content\n\nThis repository contains the Python package to control MicroFPGA. To use `microfpga` in you Python environment, you can install it directly with `pip`:\n\n```bash\npip install microfpga\n```\n\nAlternatively, you can install it from the source code:\n\n``` bash\ngit clone https://github.com/mufpga/MicroFPGA-py\ncd MicroFPGA-py\npip install -e .\n```\n\nFinally, configure your Alchitry FPGA with the correct [configuration](https://github.com/mufpga/MicroFPGA) and try some of the [example scripts](https://github.com/mufpga/MicroFPGA-py/tree/main/examples).\n\n<!---\n\n## Cite us\n\nDeschamps J, Kieser C, Hoess P, Deguchi T and Ries J, \n\n--->\n\nMicroFPGA-py was written by Joran Deschamps, EMBL (2020).\n\n',
    'author': 'Joran Deschamps',
    'author_email': 'joran.deschamps@fht.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
