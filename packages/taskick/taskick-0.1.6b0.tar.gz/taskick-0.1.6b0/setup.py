# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskick']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'schedule>=1.1.0,<2.0.0', 'watchdog>=2.1.6,<3.0.0']

setup_kwargs = {
    'name': 'taskick',
    'version': '0.1.6b0',
    'description': 'Taskick is an event-driven Python library that automatically executes scripts or any commands.',
    'long_description': '# Taskick\n\n[![pypi-taskick](https://img.shields.io/pypi/v/taskick)](https://pypi.org/project/taskick/)\n\nTaskick is an event-driven Python library that automatically executes scripts or any commands.\nIt not only automates tedious routine tasks and operations, but also makes it easy to develop [applications](https://github.com/atsuyaide/taskick#toy-example).\n\n[日本語版 README](https://github.com/atsuyaide/taskick/blob/main/README-ja.md)\n\nThe main features of Taskick are as follows\n\n- Automatically execute commands and scripts.\n- Script execution timing can be managed in a configuration file (YAML).\n- You can specify datetime and directory/file operations as task triggers.\n\nAnd,\n\n- Execution schedules can be specified in Crontab format.\n- [Watchdog](https://github.com/gorakhargosh/watchdog) is used to detect directory and file operations.  Any [events API](https://python-watchdog.readthedocs.io/en/stable/api.html#module-watchdog.events) provided by Watchdog can be specified in the configuration file.\n\n## Installation\n\n```shell\n$ pip install taskick==0.1.6b0\n$ python -m taskick\nTaskick 0.1.6b0\nusage: python -m taskick [-h] [--verbose] [--version] [--batch-load BATCH_LOAD]\n                         [--file FILE [FILE ...]] [--log-config LOG_CONFIG]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --verbose, -v         increase the verbosity of messages: \'-v\' for normal output, \'-vv\' for more\n                        verbose output and \'-vvv\' for debug\n  --version, -V         display this application version and exit\n  --batch-load BATCH_LOAD, -b BATCH_LOAD\n                        configuration files can be load in batches\n  --file FILE [FILE ...], -f FILE [FILE ...]\n                        specify configuration files (YAML) for the task to be executed\n  --log-config LOG_CONFIG, -l LOG_CONFIG\n                        specify a logging configuration file\n$ python -m taskick -V\nTaskick 0.1.6b0\n```\n\n## Toy Example\n\nHere is a toy-eample that converts a PNG image to PDF.\nIn this sample, the conversion script is automatically invoked when it detects that a PNG image has been saved to a specific folder.\nThe script converts the PNG to PDF and saves it in another folder.\n\nFirst, clone [taskick-example](https://github.com/atsuyaide/taskick-example).\n\n```shell\ngit clone https://github.com/atsuyaide/taskick-example.git\n```\n\nThen, execute the following command.\n\n```shell\n$ cd taskick-example\n$ pip install -r requirements.txt\n$ python -m taskick -b batch.yaml -vv\nINFO:taskick:Loading: ./config/welcome.yaml\nINFO:taskick:Processing: Welcome_taskick\nINFO:taskick:Startup option is selected.\nINFO:taskick:Registered\nINFO:taskick:Loading: ./config/main.yaml\nINFO:taskick:Processing: remove_files_in_input_folder\nINFO:taskick:Startup option is selected.\nINFO:taskick:Await option is selected.\nINFO:taskick:Registered\nINFO:taskick:Processing: png2pdf\nINFO:taskick:Registered\nINFO:taskick:Executing: Welcome_taskick\nINFO:taskick:"remove_files_in_input_folder" is waiting for "Welcome_taskick" to finish.\nSun Apr 24 23:25:43 JST 2022 Welcome to Taskick!\nwaiting 5 seconds...\nINFO:taskick:Executing: remove_files_in_input_folder\n```\n\nYou can now launch an application that converts PNG images to PDF.\n\nWhen a PNG image is saved in the `input` folder, a converted PDF file is output in the `output` folder.\nFiles in the input folder are automatically deleted at startup or every minute.\n\n\n![png2gif](https://github.com/atsuyaide/taskick/raw/main/toy-example.gif)\n\nThe application consists of `welcome.yaml` and `main.yaml`, and Taskick reads the two files indirectly by loading `batch.yaml`.\nFor details of the configuration files, see the [project page](https://github.com/atsuyaide/taskick-example).\n',
    'author': 'Atsuya Ide',
    'author_email': 'atsuya.ide528@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atsuyaide/taskick',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
