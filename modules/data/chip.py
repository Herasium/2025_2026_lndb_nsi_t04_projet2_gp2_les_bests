import json
import os
from typing import Dict, List, Any, Union, Optional
from line_profiler import profile

from modules.data import data
from modules.data.gate_index import gate_types
from modules.data.nodes.path import Path
from modules.logger import Logger
from modules.ui.toolbox.id_generator import random_id
from modules.data.custom import CustomGate

logger: Logger = Logger("Chip")


class Chip:
    """Gère le cycle de vie, la sérialisation et la structure d'une puce logique."""

    def __init__(self, id: str) -> None:
        """Initialise une nouvelle instance de Chip.

        Args:
            id: Identifiant unique de la puce.
        """
        self.paths: Dict[str, Path] = {}
        self.gates: Dict[str, Any] = {}
        self.id: str = id
        self.name: str = "Default Chip"
        self.type: str = "Chip"
        self.changed: bool = False
        self.requirements: List[str] = []
        self.temp_data: Optional[Dict] = None
        self.private = False

    @profile
    def copy(self) -> "Chip":
        """Crée une copie profonde de la puce avec un identifiant nouvellement généré.

        Returns:
            Une nouvelle instance de Chip reflétant l'état actuel.
        """
        new: Chip = Chip("no_id")
        new.partial_load(json.loads(self.save(no_file=True, dojson=True)))
        new.load()
        new.id = random_id()
        return new

    @profile
    def save(
        self, no_file: bool = False, dojson: bool = False
    ) -> Union[Dict, str, None]:
        """Sérialise l'état de la puce vers un dictionnaire, une chaîne JSON ou le disque.

        Args:
            no_file: Empêche les entrées/sorties (I/O) sur le disque si vrai.
            dojson: Retourne la sortie sérialisée sous forme de chaîne JSON si vrai.

        Returns:
            La représentation sérialisée ou None si la puce a été écrite sur le disque.
        """
        paths: Dict[str, Any] = {}
        gates: Dict[str, Any] = {}

        self.requirements = []

        # Sauvegarde de tous les chemins
        for id in self.paths:
            paths[id] = self.paths[id].save()

        # Sauvegarde de toutes les portes et gestion des dépendances
        for id in self.gates:
            gates[id] = self.gates[id].save()
            if self.gates[id].type == "Custom":
                self.requirements.append(self.gates[id].base_chip_id)
                self.requirements += data.loaded_chips[
                    self.gates[id].base_chip_id
                ].requirements

        # Suppression des doublons dans les prérequis
        self.requirements = list(set(self.requirements))

        result: Dict[str, Any] = {
            "type": self.type,
            "name": self.name,
            "id": self.id,
            "gates": gates,
            "paths": paths,
            "version": data.VERSION,
            "requirements": self.requirements,
        }

        if no_file and not dojson:
            return result

        dump: str = json.dumps(result, indent=1)
        if dojson:
            return dump

        # Gestion de l'écriture sur le système de fichiers
        path: str = data.current_path
        os.makedirs(os.path.join(path, "saves"), exist_ok=True)
        file_path: str = os.path.join(os.path.join(path, "saves"), f"{self.id}.chip")

        with open(file_path, "wb") as file:
            file.write(dump.encode())

        logger.print(f"Sauvegarde de {self.name}, #{self.id}")
        return None

    @profile
    def partial_load(self, data: Dict[str, Any]) -> None:
        """Charge les métadonnées de base et met en mémoire tampon les données structurelles.

        Args:
            data: Dictionnaire d'état brut.
        """
        self.type = data["type"]
        self.name = data["name"]
        self.id = data["id"]

        if data["version"] != "a.136":
            self.requirements = data["requirements"]

        self.temp_data = data

    @profile
    def load(self) -> None:
        """Construit les portes (gates) et les chemins (paths) à partir des données en tampon.

        Nécessite l'exécution préalable de partial_load.
        """
        if self.temp_data is None:
            logger.error("Vous devez effectuer un chargement partiel de la puce avant de terminer le chargement.")
            return

        data_map: Dict[str, Any] = self.temp_data

        # Instanciation des portes selon leur type
        for key in data_map["gates"]:
            gate = data_map["gates"][key]
            if gate["type"] in ["Gate", "Complex"]:
                new = gate_types[gate["gate"]]("default_id")
            elif gate["type"] == "Custom":
                new = CustomGate("default_id", Chip("default_chip"))
            else:
                new = gate_types[gate["gate"]]("default_id")

            new.load(gate)
            self.gates[key] = new

        # Instanciation des chemins réseaux
        for key in data_map["paths"]:
            new_path = Path("default_id")
            new_path.load(data_map["paths"][key])
            self.paths[key] = new_path

        self.temp_data = None
        logger.debug(f"Puce chargée : {self}")

    def __str__(self) -> str:
        """Fournit un résumé lisible de l'instance de la puce.

        Returns:
            Une chaîne formatée contenant l'ID et le décompte des objets.
        """
        return f"Chip (#{self.id}) {len(self.gates)} Portes / {len(self.paths)} Chemins"

    def get_inputs(self) -> List[str]:
        """Récupère les identifiants pour toutes les portes de type entrée (input).

        Returns:
            Liste des IDs de portes d'entrée.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].gate_type in ["Input", "8Input"]:
                result.append(i)
        return result

    def get_outputs(self) -> List[str]:
        """Récupère les identifiants pour toutes les portes de type sortie (output).

        Returns:
            Liste des IDs de portes de sortie.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].type == "Output":
                result.append(i)
        return result

    def get_gates(self) -> List[str]:
        """Récupère les identifiants pour tous les composants de type porte standard.

        Returns:
            Liste des IDs de portes standards.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].type == "Gate":
                result.append(i)
        return result