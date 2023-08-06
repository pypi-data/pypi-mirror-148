# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['offensive_azure',
 'offensive_azure.Access_Tokens',
 'offensive_azure.Azure_AD',
 'offensive_azure.Device_Code',
 'offensive_azure.Outsider_Recon',
 'offensive_azure.User_Enum']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'dnspython>=2.2.1,<3.0.0',
 'pycryptodome>=3.14.1,<4.0.0',
 'python-whois>=0.7.3,<0.8.0',
 'requests>=2.27.1,<3.0.0',
 'uuid>=1.30,<2.0']

entry_points = \
{'console_scripts': ['device_code_easy_mode = '
                     'offensive_azure.Device_Code.device_code_easy_mode:main',
                     'get_groups = offensive_azure.Azure_AD.get_groups:main',
                     'get_tenant = offensive_azure.Azure_AD.get_tenant:main',
                     'get_users = offensive_azure.Azure_AD.get_users:main',
                     'outsider_recon = '
                     'offensive_azure.Outsider_Recon.outsider_recon:runner',
                     'read_token = '
                     'offensive_azure.Access_Tokens.read_token:main',
                     'token_juggle = '
                     'offensive_azure.Access_Tokens.token_juggle:main',
                     'user_enum = offensive_azure.User_Enum.user_enum:main']}

setup_kwargs = {
    'name': 'offensive-azure',
    'version': '0.4.9',
    'description': 'Collection of tools for attacking Microsoft Cloud products',
    'long_description': '<p align="center">\n  <img src="https://user-images.githubusercontent.com/28767257/160513484-cb70370c-9fce-48d1-84ec-8b9ea3cf8e5a.png">\n</p>\n\n[![Python Version](https://img.shields.io/pypi/pyversions/offensive_azure?style=plastic)](https://www.python.org) [![Build Status](https://img.shields.io/github/workflow/status/blacklanternsecurity/offensive-azure/Pylint?style=plastic)](https://github.com/blacklanternsecurity/offensive-azure/actions/workflows/pylint.yml?query=workflow%3Apylint) [![PyPI Wheel](https://img.shields.io/pypi/wheel/offensive_azure?style=plastic)](https://pypi.org/project/offensive-azure/)\n\nCollection of offensive tools targeting Microsoft Azure written in Python to be platform agnostic. The current list of tools can be found below with a brief description of their functionality.\n\n- [`./Device_Code/device_code_easy_mode.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Device_Code)\n  - Generates a code to be entered by the target user\n  - Can be used for general token generation or during a phishing/social engineering campaign.\n- [`./Access_Tokens/token_juggle.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Access_Tokens)\n  - Takes in a refresh token in various ways and retrieves a new refresh token and an access token for the resource specified\n- [`./Access_Tokens/read_token.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Access_Tokens)\n  - Takes in an access token and parses the included claims information, checks for expiration, attempts to validate signature\n- [`./Outsider_Recon/outsider_recon.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Outsider_Recon)\n  - Takes in a domain and enumerates as much information as possible about the tenant without requiring authentication \n- [`./User_Enum/user_enum.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/User_Enum)\n  - Takes in a username or list of usernames and attempts to enumerate valid accounts using one of three methods\n  - Can also be used to perform a password spray\n- [`./Azure_AD/get_tenant.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Azure_AD)\n  - Takes in an access token or refresh token, outputs tenant ID and tenant Name\n  - Creates text output file as well as BloodHound compatible aztenant file\n- [`./Azure_AD/get_users.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Azure_AD)\n  - Takes in an access token or refresh token, outputs all users in Azure AD and all available user properties in Microsoft Graph\n  - Creates three data files, a condensed json file, a raw json file, and a BloodHound compatible azusers file\n- [`./Azure_AD/get_groups.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Azure_AD)\n  - Takes in an access token or refresh token, outputs all groups in Azure AD and all available group properties in Microsoft Graph\n  - Creates three data files, a condensed json file, a raw json file, and a BloodHound compatible azgroups file\n\n# Installation\n\nOffensive Azure can be installed in a number of ways or not at all. \n\nYou are welcome to clone the repository and execute the specific scripts you want. A `requirements.txt` file is included for each module to make this as easy as possible.\n\n## Poetry\n\nThe project is built to work with `poetry`. To use, follow the next few steps:\n\n```\ngit clone https://github.com/blacklanternsecurity/offensive-azure.git\ncd ./offensive-azure\npoetry install\n```\n\n## Pip\n\nThe packaged version of the repo is also kept on pypi so you can use `pip` to install as well. We recommend you use `pipenv` to keep your environment as clean as possible.\n\n```\npipenv shell\npip install offensive_azure\n```\n\n# Usage\n\nIt is up to you for how you wish to use this toolkit. Each module can be ran independently, or you can install it as a package and use it in that way. Each module is exported to a script named the same as the module file. For example:\n\n## Poetry\n\n```\npoetry install\npoetry run outsider_recon your-domain.com\n```\n\n## Pip\n\n```\npipenv shell\npip install offensive_azure\noutsider_recon your-domain.com\n```\n',
    'author': 'Cody Martin',
    'author_email': 'debifrank00@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blacklanternsecurity.com/offensive-azure',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
