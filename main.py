# main.py

# imports
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon
from window import Window

def main():
    app = QApplication()

    QApplication.setQuitOnLastWindowClosed(False)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray not available.")
        sys.exit(1)

    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
