"""Ponto de entrada da interface desktop de Aetheria."""
from __future__ import annotations

import sys
from pathlib import Path

PASTA_SOFTWARE = Path(__file__).resolve().parent
if str(PASTA_SOFTWARE) not in sys.path:
    sys.path.insert(0, str(PASTA_SOFTWARE))


def main() -> int:
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("PySide6 não está instalado.")
        print("Execute: py -m pip install -r requirements.txt")
        return 1

    from aetheria_app.config import AppPaths, DatabaseSettings
    from aetheria_app.ui import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("Aetheria")
    app.setOrganizationName("Aetheria RPG")
    app.setStyle("Fusion")
    paths = AppPaths.detectar(PASTA_SOFTWARE)
    settings = DatabaseSettings.carregar(paths.arquivo_configuracao)
    janela = MainWindow(paths, settings)
    janela.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
