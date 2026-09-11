# 🔬 Physics Lab Graph Generator

A ready-to-run Python web app for generating Physics laboratory graphs.

## Features

- Common Physics lab experiment presets
- Custom X/Y quantities and units
- Scatter plots
- Connected-point graphs
- Automatic linear best-fit line
- Automatic slope, intercept and R²
- Reading table
- High-resolution PNG export
- PDF export
- Simple Streamlit interface

## 1. Install Python

Install Python 3.10 or newer and make sure Python is added to PATH.

## 2. Open the project

Open this folder in VS Code.

## 3. Create a virtual environment (recommended)

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can skip activation and install directly, or use Command Prompt:

```cmd
.venv\Scripts\activate
```

## 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Run the website

```powershell
python -m streamlit run app.py
```

A browser window should open automatically.

If it does not, copy the local address shown in the terminal into your browser.

## Common experiments included

- Ohm's Law (V vs I)
- Convex Lens (u vs v)
- Convex Lens (1/u vs 1/v)
- Prism (i vs δ)
- Meter Bridge (R vs l)
- Sonometer (L vs 1/f)
- Galvanometer (V vs I)
- Custom Experiment

## Important

The example readings in the app are only demonstration values. Replace them with your actual laboratory readings.

## Stop the app

Press:

```text
Ctrl + C
```

in the terminal.
