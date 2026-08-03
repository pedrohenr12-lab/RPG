from __future__ import annotations

import html
import random
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from .config import AppPaths, DatabaseSettings
from .content import ProjectContent, REGIONS
from .core import PersistentCore
from .database import MySQLDatabase, WorldRepository
from .models import PlayerSession
from .procedural_exploration import ExplorationTurn, ProceduralExploration
from .theme import APP_STYLE


def clear_layout(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        child_layout = item.layout()
        if child_layout:
            clear_layout(child_layout)


class HomePage(QWidget):
    navigate = Signal(str)

    def __init__(self, intro: str):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(42, 34, 42, 34)
        root.setSpacing(18)

        title = QLabel("AETHERIA")
        title.setObjectName("Title")
        subtitle = QLabel("Um RPG de exploração, sobrevivência e escolhas em Eudora")
        subtitle.setObjectName("Subtitle")
        root.addWidget(title)
        root.addWidget(subtitle)

        intro_box = QTextBrowser()
        intro_box.setPlainText(intro)
        intro_box.setMaximumHeight(230)
        root.addWidget(intro_box)

        actions = QHBoxLayout()
        for text, destination in (
            ("NOVO JOGO", "new_game"),
            ("CONTINUAR", "continue"),
            ("ABRIR CODEX", "codex"),
            ("CONFIGURAR MYSQL", "database"),
        ):
            button = QPushButton(text)
            button.clicked.connect(lambda _checked=False, dest=destination: self.navigate.emit(dest))
            actions.addWidget(button)
        root.addLayout(actions)

        self.status = QLabel("MySQL desconectado — o conteúdo local continua disponível.")
        self.status.setObjectName("StatusBad")
        root.addWidget(self.status)

        self.cards = QGridLayout()
        self.card_labels = {}
        labels = (("regions", "Regiões"), ("races", "Raças"), ("species", "Espécies"), ("item_catalog", "Itens"))
        for index, (key, name) in enumerate(labels):
            frame = QFrame()
            frame.setObjectName("Card")
            layout = QVBoxLayout(frame)
            number = QLabel("—")
            number.setAlignment(Qt.AlignmentFlag.AlignCenter)
            number.setStyleSheet("font-size: 28px; font-weight: 700; color: #e6c873;")
            caption = QLabel(name)
            caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(number)
            layout.addWidget(caption)
            self.cards.addWidget(frame, 0, index)
            self.card_labels[key] = number
        root.addLayout(self.cards)
        root.addStretch()

    def set_database_state(self, connected: bool, message: str, counts: dict | None = None) -> None:
        self.status.setText(message)
        self.status.setObjectName("StatusGood" if connected else "StatusBad")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        for key, label in self.card_labels.items():
            value = counts.get(key) if counts else None
            label.setText("—" if value is None else str(value))


class DatabasePage(QWidget):
    connect_requested = Signal(object, str)

    def __init__(self, settings: DatabaseSettings):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(42, 34, 42, 34)
        title = QLabel("Banco de dados MySQL")
        title.setObjectName("SectionTitle")
        root.addWidget(title)
        root.addWidget(QLabel("A senha é usada somente nesta sessão e não será salva em arquivo."))

        form_box = QGroupBox("Conexão")
        form = QFormLayout(form_box)
        self.host = QLineEdit(settings.host)
        self.port = QSpinBox()
        self.port.setRange(1, 65535)
        self.port.setValue(settings.port)
        self.user = QLineEdit(settings.user)
        self.database = QLineEdit(settings.database)
        self.password = QLineEdit(DatabaseSettings.senha_ambiente())
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Servidor", self.host)
        form.addRow("Porta", self.port)
        form.addRow("Usuário", self.user)
        form.addRow("Banco", self.database)
        form.addRow("Senha", self.password)
        root.addWidget(form_box)

        self.connect_button = QPushButton("TESTAR E CONECTAR")
        self.connect_button.clicked.connect(self._request_connect)
        root.addWidget(self.connect_button)
        self.status = QLabel("Ainda não conectado.")
        self.status.setWordWrap(True)
        root.addWidget(self.status)

        self.counts = QTextBrowser()
        self.counts.setMaximumHeight(210)
        root.addWidget(self.counts)
        root.addStretch()

    def _request_connect(self) -> None:
        settings = DatabaseSettings(
            host=self.host.text().strip() or "127.0.0.1",
            port=self.port.value(),
            user=self.user.text().strip() or "root",
            database=self.database.text().strip() or "aetheria_rpg",
        )
        self.connect_button.setEnabled(False)
        self.status.setText("Conectando...")
        self.connect_requested.emit(settings, self.password.text())

    def show_result(self, ok: bool, message: str, counts: dict | None = None) -> None:
        self.connect_button.setEnabled(True)
        self.status.setText(message)
        self.status.setObjectName("StatusGood" if ok else "StatusBad")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        if counts:
            names = {"regions":"Regiões","biomes":"Biomas","races":"Raças","species":"Espécies","item_catalog":"Itens","characters_rpg":"Personagens"}
            rows = [f"{names.get(key,key)}: {'tabela não instalada' if value is None else value}" for key, value in counts.items()]
            self.counts.setPlainText("\n".join(rows))
        elif not ok:
            self.counts.setPlainText("Confira se o MySQL está ligado, a senha está correta e schema.sql já foi executado.")


class NewGamePage(QWidget):
    start_requested = Signal(str, str, str)

    def __init__(self, content: ProjectContent):
        super().__init__()
        self.content = content
        self.race_records: list[dict] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(42, 34, 42, 34)
        title = QLabel("Criar personagem")
        title.setObjectName("SectionTitle")
        root.addWidget(title)

        form = QFormLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Nome do personagem")
        self.race = QComboBox()
        self.race.currentIndexChanged.connect(self._race_changed)
        self.region = QComboBox()
        self.region.addItem("Destino aleatório — regra principal", "random")
        for slug, (name, _, climate) in REGIONS.items():
            self.region.addItem(f"{name} — {climate}", slug)
        form.addRow("Nome", self.name)
        form.addRow("Raça", self.race)
        form.addRow("Nascimento", self.region)
        root.addLayout(form)

        self.race_description = QTextBrowser()
        self.race_description.setMaximumHeight(220)
        root.addWidget(self.race_description)
        self.start_button = QPushButton("DESPERTAR EM EUDORA")
        self.start_button.clicked.connect(self._start)
        root.addWidget(self.start_button)
        root.addStretch()
        self.set_races(content.local_races())

    def set_races(self, records: list[dict]) -> None:
        current = self.race.currentData()
        self.race_records = [self.content.enrich_race(row) for row in records]
        self.race.blockSignals(True)
        self.race.clear()
        for row in self.race_records:
            self.race.addItem(row.get("name", row["slug"].title()), row["slug"])
        if current:
            index = self.race.findData(current)
            if index >= 0:
                self.race.setCurrentIndex(index)
        self.race.blockSignals(False)
        self._race_changed(self.race.currentIndex())

    def current_race(self) -> dict:
        index = self.race.currentIndex()
        if 0 <= index < len(self.race_records):
            return self.race_records[index]
        return self.content.enrich_race({"slug":"humanos","name":"Humanos","description":"Versáteis."})

    def _race_changed(self, index: int) -> None:
        if not (0 <= index < len(self.race_records)):
            return
        row = self.race_records[index]
        description = row.get("description") or "Descrição ainda não cadastrada."
        habitat = row.get("habitat") or "Habitat variável"
        self.race_description.setHtml(
            f"<h3>{html.escape(str(row.get('name', 'Raça')))}</h3>"
            f"<p>{html.escape(str(description))}</p><p><b>Habitat:</b> {html.escape(str(habitat))}</p>"
            f"<p><b>Vida:</b> {row['vida']} &nbsp; <b>Ataque:</b> {row['ataque']} &nbsp; "
            f"<b>Defesa:</b> {row['defesa']} &nbsp; <b>Mana:</b> {row['mana']} &nbsp; "
            f"<b>Velocidade:</b> {row['velocidade']}</p>"
        )

    def _start(self) -> None:
        name = self.name.text().strip()
        if not name:
            QMessageBox.warning(self, "Nome necessário", "Digite o nome do personagem.")
            return
        self.start_requested.emit(name, self.race.currentData(), self.region.currentData())


class StatPanel(QGroupBox):
    def __init__(self):
        super().__init__("Personagem")
        self.layout = QVBoxLayout(self)
        self.identity = QLabel("Nenhum personagem")
        self.identity.setWordWrap(True)
        self.layout.addWidget(self.identity)
        self.bars: dict[str, QProgressBar] = {}
        for key, name in (("life","Vida"),("mana","Mana"),("energy","Energia"),("hunger","Fome"),("thirst","Sede"),("temperature","Temperatura")):
            self.layout.addWidget(QLabel(name))
            bar = QProgressBar()
            bar.setRange(0, 100)
            self.layout.addWidget(bar)
            self.bars[key] = bar
        self.clock = QLabel()
        self.inventory = QLabel("Inventário vazio")
        self.inventory.setWordWrap(True)
        self.layout.addWidget(self.clock)
        self.layout.addWidget(self.inventory)

    def update_session(self, session: PlayerSession) -> None:
        self.identity.setText(f"{session.name}\n{session.race_name} — {session.region_name}")
        self.bars["life"].setValue(round(session.life / max(1, session.life_max) * 100))
        self.bars["life"].setFormat(f"{session.life}/{session.life_max}")
        self.bars["mana"].setValue(round(session.mana / max(1, session.mana_max) * 100))
        self.bars["mana"].setFormat(f"{session.mana}/{session.mana_max}")
        self.bars["energy"].setValue(session.energy)
        self.bars["energy"].setFormat(str(session.energy))
        self.bars["hunger"].setValue(session.hunger)
        self.bars["hunger"].setFormat(str(session.hunger))
        self.bars["thirst"].setValue(session.thirst)
        self.bars["thirst"].setFormat(str(session.thirst))
        self.bars["temperature"].setRange(-100, 100)
        self.bars["temperature"].setValue(session.temperature)
        self.bars["temperature"].setFormat(str(session.temperature))
        self.clock.setText(session.clock_label)
        self.inventory.setText("Inventário: " + (", ".join(session.inventory[-5:]) if session.inventory else "vazio"))


class GamePage(QWidget):
    session_changed = Signal(object)

    def __init__(self, content: ProjectContent):
        super().__init__()
        self.content = content
        self.session: PlayerSession | None = None
        self.current_scene: dict | None = None
        self.world_catalog: list[dict] = []
        self.procedural: ProceduralExploration | None = None
        self.core: PersistentCore | None = None

        root = QHBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        left = QVBoxLayout()
        self.title = QLabel("Jornada")
        self.title.setObjectName("SectionTitle")
        self.narrative = QTextBrowser()
        self.narrative.setOpenExternalLinks(False)
        self.options = QVBoxLayout()
        left.addWidget(self.title)
        left.addWidget(self.narrative, 1)
        left.addLayout(self.options)
        root.addLayout(left, 3)
        self.stats = StatPanel()
        self.stats.setMaximumWidth(310)
        root.addWidget(self.stats, 1)

    def start(self, session: PlayerSession) -> None:
        self.session = session
        self.core = PersistentCore(session, self.content.quest_definitions())
        self.procedural = ProceduralExploration(session, self.world_catalog)
        self.stats.update_session(session)
        scene = self.content.scene(session.scene_id)
        if scene:
            self.render_scene(scene)
        else:
            self._start_exploration(self.content.scene_diagnostic(session.scene_id))

    def set_world_catalog(self, records: list[dict]) -> None:
        self.world_catalog = list(records or [])
        if self.procedural:
            self.procedural.set_catalog(self.world_catalog)

    def render_scene(self, scene: dict, transition: str = "") -> None:
        self.current_scene = scene
        self.session.scene_id = scene.get("id", self.session.scene_id)
        if self.procedural:
            self.procedural.set_biome_hint((scene.get("meta") or {}).get("bioma"))
        self.title.setText(scene.get("titulo") or self.session.region_name)
        narrative = (
            scene.get("texto_continuacao")
            if transition and scene.get("texto_continuacao")
            else scene.get("texto") or scene.get("narrative") or "A cena não possui narrativa."
        )
        narrative = self._normalize_narrative(str(narrative))
        if transition:
            narrative = self._normalize_narrative(transition).strip() + "\n\n" + narrative
        if self.core:
            notifications = self.core.enter_scene(str(scene.get("id") or self.session.scene_id))
            narrative += self._format_notifications(notifications)
        self.narrative.setPlainText(narrative)
        clear_layout(self.options)
        options = [
            option for option in (scene.get("opcoes") or scene.get("choices") or [])
            if self._condition_met(option.get("condicao"))
        ]
        for option in options:
            text = option.get("texto") or option.get("choice_text") or "Continuar"
            button = QPushButton(text)
            button.setObjectName("ChoiceButton")
            button.clicked.connect(lambda _checked=False, selected=option: self._choose(selected))
            self.options.addWidget(button)
        if not options:
            button = QPushButton("INICIAR EXPLORAÇÃO LIVRE")
            button.clicked.connect(lambda: self._start_exploration("A cena termina e o território se abre ao seu redor."))
            self.options.addWidget(button)
        self.stats.update_session(self.session)
        self.session_changed.emit(self.session)

    def _choose(self, option: dict) -> None:
        source_scene_id = self.current_scene.get("id", "") if self.current_scene else ""
        self._apply_effects(option.get("efeitos"))
        mode = option.get("modo", "")
        if mode.startswith("exploracao_"):
            opening = "Você abandona a segurança de uma decisão pronta e passa a escolher cada direção."
            if self.core:
                notifications = self.core.record_choice(
                    scene_id=source_scene_id,
                    option_text=str(option.get("texto") or "Iniciar exploração livre"),
                    destination=None,
                    result_key="success",
                )
                opening += self._format_notifications(notifications)
            self._start_exploration(opening)
            self.stats.update_session(self.session)
            self.session_changed.emit(self.session)
            return
        test = option.get("teste")
        outcome = ""
        transition = option.get("transicao") or option.get("consequencia") or ""
        journey = option.get("jornada")
        action_result = None
        result_key = None
        if test:
            attribute = test.get("atributo", "sobrevivencia")
            difficulty = int(test.get("dificuldade", 10))
            success_duration = self._effects_duration(test.get("efeitos_sucesso"))
            failure_duration = self._effects_duration(test.get("efeitos_falha"))
            common_duration = success_duration if success_duration == failure_duration else 0
            if self.core:
                action_result = self.core.resolve_scene_test(
                    scene_id=source_scene_id,
                    option_text=str(option.get("texto") or "ação"),
                    attribute=str(attribute),
                    difficulty=difficulty,
                    duration_minutes=common_duration,
                )
                success = action_result.success
                result_key = action_result.degree
            else:
                die = random.randint(1, 20)
                bonus = int(self.session.attributes.get(attribute, 0))
                total = die + bonus
                success = die == 20 or (die != 1 and total >= difficulty)
                result_key = "success" if success else "failure"
            result_key = "sucesso" if success else "falha"
            self._apply_effects(
                test.get(f"efeitos_{result_key}"),
                skip_time=bool(common_duration),
            )
            destination = test.get(f"destino_{result_key}") or option.get("destino")
            transition = (
                test.get(f"transicao_{result_key}")
                or test.get(f"consequencia_{result_key}")
                or transition
            )
            journey = test.get(f"jornada_{result_key}") or journey
            if action_result:
                outcome = self.core.actions.format_result(
                    action_result, str(test.get("nome", attribute)),
                )
                result_key_for_core = action_result.degree
            else:
                outcome = (
                    f"D20: {die} + {bonus} = {total}, dificuldade {difficulty}. "
                    f"{'Sucesso' if success else 'Falha'} em {test.get('nome', attribute)}."
                )
                result_key_for_core = "success" if success else "failure"
        else:
            destination = option.get("destino") or option.get("destination_key")
            result_key_for_core = "success"
        core_notifications = []
        if self.core:
            core_notifications = self.core.record_choice(
                scene_id=source_scene_id,
                option_text=str(option.get("texto") or option.get("choice_text") or "Continuar"),
                destination=str(destination) if destination else None,
                result=action_result,
                result_key=result_key_for_core,
            )
            transition = str(transition or "") + self._format_notifications(core_notifications)
        scene = self.content.scene(destination) if destination else None
        if scene:
            if not transition:
                transition = self._default_transition(option, outcome)
            elif outcome:
                transition = outcome + "\n\n" + transition
            if source_scene_id.startswith("fr1_") and self.procedural:
                turn = self.procedural.queue_story_journey(
                    str(destination),
                    transition,
                    str(option.get("texto") or "continuar o caminho"),
                    journey,
                )
                self._render_exploration_turn(turn)
            else:
                self.render_scene(scene, transition)
        else:
            reason = (
                "A sequência narrativa terminou e o território agora reage às suas ações."
                if not destination
                else self.content.scene_diagnostic(str(destination))
            )
            self._start_exploration(reason)
            if outcome:
                self.narrative.append(f"\n\n<b>{html.escape(outcome)}</b>")
        self.stats.update_session(self.session)
        self.session_changed.emit(self.session)

    @staticmethod
    def _normalize_narrative(text: str) -> str:
        # Alguns pacotes antigos gravaram as quebras duas vezes ("\\n").
        # Normalize somente sequências de quebra; outras barras permanecem.
        return text.replace("\\r\\n", "\n").replace("\\n", "\n")

    @staticmethod
    def _default_transition(option: dict, outcome: str = "") -> str:
        decision = str(option.get("texto") or option.get("choice_text") or "continuar").strip().rstrip(".")
        if decision:
            decision = decision[0].lower() + decision[1:]
        bridge = f"Você decide {decision}. A consequência dessa escolha conduz diretamente ao que acontece a seguir."
        return (outcome + "\n\n" + bridge).strip() if outcome else bridge

    def _condition_met(self, condition: dict | None) -> bool:
        if not condition:
            return True
        if "tipo" in condition and "items" in condition:
            values = [self._condition_met(item) for item in condition.get("items", [])]
            if condition["tipo"] == "AND":
                return all(values)
            if condition["tipo"] == "OR":
                return any(values)
            if condition["tipo"] == "NOT":
                return not values[0] if values else True
        if "tipo" in condition and "valor" in condition:
            condition = {condition["tipo"]: condition["valor"]}
        if condition.get("tem_flag") and condition["tem_flag"] not in self.session.flags:
            return False
        if condition.get("nao_tem_flag") and condition["nao_tem_flag"] in self.session.flags:
            return False
        if condition.get("tem_item") and condition["tem_item"] not in self.session.inventory:
            return False
        if condition.get("nao_tem_item") and condition["nao_tem_item"] in self.session.inventory:
            return False
        if condition.get("raca") and condition["raca"] != self.session.race_slug:
            return False
        requirement = condition.get("reputacao_minima")
        if requirement and self.session.reputation.get(requirement["faccao"], 0) < requirement["valor"]:
            return False
        return True

    @staticmethod
    def _effects_duration(effects: list[dict] | None) -> int:
        minutes = 0
        for effect in effects or []:
            kind = effect.get("tipo")
            value = int(effect.get("valor") or 0)
            if kind == "tempo_minutos":
                minutes += value
            elif kind in {"tempo", "tempo_horas"}:
                minutes += value * 60
            elif kind == "tempo_dias":
                minutes += value * 24 * 60
        return minutes

    @staticmethod
    def _format_notifications(notifications: list[dict] | None) -> str:
        if not notifications:
            return ""
        rows = [f"[{item.get('title', 'Mundo')}] {item.get('text', '')}" for item in notifications]
        return "\n\n" + "\n".join(rows)

    def _apply_effects(self, effects: list[dict] | None, *, skip_time: bool = False) -> None:
        for effect in effects or []:
            kind = effect.get("tipo")
            value = effect.get("valor")
            if kind == "flag" and value:
                self.session.flags.add(str(value))
                if self.core:
                    self.core.world.set(
                        f"legacy.flag.{value}", True, category="legacy",
                        source=self.session.scene_id, visibility="system",
                    )
            elif kind == "remover_flag" and value:
                self.session.flags.discard(str(value))
            elif kind == "item" and value:
                self.session.inventory.append(str(value))
            elif kind == "dano":
                self.session.life = max(0, self.session.life - int(value or 0))
            elif kind == "cura":
                self.session.life = min(self.session.life_max, self.session.life + int(value or 0))
            elif kind in {"energia", "fome", "sede", "energy", "hunger", "thirst"}:
                self.session.change_need(kind, int(value or 0))
            elif kind == "temperatura":
                self.session.temperature = max(-100, min(100, self.session.temperature + int(value or 0)))
            elif kind == "xp":
                self.session.xp += int(value or 0)
            elif kind == "tempo":
                if not skip_time:
                    self.session.advance_time(int(value or 0))
            elif kind == "tempo_minutos":
                if not skip_time:
                    self.session.advance_minutes(int(value or 0))
            elif kind == "tempo_horas":
                if not skip_time:
                    self.session.advance_time(int(value or 0))
            elif kind == "tempo_dias":
                if not skip_time:
                    self.session.advance_minutes(int(value or 0) * 24 * 60)
            elif kind == "reputacao":
                faction = effect.get("faccao", "desconhecida")
                current = self.session.reputation.get(faction, 50)
                self.session.reputation[faction] = max(0, min(100, current + int(value or 0)))

    def _start_exploration(self, opening: str) -> None:
        if self.procedural is None:
            self.procedural = ProceduralExploration(self.session, self.world_catalog)
        self._render_exploration_turn(self.procedural.start(opening))

    def _render_exploration_turn(self, turn: ExplorationTurn) -> None:
        self.current_scene = None
        self.title.setText(turn.title)
        self.narrative.setPlainText(turn.narrative)
        clear_layout(self.options)
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(8)
        for index, choice in enumerate(turn.choices):
            button = QPushButton(str(choice.get("text") or "Continuar"))
            button.setObjectName("ChoiceButton")
            button.setMinimumHeight(44)
            button.setWordWrap(True) if hasattr(button, "setWordWrap") else None
            tone = choice.get("tone")
            if tone == "danger":
                button.setStyleSheet("border-color: #a94a4a; color: #ffb0a8;")
            elif tone == "urgent":
                button.setStyleSheet("border-color: #d89b3c; color: #ffd27a;")
            action_id = str(choice.get("id") or "continue")
            button.clicked.connect(lambda _checked=False, selected=action_id: self._procedural_choice(selected))
            grid.addWidget(button, index // 2, index % 2)
        self.options.addLayout(grid)

    def _procedural_choice(self, action_id: str) -> None:
        if self.procedural is None:
            return
        if action_id.startswith("scene:"):
            claimed = self.procedural.claim_story_destination()
            if claimed:
                destination, transition = claimed
                scene = self.content.scene(destination)
                if scene:
                    self.render_scene(scene, transition)
                    self.stats.update_session(self.session)
                    self.session_changed.emit(self.session)
                    return
        turn = self.procedural.choose(action_id)
        if self.core:
            self.core.world.append_history("procedural_action", action=action_id)
            self.core.process_due_events()
            notifications = self.core.drain_notifications()
            if notifications:
                turn.narrative += self._format_notifications(notifications)
        self._render_exploration_turn(turn)
        self.stats.update_session(self.session)
        self.session_changed.emit(self.session)


class ContinuePage(QWidget):
    load_requested = Signal(int)

    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(42, 34, 42, 34)
        title = QLabel("Personagens salvos")
        title.setObjectName("SectionTitle")
        root.addWidget(title)
        self.message = QLabel("Conecte o MySQL para consultar os personagens.")
        root.addWidget(self.message)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(("ID", "Nome", "Raça", "Cena", "Criado em", "Último save"))
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.doubleClicked.connect(self._load_selected)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.table)
        self.load_button = QPushButton("CARREGAR PERSONAGEM SELECIONADO")
        self.load_button.clicked.connect(self._load_selected)
        root.addWidget(self.load_button)

    def set_saves(self, records: list[dict]) -> None:
        self.table.setRowCount(len(records))
        for row_index, row in enumerate(records):
            values = (
                row.get("id"), row.get("name"), row.get("race"),
                row.get("current_scene_key"), row.get("created_at"), row.get("updated_at"),
            )
            for column, value in enumerate(values):
                self.table.setItem(row_index, column, QTableWidgetItem(str(value or "")))
        self.message.setText(f"{len(records)} personagem(ns) encontrado(s). Selecione um save para continuar com todo o estado persistente.")

    def _load_selected(self, _index=None) -> None:
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Selecionar save", "Selecione um personagem na tabela.")
            return
        item = self.table.item(row, 0)
        if item:
            self.load_requested.emit(int(item.text()))


class JournalPage(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        title = QLabel("Diário persistente")
        title.setObjectName("SectionTitle")
        root.addWidget(title)
        self.summary = QLabel("Inicie ou carregue uma jornada para consultar a memória do mundo.")
        self.summary.setWordWrap(True)
        root.addWidget(self.summary)
        self.tabs = QTabWidget()
        self.quests = QTextBrowser()
        self.facts = QTextBrowser()
        self.events = QTextBrowser()
        self.history = QTextBrowser()
        self.tabs.addTab(self.quests, "Missões")
        self.tabs.addTab(self.facts, "Fatos")
        self.tabs.addTab(self.events, "Próximos eventos")
        self.tabs.addTab(self.history, "Histórico")
        root.addWidget(self.tabs)

    def refresh(self, core: PersistentCore | None) -> None:
        if core is None:
            return
        snapshot = core.journal_snapshot()
        self.summary.setText(
            f"{core.session.name} — {core.session.clock_label}. "
            f"O diário mostra somente o que já pertence ao estado desta campanha."
        )
        quest_rows = []
        for quest in snapshot["quests"]:
            quest_rows.append(
                f"{quest.get('title')}\nEstado: {quest.get('status')} | Etapa: {quest.get('stage') or '—'}"
                + (f" | Resultado: {quest.get('outcome')}" if quest.get("outcome") else "")
            )
            for key, objective in (quest.get("objectives") or {}).items():
                quest_rows.append(f"  • {key}: {objective.get('status')}")
        self.quests.setPlainText("\n\n".join(quest_rows) if quest_rows else "Nenhuma missão ou rumor descoberto.")
        fact_rows = []
        for fact in snapshot["facts"][:150]:
            value = fact.get("value")
            description = fact.get("description") or ""
            fact_rows.append(
                f"Dia {fact.get('day')}, {int(fact.get('hour') or 0):02d}:{int(fact.get('minute') or 0):02d} — "
                f"{fact.get('key')} = {value}" + (f"\n{description}" if description else "")
            )
        self.facts.setPlainText("\n\n".join(fact_rows) if fact_rows else "Nenhum fato visível registrado.")
        event_rows = []
        for event in snapshot["events"]:
            stamp = core.clock.from_absolute(event["due_absolute_minute"])
            event_rows.append(f"{stamp.label} — {event['title']}\n{event['description']}")
        self.events.setPlainText("\n\n".join(event_rows) if event_rows else "Nenhum acontecimento conhecido está agendado.")
        history_rows = []
        for event in snapshot["history"]:
            history_rows.append(
                f"Dia {event.get('day')}, {int(event.get('hour') or 0):02d}:{int(event.get('minute') or 0):02d} — "
                f"{event.get('type')}"
            )
        self.history.setPlainText("\n".join(history_rows) if history_rows else "O histórico ainda está vazio.")


class CodexPage(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        title = QLabel("Codex de Eudora")
        title.setObjectName("SectionTitle")
        root.addWidget(title)
        self.message = QLabel("Conecte o MySQL para consultar o catálogo completo.")
        root.addWidget(self.message)
        self.tabs = QTabWidget()
        self.tables = {
            "regions": self._table(("Nome", "Continente", "Clima", "História")),
            "races": self._table(("Nome", "Habitat", "Descrição")),
            "species": self._table(("Nome", "Reino", "Classe", "Comportamento", "Ameaça", "Lendária")),
            "items": self._table(("Nome", "Classe", "Tipo", "Raridade", "Tier", "Dano", "Defesa", "Magia", "Efeito")),
        }
        for key, label in (("regions","Regiões"),("races","Raças"),("species","Fauna e flora"),("items","Itens")):
            self.tabs.addTab(self.tables[key], label)
        root.addWidget(self.tabs)

    @staticmethod
    def _table(headers: tuple[str, ...]) -> QTableWidget:
        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setStretchLastSection(True)
        return table

    @staticmethod
    def _fill(table: QTableWidget, rows: list[tuple]) -> None:
        table.setRowCount(len(rows))
        for row_index, values in enumerate(rows):
            for column, value in enumerate(values):
                table.setItem(row_index, column, QTableWidgetItem(str(value if value is not None else "")))

    def load_repository(self, repo: WorldRepository) -> None:
        try:
            regions = repo.regions()
            races = repo.races()
            species = repo.species()
            items = repo.items()
            self._fill(self.tables["regions"], [(r["name"],r["continent"],r["climate"],r["lore"]) for r in regions])
            self._fill(self.tables["races"], [(r["name"],r["habitat"],r["description"]) for r in races])
            self._fill(self.tables["species"], [(r["name"],r["kingdom"],r["class_name"],r["behavior"],r["threat"],"Sim" if r["legendary"] else "Não") for r in species])
            self._fill(self.tables["items"], [(r["name"],r["category_slug"],r["item_kind"],r["rarity"],r["tier"],f"{r['damage_min']}–{r['damage_max']}",r["defense"],r["magic_power"],r["effect_key"]) for r in items])
            self.message.setText(f"{len(regions)} regiões, {len(races)} raças, {len(species)} espécies e {len(items)} itens carregados.")
        except Exception as exc:
            self.message.setText(f"Falha ao carregar o Codex: {exc}")


class MainWindow(QMainWindow):
    def __init__(self, paths: AppPaths, settings: DatabaseSettings):
        super().__init__()
        self.paths = paths
        self.settings = settings
        self.content = ProjectContent(paths)
        self.database = MySQLDatabase(settings)
        self.repository = WorldRepository(self.database)
        self.setWindowTitle("Aetheria — RPG de Eudora")
        self.resize(1280, 820)
        self.setMinimumSize(1020, 680)
        self.setStyleSheet(APP_STYLE)

        central = QWidget()
        shell = QHBoxLayout(central)
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)
        self.sidebar = self._build_sidebar()
        shell.addWidget(self.sidebar)
        self.stack = QStackedWidget()
        shell.addWidget(self.stack, 1)
        self.setCentralWidget(central)

        self.home = HomePage(self.content.intro())
        self.new_game = NewGamePage(self.content)
        self.game = GamePage(self.content)
        self.continue_page = ContinuePage()
        self.journal = JournalPage()
        self.codex = CodexPage()
        self.database_page = DatabasePage(settings)
        self.pages = {
            "home": self.home, "new_game": self.new_game, "game": self.game,
            "continue": self.continue_page, "journal": self.journal,
            "codex": self.codex, "database": self.database_page,
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

        self.home.navigate.connect(self.navigate)
        self.database_page.connect_requested.connect(self.connect_database)
        self.new_game.start_requested.connect(self.start_game)
        self.continue_page.load_requested.connect(self.load_game)
        self.game.session_changed.connect(self._autosave)
        self.navigate("home")
        QTimer.singleShot(200, self._auto_connect)

    def _build_sidebar(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Sidebar")
        frame.setFixedWidth(220)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 22, 14, 22)
        logo = QLabel("AETHERIA")
        logo.setStyleSheet("font-size: 24px; font-weight: 700; color: #e6c873; padding: 8px;")
        layout.addWidget(logo)
        self.nav_buttons = {}
        for text, destination in (("Início","home"),("Novo jogo","new_game"),("Continuar","continue"),("Jornada atual","game"),("Diário","journal"),("Codex","codex"),("MySQL","database")):
            button = QPushButton(text)
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.clicked.connect(lambda _checked=False, dest=destination: self.navigate(dest))
            layout.addWidget(button)
            self.nav_buttons[destination] = button
        layout.addStretch()
        self.sidebar_status = QLabel("● Offline")
        self.sidebar_status.setObjectName("StatusBad")
        layout.addWidget(self.sidebar_status)
        return frame

    def navigate(self, destination: str) -> None:
        page = self.pages.get(destination)
        if page is None:
            return
        self.stack.setCurrentWidget(page)
        for key, button in self.nav_buttons.items():
            button.setChecked(key == destination)
        if destination == "continue" and self.database.connected:
            try:
                self.continue_page.set_saves(self.repository.saves())
            except Exception as exc:
                self.continue_page.message.setText(f"Não foi possível consultar os salvamentos: {exc}")
        elif destination == "codex" and self.database.connected:
            self.codex.load_repository(self.repository)
        elif destination == "journal":
            self.journal.refresh(self.game.core)

    def _auto_connect(self) -> None:
        password = DatabaseSettings.senha_ambiente()
        if password:
            self.connect_database(self.settings, password)

    def connect_database(self, settings: DatabaseSettings, password: str) -> None:
        self.settings = settings
        self.database.disconnect()
        self.database = MySQLDatabase(settings)
        self.repository = WorldRepository(self.database)
        result = self.database.connect(password)
        if result.ok:
            try:
                self.repository.ensure_core_schema(self.content.quest_definitions())
                result.message += " Núcleo Persistente v2 preparado."
            except Exception as exc:
                result.message += f" O jogo conectou, mas o schema do núcleo não pôde ser atualizado: {exc}"
        counts = self.repository.counts() if result.ok else None
        if result.ok:
            settings.salvar(self.paths.arquivo_configuracao)
            self.sidebar_status.setText("● MySQL conectado")
            self.sidebar_status.setObjectName("StatusGood")
            try:
                races = self.repository.races()
                if races:
                    self.new_game.set_races(races)
                self.game.set_world_catalog(self.repository.exploration_species("frostreach"))
                self.codex.load_repository(self.repository)
                self.continue_page.set_saves(self.repository.saves())
            except Exception as exc:
                result.message += f" Parte do conteúdo não pôde ser lida: {exc}"
        else:
            self.sidebar_status.setText("● Offline")
            self.sidebar_status.setObjectName("StatusBad")
        self.sidebar_status.style().unpolish(self.sidebar_status)
        self.sidebar_status.style().polish(self.sidebar_status)
        self.database_page.show_result(result.ok, result.message, counts)
        self.home.set_database_state(result.ok, result.message, counts)

    def start_game(self, name: str, race_slug: str, region_slug: str) -> None:
        race = self.new_game.current_race()
        if race["slug"] != race_slug:
            match = next((row for row in self.new_game.race_records if row["slug"] == race_slug), race)
            race = match
        if region_slug == "random":
            region_slug = random.choice(tuple(REGIONS))
        region_name, scene_id, _ = REGIONS[region_slug]
        session = PlayerSession(
            name=name, race_slug=race_slug, race_name=race.get("name", race_slug.title()),
            region_slug=region_slug, scene_id=scene_id, life_max=race["vida"],
            attack=race["ataque"], defense=race["defesa"], mana_max=race["mana"],
            speed=race["velocidade"], critical=race["critico"],
        )
        session.flags.update((f"raca_{race_slug}", f"spawn_{region_slug}"))
        save_note = ""
        if self.database.connected:
            try:
                save_id = self.repository.save_character(name, race_slug, scene_id)
                session.character_id = save_id
                self.repository.save_game(save_id, session.to_dict())
                save_note = f" Registro MySQL #{save_id} criado."
            except Exception as exc:
                save_note = f" O personagem iniciou, mas o MySQL não salvou: {exc}"
        self.game.start(session)
        self.game.narrative.append(f"\n\n<b>Destino sorteado: {html.escape(region_name)}.</b>{html.escape(save_note)}")
        self.navigate("game")

    def load_game(self, character_id: int) -> None:
        if not self.database.connected:
            QMessageBox.warning(self, "MySQL desconectado", "Conecte o MySQL para carregar este personagem.")
            return
        try:
            raw = self.repository.load_game(character_id)
            if not raw:
                QMessageBox.warning(self, "Save ausente", "Esse personagem não possui um autosave completo.")
                return
            session = PlayerSession.from_dict(raw)
            session.character_id = character_id
            self.game.start(session)
            self.game.narrative.append("\n\n[Save carregado] O estado, as missões, os fatos e os eventos pendentes foram restaurados.")
            self.navigate("game")
        except Exception as exc:
            QMessageBox.critical(self, "Falha ao carregar", f"Não foi possível restaurar o save:\n{exc}")

    def _autosave(self, session: PlayerSession) -> None:
        if not self.database.connected or not session.character_id:
            return
        try:
            self.repository.save_game(session.character_id, session.to_dict())
        except Exception:
            # O jogo continua funcionando mesmo se o banco cair durante a sessão.
            pass

    def closeEvent(self, event) -> None:
        self.database.disconnect()
        super().closeEvent(event)
