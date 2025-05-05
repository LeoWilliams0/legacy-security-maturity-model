QUESTION_RECOMMENDATIONS = {
    # Security Controls recommendations
    1: {
        "dimension": "security",
        "text": "Adopt a formal patch management process: patch critical vulnerabilities within 24 hours, with monthly scheduled updates.",
        "cost": "Medium" # Requires process definition, potentially tools/time
    },
    2: {
        "dimension": "security",
        "text": "Strengthen access control by implementing multi-factor authentication (MFA) and clear role definitions to reduce unauthorised access risks.",
        "cost": "Medium" # MFA solutions have costs, configuration effort
    },
    3: {
        "dimension": "security",
        "text": "Implement continuous security monitoring (e.g. SIEM) for early detection and rapid incident response.",
        "cost": "High" # SIEM tools and expertise can be expensive
    },
    4: {
        "dimension": "security",
        "text": "Upgrade data encryption: ensure data at rest and in transit use modern algorithms and secure key management.",
        "cost": "Medium" # Depends on system, might need config/dev time
    },
    5: {
        "dimension": "security",
        "text": "Conduct regular penetration testing and security audits to proactively identify and address vulnerabilities.",
        "cost": "High" # External testing services are costly
    },

    # Financial Viability recommendations
    6: {
        "dimension": "financial",
        "text": "Establish a dedicated maintenance budget to avoid unexpected costs and ensure ongoing support.",
        "cost": "Low" # Process change
    },
    7: {
        "dimension": "financial",
        "text": "Perform a cost-benefit analysis to confirm the system’s ROI against maintenance costs and guide budget adjustments.",
        "cost": "Low" # Analysis effort
    },
    8: {
        "dimension": "financial",
        "text": "Carry out formal financial risk assessments at least annually, factoring in fines, breach costs and downtime impacts.",
        "cost": "Low" # Analysis effort
    },
    9: {
        "dimension": "financial",
        "text": "Increase investment in staff training to ensure personnel have the necessary skills to operate, secure and modernise the system.",
        "cost": "Medium" # Training costs
    },
    10: {
        "dimension": "financial",
        "text": "Include modernisation or migration plans in budget forecasts to prevent sudden high costs and system obsolescence.",
        "cost": "Low" # Planning effort
    },

    # Operational Performance recommendations
    11: {
        "dimension": "operational",
        "text": "Enhance uptime by adding redundancy and failover mechanisms aimed at minimising unplanned downtime.",
        "cost": "High" # Hardware/infrastructure costs
    },
    12: {
        "dimension": "operational",
        "text": "Develop APIs or middleware for seamless integration with modern applications, reducing manual workarounds.",
        "cost": "High" # Development effort
    },
    13: {
        "dimension": "operational",
        "text": "Adopt robust performance monitoring with dashboards and alerts to quickly spot and address slow areas.",
        "cost": "Medium" # Monitoring tools/config
    },
    14: {
        "dimension": "operational",
        "text": "Formalise incident management: define clear roles, escalation paths and post‑incident reviews.",
        "cost": "Low" # Process definition
    },
    15: {
        "dimension": "operational",
        "text": "Scale system capacity proactively, considering containerisation, cloud solutions or load balancing.",
        "cost": "High" # Infrastructure/cloud costs
    },

    # Governance & Compliance recommendations
    16: {
        "dimension": "governance",
        "text": "Address regulatory gaps with formal compliance reviews, document requirements and track remediation.",
        "cost": "Medium" # Audit/review effort
    },
    17: {
        "dimension": "governance",
        "text": "Schedule systematic risk assessments (e.g. NIST, ISO27001) and regularly mitigate security and operational risks.",
        "cost": "Medium" # Assessment effort/tools
    },
    18: {
        "dimension": "governance",
        "text": "Implement structured auditing and reporting: log changes and review routinely to detect anomalies.",
        "cost": "Medium" # Config/tools
    },
    19: {
        "dimension": "governance",
        "text": "Maintain up-to-date governance policies, ensure adherence across teams, and review annually.",
        "cost": "Low" # Documentation effort
    },
    20: {
        "dimension": "governance",
        "text": "Integrate legal and contractual compliance checks into standard processes with a central register.",
        "cost": "Low" # Process change
    },

    # Technical Debt Management recommendations
    21: {
        "dimension": "technical_debt",
        "text": "Improve documentation (architecture diagrams, data flows); a well‑documented system is easier to maintain.",
        "cost": "Low" # Time/effort
    },
    22: {
        "dimension": "technical_debt",
        "text": "Refactor the system to enable safer and easier modifications, reducing breakage risk.",
        "cost": "High" # Significant development effort
    },
    23: {
        "dimension": "technical_debt",
        "text": "Adopt regular code maintenance sprints (monthly or quarterly) to fix bugs and pay down debt.",
        "cost": "Medium" # Ongoing dev time
    },
    24: {
        "dimension": "technical_debt",
        "text": "Replace legacy dependencies with modern, supported alternatives to avoid outdated libraries.",
        "cost": "High" # Research/dev effort
    },
    25: {
        "dimension": "technical_debt",
        "text": "Manage technical debt proactively by planning ongoing improvements to prevent unmaintainable code build-up.",
        "cost": "Low" # Planning/process
    },
}