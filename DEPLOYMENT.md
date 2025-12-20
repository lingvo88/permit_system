\# Deployment Checklist for Hostinger VPS



\## Pre-Deployment (Local)

\- \[x] Environment variables configured

\- \[x] .env file created (not committed)

\- \[x] .gitignore updated

\- \[x] Security settings added

\- \[ ] Static files collected

\- \[ ] Database migrations created

\- \[ ] Code committed to Git



\## Server Setup (Hostinger VPS)

\- \[ ] SSH access configured

\- \[ ] Python 3.14 installed

\- \[ ] Virtual environment created

\- \[ ] Project files uploaded

\- \[ ] Dependencies installed

\- \[ ] Environment variables set in ~/.bashrc

\- \[ ] Database configured (PostgreSQL or SQLite)

\- \[ ] Static files collected on server

\- \[ ] Media folder permissions set



\## Web Server Configuration

\- \[ ] Nginx installed and configured

\- \[ ] Gunicorn installed and configured

\- \[ ] Systemd service created

\- \[ ] SSL certificate installed (Let's Encrypt)

\- \[ ] Domain DNS configured



\## Final Checks

\- \[ ] DEBUG=False on server

\- \[ ] ALLOWED\_HOSTS configured

\- \[ ] Static files serving correctly

\- \[ ] Media files serving correctly

\- \[ ] Admin panel accessible

\- \[ ] User registration/login working

\- \[ ] All features tested



\## Environment Variables on Server

```bash

export DJANGO\_SECRET\_KEY="production-secret-key"

export DJANGO\_DEBUG="False"

export EMAIL\_HOST="smtp.gmail.com"

export EMAIL\_PORT="587"

export EMAIL\_USE\_TLS="True"

export EMAIL\_HOST\_USER="your-email@gmail.com"

export EMAIL\_HOST\_PASSWORD="your-gmail-app-password"

export DEFAULT\_FROM\_EMAIL="permits@bigrigpermits.org"

```

