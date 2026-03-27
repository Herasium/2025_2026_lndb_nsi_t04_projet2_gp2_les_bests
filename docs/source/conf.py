# Fichier de configuration pour le générateur de documentation Sphinx.
#
# Pour la liste complète des options de configuration, veuillez consulter la documentation :
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Informations sur le projet -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LogicBox'
copyright = '2026, Victor, Marine, Théodore, Timéo'
author = 'Victor, Marine, Théodore, Timéo'
release = '300'

# -- Configuration générale ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# Ajoutez ici tous les chemins contenant des modèles, relatifs à ce répertoire.
templates_path = ['_templates']

# Liste de motifs, relatifs au répertoire source, qui correspondent à des fichiers et
# répertoires à ignorer lors de la recherche de fichiers sources.
# Ce motif affecte également html_static_path et html_extra_path.
exclude_patterns = []

# Le style Pygments (coloration syntaxique) à utiliser.
pygments_style = 'sphinx'

# -- Options pour la sortie HTML -------------------------------------------------

# Le thème à utiliser pour les pages HTML et l'aide HTML. Consultez la documentation
# pour obtenir une liste des thèmes intégrés.
#
html_theme = 'sphinx_rtd_theme'

# Ajoutez ici tous les chemins contenant des fichiers statiques personnalisés (tels que des feuilles de style),
# relatifs à ce répertoire. Ils sont copiés après les fichiers statiques intégrés,
# ainsi un fichier nommé "default.css" écrasera le fichier "default.css" intégré.
html_static_path = ['_static']

# Ajoutez le répertoire source de votre projet au sys.path afin qu'autodoc puisse localiser vos modules.
import os
import sys
sys.path.insert(0, os.path.abspath('../../modules'))

sys.path.insert(0, os.path.abspath('../..'))

# -- Options pour autodoc -----------------------------------------------------

# Extraire automatiquement les annotations de type (type hints) lorsqu'elles sont spécifiées 
# et les intégrer dans les descriptions des fonctions ou méthodes concernées.
autodoc_typehints = 'description'

# Définir le format d'extraction des annotations de type à partir des commentaires.
autodoc_typehints_format = 'short'