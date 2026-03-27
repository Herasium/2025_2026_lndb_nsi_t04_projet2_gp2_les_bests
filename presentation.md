# LogicBox

**Membres de l'équipe :** Victor, Marine, Théodore, Timéo
**Niveau scolaire :** Terminale NSI
**Professeur de NSI :** M. Jim Pioche
**Établissement scolaire :** Lycée Notre-Dame de Boulogne 

---

### 1. Présentation globale du projet

*   **Naissance de l'idée :** C'est une idée que nous avions depuis plusieurs mois, à l'issue du Trophée NSI 2025. L'idée d'un simulateur logique qui nous rapprocherait au plus près du cœur de la machine était très tentante, et nous pensions que ce serait un excellent outil d'apprentissage pour nous.
*   **Problématique initiale :** L'objectif était de fournir une simulation de portes logiques qui soit à la fois performante, éducative et qui laisse à l'utilisateur le plus de liberté possible.
*   **Objectifs :** 
    *   Offrir un espace **"Sandbox"** sans limites pour la créativité des utilisateurs.
    *   Proposer un mode **"Niveaux"** pour apprendre les bases de la logique binaire de manière progressive (46 niveaux disponibles).
    *   Concevoir une architecture extensible supportant des portes personnalisées et différents niveaux d'abstraction (1-bit, 8-bits, mixte).

### 2. Organisation du travail

*   **Présentation de l'équipe :** L'équipe est composée de quatre élèves travaillant sur des pôles d'expertise complémentaires.
*   **Rôle de chacun et chacune :**
    *   **Théodore :** Game designer principal. Responsable de la majorité des portes logiques, des tables de vérité, de la création des niveaux et de leurs solutions.
    *   **Timéo :** Testeur en chef. Responsable du play-test, de la traque des bugs et développeur de menus spécifiques (comme la sauvegarde des puces).
    *   **Marine :** Responsable graphique. En charge de l'identité visuelle (textures, boutons, bordures, titres) et de la conception des menus tutoriel et options.
    *   **Victor :** Chef "Logic". Responsable du cœur du moteur de simulation, des règles de fonctionnement et du développement des interfaces complexes (éditeur, résolveur de niveaux).
*   **Répartition des tâches :** Le code a été rédigé à 99,9 % par les élèves, structuré en modules distincts (`logic`, `ui`, `data`, `engine`) pour faciliter la collaboration.
*   **Temps passé sur le projet :** Nous travaillons sur le projet depuis novembre 2025, à raison de 4h par semaine en cours de NSI.

### 3. Présentation des étapes du projet

*   **Déroulement :** Le projet a été segmenté en modules pour organiser le développement : 
    *   Module `data` : Modèle de domaine.
    *   Module `engine` : Logique de simulation pure.
    *   Module `ui` : Interfaces et interactions utilisateurs.
    *   Module `logger` : Outil de débogage interne.
*   **Chronologie :**
    *   Tout d'abord, un premier éditeur a été développé pour tester les bases du design.
    *   Ensuite est venu le cœur logique, qui a permis d'animer les portes logiques.
    *   Puis, petit à petit, sont venus les différents menus, options et paramètres.
    *   Enfin sont venus les niveaux, chacun réalisé manuellement par nos soins.

### 4. Validation de l'opérationnalité du projet

*   **État d'avancement :** Le projet est pleinement fonctionnel au moment du dépôt. Il inclut un éditeur, 46 niveaux progressifs, un système de tutoriel, des options de configuration et une sauvegarde automatique.
*   **Approches de vérification :** Un processus rigoureux de play-test a été mené par Timéo pour déceler les bugs. L'utilisation d'outils comme *Line Profiler* a permis d'optimiser les performances.
*   **Difficultés rencontrées :** L'équipe a dû faire face à des bugs complexes dans le moteur logique et à des défis d'optimisation. Ces problèmes ont été résolus par une restructuration du code et l'utilisation ponctuelle d'IA pour reformuler certaines fonctions critiques.

### 5. Ouverture

*   **Idées d'amélioration :** 
    *   Implémentation de nouvelles portes logiques "natives" pour gagner en performance.
    *   Ajout de nouveaux packs de niveaux via l'éditeur intégré.
    *   Ajout d'un éditeur de design de portes logiques pour apporter de la diversité visuelle.
*   **Compétences développées :** Conception d'une architecture modulaire, maîtrise de la logique binaire et utilisation d'outils professionnels (*Black*, *Ruff*).