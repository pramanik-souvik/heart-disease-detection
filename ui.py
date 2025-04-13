import tkinter as tk
from tkinter import ttk, messagebox
import requests

fields = [
    ("Age", "entry"),
    ("Sex (1 = Male, 0 = Female)", "dropdown", [0, 1]),
    ("Chest Pain Type (0-3)", "dropdown", [0, 1, 2, 3]),
    ("Resting Blood Pressure", "entry"),
    ("Cholesterol", "entry"),
    ("Fasting Blood Sugar > 120? (1 = Yes, 0 = No)", "dropdown", [0, 1]),
    ("Resting ECG", "dropdown", ["0 = Normal", "1 = ST-T abnormality", "2 = LV hypertrophy"]),
    ("Max Heart Rate Achieved", "entry"),
    ("Exercise Induced Angina", "dropdown", ["0 = No", "1 = Yes"]),
    ("Oldpeak (ST Depression)", "entry"),
    ("Slope", "dropdown", ["0 = Upsloping", "1 = Flat", "2 = Downsloping"]),
    ("Number of Major Vessels (0-3)", "dropdown", [0, 1, 2, 3]),
    ("Thalassemia", "dropdown", ["1 = Normal", "2 = Fixed defect", "3 = Reversible defect"])
]


root = tk.Tk()
root.title("Heart Disease Prediction System")
root.geometry("600x780")
root.configure(bg="#f2f2f2")
root.resizable(False, False)


tk.Label(root, text="Heart Disease Prediction", font=("Helvetica", 18, "bold"), bg="#f2f2f2", fg="#2c3e50").pack(pady=20)

form_frame = tk.Frame(root, bg="#f2f2f2")
form_frame.pack()

inputs = {}

for i, (label, input_type, *options) in enumerate(fields):
    tk.Label(form_frame, text=label + ":", anchor="w", font=("Helvetica", 11), bg="#f2f2f2")\
        .grid(row=i, column=0, padx=10, pady=8, sticky='w')

    if input_type == "entry":
        entry = tk.Entry(form_frame, font=("Helvetica", 11), width=25)
        entry.grid(row=i, column=1, padx=10, pady=8)
        inputs[label] = entry

    elif input_type == "dropdown":
        display_values = options[0]
        combo = ttk.Combobox(form_frame, values=display_values, state="readonly", font=("Helvetica", 11), width=23)
        combo.grid(row=i, column=1, padx=10, pady=8)
        combo.set(display_values[0])
        inputs[label] = combo

def predict():
    try:
        user_data = []
        for label, input_type, *opts in fields:
            val = inputs[label].get()
            if "dropdown" in input_type and "=" in str(val):
                val = val.split("=")[0].strip()
            user_data.append(float(val))

        response = requests.post("http://127.0.0.1:5000/predict", json={"features": user_data})
        result = response.json()

        if "error" in result:
            raise Exception(result["error"])

        prediction_text = "Heart Disease Detected" if result["prediction"] == 1 else "No Heart Disease"
        if result.get("probability") != "Not available":
            prediction_text += f"\nProbability: {result['probability']}"

        messagebox.showinfo("Prediction Result", prediction_text)

    except Exception as e:
        messagebox.showerror("Error", f"Prediction failed: {e}")

tk.Button(root, text="🔍 Predict", command=predict,
          font=("Helvetica", 12, "bold"), bg="#27ae60", fg="white",
          padx=12, pady=8).pack(pady=30)

root.mainloop()
