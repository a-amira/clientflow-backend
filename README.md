# 🚀 ClientFlow Backend

Une plateforme B2B SaaS moderne pour la gestion de projets, clients et documents. Construite avec Django REST Framework et PostgreSQL.

## 🎯 Objectif
ClientFlow aide les PMEs en Afrique et MENA à :
- Gérer leurs clients et projets
- Suivre la progression des projets
- Gérer les paiements et les documents
- Organiser les événements et réunions

## 🚀 Tech Stack
- **Framework**: Django 4.2 + Django REST Framework 3.14
- **Base de données**: PostgreSQL (Neon Cloud)
- **Authentification**: JWT (djangorestframework-simplejwt)
- **CORS**: django-cors-headers
- **Environment**: python-decouple

## 📋 Prérequis
- Python 3.11+
- pip
- Virtual Environment

## 💾 Installation

### 1. Cloner le repo
bash
git clone [https://github.com/a-amira/clientflow-backend.git](https://github.com/a-amira/clientflow-backend.git)
cd clientflow-backend


### 2. Setup technique
bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les bibliothèques
pip install -r requirements.txt
## 🏗️ Déploiement (Production)
1. **Configuration**: Mettre à jour les settings (DEBUG=False).
2. **Fichiers statiques**: python manage.py collectstatic
3. **Serveur**: Utiliser Gunicorn + Nginx comme reverse proxy.

text
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,[www.your-domain.com](https://www.your-domain.com)
DB_HOST=neon-db-host
DB_NAME=production-db
DB_USER=production-user
DB_PASSWORD=strong-password

## 📞 Support
Pour les questions ou problèmes :
* **Consultez la documentation API**: API_DOCUMENTATION.md
* **Vérifiez les logs du serveur**: utilisez les commandes de logs habituelles.
* **Contactez l'équipe développement**: pour toute assistance technique.

## 📝 Licence
MIT License - Voir le fichier LICENSE pour plus de détails.

## 👥 Équipe
- **AMIRA**: Backend Core, Models, Views, Permissions
- **SABRINE**: Serializers, Auth, Documentation, Testing
- **HAFSA**: Database Configuration (Neon)

---
*Créé le : 15 Mars 2026 | Version : 1.0.0 | Status : En développement ✅*
