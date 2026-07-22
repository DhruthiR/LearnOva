# 🎮 LEARNOVA – The DSA Hurdle

## 📌 Overview

**LEARNOVA** is a full-stack interactive web application designed to make **Data Structures & Algorithms (DSA)** learning engaging through **gamified challenges**.

The platform provides multiple game modes like quizzes, riddles, code fixing, and logic sequencing — helping users strengthen conceptual understanding in an interactive way.

This project demonstrates strong skills in **backend API design, frontend UI development, and logical problem structuring**.

---

## 🎯 Key Features

### 🔐 Authentication System

* User Registration & Login APIs
* In-memory user management (lightweight simulation)
* Session-like behavior using backend tracking

---

### 🎮 Multiple Game Modes

* 🧩 **Mystery Match**

  * Solve riddles based on DSA concepts

* ⚡ **Rapid Recall Arena**

  * Timed MCQ-based questions

* 🚀 **Concept Rocket Launch**

  * Arrange steps in correct logical order

* 🛠️ **Fix the Code**

  * Identify missing lines in code snippets

* 🧠 **Block Identifier**

  * Fill missing concepts in structured flow

* 🎡 **Spin and Solve**

  * Random topic generator + mixed challenges

* 👑 **Boss Fight**

  * Advanced-level DSA questions

---

### 📊 Performance Tracking

* Tracks:

  * Game history
  * Attempts per topic
  * Perfect scores
* Stored using **in-memory data structures (Python dictionaries)**

---

### 🌐 Frontend UI

* Responsive UI using **HTML + Tailwind CSS**
* Interactive components:

  * Drag & drop
  * Dynamic MCQs
  * Code input areas
  * Animated transitions

---

## 🏗️ Tech Stack

| Layer       | Technology                                 |
| ----------- | ------------------------------------------ |
| Backend     | Flask (Python)                             |
| Frontend    | HTML, Tailwind CSS, JavaScript             |
| API         | REST APIs (Flask routes)                   |
| Storage     | Local Storage                              |
| Integration | CORS enabled                               |

---

## 📂 Project Structure

```
LEARNOVA/
│── app.py                # Flask backend (APIs & game logic)
│── index.html           # Frontend UI
│── requirements.txt     # Dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/learnova.git
cd learnova
```

### 2️⃣ Install Dependencies

```bash
pip install flask flask-cors
```

### 3️⃣ Run Backend

```bash
python app.py
```

### 4️⃣ Open Frontend

* Open `index.html` in browser
  OR
* Serve using Live Server (recommended)

---

## 🔌 API Endpoints

### 🔐 Authentication

* `POST /register`
* `POST /login`

### 🎮 Game Content

* `POST /generate_game_content`

---

## 🧠 Core Logic (Important for Recruiters)

* Dynamic content generation based on:

  * Game type
  * Selected DSA topic
* Structured JSON-based API responses 
* Efficient use of:

  * Dictionaries for tracking user stats
  * Conditional logic for game modes
* Modular backend handling multiple game engines

---

## 🖥️ Frontend Highlights

* Dynamic UI rendering using JavaScript 
* Drag-and-drop interaction for sequencing problems
* Real-time feedback for answers
* Game-based learning experience with animations

---

---

## 🎯 Why This Project Matters

This project showcases:

* Full-stack development skills
* REST API design
* Advanced frontend interaction
* Strong problem-solving and logic building
* Scalable architecture for EdTech platforms

---

## 👩‍💻 Author

Dhruthi R
---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!

---
