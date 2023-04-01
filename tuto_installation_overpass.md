# Installation du serveur Overpass en local pour Windows 10

## Installer WSL sur Windows 10

WSL (Windows Subsystem for Linux) est un sous-système de Windows 10 qui permet d'exécuter des commandes Linux directement sur votre ordinateur Windows. Pour installer WSL, suivez les étapes suivantes:

1. Ouvrez le **Panneau de configuration** et cliquez sur **Programmes et fonctionnalités**.

2. Cliquez sur **Activer ou désactiver des fonctionnalités Windows** dans le volet de gauche.

3. Cochez la case **Sous-système Windows pour Linux** et cliquez sur **OK**.

4. Redémarrez votre ordinateur lorsque vous y êtes invité.

5. Une fois que votre ordinateur a redémarré, ouvrez le **Microsoft Store**.

6. Recherchez le système d'exploitation Linux que vous souhaitez installer (dans notre cas, ce sera **Debian**) et cliquez sur **Installer**.

7. Suivez les instructions à l'écran pour terminer l'installation.

## Mises à jour de la distribution Debian

1. Ouvrez votre terminal Debian en cliquant sur le bouton Démarrer de Windows 10, tapez "Debian" et cliquez sur l'icône du terminal.

2. Mettez à jour les informations de votre distribution Debian en entrant la commande suivante :

```bash
sudo apt-get update
```


Cette commande permet de récupérer les informations les plus récentes sur les packages disponibles.

3. Mettez à jour les packages installés sur votre distribution Debian en entrant la commande suivante :

```bash
sudo apt-get upgrade
```

Cette commande permet de mettre à jour tous les packages de votre distribution Debian installés sur votre système.

4. Mettez à jour le système de paquets APT (Advanced Packaging Tool) en entrant la commande suivante :

```bash
sudo apt-get dist-upgrade
```

Cette commande permet de mettre à jour les packages qui ont des dépendances non satisfaites.

5. Redémarrez votre système pour vous assurer que toutes les mises à jour ont été prises en compte en entrant la commande suivante :
```bash
sudo reboot
```
## Installer les packages requis

Avant de continuer avec l'installation de l'Overpass API, vous devez installer les packages suivants : g++, make, expat, libexpat1-dev et zlib1g-dev. Pour cela, exécutez les commandes suivantes :

1. Mettez à jour la liste des packages :
```bash
sudo apt update
```

2. Installez les packages nécessaires :
```bash
sudo apt install g++ make expat libexpat1-dev zlib1g-dev
```

Cette commande peut prendre un certain temps en fonction de la vitesse de votre ordinateur et de la taille des packages. Il est recommandé de patienter jusqu'à ce qu'elle soit terminée.

**Temps estimé :** entre 1 et 5 minutes en fonction de la vitesse de l'ordinateur.



## Télécharger les fichiers nécessaires pour Overpass-API

1. Ouvrez votre terminal Debian et créez un dossier appelé "Overpass-API" en entrant la commande suivante :
```bash
mkdir Overpass-API
```

2. Accédez au dossier "Overpass-API" en entrant la commande suivante :
```bash
cd Overpass-API
```

3. Téléchargez les données de la carte de l'Ile de France en utilisant la commande wget :

```bash
wget https://download.geofabrik.de/europe/france/ile-de-france-latest.osm.bz2
```

Cette commande télécharge les dernières données de la carte de l'Ile de France depuis le site de téléchargement Geofabrik.

4. Téléchargez la dernière version de Overpass-API en utilisant la commande wget :
```bash
wget http://dev.overpass-api.de/releases/osm-3s_v0.7.59.4.tar.gz
```

Cette commande télécharge la dernière version de Overpass-API à partir du site officiel.

5. Décompressez le fichier Overpass-API téléchargé en entrant la commande suivante :
```bash
tar xvfz osm-3s_v0.7.59.4.tar.gz
```

Cette commande décompresse le fichier tar.gz téléchargé.

6. Déplacez le fichier des données de la carte Ile-de-France vers le dossier "db" situé dans le dossier Overpass-API en entrant la commande suivante :

```
mv ile-de-france-latest.osm.bz2 db/
```

Cette commande déplace le fichier de données de la carte téléchargé précédemment dans le dossier "db" du dossier Overpass-API.


## Compiler Overpass-API à partir du dossier osm-3s_v0.7.59.4

1. Assurez-vous que votre terminal Debian est toujours ouvert et accédez au dossier osm-3s_v0.7.59.4 en entrant la commande suivante :
```bash
cd /home/USERNAME/Overpass-API/osm-3s_v0.7.59.4
```

Cette commande accède au dossier osm-3s_v0.7.59.4 à partir du dossier Overpass-API en utilisant le chemin d'accès absolu.

2. Configurez Overpass-API en utilisant la commande suivante :
```bash
./configure CXXFLAGS="-O2" --prefix=/home/USERNAME/Overpass-API/
```

Cette commande configure Overpass-API avec les options spécifiées.

3. Compilez Overpass-API en utilisant la commande suivante :

```bash
make install
```

