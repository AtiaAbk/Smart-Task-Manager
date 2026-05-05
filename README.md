# Smart Task Manager

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

A lightweight, intuitive task management web application built with **Python** and **Streamlit**. Manage your daily tasks with real-time scheduling, flexible date/time input, and a clean, responsive interface — all running locally with zero configuration.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Date & Time Formats](#supported-date--time-formats)
- [Built With](#built-with)
- [Author](#author)
- [License](#license)

---

## Overview

Smart Task Manager is a single-file Streamlit application designed for simplicity and productivity. It allows users to create time-stamped tasks, track their completion status, and manage their schedule — all within a clean browser-based UI. Session state ensures that tasks persist seamlessly across interactions without any database setup.

---

## Features

- **Task Scheduling** — Add tasks with a name, date, and time
- **Flexible Input Formats** — Supports multiple date and time formats (12-hour and 24-hour)
- **Past Date Prevention** — Automatically blocks scheduling tasks in the past
- **Task Completion** — Mark tasks as Done with a single click
- **Instant Deletion** — Remove tasks immediately from the list
- **Live Clock** — Displays the current date and time in the header
- **Persistent State** — Tasks are preserved across interactions using Streamlit session state

---

## Project Structure

```
smart-task-manager/
│
├── app.py          # Main Streamlit application
└── README.md       # Project documentation
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/your-username/smart-task-manager.git
cd smart-task-manager
```

**2. (Recommended) Create and activate a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install streamlit
```

---

## Usage

Run the application with the following command:

```bash
streamlit run app.py
```

Then open your browser and navigate to:

```
http://localhost:8501
```

### Quick Start

1. Enter a **task name** in the input field
2. Provide a **date** and **time** using any supported format
3. Click **Add Task** to schedule it
4. Use the **Done** button to mark a task as complete
5. Use the **Delete** button to remove a task from the list

---

## Supported Date & Time Formats

The application accepts a variety of date and time input formats for user convenience.

| Date Format  | Time Format   | Full Example          |
|---|---|---|
| `YYYY-MM-DD` | `HH:MM`       | `2025-12-31 18:30`    |
| `DD/MM/YYYY` | `HH:MM`       | `31/12/2025 18:30`    |
| `YYYY-MM-DD` | `HH:MM AM/PM` | `2025-12-31 06:30 PM` |
| `DD/MM/YYYY` | `HH:MM AM/PM` | `31/12/2025 06:30 PM` |

> **Note:** Tasks scheduled in the past will be rejected automatically.

---

## Built With

| Technology | Purpose |
|---|---|
| [Python 3.8+](https://www.python.org/) | Core application logic |
| [Streamlit](https://streamlit.io/) | Web UI framework |

---

## Author

**Atia Sanjida**

- 📧 Email: your-email@example.com
- 🔗 LinkedIn: [linkedin.com/in/your-profile](https://www.linkedin.com/in/atia-oishe-085947233/)
- 💻 GitHub: [github.com/your-username](https://github.com/atiaabk)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

