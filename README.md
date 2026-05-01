# 🗂️ Smart Task Manager

A simple and clean task management web app built with **Python** and **Streamlit**. Add tasks with a date and time, mark them as done, and delete them — all in a clean UI.

---

## 🚀 Features

- Add tasks with a **name**, **date**, and **time**
- Supports multiple date/time formats (e.g. `YYYY-MM-DD`, `DD/MM/YYYY`, 12-hour and 24-hour time)
- Prevents adding tasks in the **past**
- Mark tasks as **Done** ✔
- **Delete** tasks instantly
- Displays **current date & time** in the header
- State is preserved across interactions using Streamlit session state

---

## 🖥️ Demo

> Run locally — see setup instructions below.

---

## 📦 Requirements

- Python 3.8+
- Streamlit

Install dependencies:

```bash
pip install streamlit
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
smart-task-manager/
│
├── app.py          # Main Streamlit application
└── README.md       # Project documentation
```

---

## 📅 Supported Date & Time Formats

| Date Format     | Time Format   | Example                    |
|-----------------|---------------|----------------------------|
| `YYYY-MM-DD`    | `HH:MM`       | `2025-12-31 18:30`         |
| `DD/MM/YYYY`    | `HH:MM`       | `31/12/2025 18:30`         |
| `YYYY-MM-DD`    | `HH:MM AM/PM` | `2025-12-31 06:30 PM`      |
| `DD/MM/YYYY`    | `HH:MM AM/PM` | `31/12/2025 06:30 PM`      |

---

## 🛠️ Built With

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
