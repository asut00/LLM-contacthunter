# LLM-contacthunter 🏹

## Description
Ce projet propose une API permettant d'extraire automatiquement les informations de contact présentes dans un fichier PDF. L'API s'appuie le service GitHub Marketplace, permettant d'accéder à de nombreux modèles de qualité gratuitement.

Une interface frontend simple est également fournie afin de faciliter le test et l'utilisation de l'API.

## Stack Technique
### Backend
- **Langage** : Python
- **Framework** : FastAPI
- **Pourquoi ?** : Simplicité, rapidité d'exécution et accès aux bibliothèques Python pour le parsing de PDF et l'utilisation de LLM.

### Frontend
- **Technologies** : HTML, CSS, JavaScript
- **Pourquoi ?** : Interface légère et simple pour tester l'API.

### Base de Données
- **Choix principal** : SQLite
- **Pourquoi ?** : Légèreté et simplicité pour ce projet.
- **Évolutivité** : Pour une mise en production à plus grande échelle, PostgreSQL ou MySQL seraient à envisager.

## Installation et Utilisation

### Prérequis
- Docker

### Installation
1. Clonez ce dépôt GitHub :
   ```bash
   git clone https://github.com/asut00/LLM-contacthunter
   cd LLM-contacthunter
   ```
2. Connectez-vous à github et générez un token : https://github.com/settings/tokens (un token classique sans aucune option cochée suffit)
   ```bash
   echo <VOTRE TOKEN> > ./backend/github_token.txt
   ```

### Lancement de l'API
Le lancement du serveur FastAPI (uvicorn) desservant l'API et du serveur nginx desservant le frontend se fait avec une simple commande docker compose :
   ```bash
   docker compose up --build
   ```
Le frontend est alors accessible à l'adresse : [http://localhost/](http://localhost/)
Et l'API est accessible à l'adresse : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Utilisation de l'API
#### Endpoint principal : `/analyze`
- **Méthode** : `POST`
- **Paramètre** : Fichier PDF en tant que `multipart/form-data`
- **Réponse** : JSON contenant les informations de contact extraites (nom, email, téléphone, adresse).

#### Endpoint principal : `/contacts`
- **Méthode** : `GET`
- **Réponse** : Informations de contact précdemment stockées dans la database.

Exemple de requête avec `curl` :
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.pdf'
```

### Interface Frontend
L'interface frontend permet d'uploader un fichier PDF et d'afficher les informations extraites, ainsi que d'afficher tous les contacts précédemment enregistrés dans la database.
Pour l'utiliser rendez vous à l'adresse : [http://localhost/](http://localhost/)

## Limitations et Améliorations Possibles
- **Limite du service API** : Le service LLM utilisé impose un quota d'appels gratuits. Pour un déploiement en production, l'utilisation d'un service cloud proposant une solide compute power serait à envisager.
- **Scalabilité** : SQLite est adapté pour le développement, mais une base de données plus robuste est recommandée pour la production.
- **Amélioration de la précision** : Entraînement de modèles spécialisés pour l'extraction d'informations de contact.
- **Déploiement** : Hébergement sur un serveur cloud avec gestion des logs et monitoring.

