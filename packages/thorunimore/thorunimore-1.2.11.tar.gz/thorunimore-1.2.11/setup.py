# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thorunimore',
 'thorunimore.database',
 'thorunimore.database.base',
 'thorunimore.telegram',
 'thorunimore.web']

package_data = \
{'': ['*'], 'thorunimore.web': ['static/*', 'templates/*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'authlib>=0.14.3,<0.15.0',
 'coloredlogs>=14.0,<15.0',
 'flask-sqlalchemy>=2.4.4,<3.0.0',
 'flask>=1.1.2,<2.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'markupsafe>=1,<2',
 'psycopg2>=2.9.3,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'royalnet==6.0.0a4',
 'telethon>=1.16.4,<2.0.0']

entry_points = \
{'console_scripts': ['thorunimore-telegram = '
                     'thorunimore.telegram.__main__:main',
                     'thorunimore-web = thorunimore.web.__main__:main']}

setup_kwargs = {
    'name': 'thorunimore',
    'version': '1.2.11',
    'description': 'Authentication gateway bot for the Unimore Informatica Telegram group',
    'long_description': '# thorunimore\n\n![](resources/bot_image.png)\n\nA moderator bot for the Unimore Informatica group\n\n## Installation\n\n1. Create a new venv and enter it:\n   ```bash\n   python -m venv venv\n   source venv/bin/activate\n   ```\n   \n2. Download through PyPI:\n   ```bash\n   pip install thorunimore\n   ```\n   \n3. Install the packages required to connect to the desired SQL database:\n   \n   - For PostgreSQL:\n     ```bash\n     pip install psycopg2-binary\n     ```\n\n## Running\n\n### Development\n\n1. Set the following env variables:\n\n   - [The URI of the SQL database you want to use](https://docs.sqlalchemy.org/en/13/core/engines.html)\n     ```bash\n     SQLALCHEMY_DATABASE_URI=postgresql://steffo@/thor_dev\n     ```\n   \n   - [A Google OAuth 2.0 client id and client secret](https://console.developers.google.com/apis/credentials)\n     ```bash\n     GOOGLE_CLIENT_ID=000000000000-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.apps.googleusercontent.com\n     GOOGLE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaa\n     ```\n   \n   - A random string of characters used to sign Telegram data\n     ```bash\n     SECRET_KEY=Questo è proprio un bel test.\n     ```\n   \n   - [api_id and api_hash for a Telegram application](https://my.telegram.org/apps)\n     ```bash\n     TELEGRAM_API_ID=1234567\n     TELEGRAM_API_HASH=abcdefabcdefabcdefabcdefabcdefab\n     ```\n\n   - [The username and token of the Telegram bot](https://t.me/BotFather)\n     ```bash\n     TELEGRAM_BOT_USERNAME=thorunimorebot\n     TELEGRAM_BOT_TOKEN=1111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n     ```\n\n   - The desired logging level and format\n     ```bash\n     LOG_LEVEL=DEBUG\n     LOG_FORMAT={asctime}\\t| {name}\\t| {message}\n     ```\n   \n   - The url at which web is hosted\n     ```bash\n     BASE_URL=http://lo.steffo.eu:30008\n     ```\n     \n   - The url to join the Telegram group\n     ```bash\n     GROUP_URL=https://t.me/joinchat/AAAAAAAAAAAAAAAAAAAAAA\n     ```\n\n2. Run both the following processes:\n   ```bash\n   python -m thorunimore.telegram &\n   python -m thorunimore.web &\n   ```\n\n### Production\n\n1. Install `gunicorn` in the previously created venv:\n   ```\n   pip install gunicorn\n   ```\n\n2. Create the `bot-thorunimore` systemd unit by creating the `/etc/systemd/system/bot-thorunimore.service` file:\n   ```ini\n   [Unit]\n   Name=bot-thorunimore\n   Description=A moderator bot for the Unimore Informatica group\n   Requires=network-online.target postgresql.service\n   After=network-online.target nss-lookup.target\n   \n   [Service]\n   Type=exec\n   User=thorunimore\n   WorkingDirectory=/opt/thorunimore\n   ExecStart=/opt/thorunimore/venv/bin/python -OO -m thorunimore.telegram\n   Environment=PYTHONUNBUFFERED=1\n   \n   [Install]\n   WantedBy=multi-user.target\n   ```\n\n3. Create the `web-thorunimore` systemd unit by creating the `/etc/systemd/system/web-thorunimore.service` file:\n   ```ini\n   [Unit]\n   Name=web-thorunimore\n   Description=Thorunimore Gunicorn Server\n   Wants=network-online.target postgresql.service\n   After=network-online.target nss-lookup.target\n   \n   [Service]\n   Type=exec\n   User=thorunimore\n   WorkingDirectory=/opt/thorunimore\n   ExecStart=/opt/thorunimore/venv/bin/gunicorn -b 127.0.0.1:30008 thorunimore.web.__main__:reverse_proxy_app\n   \n   [Install]\n   WantedBy=multi-user.target\n   ```\n   \n4. Create the `/etc/systemd/system/bot-thorunimore.d/override.conf` and \n   `/etc/systemd/system/web-thorunimore.d/override.conf` files:\n   ```ini\n   [Service]\n   Environment="SQLALCHEMY_DATABASE_URI=postgresql://thorunimore@/thor_prod"\n   Environment="GOOGLE_CLIENT_ID=000000000000-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.apps.googleusercontent.com"\n   Environment="GOOGLE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaa"\n   Environment="SECRET_KEY=Questo è proprio un bel server."\n   Environment="TELEGRAM_API_ID=1234567"\n   Environment="TELEGRAM_API_HASH=abcdefabcdefabcdefabcdefabcdefab"\n   Environment="TELEGRAM_BOT_USERNAME=thorunimorebot"\n   Environment="TELEGRAM_BOT_TOKEN=1111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\n   Environment="LOG_LEVEL=DEBUG"\n   Environment="LOG_FORMAT={asctime}\\t| {name}\\t| {message}"\n   Environment="BASE_URL=https://thor.steffo.eu"\n   Environment="GROUP_URL=https://t.me/joinchat/AAAAAAAAAAAAAAAAAAAAAA"\n   ```\n   \n5. Start (and optionally enable) both services:\n   ```bash\n   systemctl start "*-thorunimore"\n   systemctl enable "*-thorunimore"\n   ```\n\n6. Reverse-proxy the web service:\n   ```\n   <VirtualHost *:80>\n   \n   ServerName "thor.steffo.eu"\n   Redirect permanent "/" "https://thor.steffo.eu/"\n   \n   </VirtualHost>\n   \n   <VirtualHost *:443>\n   \n   ServerName "thor.steffo.eu"\n   \n   ProxyPass "/" "http://127.0.0.1:30008/"\n   ProxyPassReverse "/" "http://127.0.0.1:30008/"\n   RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}\n   \n   SSLEngine on\n   SSLCertificateFile "/root/.acme.sh/*.steffo.eu/fullchain.cer"\n   SSLCertificateKeyFile "/root/.acme.sh/*.steffo.eu/*.steffo.eu.key"\n   \n   </VirtualHost>\n   ```\n   ```bash\n   a2ensite rp-thorunimore\n   ```\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': 'Stefano Pigozzi',
    'maintainer_email': 'me@steffo.eu',
    'url': 'https://thor.steffo.eu/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
