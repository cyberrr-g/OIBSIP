import sys

from PyQt5.QtWidgets import QApplication

from Bmi.gui import BMICalculatorWindow
from Bmi.storage import init_db
from Bmi.style import APP_STYLESHEET


def main():
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLESHEET)
    window = BMICalculatorWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
