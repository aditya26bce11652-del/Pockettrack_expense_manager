# PocketTrack - Student Expense Manager

PocketTrack is a small Python project for keeping track of daily expenses. I made it as a command-line project for Python Essentials.

The idea is simple. Instead of writing down small expenses separately, the user can enter them into the program and check them later.

## Features

- Add an expense
- View saved expenses
- Search by category or description
- Update an expense
- Delete an expense
- Calculate total spending
- Show category-wise spending
- Export data to CSV
- Store data locally using SQLite

## Technologies

- Python 3
- SQLite
- CSV
- Python standard library

No external packages are required.

## Files

```text
PocketTrack/
├── main.py
└── README.md
```

When the program is run, it automatically creates `pockettrack.db`.

## How to run

Open a terminal in the project folder and run:

```bash
python main.py
```

If your computer uses `python3`, run:

```bash
python3 main.py
```

Then select an option from the menu.

## Example

An expense can look like:

```text
Date: 2026-09-29
Category: Food
Description: Lunch
Amount: 120
Payment method: UPI
```

The information is saved in the SQLite database.

The report option can show total spending and spending by category.

## CSV Export

Choose option 7 to create:

```text
pockettrack_expenses.csv
```

The CSV contains the ID, date, category, description, amount and payment method.

## Notes

The database and CSV files are generated automatically. They do not need to be created manually.

The project is intentionally command-line based and uses Python concepts such as functions, loops, conditions, exception handling, SQLite, CSV file handling and input validation.

## Learning Objective

The main purpose of PocketTrack was to combine the Python concepts learned in the course into one practical application instead of making several unrelated small programs.
