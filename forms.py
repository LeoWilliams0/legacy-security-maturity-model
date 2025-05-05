from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf import FlaskForm
from wtforms import DecimalField, RadioField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class SystemForm(FlaskForm):
    name = StringField('System Name', validators=[DataRequired(), Length(min=2, max=100)])
    num_devices = IntegerField('Number of Devices', validators=[Optional()])
    device_details = TextAreaField('Device Details', validators=[Optional()])
    description = TextAreaField('Description')
    submit = SubmitField('Create System')

class InitialAssessmentForm(FlaskForm):
    # Security Controls Section
    security_patching = RadioField('How frequently does the system receive security patches?',
        choices=[
            (0, 'No patches applied'),
            (1, 'Patches applied only after security incidents'),
            (2, 'Patches applied once per year'),
            (3, 'Patches applied quarterly with a formalised schedule'),
            (4, 'Regular patching with a structured governance framework')
        ],
        coerce=int
    )
    
    access_control = RadioField('What level of access control is in place?',
        choices=[
            (0, 'No access control, all users have the same privileges'),
            (1, 'Basic authentication (single username/password)'),
            (2, 'Some role-based access control but inconsistently enforced'),
            (3, 'Role-based access with strong password policies'),
            (4, 'Multi-factor authentication (MFA) with strict access control')
        ],
        coerce=int
    )

    security_monitoring = RadioField('How is security monitoring handled?',
        choices=[
            (0, 'No monitoring, security incidents go undetected'),
            (1, 'Manual log reviews only when an issue occurs'),
            (2, 'Basic logging with occasional review'),
            (3, 'Automated security monitoring with alerts'),
            (4, 'Continuous threat detection with incident response automation')
        ],
        coerce=int
    )

    data_encryption = RadioField('How is data encryption managed?',
        choices=[
            (0, 'No encryption, data stored in plaintext'),
            (1, 'Some sensitive data encrypted, but inconsistent'),
            (2, 'Basic encryption at rest but not in transit'),
            (3, 'Encryption in transit and at rest using industry standards'),
            (4, 'Strong encryption with key management and regular audits')
        ],
        coerce=int
    )

    security_testing = RadioField('How often is penetration testing or security audits conducted?',
        choices=[
            (0, 'No testing or audits conducted'),
            (1, 'Informal reviews, but no structured security audits'),
            (2, 'Annual external security audits are conducted'),
            (3, 'Security audits and penetration testing performed quarterly'),
            (4, 'Continuous security testing with real-time risk analysis')
        ],
        coerce=int
    )

    # Financial Viability Section
    maintenance_budget = RadioField('Is there a dedicated budget for system maintenance?',
        choices=[
            (0, 'No budget allocated'),
            (1, 'Maintenance funded only when critical failures occur'),
            (2, 'Some budget exists, but often inadequate'),
            (3, 'Regular budget planning for maintenance'),
            (4, 'Well-defined budget with forecasting for future upgrades')
        ],
        coerce=int
    )

    cost_value_ratio = RadioField('How does the cost of maintaining the system compare to its business value?',
        choices=[
            (0, 'Costs far exceed business value'),
            (1, 'Costs are difficult to justify'),
            (2, 'Costs are high but mostly sustainable'),
            (3, 'Costs align with the business value'),
            (4, 'Costs are optimised, with clear ROI justification')
        ],
        coerce=int
    )

    financial_risk = RadioField('How frequently are financial risks associated with the system assessed?',
        choices=[
            (0, 'No financial risk analysis performed'),
            (1, 'Financial risks considered informally'),
            (2, 'Financial risk assessments conducted occasionally'),
            (3, 'Formal risk assessments conducted annually'),
            (4, 'Continuous financial risk tracking and mitigation planning')
        ],
        coerce=int
    )

    training_investment = RadioField('What level of investment is made in training staff to manage the legacy system?',
        choices=[
            (0, 'No training budget or staff development'),
            (1, 'Staff training is ad-hoc, no structured learning'),
            (2, 'Some training is available but not well-structured'),
            (3, 'Employees regularly trained with planned courses'),
            (4, 'Continuous skill development and certification programs')
        ],
        coerce=int
    )

    modernisation_planning = RadioField('Are modernisation or migration plans financially accounted for?',
        choices=[
            (0, 'No modernisation plans exist'),
            (1, 'Modernisation has been discussed but no action taken'),
            (2, 'A long-term modernisation strategy exists'),
            (3, 'A phased modernisation/migration plan is being executed'),
            (4, 'The system is fully optimised or successfully modernised')
        ],
        coerce=int
    )

    # Operational Performance Section
    system_uptime = RadioField('What is the system\'s uptime and reliability?',
        choices=[
            (0, 'Frequent unplanned downtime, unreliable system'),
            (1, 'Downtime occurs regularly, recovery is slow'),
            (2, 'Downtime occurs occasionally but is manageable'),
            (3, 'High availability with minimal downtime'),
            (4, '99.9%+ uptime with redundancy and failover mechanisms')
        ],
        coerce=int
    )

    system_integration = RadioField('How well does the system integrate with modern applications?',
        choices=[
            (0, 'No integration possible, completely isolated system'),
            (1, 'Limited integration with major compatibility issues'),
            (2, 'Some integrations exist but require workarounds'),
            (3, 'Well-integrated with modern applications'),
            (4, 'Seamless API-driven integration with full automation')
        ],
        coerce=int
    )

    performance_monitoring = RadioField('How effective is performance monitoring and optimisation?',
        choices=[
            (0, 'No performance monitoring in place'),
            (1, 'Manual monitoring done occasionally'),
            (2, 'Basic automated monitoring with limited insights'),
            (3, 'Performance is regularly optimised based on monitoring'),
            (4, 'Real-time analytics with AI-driven optimisations')
        ],
        coerce=int
    )

    incident_management = RadioField('How are system failures and incidents managed?',
        choices=[
            (0, 'No incident management process, issues cause extended outages'),
            (1, 'Issues are addressed reactively without structured processes'),
            (2, 'Some incident tracking and resolution processes exist'),
            (3, 'Incidents are logged, analysed, and mitigated systematically'),
            (4, 'Automated incident detection, response, and continuous improvements')
        ],
        coerce=int
    )

    scalability = RadioField('How well does the system handle increasing workloads and scalability?',
        choices=[
            (0, 'Cannot handle increased workload, frequently crashes'),
            (1, 'Limited scalability, performance degrades under load'),
            (2, 'Some scalability built-in, but manual intervention is needed'),
            (3, 'Can scale dynamically with planned resource allocation'),
            (4, 'Fully elastic and scalable with automated load balancing')
        ],
        coerce=int
    )

    # Governance & Compliance Section
    regulatory_compliance = RadioField('Does the system meet regulatory compliance requirements?',
        choices=[
            (0, 'No compliance measures in place'),
            (1, 'Some compliance efforts, but insufficient for audits'),
            (2, 'Partially compliant, gaps in adherence exist'),
            (3, 'Fully compliant with external audits'),
            (4, 'Continuous compliance monitoring and proactive improvements')
        ],
        coerce=int
    )

    risk_assessment = RadioField('How frequently are security and operational risks assessed?',
        choices=[
            (0, 'No risk assessments performed'),
            (1, 'Informal risk assessments occur occasionally'),
            (2, 'Some structured risk assessments are conducted annually'),
            (3, 'Risks are systematically tracked and mitigated proactively'),
            (4, 'Continuous risk monitoring with AI-driven mitigation')
        ],
        coerce=int
    )

    system_auditing = RadioField('How is system auditing and reporting handled?',
        choices=[
            (0, 'No audits or reporting exist'),
            (1, 'Basic auditing is done manually, not standardised'),
            (2, 'Audits are performed periodically with partial automation'),
            (3, 'Regular audits with detailed reporting and compliance tracking'),
            (4, 'Automated auditing with real-time compliance dashboards')
        ],
        coerce=int
    )

    documentation_governance = RadioField('What level of documentation exists for governance and policies?',
        choices=[
            (0, 'No documented policies or governance procedures'),
            (1, 'Some policies exist, but they are outdated or incomplete'),
            (2, 'Governance policies are documented but not strictly enforced'),
            (3, 'Well-documented policies are actively followed'),
            (4, 'Governance is continuously reviewed, with best practices applied')
        ],
        coerce=int
    )

    legal_compliance = RadioField('How does the system ensure legal and contractual compliance?',
        choices=[
            (0, 'No tracking of legal or contractual obligations'),
            (1, 'Some contracts reviewed, but enforcement is inconsistent'),
            (2, 'Compliance is checked, but enforcement needs improvement'),
            (3, 'Legal compliance is well-integrated into processes'),
            (4, 'Continuous monitoring ensures full legal and contractual compliance')
        ],
        coerce=int
    )

    # Technical Debt Section
    system_documentation = RadioField('How well is the system documented?',
        choices=[
            (0, 'No documentation exists'),
            (1, 'Outdated or incomplete documentation'),
            (2, 'Some documentation, but lacks detail'),
            (3, 'Comprehensive and up-to-date documentation'),
            (4, 'Detailed documentation with version control and best practices')
        ],
        coerce=int
    )

    system_modification = RadioField('How easy is it to modify the system to meet new requirements?',
        choices=[
            (0, 'Any change risks breaking the entire system'),
            (1, 'Changes are extremely difficult and costly'),
            (2, 'Some flexibility exists, but requires workarounds'),
            (3, 'Changes can be made efficiently with minimal disruption'),
            (4, 'The system is highly modular and easy to update')
        ],
        coerce=int
    )

    codebase_maintenance = RadioField('How actively is the system codebase maintained?',
        choices=[
            (0, 'No maintenance is performed'),
            (1, 'Code is updated only when critical issues arise'),
            (2, 'Some proactive maintenance occurs'),
            (3, 'Regular maintenance schedules are followed'),
            (4, 'Continuous improvements and refactoring are in place')
        ],
        coerce=int
    )

    legacy_dependency = RadioField('What is the level of dependency on legacy technologies?',
        choices=[
            (0, 'Completely dependent on outdated technology'),
            (1, 'High reliance on legacy technology, no migration plans'),
            (2, 'Some modernisation is occurring'),
            (3, 'System is being actively upgraded'),
            (4, 'Fully modernised or migrated to current technologies')
        ],
        coerce=int
    )

    technical_debt = RadioField('How well does the system handle technical debt reduction?',
        choices=[
            (0, 'No technical debt management, accumulating legacy issues'),
            (1, 'Some awareness of technical debt, but no mitigation plans'),
            (2, 'Technical debt is reviewed but rarely addressed'),
            (3, 'Regular efforts to reduce technical debt through code refactoring'),
            (4, 'Continuous reduction of technical debt with proactive strategies')
        ],
        coerce=int
    )

    submit = SubmitField('Submit Assessment')

