Utilisation du projet
=====================

Éditeur
-------

Portes
~~~~~~

Vous pouvez ajouter des portes à votre circuit en les faisant glisser depuis la barre du bas.  
Les portes sont réparties en 3 catégories :

- 1 bit (logique binaire)
- Portes personnalisées (basées sur d'autres circuits créés par l'utilisateur)
- 8 bits  

Vous pouvez faire défiler la barre du bas pour afficher toutes les portes.

Connexions
~~~~~~~~~~

Vous pouvez relier plusieurs portes en créant une connexion.  
Une connexion est créée en cliquant sur les entrées/sorties d’une porte (trous en forme de serrure en bas d’une porte).  
Une connexion ne peut être reliée qu’à des entrées/sorties de même taille en bits (1 bit avec 1 bit, 8 bits avec 8 bits).  
Une connexion transmet uniquement des Sorties -> Entrées.  
En cas de conflit, les sorties connectées en premier sont retenues comme solution finale.

Suppression
~~~~~~~~~~~

Vous pouvez utiliser la touche Retour arrière (Suppr) sur n’importe quelle porte ou connexion dans l’éditeur pour les supprimer.  
Supprimer une porte supprimera également toutes les connexions liées à cette porte.  
Une suppression ne peut pas être annulée, veuillez supprimer avec précaution.

Sauvegarde
~~~~~~~~~~

Vous pouvez sauvegarder votre circuit actuel en utilisant la touche **"S"**.  
En appuyant dessus, vous accéderez au menu de sauvegarde, où vous pourrez entrer un nom pour votre circuit (17 caractères max.).  
Une fois sauvegardé, le menu vous ramènera à l’éditeur.  
Tous les circuits sont sauvegardés automatiquement chaque minute afin d’éviter toute perte en cas de crash du jeu.

Basculer une entrée
~~~~~~~~~~~~~~~~~~~

Vous pouvez modifier une entrée en survolant la porte et en appuyant sur la touche **"E"**.  
Si l’entrée est de 1 bit, sa valeur sera simplement inversée : Activé -> Désactivé, Désactivé -> Activé.  
Si l’entrée est supérieure à 1 bit, un nouvel écran apparaîtra, similaire à l’écran de sauvegarde, où il vous sera demandé d’entrer une nouvelle valeur.  
Pour 8 bits, la valeur est comprise entre 0 et 255.  
Appuyer sur **"OK"** vous ramènera à l’éditeur.  
Appuyer sur **"Shift"** en même temps que **"OK"** assignera une valeur aléatoire, dans la plage autorisée, à l’entrée.

Niveau
------

Liste des niveaux
~~~~~~~~~~~~~~~~~

Une liste de tous les niveaux inclus dans le jeu. Ils sont tous numérotés de 0 à 35, mais l’ordre est seulement indicatif ; vous êtes libre d’essayer n’importe quel niveau, même si vous n’avez pas terminé le précédent.  
Les niveaux sont également colorés selon leur difficulté : Vert -> Jaune -> Orange -> Rouge -> Violet -> Noir.

Joueur de niveau
~~~~~~~~~~~~~~~~

Lorsque vous jouez à un niveau, trois éléments vous sont fournis :

- Une limite de temps, définie par l’auteur du niveau. Elle ne vous fera pas échouer le niveau, mais vous empêchera d’obtenir 3 étoiles.
- Les portes à utiliser, dans la barre du bas. Vous êtes limité à ces portes uniquement.
- Une table de vérité, montrant la solution attendue selon les entrées, ainsi que ce que votre circuit produira.

Pour mettre à jour la table de vérité, vous pouvez cliquer sur **"CHECK"** ; cela déclenchera également l’animation de victoire si nécessaire.  
Chaque niveau a une solution, et la réponse peut être affichée en appuyant sur **"ANSWER"**, ce qui validera aussi le niveau avec seulement 1 étoile.  
Dans un niveau, vous ne pouvez pas supprimer les entrées/sorties, seulement les déplacer.

Tutoriel
--------

Le tutoriel vous fournit des bases sur le fonctionnement du jeu, tout comme ce document, avec un rappel du fonctionnement de chaque porte logique de base et de leur table de vérité.

Options
-------

Les options vous permettent d’ajuster certains paramètres du jeu.  
Les paramètres liés à la vidéo, comme les FPS et le plein écran, nécessiteront un redémarrage complet du jeu pour être appliqués.  
Les paramètres sont enregistrés dans le fichier **preferences.json**, à la racine du projet.