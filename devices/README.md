# INFOM453-project-app

Projet en informatique ambiante et mobile

## EcoTherm

EcoTherm est une application connectée conçue pour la gestion d'un thermostat intelligent. Elle offre la possibilité de contrôler la température, l'éclairage et la consommation énergétique de votre appartement. (à complèter) 

## Démarrage (mode développement)

Ces instructions vous donneront une copie du projet opérationnel sur votre machine locale à des fins de développement et de test.

### Pré-requis

- Python 3.10+
- Django 4.2+
- un environnement virtuel (ex: venv)

### Installation

Si vous souhaitez utiliser le projet, suivez ces instructions.

- Rendez-vous sur le terminal et clonez le dépôt GitHub :

```shell
git clone https://github.com/ton-s/INFOM453-project-app.git
```

- Ensuite, aller dans le répertoire du projet et créer un environnement virtuel :

```shell
cd src
python -m venv env
./env/Scripts/activate (Windows)
source ./env/bin/activate (Linux)
```

- Installer les dépendances Python à partir de la racine du dépôt :

```shell
pip install -r requirements.txt
```

- Maintenant, nous allons appliquer les migrations à la base de données :

```shell
python manage.py makemigrations
python manage.py migrate
```

### Configuraton

- Créer un super utilisateur afin d'avoir accès au panneau administration de Django :

```shell
python manage.py createsuperuser
```

Après avoir executé cette commande, suiver les instructions affichées dans le terminal.

- Connectez-vous ensuite au panneau d'administration en accédant à `/admin` sur votre navigateur

### Exécution

- Utiliser la commande suivant pour lancer le serveur en mode développement :

```shell
python manage.py runserver
```

Accèder au site sur le serveur local à l'adresse suivante :  http://localhost:8000

## Test
pass

## Déploiement

pass
