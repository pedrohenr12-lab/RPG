from __future__ import annotations

import json
from pathlib import Path

from .config import AppPaths


RACE_STATS = {
    "humanos": (20, 4, 2, 10, 5, 0.10),
    "sylvani": (16, 5, 1, 12, 7, 0.14),
    "aureli": (26, 4, 4, 8, 4, 0.08),
    "aquari": (20, 4, 2, 12, 6, 0.11),
    "solari": (20, 5, 2, 11, 6, 0.12),
    "glacari": (24, 4, 3, 12, 4, 0.09),
    "luminari": (14, 4, 1, 16, 8, 0.15),
    "kragari": (24, 6, 1, 8, 5, 0.10),
    "ziraki": (16, 4, 1, 11, 8, 0.16),
    "ninfari": (18, 4, 2, 14, 7, 0.12),
    "umbrari": (18, 5, 1, 12, 8, 0.16),
    "ferrari": (25, 4, 5, 8, 3, 0.07),
    "drakari": (24, 6, 3, 10, 5, 0.11),
    "ethari": (17, 3, 2, 17, 7, 0.13),
    "voraki": (22, 5, 3, 9, 5, 0.11),
}

FALLBACK_RACES = [
    ("humanos", "Humanos", "Versáteis, curiosos e adaptáveis."),
    ("sylvani", "Elfos (Sylvani)", "Esguios, perceptivos e conectados a plantas."),
    ("aureli", "Anões (Aureli)", "Robustos, fortes e ligados à pedra e à forja."),
    ("aquari", "Aquari", "Nadadores adaptados a rios, lagos e pântanos."),
    ("solari", "Solari", "Resistentes ao calor e grandes observadores do céu."),
    ("glacari", "Glacari", "Metabolismo lento e extrema resistência ao frio."),
    ("luminari", "Fadas (Luminari)", "Pequenas, luminosas e capazes de planar."),
    ("kragari", "Orcs (Kragari)", "Fortes, resistentes e orientados por honra."),
    ("ziraki", "Goblins (Ziraki)", "Ágeis, inventivos e especialistas em armadilhas."),
    ("ninfari", "Ninfari", "Guardiões semi-aquáticos de lagos e piscinas naturais."),
    ("umbrari", "Umbrari", "Silenciosos, noturnos e conhecedores de venenos."),
    ("ferrari", "Ferrari", "Construtores subterrâneos de pele semelhante a pedra."),
    ("drakari", "Drakari", "Escamosos, imponentes e sensíveis ao calor."),
    ("ethari", "Ethari", "Leves, translúcidos e sensíveis a vibrações."),
    ("voraki", "Voraki", "Territoriais, escavadores e atentos ao solo."),
]

REGIONS = {
    "frostreach": ("Frostreach", "00_despertar_frostreach", "Polar e implacável"),
    "eldorwood": ("Eldorwood", "00_despertar_eldorwood_floresta", "Frio, úmido, florestal e urbano"),
    "arkanor": ("Arkanor", "00_despertar_arkanor_planicies", "Planícies, rios e cidades"),
    "stonevale": ("Stonevale", "00_despertar_stonevale", "Platôs secos e cânions"),
    "blackmarsh": ("Blackmarsh", "00_despertar_blackmarsh", "Pântanos, névoa e ilhas"),
    "espinha_do_mundo": ("Espinha do Mundo", "00_despertar_espinha", "Montanhas, vales e cavernas"),
}


class ProjectContent:
    def __init__(self, paths: AppPaths):
        self.paths = paths
        self._scenes: dict[str, dict] | None = None

    def intro(self) -> str:
        try:
            return self.paths.intro_file.read_text(encoding="utf-8")
        except OSError:
            return "Eudora é um continente ferido pelo Aether. Sua jornada começa sem memórias e sem certezas."

    def scenes(self) -> dict[str, dict]:
        if self._scenes is not None:
            return self._scenes
        result: dict[str, dict] = {}
        if self.paths.scenes_root.is_dir():
            for path in sorted(self.paths.scenes_root.glob("*.json")):
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    entries = data if isinstance(data, list) else [data]
                    for scene in entries:
                        if isinstance(scene, dict) and scene.get("id"):
                            result[scene["id"]] = scene
                except (OSError, ValueError):
                    continue
        self._scenes = result
        return result

    def scene(self, scene_id: str) -> dict | None:
        scene = self.scenes().get(scene_id)
        if scene is not None:
            return scene
        # Permite instalar um pacote de cenas enquanto o programa está aberto.
        # Uma ausência real ainda será informada pela interface com o caminho
        # exato pesquisado, em vez de virar um fallback silencioso.
        self._scenes = None
        return self.scenes().get(scene_id)

    def scene_diagnostic(self, scene_id: str) -> str:
        return (
            f"Cena '{scene_id}' ausente. Pasta pesquisada: {self.paths.scenes_root}. "
            f"JSONs carregados: {len(self.scenes())}."
        )

    def quest_definitions(self) -> dict[str, dict]:
        result: dict[str, dict] = {}
        roots = (
            self.paths.software_root / "content" / "quests",
            self.paths.data_root / "quests",
        )
        for root in roots:
            if not root.is_dir():
                continue
            for path in sorted(root.glob("*.json")):
                try:
                    raw = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    continue
                entries = raw if isinstance(raw, list) else [raw]
                for entry in entries:
                    if isinstance(entry, dict) and entry.get("id"):
                        result[str(entry["id"])] = entry
        return result

    def local_races(self) -> list[dict]:
        result = []
        try:
            raw = json.loads(self.paths.races_file.read_text(encoding="utf-8"))
            aliases = {"humano": "humanos", "elfo": "sylvani", "anao": "aureli", "orc": "kragari", "draconato": "drakari"}
            for slug, data in raw.items():
                normalized = aliases.get(slug, slug)
                result.append({"slug": normalized, "name": data.get("nome_exibicao", slug.title()), "description": data.get("descricao", "")})
        except (OSError, ValueError):
            pass
        known = {item["slug"] for item in result}
        for slug, name, description in FALLBACK_RACES:
            if slug not in known:
                result.append({"slug": slug, "name": name, "description": description})
        return result

    @staticmethod
    def enrich_race(data: dict) -> dict:
        slug = data.get("slug", "humanos")
        stats = RACE_STATS.get(slug, RACE_STATS["humanos"])
        return {
            **data,
            "vida": stats[0], "ataque": stats[1], "defesa": stats[2],
            "mana": stats[3], "velocidade": stats[4], "critico": stats[5],
        }
