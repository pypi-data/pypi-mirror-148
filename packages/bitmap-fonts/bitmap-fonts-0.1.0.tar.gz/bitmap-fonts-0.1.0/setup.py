# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bitmap_fonts']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<9.0.0', 'numpy>=1.22.3,<2.0.0', 'pillow>=9.1.0,<10.0.0']

entry_points = \
{'console_scripts': ['create-font-texture = '
                     'bitmap_fonts.create_font_texture:main']}

setup_kwargs = {
    'name': 'bitmap-fonts',
    'version': '0.1.0',
    'description': 'Creation of bitmap fonts useful in OpenGL context..',
    'long_description': '## Bitmap fonts\nBitmap fonts are useful in generating text messages in OpenGL contexts. This utility allows to \nconvert a TTF font file into a bitmap font.\n\n\n## Description\ncreate-font-texture script should be self-explanatory.\n\n\n## Installation\npip install bitmap-fonts\n\n\n## Usage\n\n\n## Authors and acknowledgment\nPeter Koval <koval.peter@gmail.com>\n\n## License\nMIT,\nthe font UbuntuMono-Regular.ttf is Ubuntu font license 1.0\n\n## Project status\nUseful\n\n',
    'author': 'Simune Team',
    'author_email': 'devops@simuneatomistics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.simuneatomistics.com/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
