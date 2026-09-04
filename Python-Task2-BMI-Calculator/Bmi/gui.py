from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from .calc import calc_bmi, classify_bmi, CATEGORY_COLORS
from .storage import save_record, fetch_records


class BMICalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        self.resize(760, 720)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        title = QLabel("BMI Calculator")
        title.setObjectName("Title")
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        input_widget = QWidget()
        input_widget.setObjectName("Card")
        grid = QGridLayout(input_widget)

        name_label = QLabel("Name:")
        name_label.setObjectName("FieldLabel")
        grid.addWidget(name_label, 0, 0)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter your name")
        grid.addWidget(self.name_edit, 0, 1)

        weight_label = QLabel("Weight (kg):")
        weight_label.setObjectName("FieldLabel")
        grid.addWidget(weight_label, 1, 0)
        self.weight_edit = QLineEdit()
        self.weight_edit.setPlaceholderText("e.g. 70")
        grid.addWidget(self.weight_edit, 1, 1)

        height_label = QLabel("Height (cm):")
        height_label.setObjectName("FieldLabel")
        grid.addWidget(height_label, 2, 0)
        self.height_edit = QLineEdit()
        self.height_edit.setPlaceholderText("e.g. 175")
        grid.addWidget(self.height_edit, 2, 1)

        grid.setColumnStretch(1, 1)
        main_layout.addWidget(input_widget)

        btn_row = QHBoxLayout()
        self.calc_btn = QPushButton("Calculate BMI")
        self.calc_btn.clicked.connect(self.calculate)
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("SecondaryBtn")
        clear_btn.clicked.connect(self.clear)
        btn_row.addWidget(self.calc_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        main_layout.addLayout(btn_row)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.category_label = QLabel("")
        self.category_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.category_label, alignment=Qt.AlignCenter)

        history_title = QLabel("History")
        history_title.setObjectName("SectionTitle")
        main_layout.addWidget(history_title)

        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Filter by name:"))
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("All users")
        self.filter_edit.setFixedWidth(160)
        filter_row.addWidget(self.filter_edit)
        load_btn = QPushButton("Load")
        load_btn.clicked.connect(self.load_history)
        filter_row.addWidget(load_btn)
        filter_row.addStretch()
        main_layout.addLayout(filter_row)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Name", "Weight", "Height (cm)", "BMI", "Category", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        self.load_history()

    def show_error(self, msg):
        QMessageBox.critical(self, "Input Error", msg)

    def validate_inputs(self):
        name = self.name_edit.text().strip()
        if not name:
            self.show_error("Please enter a name.")
            return None

        try:
            weight = float(self.weight_edit.text().strip())
        except ValueError:
            self.show_error("Weight must be a numeric value.")
            return None
        if weight <= 0:
            self.show_error("Weight must be a positive number.")
            return None

        try:
            height = float(self.height_edit.text().strip())
        except ValueError:
            self.show_error("Height must be a numeric value.")
            return None
        if height <= 0:
            self.show_error("Height must be a positive number.")
            return None
        if height < 50 or height > 300:
            self.show_error("Height must be between 50 cm and 300 cm.")
            return None

        return name, weight, height

    def calculate(self):
        result = self.validate_inputs()
        if not result:
            return

        name, weight, height = result
        bmi = calc_bmi(weight, height)
        category = classify_bmi(bmi)

        self.result_label.setText(f"BMI: {bmi:.2f}")
        color = CATEGORY_COLORS.get(category, "#000000")
        self.category_label.setText(f"Category: {category}")
        self.category_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color};")

        save_record(name, weight, height, bmi, category)
        self.load_history()

    def clear(self):
        self.name_edit.clear()
        self.weight_edit.clear()
        self.height_edit.clear()
        self.result_label.setText("")
        self.category_label.setText("")