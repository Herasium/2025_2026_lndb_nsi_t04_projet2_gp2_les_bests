Futur
=====

Conseils et instructions pour les futurs développeurs qui reprendront ce projet.

Comment créer une nouvelle porte logique
----------------------------------------

Créer une porte logique "native" permet d'optimiser les performances par rapport aux portes personnalisées (*custom gates*). Voici les étapes pour intégrer une nouvelle porte :

1. **Créer un nouveau fichier** dans ``data/nodes/``.
   Il n'est pas nécessaire de le placer dans l'un des sous-dossiers existants ; ceux-ci servent uniquement à l'organisation.
   
2. **Éditer le fichier** pour définir les propriétés de la porte :

.. code-block:: python

    self.name: str = "AND"           # Nom affiché visuellement
    self.type: str = "Gate"         # Type d'entité (ne pas modifier)
    self.gate_type: str = "AND"      # Identifiant unique de la porte

    self.inputs: list[int] = [0, 0]  # Nombre et valeurs par défaut des entrées
    self.outputs: list[int] = [0]    # Nombre et valeurs par défaut des sorties
    self.inputs_sizes: list[int] = [1, 1]  # Taille des entrées (1bit, 4bit, 8bit, etc.)
    self.outputs_sizes: list[int] = [1]    # Taille des sorties (1bit, 4bit, 8bit, etc.)

3. **Inscrire la porte dans l'index** :
   Modifiez le fichier ``data/gate_index.py``. Ajoutez votre porte à la liste générale (``gate_types``) **et** à la liste correspondante de l'éditeur (``gate_types_1`` ou ``gate_types_8``). 
   
   .. note:: 
      À ce stade, la porte est visible dans l'éditeur, mais elle n'a pas encore de comportement logique.

4. **Définir la logique** dans le moteur (``engine/logic.py``) :

.. code-block:: python

    def gate_and(inputs: list[int]) -> list[int]:
        """
        Calcule l'opération ET (AND).

        Args:
            inputs: Liste des valeurs d'entrée.

        Returns:
            list[int]: Liste des valeurs de sortie calculées.
        """
        # On multiplie par 1 pour convertir le booléen en entier (0 ou 1)
        return [(inputs[0] and inputs[1]) * 1]

5. **Lier la fonction à l'index logique** (``engine/logic.py``) :
   Ajoutez votre fonction au dictionnaire ``LOGIC_MAP`` pour que le moteur puisse l'appeler :

.. code-block:: python

    LOGIC_MAP: dict[str, callable] = {
        "AND": gate_and,
    }
    
6. **Profitez !** 
   Bravo, vous venez d'ajouter votre première porte logique native !

Créer un nouveau niveau
-----------------------

Il est possible d'accéder au menu d'édition des niveaux en maintenant la touche **Shift** (ou **Maj**) tout en cliquant sur le bouton **"Level"**.

Voici la marche à suivre pour intégrer un nouveau défi :

1. **Conception** : Créez votre propre niveau dans l'éditeur et n'oubliez pas d'y ajouter une solution valide.
2. **Sauvegarde** : Appuyez sur la touche **"S"** pour sauvegarder. Le système vous demandera alors :
   * Un numéro de niveau ;
   * Une difficulté ;
   * Un temps limite.
3. **Personnalisation** : Pour modifier le nom et la description du niveau, vous devez ouvrir le fichier JSON généré dans un éditeur de texte (ex: VS Code, Notepad++) et modifier les champs suivants situés à la fin du fichier :

.. code-block:: json

    {
      "name": "8 Bits Adder",
      "description": "Add two 8-bit inputs using breaker, maker, and other gates. Output is SUM."
    }

.. tip::
   Assurez-vous que le format JSON reste valide après vos modifications (attention aux virgules et aux guillemets).