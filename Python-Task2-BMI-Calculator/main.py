import sys


def main():
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLESHEET)
    window = BMICalculatorWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
