import sys
from PyQt6.QtWidgets import QApplication
from game.ui.menu_window import MenuWindow
from styling.colours import *
from game.data import database

def main():
    app = QApplication(sys.argv)

    # Load and apply stylesheet
    with open("src/styling/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    database.initialize_database()

    # database.clear_leaderboard()


    menu = MenuWindow()
    menu.showFullScreen()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
