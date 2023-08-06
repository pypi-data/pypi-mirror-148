# RYGforms

Ask for a OAuth2 login, then redirect to a Typeform having one or more hidden fields.

## Running

### Development

1. Clone this repository:
   ```bash
   git clone git@github.com:RYGhub/rygforms.git
   ```

2. Enter the cloned directory:
   ```bash
   cd rygforms
   ```

3. Create a new `.env` file inside containing your configuration (see [the example](EXAMPLE.env)):
   ```bash
   cp EXAMPLE.env .env
   vim .env
   ```

4. Install the requirements using Poetry:
   ```bash
   poetry install
   ```

5. Run the debug server from inside the Poetry environment:
   ```bash
   poetry shell
   python -m rygforms
   ```

### Production

1. Create a new `rygforms` user:
   ```bash
   adduser rygforms --system
   ```

1. Create a working directory for RYGforms, set the owner to `rygforms` and enter it:
   ```
   mkdir /opt/rygforms
   cd /opt/rygforms
   ```

1. Create a new venv and enter it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

1. Install through PyPI:
   ```bash
   pip install rygforms gunicorn
   ```

1. Create a new `.env` file inside containing your configuration (see [the example](EXAMPLE.env)):
   ```bash
   curl https://raw.githubusercontent.com/RYGhub/rygforms/master/EXAMPLE.env > .env
   vim .env
   ```

1. Change the owner of the working directory to `rygforms`:
   ```bash
   chown rygforms: /opt/rygforms
   ```
   
1. Copy the [provided systemd unit file](web-rygforms.service) to the `/etc/systemd/system` directory:
   ```bash
   curl https://raw.githubusercontent.com/RYGhub/rygforms/master/web-rygforms.service > /etc/systemd/system/web-rygforms.service
   ```   

1. Reload the systemd unit files:
   ```bash
   systemctl daemon-reload
   ```

1. Start (and optionally enable) the service:
   ```bash
   systemctl start "web-rygforms"
   systemctl enable "web-rygforms"
   ```

1. Copy the [provided Apache site file](rp-rygforms.conf) to the `/etc/apache2/sites-available` directory:
   ```bash
   curl https://raw.githubusercontent.com/RYGhub/rygforms/master/rp-rygforms.conf > /etc/apache2/sites-available/rp-rygforms.conf
   ```

1. Enable the `rp-rygforms` site and reload the Apache configuration:
   ```bash
   a2ensite rp-rygforms
   systemctl reload apache2
   ```
