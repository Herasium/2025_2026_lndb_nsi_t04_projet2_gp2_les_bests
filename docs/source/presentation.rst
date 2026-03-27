LogicBox Overview
=================

Vue d’ensemble
--------------

Ce projet fournit à l’utilisateur une simulation de portes logiques performante, Turing-complète.
Le projet peut être divisé en trois parties :

- **Le Sandbox**, où les utilisateurs sont libres d’utiliser tous les outils pour laisser libre cours à leur créativité.
- **Les Niveaux**, où les utilisateurs apprennent de manière progressive et structurée les bases de la logique binaire.

L’architecture est conçue pour être extensible, permettant des portes personnalisées et plusieurs niveaux d’abstraction (1-bit, 8-bit, mixte).

Architecture
------------

Le projet est organisé en principaux modules suivants :

- ``modules.data``  
  Modèle de domaine principal : portes, nœuds, circuits (chips) et définitions de niveaux  
  Classes partagées et données de textures pour l’ensemble du projet

- ``modules.engine``  
  Logique de simulation et pipeline d’exécution

- ``modules.ui``  
  Toutes les interactions utilisateur, menu principal, éditeurs et niveaux

- ``modules.logger``  
  Outils de journalisation et de débogage


Concepts clés
-------------

Portes
~~~~~~
Opérateurs logiques (AND, OR, NOT, etc.) implémentés sur différentes tailles de bits.

Niveaux
~~~~~~~
Préconçus par nous, ils représentent un objectif vers lequel l’utilisateur est guidé.

Systèmes UI
~~~~~~~~~~~
Outils pour éditer, déboguer et interagir avec la simulation.


Prise en main
-------------

Flux de travail typique :

1. Sélectionner un niveau
2. Trouver la bonne solution
3. Apprendre à créer vos propres projets
4. Construire vos propres circuits, sans limitations
5. Amusez-vous !


Référence API
-------------

Voir la section :doc:`api` pour la documentation technique complète.