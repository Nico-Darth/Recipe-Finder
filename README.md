
# Flavor Finder

**Flavor Finder** is a desktop application that helps you discover recipes based on the ingredients you select. It is powered by the Edamam Recipe Search API.

## Features
- Select ingredients from various categories (Fruits, Vegetables, Proteins, etc.).
- Find recipes tailored to your chosen ingredients.
- Light and Dark mode theme switching.
- Easily remove selected ingredients with confirmation.
- View recipe details and open recipe URLs directly in your browser.

---

## Requirements
To run this application, you need the following installed on your system:
- **Python 3.7 or higher**
- Required Python libraries:
  - `PyQt5`
  - `requests`

---

## Setup Instructions

### Step 1: Check Python Installation
To check if Python is installed on your machine, open a terminal or command prompt and type:
```bash
python --version
```
or:
```bash
python3 --version
```

If Python is not installed, you can download it from the [official Python website](https://www.python.org/downloads/).

### Step 2: Install Dependencies
Once Python is installed, open a terminal in the directory containing the `Flavor Finder` files and run:
```bash
pip install -r requirements.txt
```
This will install all necessary dependencies, including `PyQt5` and `requests`.

---

## Running the Application

To start the application, navigate to the folder containing `main.py` and execute:
```bash
python app.py
```

---

## No Python? Download Executable
If you don't have Python installed or prefer not to install it, you can download a pre-built executable of the app. 
- **[Download Flavor Finder Executable](https://your-download-url.com)**

Simply download and run the `.exe` file—no Python setup required!

---

## Powered By
This app uses the **Edamam Recipe Search API** for fetching recipes. Learn more about Edamam at [https://developer.edamam.com](https://developer.edamam.com).

---

## Developed By
**Niels Coert**  
Feel free to reach out with feedback or suggestions!

---

### Notes
1. Internet connectivity is required for fetching recipes.

