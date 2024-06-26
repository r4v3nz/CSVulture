# CSVulture

This simple Python project allows users to load a massive CSV file, select specific columns to save, and rename those columns before saving them as a new CSV file. It uses the `polars` library for handling CSV data and `tkinter` for the graphical user interface.

![Logo](assets/CSVulture.png)

## Features

- Load a massive CSV file and display its columns.
- Select columns to save to a new CSV file.
- Rename selected columns.

## Requirements

- Python 3.x

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/r4v3nz/CSVulture.git
   cd CSVulture
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```bash
   python app.py
   ```

2. Use the file dialog to select a CSV file to load.

3. Select the columns you want to save by checking the checkboxes next to each column name.

4. Enter new names for the selected columns in the text fields.

5. Click the "Save" button to choose a location to save the new CSV file.
