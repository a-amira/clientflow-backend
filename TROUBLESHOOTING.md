# 🔧 Troubleshooting ClientFlow Backend

Ce guide répertorie les problèmes courants rencontrés lors du développement et du déploiement de l'API ClientFlow, ainsi que leurs solutions.

---
## 🚀 Problèmes de Démarrage

### *Problem 1: "No module named 'django'"*
*Cause:* Les dépendances ne sont pas installées dans l'environnement virtuel.
*Solution:*
```bash
pip install -r requirements.txt
```
### Problem 2: “ConnectionRefusedError” (Base de données)
**Cause:** PostgreSQL n’est pas accessible ou le service est arrêté.
**Solution:**
```bash
# Vérifier que PostgreSQL est en cours d'exécution
sudo systemctl status postgresql

# Redémarrer PostgreSQL
sudo systemctl restart postgresql
# Tester la connexion
python manage.py dbshell
```
### Problem 3: “django.db.utils.OperationalError: FATAL: Ident authentication failed”
*Cause:* Problème d’authentification PostgreSQL.
*Solution:*
```bash
# Vérifier les variables d'environnement
cat .env | grep DB_

# Vérifier la configuration PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_user;"
```
## Problèmes d’API

### Problem 4: “404 Not Found” sur /api/
**Cause:** Les URLs ne sont pas configurées correctement.
**Solution:**
```bash
# Vérifier les URLs enregistrées
python manage.py show_urls

# Vérifier que l'app est bien présente dans INSTALLED_APPS
grep -n "INSTALLED_APPS" clientflow/settings.py
```
### Problem 5: “401 Unauthorized” sur tous les endpoints
*Cause:* L’authentification JWT n’est pas correctement configurée ou le token est manquant.
*Solution:*
```bash
# Vérifier les settings JWT
grep -n "SIMPLE_JWT" clientflow/settings.py

# Tester le login pour obtenir un nouveau token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```
### Problem 6: “CORS error” dans le navigateur
**Cause:** CORS n’est pas configuré correctement.
**Solution:**
```bash
# Vérifier CORS dans settings.py
grep -n "CORS" clientflow/settings.py

# Ajouter le domaine frontend aux ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "[https://your-frontend.com](https://your-frontend.com)",
]
```
## Problèmes de Permissions

### Problem 7: “Permission denied” sur les données
*Cause:* L’utilisateur n’a pas les permissions suffisantes.
*Solution:*
```bash
# Vérifier les permissions dans le code
grep -r "permission_classes" api/

# Utiliser le token correct dans Insomnia
# Auth > Bearer Token > [votre token access]
```
### Problem 8: “You do not have permission” même avec token
**Cause :** Le token est expiré ou les  permissions sont incorrectes.
**Solution :**
```bash
# Obtenir un nouveau token frais
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Copier le nouveau token « access »
# Utiliser le nouveau token dans Insomnia
```
## Problèmes de Migration

### Problem 9: “No such table: api_company”
*Cause :* Les migrations n’ont pas été exécutées.
*Solution :*
```bash
# Vérifier l'état des migrations
python manage.py showmigrations

# Appliquer les migrations
python manage.py migrate

# Verifier à nouveau
python manage.py check 
```
### Problem 10: “ERROR: relation ‘api_company’ already exists”
**Cause:** Il y a un conflit de migration.
**Solution:**
```bash
# Rollback à zéro
python manage.py migrate api zero

# Refaire les migrations
python manage.py makemigrations
python manage.py migrate
```
## Problèmes de Performance

### Problem 11: "Server response time > 5 seconds"
*Cause:* Requête lente ou base de données non optimisée.
*Solution:*
```bash
# Vérifier les logs
python manage.py runserver --verbosity 2

# Ajouter des index
python manage.py sqlsequencereset api | python manage.py dbshell

# Utiliser select_related
# Dans views.py:
queryset = Company.objects.select_related('owner').all()
```
### Problem 12: "Memory usage too high"
**Cause:** Trop de données en mémoire.
**Solution:**
```bash
# Paginer les résultats dans settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Utiliser values() pour les grandes requêtes
queryset = Company.objects.values('id', 'name')
```
## Problèmes en Production

### Problem 13: "502 Bad Gateway" nginx
*Cause:* Gunicorn ou l'application a crashé.
*Solution:*
```bash
# Vérifier l'état de Gunicorn
sudo supervisorctl status clientflow

# Redémarrer
sudo supervisorctl restart clientflow

# Vérifier les logs
tail -f /var/log/supervisor/clientflow-stderr.log
```
### Problem 14: "Connection timed out"
**Cause:** Firewall ou configuration réseau bloquée.
**Solution:**
```bash
# Vérifier les ports
sudo netstat -tinp | grep :8000
sudo netstat -tinp | grep :80
sudo netstat -tinp | grep :443

# Vérifier le firewall
sudo ufw status
sudo ufw allow 80
sudo ufw allow 443
sudo ufw status
sudo ufw allow 80
```
## 🛠 Commandes Utiles

### Debug Mode
```bash
# Activer le mode debug
DEBUG=True python manage.py runserver

# Désactiver après debug
DEBUG=False
```
### Database Shell
```bash
# Accéder à la console PostgreSQL
python manage.py dbshell

# Vérifier les tables
\dt

# Vérifier les données
SELECT * FROM api_company;
```
### Django Shell
```bash
# Accéder à la console Django
python manage.py shell
# Tester le modèle
from api.models import Company
companies = Company.objects.all()
print(companies)
```
### Tests
```bash
# Exécuter les tests
python manage.py test

# Avec couverture
pytest --cov=api
```
## 🔍 Checklist pour Déboguer

***Vérifier que le serveur tourne :**
 ```bash
 python manage.py runserver
 ```
*** Vérifier les logs:**
 ```bash
 tail -f logs/
 ```
***Vérifier les variables d'environnement:**
 ```bash
 cat.env
 ```
*** Vérifier la BD: **
 ```bash
 python manage.py dbshell
 ```
***Vérifier les URLs: **
 ```bash
 python manage.py show_urls
 ```
*** Vérifier les migrations:** 
 ```bash
 python manage.py showmigrations
 ```
***Vérifier les permissions:**
 ```bash
 grep -r permission_classes
 ```
*** Tester avec curl: **
 ```bash
 curl -v http://localhost:8000/api/
 ```
***Vérifier les tokens: **
 ```bash
 Obtenir un nouveau token
 ```
---
**Besoin d'aide ?** Consultez la documentation API : 'API_DOCUMENTATION.md'