class FinancialSecurityForm(FlaskForm):
    annual_security_budget = DecimalField(
        "Annual Security Budget (£)",
        validators=[DataRequired(), NumberRange(min=0, message="Must be zero or positive")]
    )
    planned_security_investment = DecimalField(
        "Planned Security Investment (£)",
        validators=[Optional(), NumberRange(min=0)]
    )
    security_staff_training = DecimalField(
        "Security Staff & Training (£)",
        validators=[Optional(), NumberRange(min=0)]
    )
    annual_revenue = DecimalField(
        "Annual Revenue (£)",
        validators=[DataRequired(), NumberRange(min=0, message="Must be zero or positive")]
    )
    potential_fine = DecimalField(
        "Potential Fine (£)",
        validators=[DataRequired(), NumberRange(min=0, message="Must be zero or positive")]
    )
    potential_breach_cost = DecimalField(
        "Potential Breach Cost (£)",
        validators=[DataRequired(), NumberRange(min=0, message="Must be zero or positive")]
    )
    downtime_cost_per_hour = DecimalField(
        "Downtime Cost per Hour (£)",
        validators=[Optional(), NumberRange(min=0)]
    )
    average_downtime_hours = IntegerField(
        "Average Downtime per Year (hours)",
        validators=[Optional(), NumberRange(min=0, message="Must be zero or positive")]
    )
    acceptable_risk_level = RadioField(
        "Acceptable Risk Level",
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium",
        validators=[DataRequired()]
    )
    has_cyber_insurance = RadioField(
        "Has Cyber Insurance?",
        choices=[("yes", "Yes"), ("no", "No")],
        default="no",
        validators=[DataRequired()]
    )
    cyber_insurance_coverage = DecimalField(
        "Cyber Insurance Coverage (£)",
        validators=[Optional(), NumberRange(min=0)]
    )
    submit = SubmitField("Save Financial Security Assessment")