Cette commande compile Overpass-API et installe les fichiers dans le dossier Overpass-API. **Assurez-vous de bien changer** *USERNAME* **par votre nom d'utilisateur**. Cette opération peut prendre du temps, prévoyez 5 à 10 minutes !

## Installer les données de la carte Ile-de-France

1. Accédez au dossier Overpass-API en utilisant la commande suivante :

```bash
cd /home/USERNAME/Overpass-API
```


2. Exécutez la commande suivante pour installer les données de la carte, en remplaçant les chemins d'accès par les bons :

```bash
/home/USERNAME/Overpass-API/bin/init_osm3s.sh /home/USERNAME/Overpass-API/map_data.osm.bz2 /home/USERNAME/Overpass-API/db /home/USERNAME/Overpass-API/bin
```

Cette commande peut prendre un certain temps en fonction de la vitesse de votre ordinateur et de la taille des données de la carte. Il est recommandé de patienter jusqu'à ce qu'elle soit terminée.

**Temps estimé :** entre 5 et 15 minutes en fonction de la vitesse de l'ordinateur.

## Installer Apache2 et activer CGI

Pour pouvoir utiliser l'Overpass API, vous devez installer le serveur web Apache2 et activer le module CGI. Voici les étapes à suivre :

1. Installez Apache2 en exécutant la commande suivante :

```
sudo apt install apache2
```

Cette commande peut prendre un certain temps en fonction de la vitesse de votre ordinateur et de la taille des packages. Il est recommandé de patienter jusqu'à ce qu'elle soit terminée.

2. Activez le module CGI en exécutant la commande suivante :
```bash
sudo a2enmod cgi
```

Cette commande va activer le module CGI dans Apache2.

Une fois ces étapes terminées, vous avez installé Apache2 et activé le module CGI. Vous êtes prêt à passer à la prochaine étape.

## Configuration d'Apache2 et ouverture du fichier par défaut

Maintenant que vous avez installé Apache2 et activé le module CGI, vous devez configurer le serveur web pour qu'il puisse utiliser l'Overpass API. Voici les étapes à suivre :

1. Ouvrez le fichier de configuration Apache2 par défaut en exécutant la commande suivante :
```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

Cette commande va ouvrir le fichier de configuration Apache2 par défaut dans l'éditeur de texte nano.

2. Faites en sorte que le fichier de configuration ressemble à ceci :
```bash
<VirtualHost  *:80>
  ServerAdmin  webmaster@localhost
  ExtFilterDefine  gzip  mode=output  cmd=/bin/gzip
  DocumentRoot  /var/www/html

  # This directive indicates that whenever someone types http://www.mydomain.com/api/ 
  # Apache2 should refer to what is in the local directory [YOUR_EXEC_DIR]/cgi-bin/
  ScriptAlias  /api/  /home/USERNAME/Overpass-API/cgi-bin/
  
  <Directory "/home/USERNAME/Overpass-API/src/cgi-bin/">
	  AllowOverride None
	  Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
	  Order allow,deny
	  Allow from all
	  Require all granted
  </Directory>

  ErrorLog  /var/log/apache2/error.log

  # Possible values include: debug, info, notice, warn, error, crit, alert, emerg
  LogLevel  warn

  CustomLog  /var/log/apache2/access.log  combined

</VirtualHost>
```

Ces lignes vont indiquer à Apache2 où se trouvent les scripts CGI de l'Overpass API.

3. Enregistrez et fermez le fichier en appuyant sur `CTRL+X`, suivi de `Y`, puis `ENTER`.

4. Vous devez vous assurez que le dossier Overpass-API donne les autorisations suffisantes à Apache2 pour y accéder :
```bash
chmod -R 755 /home/USERNAME/Overpass-API/ 
``` 

5. Redémarrez Apache2 en exécutant la commande suivante :
```bash
sudo systemctl restart apache2
```

Cette commande va redémarrer le serveur web Apache2 avec les nouvelles configurations.

Une fois ces étapes terminées, vous avez configuré Apache2 pour utiliser l'Overpass API. Vous êtes prêt à passer à la prochaine étape.

6. Lancer le serveur avec la commande suivante :
```bash
nohup /home/USERNAME/Overpass-API/bin/dispatcher --osm-base --db-dir=/home/USERNAME/Overpass-API/db/ &
```
Cette commande permet de lancer le dispatcher en arrière-plan sans bloquer le terminal. Maintenant vous pouvez tester la requête suivante sur un terminal **Windows** pour voir si le serveur Overpass fonctionne ainsi que la configuration Apache2 :
```
curl http://localhost/api/interpreter?data=%3Cprint%20mode=%22body%22/%3E
```

Vous devriez obtenir la réponse suivante :
```bash
<?xml version="1.0" encoding="UTF-8"?>
<osm-derived>
  <note>
    The data included in this document is from www.openstreetmap.org. It has there been collected 
    by a large group of contributors. For individual attribution of each item please refer to 
    https://www.openstreetmap.org/api/0.6/[node|way|relation]/#id/history 
  </note>
  <meta osm_base=""/>
</osm-derived>
```

Si vous avez le bon résultat, c'est que vous avez terminé l'installation du serveur Overpass sur votre PC ! Sinon, vous pouvez m'envoyer un message sur Discord pour que je debug votre installation...