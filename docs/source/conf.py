The Prompt
Role: You are an expert Python developer and a native French speaker.
Task: Please translate all comments and docstrings in the provided Python code into French.
Guidelines:

Code Integrity: Do NOT translate Python keywords (from, import, try, except), variable names, or class names (e.g., keep MainMenuView as is). Do not modify anything except the comments, no log output, not text value. Keep the project in english, only the comments in french.
Technical Accuracy: Use professional French programming terminology (e.g., use "boucle principale" for "main loop", "données" for "data").
Context: Ensure the initial docstring is translated in a formal, professional tone.
Output: Return the full code block with the translated text.
Code to translate:

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