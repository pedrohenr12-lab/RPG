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
from .database import MySQLDatabase, WorldRepository
from .models import PlayerSession
from .theme import APP_STYLE


def clear_layout(layout: QVBoxLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()


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
        self.clock.setText(f"Dia {session.day} — {session.hour:02d}:00")
        self.inventory.setText("Inventário: " + (", ".join(session.inventory[-5:]) if session.inventory else "vazio"))


class GamePage(QWidget):
    session_changed = Signal(object)

    def __init__(self, content: ProjectContent):
        super().__init__()
        self.content = content
        self.session: PlayerSession | None = None
        self.current_scene: dict | None = None

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
        self.stats.update_session(session)
        scene = self.content.scene(session.scene_id)
        if scene:
            self.render_scene(scene)
        else:
            self._start_exploration(f"A cena {session.scene_id} não foi encontrada; a exploração livre foi iniciada.")

    def render_scene(self, scene: dict) -> None:
        self.current_scene = scene
        self.session.scene_id = scene.get("id", self.session.scene_id)
        self.title.setText(scene.get("titulo") or self.session.region_name)
        self.narrative.setPlainText(scene.get("texto") or scene.get("narrative") or "A cena não possui narrativa.")
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
        self._apply_effects(option.get("efeitos"))
        mode = option.get("modo", "")
        if mode.startswith("exploracao_"):
            self._start_exploration("Você abandona a segurança de uma decisão pronta e passa a escolher cada direção.")
            self.stats.update_session(self.session)
            self.session_changed.emit(self.session)
            return
        test = option.get("teste")
        outcome = ""
        if test:
            die = random.randint(1, 20)
            attribute = test.get("atributo", "sobrevivencia")
            bonus = int(self.session.attributes.get(attribute, 0))
            difficulty = int(test.get("dificuldade", 10))
            total = die + bonus
            success = die == 20 or (die != 1 and total >= difficulty)
            result_key = "sucesso" if success else "falha"
            self._apply_effects(test.get(f"efeitos_{result_key}"))
            destination = test.get(f"destino_{result_key}") or option.get("destino")
            outcome = (
                f"D20: {die} + {bonus} = {total}, dificuldade {difficulty}. "
                f"{'Sucesso' if success else 'Falha'} em {test.get('nome', attribute)}."
            )
        else:
            destination = option.get("destino") or option.get("destination_key")
        scene = self.content.scene(destination) if destination else None
        if scene:
            self.render_scene(scene)
            if outcome:
                self.narrative.append(f"\n\n<b>{html.escape(outcome)}</b>")
        else:
            self._start_exploration("O caminho deixa de seguir uma cena fixa. A exploração livre começa.")
            if outcome:
                self.narrative.append(f"\n\n<b>{html.escape(outcome)}</b>")
        self.stats.update_session(self.session)
        self.session_changed.emit(self.session)

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

    def _apply_effects(self, effects: list[dict] | None) -> None:
        for effect in effects or []:
            kind = effect.get("tipo")
            value = effect.get("valor")
            if kind == "flag" and value:
                self.session.flags.add(str(value))
            elif kind == "remover_flag" and value:
                self.session.flags.discard(str(value))
            elif kind == "item" and value:
                self.session.inventory.append(str(value))
            elif kind == "dano":
                self.session.life = max(0, self.session.life - int(value or 0))
            elif kind == "cura":
                self.session.life = min(self.session.life_max, self.session.life + int(value or 0))
            elif kind in {"energia", "fome", "sede"}:
                current = getattr(self.session, kind)
                setattr(self.session, kind, max(0, min(100, current + int(value or 0))))
            elif kind == "temperatura":
                self.session.temperature = max(-100, min(100, self.session.temperature + int(value or 0)))
            elif kind == "xp":
                self.session.xp += int(value or 0)
            elif kind == "tempo":
                self.session.hour += int(value or 0)
                while self.session.hour >= 24:
                    self.session.hour -= 24
                    self.session.day += 1
            elif kind == "reputacao":
                faction = effect.get("faccao", "desconhecida")
                current = self.session.reputation.get(faction, 50)
                self.session.reputation[faction] = max(0, min(100, current + int(value or 0)))

    def _start_exploration(self, opening: str) -> None:
        self.title.setText(f"Exploração — {self.session.region_name}")
        self.narrative.setPlainText(opening + "\n\nO ambiente não avança sozinho: caminhar, escutar, procurar e descansar são decisões separadas.")
        self._render_exploration_buttons()

    def _render_exploration_buttons(self) -> None:
        clear_layout(self.options)
        grid = QGridLayout()
        directions = (("NORTE", "norte", 0, 1), ("OESTE", "oeste", 1, 0), ("LESTE", "leste", 1, 2), ("SUL", "sul", 2, 1))
        for text, direction, row, column in directions:
            button = QPushButton(f"CAMINHAR PARA {text}")
            button.clicked.connect(lambda _checked=False, selected=direction: self._travel(selected))
            grid.addWidget(button, row, column)
        self.options.addLayout(grid)
        support = QHBoxLayout()
        for text, action in (("ESCUTAR", "listen"), ("PROCURAR RECURSOS", "search"), ("MONTAR ABRIGO", "shelter"), ("ROLAR D20", "d20")):
            button = QPushButton(text)
            button.clicked.connect(lambda _checked=False, selected=action: self._support_action(selected))
            support.addWidget(button)
        self.options.addLayout(support)

    def _travel(self, direction: str) -> None:
        result = self.session.travel(direction)
        self.narrative.append(
            f"\n\n<b>Caminhada para {html.escape(direction.title())} — D20: {result['roll']}</b>"
            f"<br>{html.escape(result['event'])}"
        )
        self.stats.update_session(self.session)
        self.session_changed.emit(self.session)

    def _support_action(self, action: str) -> None:
        roll, label = self.session.roll_d20()
        if action == "d20":
            text = f"O dado mostra {roll}: {label}. Nenhuma ação foi consumida."
        elif action == "listen":
            text = "Você interrompe a marcha e escuta por vários minutos. " + (
                "Há deslocamento consciente além do alcance da visão." if roll >= 11 else "O ambiente não revela uma origem clara para os ruídos."
            )
        elif action == "search":
            self.session.energy = max(0, self.session.energy - 3)
            if roll >= 10:
                found = random.choice(("fibra resistente", "erva desconhecida", "pedra útil", "água coletada", "madeira seca"))
                self.session.inventory.append(found)
                text = f"Depois de uma busca cuidadosa, você encontra {found}."
            else:
                text = "A procura consome energia, mas nada seguro pode ser recolhido."
        else:
            self.session.energy = max(0, self.session.energy - 5)
            if roll >= 10:
                self.session.temperature = max(-100, min(100, self.session.temperature + (10 if self.session.region_slug == 'frostreach' else -3)))
                text = "O abrigo improvisado fica estável. A exposição ambiental diminui."
            else:
                text = "O terreno e o clima vencem a tentativa. Será preciso buscar outro ponto."
        self.narrative.append(f"\n\n<b>Ação — D20: {roll}</b><br>{html.escape(text)}")
        self.stats.update_session(self.session)
        self.session_changed.emit(self.session)


class ContinuePage(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(42, 34, 42, 34)
        title = QLabel("Personagens salvos")
        title.setObjectName("SectionTitle")
        root.addWidget(title)
        self.message = QLabel("Conecte o MySQL para consultar os personagens.")
        root.addWidget(self.message)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(("ID", "Nome", "Raça", "Cena", "Criado em"))
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.table)

    def set_saves(self, records: list[dict]) -> None:
        self.table.setRowCount(len(records))
        for row_index, row in enumerate(records):
            values = (row.get("id"), row.get("name"), row.get("race"), row.get("current_scene_key"), row.get("created_at"))
            for column, value in enumerate(values):
                self.table.setItem(row_index, column, QTableWidgetItem(str(value or "")))
        self.message.setText(f"{len(records)} personagem(ns) encontrado(s). O salvamento completo de atributos entra na próxima etapa.")


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
        self.codex = CodexPage()
        self.database_page = DatabasePage(settings)
        self.pages = {
            "home": self.home, "new_game": self.new_game, "game": self.game,
            "continue": self.continue_page, "codex": self.codex, "database": self.database_page,
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

        self.home.navigate.connect(self.navigate)
        self.database_page.connect_requested.connect(self.connect_database)
        self.new_game.start_requested.connect(self.start_game)
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
        for text, destination in (("Início","home"),("Novo jogo","new_game"),("Continuar","continue"),("Jornada atual","game"),("Codex","codex"),("MySQL","database")):
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
        counts = self.repository.counts() if result.ok else None
        if result.ok:
            settings.salvar(self.paths.arquivo_configuracao)
            self.sidebar_status.setText("● MySQL conectado")
            self.sidebar_status.setObjectName("StatusGood")
            try:
                races = self.repository.races()
                if races:
                    self.new_game.set_races(races)
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

