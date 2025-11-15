README – PROJET DASHBOARD PYTHON

GALLINA Matéo
WU Lucas
TORRES Diego

User Guide

Cette section explique comment installer, lancer et utiliser le dashboard sur n’importe quelle machine.

PREREQUIS :

Python 3.10 ou supérieur
Modules listés dans requirements.txt
Le fichier de données doit être présent à l’emplacement :
data/cleaned/pred-mai-mef-dhup_clean.csv

INSTALLATION :

Cloner le dépôt :
git clone https://github.com/<votre_repo>.git
Se rendre dans le dossier :
cd <votre_repo>
Installer les dépendances :
pip install -r requirements.txt

LANCEMENT DU DASHBOARD :

Depuis la racine du projet :
python3 main.py

UTILISATION :

Le dashboard permet :
de charger automatiquement les données,
d’afficher des visualisations interactives,
d’analyser les zones littorales et non littorales,
de manipuler les données grâce à plusieurs pages,
d’enregistrer des graphiques dans le dossier outputs.
Data

FICHIER PRINCIPAL :

data/cleaned/pred-mai-mef-dhup_clean.csv

DESCRIPTION DES DONNEES :

Les données incluent notamment :
Types de logements
Informations géographiques
Littoral vs non-littoral
Indicateurs socio-économiques nettoyés
Les données ont été préalablement nettoyées et harmonisées.
Developer Guide

ARCHITECTURE DU PROJET :

project/
│
│
│
├── bdd/
│   └── db.py
│   └── import_to_postgre.py #avant sous postgre maintenant sous sqlite
│
│
├── data/
│ └── cleaned/
│        └── pred-mai-mef-dhup_clean.csv
│        └── pred-mai-mef-dhup_clean_coords.csv
│ └── raw/
│        └── pred-mai-mef-dhup.csv
│
├── Histo/
│        └── tous_les_fichiers_de_création_d_Histo.py
│
├── assets/
│ └── graphiques générés
│ └── styles.css
│
├── pages/
│ ├── home.py
│ ├── carte.py
│ └── ...
│
│
├── main.py
├── requirements.txt
└── README.txt

AJOUTER UNE NOUVELLE PAGE :

Créer un fichier dans /pages/, par exemple :
pages/page_nouvelle_analyse.py
Déclarer la page dans le fichier :
dash.register_page(name, path="/nouvelle-analyse")
Ajouter un layout contenant titres, graphes ou analyses.
Le dashboard détecte automatiquement la nouvelle page.

AJOUTER UN GRAPHIQUE DANS UNE PAGE :

Importer les données :
from utils.load import load_data
df = load_data()
Créer la figure avec Plotly.
Ajouter un composant dcc.Graph dans le layout.

RAPPORT D'ANALYSE
Principales conclusions du projet :

Les zones littorales et non littorales présentent des comportements différents.
Les types de logements montrent des répartitions contrastées selon les zones.
Certains départements affichent des valeurs atypiques qui ressortent dans les visualisations.
Les graphiques ont permis d’identifier des tendances fortes et des dynamiques régionales.
Le dashboard facilite la compréhension des disparités territoriales en France.
Les visualisations interactives permettent d’explorer les données facilement.

COPYRIGHT :

Une partie du code présent dans ce projet a été rédigée à l’aide d’outils d’assistance au développement, notamment GitHub Copilot et ChatGPT.
Ces outils ont été utilisés pour accélérer l’écriture de certaines fonctions, proposer des structures de fichiers et suggérer des corrections syntaxiques ou logiques.
Toutefois, l’intégration, l’adaptation, la vérification et la validation finale du code ont été réalisées par l’auteur du projet.
Les parties générées automatiquement ont été relues, comprises et modifiées si nécessaire afin de garantir leur adéquation avec les objectifs du travail.