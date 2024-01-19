# INFOM453-project-app

Projet en informatique ambiante et mobile

## EcoTherm

Afin de répondre aux attentes du persona, le projet propose un thermostat intelligent baptisé EcoTherm, conçu pour la gestion automatisée de divers aspects d'une habitation par le biais de la domotique. Accessible via une interface web sur ordinateur ou mobile, EcoTherm permet de réguler le chauffage, l'éclairage, ainsi que les appareils électroménagers spécifiques à chaque pièce de la maison, tout en surveillant la consommation globale. L'application EcoTherm offre également des conseils personnalisés pour aider l'utilisateur à optimiser la gestion énergétique de son logement. En facilitant l'accès et l'interprétation des données de consommation à travers des graphiques clairs, EcoTherm permet à l'utilisateur de suivre et de recevoir des recommandations pour interagir de manière éco-responsable avec son domicile, minimisant ainsi son impact sur l'environnement.

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

Les informations suivantes serviront d'aide au déploiement du projet Django (application web):
- D'abord, je vous réfère à la documentation de Django au niveau du déploiement afin d'avoir l'ensemble des étapes et bonnes pratiques.
https://docs.djangoproject.com/fr/4.1/howto/deployment/
