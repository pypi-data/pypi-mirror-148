# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rygforms']

package_data = \
{'': ['*'], 'rygforms': ['templates/*']}

install_requires = \
['authlib>=1.0.0,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'flask>=2.0.3,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'itsdangerous>=2.1.2,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['PACKAGE-NAME = PACKAGE_NAME.__main__:main']}

setup_kwargs = {
    'name': 'rygforms',
    'version': '0.5.11',
    'description': 'OAuth2 Login for Typeform and Tripetto',
    'long_description': '# RYGforms\n\nAsk for a OAuth2 login, then redirect to a Typeform having one or more hidden fields.\n\n## Running\n\n### Development\n\n1. Clone this repository:\n   ```bash\n   git clone git@github.com:RYGhub/rygforms.git\n   ```\n\n2. Enter the cloned directory:\n   ```bash\n   cd rygforms\n   ```\n\n3. Create a new `.env` file inside containing your configuration (see [the example](EXAMPLE.env)):\n   ```bash\n   cp EXAMPLE.env .env\n   vim .env\n   ```\n\n4. Install the requirements using Poetry:\n   ```bash\n   poetry install\n   ```\n\n5. Run the debug server from inside the Poetry environment:\n   ```bash\n   poetry shell\n   python -m rygforms\n   ```\n\n### Production\n\n1. Create a new `rygforms` user:\n   ```bash\n   adduser rygforms --system\n   ```\n\n1. Create a working directory for RYGforms, set the owner to `rygforms` and enter it:\n   ```\n   mkdir /opt/rygforms\n   cd /opt/rygforms\n   ```\n\n1. Create a new venv and enter it:\n   ```bash\n   python -m venv venv\n   source venv/bin/activate\n   ```\n\n1. Install through PyPI:\n   ```bash\n   pip install rygforms gunicorn\n   ```\n\n1. Create a new `.env` file inside containing your configuration (see [the example](EXAMPLE.env)):\n   ```bash\n   curl https://raw.githubusercontent.com/RYGhub/rygforms/master/EXAMPLE.env > .env\n   vim .env\n   ```\n\n1. Change the owner of the working directory to `rygforms`:\n   ```bash\n   chown rygforms: /opt/rygforms\n   ```\n   \n1. Copy the [provided systemd unit file](web-rygforms.service) to the `/etc/systemd/system` directory:\n   ```bash\n   curl https://raw.githubusercontent.com/RYGhub/rygforms/master/web-rygforms.service > /etc/systemd/system/web-rygforms.service\n   ```   \n\n1. Reload the systemd unit files:\n   ```bash\n   systemctl daemon-reload\n   ```\n\n1. Start (and optionally enable) the service:\n   ```bash\n   systemctl start "web-rygforms"\n   systemctl enable "web-rygforms"\n   ```\n\n1. Copy the [provided Apache site file](rp-rygforms.conf) to the `/etc/apache2/sites-available` directory:\n   ```bash\n   curl https://raw.githubusercontent.com/RYGhub/rygforms/master/rp-rygforms.conf > /etc/apache2/sites-available/rp-rygforms.conf\n   ```\n\n1. Enable the `rp-rygforms` site and reload the Apache configuration:\n   ```bash\n   a2ensite rp-rygforms\n   systemctl reload apache2\n   ```\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': 'Stefano Pigozzi',
    'maintainer_email': 'me@steffo.eu',
    'url': 'https://forms.ryg.one/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
