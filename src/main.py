import sys
from PyQt6.QtWidgets import QApplication
from game.menu_window import MenuWindow
from styling.colours import *

def main():
    app = QApplication(sys.argv)

    # Load and apply stylesheet
    with open("src/styling/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    menu = MenuWindow()
    menu.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
