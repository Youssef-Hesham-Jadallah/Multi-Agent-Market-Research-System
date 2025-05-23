# 🤖 Multi-Agent AI/ML Market Research System (MENA)

Welcome to the **Multi-Agent Intelligence System** — a smart, modular framework for autonomous market research on AI/ML job trends across the MENA region.

---

## 🌟 Project Objective

To autonomously analyze the job market for AI/ML roles in MENA by:
- Scraping online job platforms
- Extracting roles, skills, and locations
- Analyzing demand trends
- Generating a PDF report & interactive dashboard

---

## 🧠 Architecture Overview

This system is made up of four collaborative agents:

| Agent | Description |
|-------|-------------|
| 🔍 **WebSearchAgent** | Scrapes job listings from platforms like LinkedIn |
| 🧾 **DataExtractionAgent** | Extracts and cleans job title, company, skills, location |
| 📊 **TrendAnalysisAgent** | Analyzes most in-demand titles, skills, and locations |
| 📝 **ReportWriterAgent** | Generates a professional PDF report with insights and visualizations |

---

## 🗂️ Project Structure

```bash
multi-agent-ai-ml-jobs-mena/
├── agents/                    # Core agents (modular)
├── utils/                     # Visualization & NLP helpers
├── data/                      # Raw and processed job data
├── reports/                   # Final report PDF
├── visuals/                   # Auto-generated charts
├── dashboard.py               # Streamlit dashboard app
├── main.py                    # System runner
├── README.md
```

---

## ⚙️ How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Full Pipeline
```bash
python main.py
```

### 3. Launch the Dashboard
```bash
streamlit run dashboard.py
```

---

## 📈 Outputs

- ✅ Raw job listings (JSON)
- ✅ Cleaned + structured job data
- ✅ Trend insights (skills, titles, locations)
- ✅ PDF Report
- ✅ Interactive Dashboard

---

## 📌 Future Enhancements
- [ ] Multi-platform scraping (Bayt, Wuzzuf, Glassdoor)
- [ ] Auto-refresh cronjob
- [ ] Keyword-based search filter
- [ ] Arabic language support

---

## 👨‍💼 Author

- Developed by **Youssef Hesham Jad-allah**
- [GitHub](https://github.com/Youssef-Hesham-Jadallah) | [LinkedIn](www.linkedin.com/in/youssef-hesham-jadallah-435906298)

---

