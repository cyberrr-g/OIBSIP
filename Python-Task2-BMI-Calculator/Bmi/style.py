APP_STYLESHEET = """
QMainWindow {
    background-color: #f5f6fa;
}
QWidget {
    background-color: #f5f6fa;
    color: #2f3640;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 12px;
}
#Title {
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
    padding: 8px;
}
#SectionTitle {
    font-size: 14px;
    font-weight: bold;
    color: #2c3e50;
    padding-top: 10px;
}
QLabel#FieldLabel {
    font-weight: bold;
    color: #34495e;
}
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #dcdde1;
    border-radius: 6px;
    padding: 7px 9px;
}
QLineEdit:focus {
    border: 1px solid #3498db;
}
#Card {
    background-color: #ffffff;
    border: 1px solid #dcdde1;
    border-radius: 8px;
    padding: 10px;
}
QPushButton {
    background-color: #3498db;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 9px 18px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2980b9;
}
QPushButton:pressed {
    background-color: #21618c;
}
QPushButton#SecondaryBtn {
    background-color: #bdc3c7;
    color: #2f3640;
}
QPushButton#SecondaryBtn:hover {
    background-color: #aab2b8;
}
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #dcdde1;
    border-radius: 6px;
    gridline-color: #e8eaed;
}
QHeaderView::section {
    background-color: #2c3e50;
    color: #ffffff;
    padding: 7px;
    border: none;
    font-weight: bold;
}
QTableWidget::item {
    padding: 5px;
}
QTableWidget::item:selected {
    background-color: #d6eaf8;
    color: #2c3e50;
}
"""
