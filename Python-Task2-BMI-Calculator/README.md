# BMI Calculator

A desktop BMI (Body Mass Index) Calculator application built with Python and PyQt5. Calculate your BMI, get instant health category feedback, and maintain a history of your measurements.

## Features

- **Instant BMI Calculation** — Enter your weight (kg) and height (cm) to calculate BMI instantly
- **Health Category Classification** — Automatically classifies BMI into:
  - **Underweight** — BMI < 18.5
  - **Normal** — BMI 18.5–24.9
  - **Overweight** — BMI 25–29.9
  - **Obese** — BMI ≥ 30
- **Color-Coded Results** — Categories displayed with intuitive color coding
- **History Tracking** — All records saved to SQLite database and CSV file
- **Filter History** — Search and filter past records by name
- **Input Validation** — Validates all inputs with descriptive error messages
- **Modern UI** — Clean, styled interface with a card-based layout

## Project Structure

```
Python-Task2-BMI-Calculator/
├── main.py              # Application entry point
├── Bmi/
│   ├── __pycache__/
│   ├── calc.py          # BMI calculation and classification logic
│   ├── gui.py           # PyQt5 GUI (main window, inputs, table)
│   ├── storage.py       # SQLite + CSV storage operations
│   └── style.py         # Application stylesheet (QSS)
├── bmi_records.db       # SQLite database (auto-created)
├── bmi_records.csv      # CSV export of records (auto-created)
└── README.md
```

## Prerequisites

- Python 3.6+
- PyQt5

## Installation

```bash
pip install PyQt5
```

## Usage

```bash
python main.py
```

1. Enter your **name**, **weight (kg)**, and **height (cm)**
2. Click **Calculate BMI** to see your result
3. View your history in the table below
4. Use the **Filter by name** field and **Load** button to search records

## BMI Categories

| Category    | BMI Range    | Color  |
|-------------|--------------|--------|
| Underweight | < 18.5       | Blue   |
| Normal      | 18.5 – 24.9  | Green  |
| Overweight  | 25 – 29.9    | Orange |
| Obese       | ≥ 30         | Red    |

## Data Storage

Records are saved in two formats:

- **SQLite Database** (`bmi_records.db`) — Primary storage for the history table
- **CSV File** (`bmi_records.csv`) — Portable export for external use

## License

This project is part of the OIBSIP (Oasis Infobyte) Python Task Series.
