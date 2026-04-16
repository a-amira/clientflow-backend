# Déploiement ClientFlow Backend

## 🚀 Guide de déploiement en production

---

## 1. Prérequis

- Server Linux (Ubuntu 20.04+)
- Python 3.11+
- PostgreSQL 12+
- Nginx
- Supervisor (ou systemd)

---

## 2. Préparation du serveur

### 2.1 Installer les dépendances système

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3-pip
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y nginx
sudo apt-get install -y supervisor

##2.2 Créer l'utilisateur de l'application
sudo useradd -m -s /bin/bash clientflow
sudo su - clientflow

##3. Déployer l'application
###3.1 Cloner le repository

git clone https://github.com/a-amira/clientflow-backend.git
cd clientflow-backend

###3.2 Créer l'environnement virtuel

python3.11 -m venv venv
source venv/bin/activate

###3.3 Installer les dépendances de production
pip install -r requirements-prod.txt

###3.4 Configurer les variables d'environnement

cat > .env << 'ENVFILE'
# Django Settings
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECRET_KEY=your-secret-key-here

# Database
DB_ENGINE=django.db.backends.postgresql
DB_HOST=localhost
DB_NAME=clientflow_prod
DB_USER=clientflow_user
DB_PASSWORD=strong-password
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis (for caching)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
ENVFILE

###3.5 Créer la base de données PostgreSQL

sudo su - postgres
psql

Dans PostgreSQL:

CREATE DATABASE clientflow_prod;
CREATE USER clientflow_user WITH PASSWORD 'strong-password';
ALTER ROLE clientflow_user SET client_encoding TO 'utf8';
ALTER ROLE clientflow_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE clientflow_user SET default_transaction_deferrable TO on;
ALTER ROLE clientflow_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE clientflow_prod TO clientflow_user;
\q

###3.6 Exécuter les migrations

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

###3.7 Créer un superuser

python manage.py createsuperuser

##4. Configurer Gunicorn
###4.1 Créer le script Gunicorn

cat > /home/clientflow/gunicorn_start.sh << 'BASH'
#!/bin/bash

NAME="clientflow"
DJANGODIR=/home/clientflow/clientflow-backend
SOCKFILE=/home/clientflow/gunicorn.sock
USER=clientflow
GROUP=clientflow
WORKERS=3
WORKER_CLASS=sync
BIND=unix:$SOCKFILE

cd $DJANGODIR
source venv/bin/activate

export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec venv/bin/gunicorn \
  --name $NAME \
  --workers $WORKERS \
  --worker-class $WORKER_CLASS \
  --bind $BIND \
  --log-level debug \
  clientflow.wsgi:application
BASH

chmod +x /home/clientflow/gunicorn_start.sh

##5. Configurer Supervisor
###5.1 Créer le fichier de configuration
Supervisor

sudo cat > /etc/supervisor/conf.d/clientflow.conf << 'CONF'
[program:clientflow]
directory=/home/clientflow/clientflow-backend
command=/home/clientflow/gunicorn_start.sh
user=clientflow
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/clientflow/logs/gunicorn.log
CONF

###5.2 Mettreà jour Supervisor

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start clientflow

##6. Configurer Nginx
###6.1 Créer la configuration Nginx

sudo cat > /etc/nginx/sites-available/clientflow << 'NGINX'
upstream clientflow_app {
    server unix:/home/clientflow/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 100M;

    location /static/ {
        alias /home/clientflow/clientflow-backend/staticfiles/;
    }

    location /media/ {
        alias /home/clientflow/clientflow-backend/media/;
    }

    location / {
        proxy_pass http://clientflow_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX

###6.2 Activer le site Nginx

sudo ln -s /etc/nginx/sites-available/clientflow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

##7. Configurer SSL avec Let's Encrypt
###7.1 Installer Certbot

sudo apt-get install -y certbot python3-certbot-nginx

###7.2 Obtenir un certificat

sudo certbot --nginx -d your-domain.com -d www.your-domain.com

##8. Logs et Monitoring
###8.1 Vérifier les logs

# Logs Gunicorn
tail -f /home/clientflow/logs/gunicorn.log

# Logs Django
tail -f /var/log/supervisor/clientflow-stderr.log

# Logs Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

###8.2 Health Check

curl https://your-domain.com/api/

##9. Backup et Maintenance
###9.1 Backup de la base de données

pg_dump -U clientflow_user clientflow_prod > /backup/clientflow_$(date +\%Y\%m\%d).sql

###9.2 Mise à jour du code

cd /home/clientflow/clientflow-backend
git pull origin main
source venv/bin/activate
pip install -r requirements-prod.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart clientflow

##10. Troubleshooting
Problem: 502 Bad Gateway
Solution:

sudo supervisorctl restart clientflow
sudo nginx -t
sudo systemctl restart nginx

Problem: Permission Denied
Solution:

sudo chown -R clientflow:clientflow /home/clientflow/
sudo chmod -R u+rwx /home/clientflow/

Problem: Database Connection Error
Solution:

python manage.py dbshell
# Vérifier que la connexion fonctionne

Checklist Final
* ﻿﻿Variables d'environnement configurées
* ﻿﻿Base de données créée et migrée
* ﻿﻿Gunicorn configuré et en cours d'exécution
* ﻿﻿Nginx configuré
* ﻿﻿SSL configuré
* ﻿﻿Logs configurés
* Logs configurés
* ﻿﻿Backup configuré
* ﻿﻿Health check réussi
* Déploiement terminé! 
