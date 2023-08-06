# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recorder', 'recorder.device', 'recorder.listener']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.1,<3.0.0',
 'PyInquirer>=1.0.3,<2.0.0',
 'PyYAML>=5.1,<6.0',
 'numpy>=1.22.2,<2.0.0',
 'sounddevice>=0.4.4,<0.5.0',
 'typer[all]>=0.4.0,<0.5.0']

extras_require = \
{'all': ['pyrealsense2>=2.50.0,<3.0.0'],
 'realsense': ['pyrealsense2>=2.50.0,<3.0.0']}

entry_points = \
{'console_scripts': ['recorder = recorder.__main__:app']}

setup_kwargs = {
    'name': 'python-recorder',
    'version': '0.0.2',
    'description': '',
    'long_description': '# python-recorder\n\nVisual and Acoustic Odometry recorder using python. Devices: RealSense D435i\ncamera, RODE VideoMicNTG and smartLav+ microphones\n\nFramework\n\nTODO ros\n\n# Setup\n\nClone this repository to your local machine. Detailed instructions about\ncloning repositories and installing python dependencies can be found\n[here](https://docs.google.com/document/d/15Mj3x9Im7Yfz3sPo5f4dUjQZgabjVtIL2RBHvM2798E/edit?usp=sharing).\n\n## Install Python (3.5 - 3.9)\nDo not install the latest version of Python (currently 3.10) as it is not\ncompatible with Intel RealSense SDK yet.\n\nhttps://www.python.org/downloads/\n\n## Install Intel RealSense SDK 2.0\n\nhttps://github.com/IntelRealSense/librealsense/releases\n\n## Install dependencies\nOpen a terminal in the directory where this file is located. Then create a\nvirtual environment:\n```\npython -m venv venv\n```\n\nActivate the environment on Windows:\n```\nvenv\\Scripts\\activate\n```\nor on MacOS and Linux:\n```\nsource venv/bin/activate\n```\n\nFinally, install dependencies with pip:\n```\npip install -r requirements.txt\n```\n\n# Usage\nCheck the usage with the `--help` option:\n```\npython vao-recorder.py --help\n```\n\n# Workflow\n\nConfigure the devices to be used. One can always modify the configuration\nmanually in the generated `yaml` file.\n```\npython vao-recorder.py config\n```\n\nTest that the chosen audio devices are working\n```\npython vao-recorder.py test microphone\n```\n\nRecord an experiment with the configured devices\n```\npython vao-recorder.py record\n```',
    'author': 'Andreu Gimenez',
    'author_email': 'esdandreu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
