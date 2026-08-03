APP_STYLE = """
QWidget {
    background: #0d1117;
    color: #e6edf3;
    font-family: "Segoe UI";
    font-size: 14px;
}
QMainWindow { background: #080b10; }
QFrame#Sidebar { background: #111823; border-right: 1px solid #273447; }
QFrame#Card, QGroupBox {
    background: #141c27;
    border: 1px solid #2c3d52;
    border-radius: 10px;
}
QGroupBox { margin-top: 14px; padding: 14px 10px 10px; font-weight: 600; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; color: #d6b76b; }
QLabel#Title { color: #e6c873; font-size: 34px; font-weight: 700; }
QLabel#Subtitle { color: #8ea4bb; font-size: 16px; }
QLabel#SectionTitle { color: #e6c873; font-size: 23px; font-weight: 650; }
QLabel#StatusGood { color: #65d18b; font-weight: 600; }
QLabel#StatusBad { color: #ff7b72; font-weight: 600; }
QPushButton {
    background: #1f6f78;
    border: 1px solid #328d96;
    border-radius: 7px;
    padding: 10px 15px;
    color: white;
    font-weight: 600;
}
QPushButton:hover { background: #29838d; }
QPushButton:pressed { background: #16565e; }
QPushButton#NavButton { background: transparent; border: none; text-align: left; padding: 12px; color: #b8c7d9; }
QPushButton#NavButton:hover { background: #1b2736; color: #f2d989; }
QPushButton#NavButton:checked { background: #233247; color: #f2d989; border-left: 3px solid #e6c873; }
QPushButton#ChoiceButton { text-align: left; background: #182433; border-color: #344b66; padding: 12px; }
QPushButton#ChoiceButton:hover { background: #23364c; border-color: #d6b76b; }
QLineEdit, QSpinBox, QComboBox, QTableWidget, QTextBrowser, QListWidget {
    background: #0f1620;
    border: 1px solid #32445a;
    border-radius: 6px;
    padding: 8px;
    selection-background-color: #275866;
}
QComboBox QAbstractItemView { background: #16202d; selection-background-color: #275866; }
QHeaderView::section { background: #1a2635; color: #d6b76b; padding: 7px; border: none; }
QProgressBar { background: #0b1118; border: 1px solid #2c3d52; border-radius: 5px; text-align: center; min-height: 18px; }
QProgressBar::chunk { background: #2e8b72; border-radius: 4px; }
QTabWidget::pane { border: 1px solid #2c3d52; }
QTabBar::tab { background: #141c27; padding: 10px 18px; }
QTabBar::tab:selected { background: #233247; color: #e6c873; }
QScrollBar:vertical { background: #0d1117; width: 12px; }
QScrollBar::handle:vertical { background: #344b66; border-radius: 5px; min-height: 30px; }
"""
