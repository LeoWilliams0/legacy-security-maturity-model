# Legacy System Maturity & Financial Security Assessment Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/) <!-- Updated Python Version --> [![Framework](https://img.shields.io/badge/Flask-2.x-orange.svg)](https://flask.palletsprojects.com/) [![Database](https://img.shields.io/badge/SQLAlchemy-1.4+-lightgrey.svg)](https://www.sqlalchemy.org/)

A Flask-based web application implementing a bespoke maturity model to help organisations securely manage legacy information systems, especially under financial constraints.

Based on the dissertation **“A Maturity Model for Managing Legacy System Security under Financial Constraints”** (UWE Bristol, UXCFPU-30-3).

**Author:** Leo Williams (Student ID: 22073036)

---

## Table of Contents

1.  [Overview](#overview)
2.  [Key Features](#key-features)
3.  [Technology Stack](#technology-stack)
4.  [Architecture & Repository Structure](#architecture--repository-structure)
5.  [Getting Started](#getting-started)
6.  [Usage](#usage)
7.  [Limitations & Disclaimer](#limitations--disclaimer)
8.  [Future Enhancements](#future-enhancements)
9.  [Contributing](#contributing)
10. [License](#license)
11. [Acknowledgements](#acknowledgements)
12. [Contact](#contact)

---

## Overview

Critical legacy systems often pose significant security risks, yet organisations face challenges in modernising them due to operational dependencies and financial limitations. Existing frameworks provide limited guidance for prioritising security investments under these conditions.

This project introduces a bespoke maturity model and a prototype tool that integrates:

1.  **Cybersecurity Maturity Assessment:** Evaluating practices across Security Controls, Operational Performance, Governance & Compliance, and Technical Debt.
2.  **Financial Context Assessment:** Capturing organisational financial data like security budgets, potential breach costs, and insurance status.
3.  **Context-Aware Recommendations:** Generating prioritised, actionable security recommendations influenced by both the maturity assessment results and the organisation's financial posture.

The goal is to provide a structured, financially-informed approach to help resource-constrained organisations make better decisions about managing and securing their vital legacy systems.

---

## Key Features

- **Legacy System Management:** Register, view, edit, and delete legacy system profiles.
- **Multi-Dimension Maturity Assessment:** Guided questionnaire covering 5 key dimensions (Security Controls, Financial Viability, Operational Performance, Governance & Compliance, Technical Debt & Maintenance - 25 questions total).
- **Weighted Scoring:** Calculates scores (0-100) for each dimension using predefined weights reflecting question importance.
- **Overall Maturity Level:** Determines an overall maturity level (1-5: Ad Hoc to Optimised) based on dimension scores.
- **Financial Security Assessment:** Dedicated form to capture organisation-wide financial metrics relevant to security risk.
- **Financial Score Calculation:** Prototype calculation providing an indicator of financial readiness against potential risks.
- **Prioritised Recommendations Engine:** Generates Critical, High, Medium, and Low priority recommendations based on maturity scores and financial context adjustments. Includes estimated qualitative costs ('Low', 'Medium', 'High').
- **Implementation Guidance:** Suggests a phased implementation timeline based on recommendation priority.
- **Assessment History & Comparison:** View past assessments for a system and compare scores side-by-side (Radar Chart visualization).
- **Financial Assessment History & Comparison:** View and compare historical financial assessment snapshots with change indicators.
- **Interactive Dashboard:** Summarizes registered systems, latest assessment scores, and financial posture with key metrics.
- **Data Export:** Generate PDF and CSV reports for:
  - Maturity Assessment Scores
  - Detailed Reports (Scores + Financial Context + Recommendations)
  - Financial Assessment Details
  - Combined Data (Maturity + Financial + Recommendations)
- **Informational Pages:** Explanations for Maturity Levels, Scoring Methodology, and Recommendations Engine logic.

---

## Technology Stack

- **Backend:** Python 3.9+, Flask
- **Database:** SQLAlchemy (ORM), Flask-Migrate (Migrations). Defaults to SQLite, configurable via `DATABASE_URL`.
- **Forms:** Flask-WTF, WTForms
- **PDF Generation:** ReportLab
- **Frontend:** HTML, Tailwind CSS, JavaScript (including Alpine.js for UI interactions)
- **Charting:** Chart.js
- **Icons:** Font Awesome

---

## Architecture & Repository Structure

The application follows a standard Flask structure:

```
app/ # Main application package
├── init.py # Application factory, extension initialization
├── routes.py # Defines URL routes and view functions
├── models.py # SQLAlchemy database models
├── forms.py # WTForms form definitions
├── utils.py # Helper functions (scoring, levels)
├── recommendations.py # Recommendation generation logic
├── exports.py # PDF/CSV report generation
├── config.py # Configuration settings
├── dic_recomentations.py # Static recommendation text mapping
└── templates/ # HTML templates (Jinja2)
├── base.html
# ... (all other .html files) ...
└── components/ # Reusable template parts
└── sidebar.html
└── navbar.html

instance/ # Instance folder (NOT version controlled)
└── legacy_assessment.db # Default SQLite database location
venv/ # Virtual environment (NOT version controlled)
└── ...

requirements.txt # Python dependencies
README.md # This file
run.py # Script to create and run the Flask app (or manage.py)
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- `pip` (Python package installer)
- Virtual environment tool (like `venv` or `conda`) - Recommended

### Installation & Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git # Replace with your repo URL
    cd your-repo-name
    ```

2.  **Create and Activate Virtual Environment:**

    ```bash
    # Using venv (cross-platform)
    python -m venv venv
    # Activate (Linux/macOS)
    source venv/bin/activate
    # Activate (Windows - Command Prompt / Git Bash)
    # venv\Scripts\activate
    # Activate (Windows - PowerShell)
    # venv\Scripts\Activate.ps1
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Initialization/Migration:** This project uses Flask-Migrate for database schema management.

    ```bash
    # Initialize the migration environment (run once if 'migrations' folder doesn't exist)
    # flask db init

    # Create an initial migration based on models (run once if no migrations exist)
    # flask db migrate -m "Initial database schema"

    # Apply migrations to create/update the database tables (run this command initially and after model changes + new migration)
    flask db upgrade
    ```

    This will create/update the SQLite database file (`instance/legacy_assessment.db` by default) and tables based on `app/models.py`.

5.  **Environment Variables (Optional but Recommended for `SECRET_KEY`):**

    - `SECRET_KEY`: Set a strong, random string for session security, especially if deploying.
    - `DATABASE_URL`: (Optional) Override the default SQLite URI if using PostgreSQL, MySQL, etc. Create a `.flaskenv` file in the root directory (alongside `run.py`) or set system environment variables:

    ```.flaskenv
    FLASK_APP=run.py  # Or your main app entry point
    FLASK_DEBUG=1     # Enable debug mode for development (optional)
    SECRET_KEY='your-very-strong-random-secret-key'
    # DATABASE_URL='postgresql://user:password@host:port/database' # Example
    ```

6.  **Run the Application:**
    ```bash
    flask run
    ```
    The application should be accessible at `http://127.0.0.1:5000/` (or the port shown in the output).

---

## Usage

1.  Navigate to the application URL in your browser.
2.  **Dashboard:** Get an overview of systems and assessments.
3.  **Add System:** Define a new legacy system to track.
4.  **View/Edit System:** Access details for a system. From here you can:
    - **Start New Assessment:** Complete the 5-section maturity questionnaire.
    - **View Assessment History:** Select past assessments to view results or compare.
5.  **Financial Security:** Enter/update organisation-wide financial context data. Compare historical financial snapshots.
6.  **View Results:** After completing an assessment, view scores and the radar chart.
7.  **View Recommendations:** Access prioritised actions based on the latest assessment and financial data for a system.
8.  **Export Reports:** Download PDF or CSV reports from results, recommendations, or financial view pages.

---

## Limitations & Disclaimer

- **Prototype Status:** Developed as an academic prototype. Tested via scenarios, but not validated in live production environments.
- **Subjectivity:** Results depend heavily on accurate self-reported data.
- **Simplified Models:** Scoring weights, financial calculations, and recommendation rules are prototype implementations requiring potential tuning.
- **No Real-time Data:** Does not integrate with live monitoring/security tools.
- **Security:** Basic security practices implemented, but no formal security audit performed. **Use caution if deploying.**

**Disclaimer:** **This tool is for informational and educational purposes only.** Outputs should be used as **one input** to support professional judgment and further analysis. **It does not replace formal cybersecurity audits, risk assessments, financial analysis, or expert consultation.** Use responsibly.

---

## Future Enhancements

- Real-World Validation & User Feedback (UAT)
- Enhanced Financial Analysis (ROI, Cost-Benefit)
- Sector-Specific Compliance Modules
- Granular, Step-by-Step Recommendations
- Formal Usability Testing
- Expanded Functionality (RBAC, Advanced Reporting)
- Security Hardening & Auditing

---

## Contributing

This was developed as an individual academic project. Contributions are not actively sought, but feedback is welcome. If forking for further development:

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/YourAmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/YourAmazingFeature`).
5.  Open a Pull Request (if applicable to your fork).

Please adhere to existing code style and provide documentation/tests.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- My supervisor, Zeinab Rezaeifar, for guidance.
- Lecturers and staff at UWE Bristol and Gloucestershire College.
- Mentors and colleagues at Thales for industry insights.
- Family and friends for their support.

---

## Contact

- **Author:** Leo Williams

---
