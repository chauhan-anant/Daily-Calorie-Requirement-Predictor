# 🔥 Daily Calorie Requirement Predictor

A simple web app built with **Streamlit** that predicts a person's **Daily Calorie Requirement** based on their personal details, activity level, and lifestyle habits — using a trained **Linear Regression** machine learning model.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Input Fields](#input-fields)
- [How It Works](#how-it-works)
- [Model Details](#model-details)
- [Encoding Notes (Important)](#encoding-notes-important)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)
- [Disclaimer](#disclaimer)

---

## Overview

This app takes in a user's:

- Age
- Gender
- Height
- Weight
- Activity Level
- Sleep Hours
- Water Intake
- Goal (weight loss / gain / maintenance)
- Diet Type

...and predicts the **estimated daily calorie requirement (kcal/day)** using a pre-trained Linear Regression model (`Model.pkl`).

---

## Features

- ✅ Clean, simple web interface (no coding needed to use it)
- ✅ Instant calorie prediction on button click
- ✅ Model loading with error handling (checks if file exists, is valid, etc.)
- ✅ Easy to customize inputs, ranges, and encoding logic
- ✅ Works fully offline once dependencies are installed

---

## Project Structure

```
Ca/
│
├── app.py           # Main Streamlit application
├── Model.pkl        # Pre-trained Linear Regression model (joblib format)
└── README.md        # This file
```

> ⚠️ Both `app.py` and `Model.pkl` **must be in the same folder** for the app to work.

---

## Requirements

- Python 3.8 or higher
- Libraries:
  - `streamlit`
  - `numpy`
  - `joblib`
  - `scikit-learn` (needed internally to unpickle the model)

---

## Installation

1. **Clone or download** this project folder to your computer.

2. **Install the required libraries** by running this command in your terminal / command prompt:

   ```bash
   pip install streamlit numpy joblib scikit-learn
   ```

3. Make sure `Model.pkl` is present in the same folder as `app.py`.

---

## Running the App

Open a terminal in the project folder and run:

```bash
streamlit run app.py
```

This will automatically open the app in your default web browser at:

```
http://localhost:8501
```

---

## Input Fields

| Field | Description | Type |
|---|---|---|
| **Age** | Age in years | Number (1–100) |
| **Gender** | Male / Female | Dropdown |
| **Height_cm** | Height in centimeters | Number (50–250) |
| **Weight_kg** | Weight in kilograms | Number (20–250) |
| **Activity_Level** | Sedentary / Lightly Active / Moderately Active / Very Active / Extra Active | Dropdown |
| **Sleep_Hours** | Average hours of sleep per day | Number (0–24) |
| **Water_Intake_L** | Daily water intake in liters | Number (0–10) |
| **Goal** | Weight Loss / Maintain Weight / Weight Gain | Dropdown |
| **Diet_Type** | Vegetarian / Non-Vegetarian / Vegan / Eggetarian | Dropdown |

After filling these in, click **"Calculate Calorie Requirement"** to see the prediction.

---

## How It Works

1. The app loads the trained model (`Model.pkl`) once at startup using `joblib.load()`, cached via `@st.cache_resource` so it doesn't reload on every interaction.
2. User inputs are collected through Streamlit widgets (number inputs and dropdowns).
3. Categorical fields (Gender, Activity_Level, Goal, Diet_Type) are converted into numbers using fixed mapping dictionaries, since the ML model only understands numeric input.
4. All 9 values are arranged into a single row, in the **exact same order** the model was trained on:

   ```
   Age, Gender, Height_cm, Weight_kg, Activity_Level,
   Sleep_Hours, Water_Intake_L, Goal, Diet_Type
   ```

5. This row is passed to `model.predict()`, and the resulting number is displayed as the estimated daily calorie requirement.

---

## Model Details

- **Model type:** `sklearn.linear_model.LinearRegression`
- **Number of input features:** 9
- **Saved using:** `joblib.dump(model, "Model.pkl")`
- **Feature names:** Not stored in the model file — the model only relies on the **order** of input values, not their names. This is why keeping the input order consistent with training is critical.

---

## Encoding Notes (Important)

Since the model does not store feature names or category mappings, the app uses **alphabetical order encoding** for categorical fields (this is the default behavior of scikit-learn's `LabelEncoder`):

```python
gender_map = {"Female": 0, "Male": 1}

activity_map = {
    "Extra Active": 0,
    "Lightly Active": 1,
    "Moderately Active": 2,
    "Sedentary": 3,
    "Very Active": 4
}

goal_map = {
    "Maintain Weight": 0,
    "Weight Gain": 1,
    "Weight Loss": 2
}

diet_map = {
    "Eggetarian": 0,
    "Non-Vegetarian": 1,
    "Vegan": 2,
    "Vegetarian": 3
}
```

> ⚠️ **If predictions look unusually high, low, or incorrect**, it likely means the categorical encoding used during model training was different from the above (e.g., manually assigned numbers instead of alphabetical order).
>
> **To fix this:** Check your original training notebook/script for how `LabelEncoder` or manual mapping was applied — for example, print:
> ```python
> print(list(le.classes_))
> ```
> Then update the mapping dictionaries in `app.py` to match exactly.

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---|---|---|
| `FileNotFoundError: Model.pkl` | File not in the same folder as `app.py` | Move `Model.pkl` next to `app.py` |
| `pickle.UnpicklingError: invalid load key` | File is corrupted or was saved with `joblib` but loaded with `pickle` | Re-save/re-download the file; app already uses `joblib.load()` which matches how the model was saved |
| Predictions look wrong/unrealistic | Categorical encoding mismatch with training | Match the mapping dictionaries to your training encoding (see above) |
| `InconsistentVersionWarning` on load | Model trained with a different scikit-learn version than installed | Safe to ignore for most cases, but for best results install the same scikit-learn version used during training |
| App won't start / `ModuleNotFoundError` | Missing library | Run `pip install streamlit numpy joblib scikit-learn` |

---

## Customization

- **Change input ranges:** Edit the `min_value` / `max_value` / `value` parameters in the `st.number_input()` calls in `app.py`.
- **Add more activity/goal/diet options:** Update both the `st.selectbox()` list and the corresponding mapping dictionary — keep them in sync.
- **Change the model file name:** Update the `MODEL_PATH` variable at the top of `app.py`.
- **Style the app:** Streamlit supports custom themes via a `.streamlit/config.toml` file if you want to change colors/fonts.

---

## Disclaimer

This app provides an **estimated** calorie requirement based on a simple linear regression model and general inputs. It is intended for **informational purposes only** and should not replace advice from a certified nutritionist, dietitian, or medical professional.

---

*Built with ❤️ using Python & Streamlit.*
