## 🎓 Project Details

- **Course:** Artificial Intelligence (AI)
- **Project Title:** AI Quiz & Exam Generator System
- **Deadline:** May 19, 2026
- **Status:** Complete & Working


# AI Quiz & Exam Generator System 🎓

A professional, production-ready web application built with **Python**, **Streamlit**, and the **Google Gemini API** (`google-genai` SDK). This system allows educators, students, and trainers to instantly transform study materials—such as PDF documents or raw text—into custom, structured examinations.

---

## 🌟 Key Features

- **Multi-Format Ingestion**: Upload PDF/TXT documents or paste plain text directly.
- **Dynamic Exam Customization**:
  - **Difficulty Levels**: Easy, Medium, or Hard.
  - **Flexible Question Types**: Select from Multiple Choice (MCQs), True/False, and Short Answer questions.
  - **Adjustable Volume**: Generate up to 30 questions at once.
- **Structured JSON Outputs**: Leverages Gemini’s structured output schema to guarantee clean, valid questions, options, and explanations.
- **Interactive Exam UI**: Review generated questions, select answers, and toggle detailed explanations & correct answer keys.
- **Professional PDF Export**: Instantly export a formatted, print-ready exam PDF that contains the questions on the front pages and a dedicated **Answer Key & Explanation Sheet** at the end.
- **Premium User Interface**: Dark-mode SaaS aesthetic with custom styling, hover transitions, and glowing micro-animations.

---

## 📁 Repository Structure

```text
├── app.py              # Main Streamlit web application (UI and state management)
├── ai_engine.py        # Gemini API client integration & schema definitions
├── pdf_processor.py    # Extracts raw text from uploaded PDF/TXT files using PyPDF
├── pdf_exporter.py     # Renders a print-ready PDF exam using ReportLab
├── requirements.txt    # List of project dependencies
└── .gitignore          # Files ignored by Git (caches, environment files)
```

---

## ⚙️ Installation & How to Run

Follow these steps to run the application locally:

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd "Ai Quiz And Exam Generator System"
```

### 2. Create a Virtual Environment
It is highly recommended to use a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key
To run the app, you need a Gemini API Key from Google AI Studio. 

1. Open `app.py`.
2. Locate the API Key variable at line 9:
   ```python
   GEMINI_API_KEY = "YOUR_API_KEY_HERE"
   ```
3. Replace the placeholder with your actual API key.

> [!WARNING]
> **API Key Security Warning:** Never commit your actual API key to a public GitHub repository. Secret scanners will automatically detect it and revoke it. Instead, you can load it from a safe place or enter it dynamically.

### 5. Launch the Streamlit App
Start the local server:
```bash
streamlit run app.py
```
This will launch the app in your default browser at `http://localhost:8501`.

---

## 👥 Group Members ( Group Three )
1. Hamse aadan mohamed 
2. Sacad hariir ahmed 
3. Hamse ismail iman 
4. Cabdifataax daahir adan 
5. Khadiir mahamuud mahamed
6. Mahamed abdiqaadir mohamed
7. Cabdi casiis  cali barre 
8. Cabdirisaaq mohamed ahmed 
9. Mahamed muuse muhumed 
10. Cabdale cismaan ahmed


*(Note: Please edit this table in the repository to fill in your group's details.)*

---

## 📸 Screenshots & Demos

<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/f9caab70-c4e3-4188-aa4a-36591accb93d" />
<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/a1c09db1-bbd0-4ce2-ae43-d8214fa26f54" />


https://github.com/user-attachments/assets/0c4b5935-7142-420d-b65e-8a6e1bd78377








### 🖥️ Main Dashboard Interface
<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/f9caab70-c4e3-4188-aa4a-36591accb93d" />

### 📄 Exported PDF Exam Example
<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/9ae7e071-bbf3-41ca-b291-c40998db25c6" />
<img width="1920" height="1032" alt="Screenshot 2026-05-19 141423" src="https://github.com/user-attachments/assets/3c9d3040-09dd-49dc-b63a-402d2158266b" />
<img width="1920" height="1032" alt="Screenshot 2026-05-19 141417" src="https://github.com/user-attachments/assets/5b268cfa-1b82-4ac5-a634-f80a57f328d9" />
<img width="1920" height="1032" alt="Screenshot 2026-05-19 141426" src="https://github.com/user-attachments/assets/5e523804-540d-44a9-9778-aca1f6ecca47" />
<img width="1920" height="1032" alt="Screenshot 2026-05-19 141413" src="https://github.com/user-attachments/assets/d39d8c6b-af9d-4a9d-a47f-698f39c25806" />


---


