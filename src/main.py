import sys
from PyQt6.QtWidgets import QApplication
from game.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Load and apply stylesheet
    with open('src/styling/styles.qss', 'r') as f:
        app.setStyleSheet(f.read())
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()