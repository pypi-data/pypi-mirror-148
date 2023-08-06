# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpusm']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.9.0,<6.0.0']

setup_kwargs = {
    'name': 'gpusm',
    'version': '0.1.0',
    'description': 'Cross-platform lib for GPU status monitoring in Python',
    'long_description': '# GPUSM\n\nCross-platform lib for GPU status monitoring in Python.\n\n## Install\n\n```bash\npip install gpusm\n```\n\n## Usage\n\n`$ gpusm`\n\n## Changelog\n\nSee [CHANGELOG.md](CHANGELOG.md)\n\n## License\n\n[MIT License](License)\n\n## References\n\n- [gpustat](https://github.com/wookayin/gpustat)\n- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)\n- [psutil documentation](https://psutil.readthedocs.io/en/latest/)',
    'author': 'XavierJiezou',
    'author_email': '878972272@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/XavierJiezou/GPUSM',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
