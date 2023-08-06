# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['giant_faqs', 'giant_faqs.migrations', 'giant_faqs.tests']

package_data = \
{'': ['*'],
 'giant_faqs': ['templates/*',
                'templates/faqs/*',
                'templates/faqs/_components/*']}

install_requires = \
['flake8>=4.0.1,<5.0.0',
 'giant-mixins',
 'giant-plugins',
 'isort>=5.10.1,<6.0.0']

setup_kwargs = {
    'name': 'giant-faqs',
    'version': '0.1.0',
    'description': 'A small reusable package that adds a FAQ app to a project',
    'long_description': '# Giant-FAQs\n\nA small reusable package that adds a \'Frequently Asked Questions\' app to a django site.\n\nThis will include the basic formatting and functionality such as model creation via the admin.\n\nSupported Django versions:\n\n    Django 2.2, 3.2\n\nSupported django CMS versions:\n\n    django CMS 3.8, 3.9\n\n## Installation and set up\n\nYou should then add "giant_faqs" to the INSTALLED_APPS in your settings file. For use of the RichText plugin needed for the answer entry field on the model, it is required that you use the giant-plugins app.\n\nThere is an optional search bar which can be removed from the top of the index template by adding \n    \n    FAQ_SEARCH = False\n\nto your project\'s settings.\n\n',
    'author': 'Dominic Chaple',
    'author_email': 'domchaple@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-faqs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
