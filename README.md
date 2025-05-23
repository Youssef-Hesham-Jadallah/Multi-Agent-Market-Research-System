# 📊 Multi-Agent Market Research System: AI/ML Jobs in MENA

Welcome to the official repository for the **Multi-Agent Market Intelligence System**, a smart, autonomous tool built to explore and analyze AI/ML job trends across the MENA region.

> **Objective**: Automate the discovery, extraction, and reporting of the most in-demand AI/ML jobs using a modular multi-agent architecture.

---

## 🚀 Features

- 🔍 **Web Search Agent** — Scrapes job platforms like LinkedIn for live job postings.
- 🧠 **Data Extraction Agent** — Parses and cleans raw job data, identifying titles, skills, and locations.
- 📈 **Trend Analysis Agent** — Analyzes trends across skills, titles, and geographic distribution.
- 📝 **Report Writer Agent** — Generates a polished PDF report with insights and charts.
- 📦 Modular architecture, fully extensible, production-ready.

---

## 🧩 Project Structure
```bash
multi-agent-ai-ml-jobs-mena/
├── agents/                    # Core agents for scraping, extraction, analysis, reporting
├── data/                      # Stores raw and processed job data
├── reports/                   # Final report output (PDF)
├── utils/                     # Helper functions (regex, location normalization, etc.)
├── main.py                    # Pipeline orchestration script
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview and usage
```

---

## 🛠️ Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/multi-agent-ai-ml-jobs-mena.git
cd multi-agent-ai-ml-jobs-mena
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the system
```bash
python main.py
```
> Output: A PDF report will be generated in the `reports/` folder.

---

## 📄 Sample Output
- 📘 `Top AI/ML Jobs in MENA – May 2025.pdf`
- Contains:
  - Top 10 job titles
  - Key skills distribution
  - Location-based job counts
  - Summary insights

---

## 📌 To-Do
- [ ] Add .gitignore and LICENSE
- [ ] Support additional job platforms (e.g., Bayt, Wuzzuf)
- [ ] Streamlit dashboard for real-time exploration

---

## 📜 License
You can add an open-source license of your choice (MIT, Apache 2.0, etc.).

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---


