import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import create_main_window

def main():
    app = QApplication(sys.argv)
    
    # Load and apply stylesheet
    with open('src/ui/styles.qss', 'r') as f:
        app.setStyleSheet(f.read())
    
    window = create_main_window()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()