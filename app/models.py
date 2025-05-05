from datetime import datetime
from app import db

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    num_devices = db.Column(db.Integer, nullable=True)
    device_details = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assessments = db.relationship('Assessment', backref='system', lazy=True, cascade="all, delete-orphan")


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    security_score = db.Column(db.Integer)
    financial_score = db.Column(db.Integer)
    operational_score = db.Column(db.Integer)
    governance_score = db.Column(db.Integer)
    technical_debt_score = db.Column(db.Integer)

    @property
    def overall_score(self):
        # Calculate the average score across all dimensions
        scores = [self.security_score, self.financial_score, self.operational_score, self.governance_score, self.technical_debt_score]
        # Handle potential None values if an assessment wasn't fully scored
        valid_scores = [s for s in scores if s is not None]
        if not valid_scores:
            return 0 
        return sum(valid_scores) / len(valid_scores)

    def to_dict(self):
        # Convert assessment to dictionary for API/charts
        return {
            'id': self.id,
            'system_id': self.system_id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M'),
            'security_score': self.security_score,
            'financial_score': self.financial_score,
            'operational_score': self.operational_score,
            'governance_score': self.governance_score,
            'technical_debt_score': self.technical_debt_score,
            'overall_score': self.overall_score
        }

class AssessmentResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    response = db.Column(db.Integer)  # 0-4 score for each question
    dimension = db.Column(db.String(50))  # Which dimension this question belongs to
    assessment = db.relationship('Assessment', backref=db.backref('responses', lazy=True, cascade="all, delete-orphan"))

class FinancialSecurityAssessment(db.Model):
    __tablename__ = 'financial_security_assessments'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    annual_security_budget = db.Column(db.Numeric(precision=14, scale=2), nullable=True)
    planned_security_investment = db.Column(db.Numeric(precision=14, scale=2), nullable=True)
    security_staff_training = db.Column(db.Numeric(precision=14, scale=2), nullable=True)
    annual_revenue = db.Column(db.Numeric(precision=14, scale=2), nullable=True)
    potential_fine = db.Column(db.Numeric(precision=14, scale=2), nullable=True)
    potential_breach_cost = db.Column(db.Numeric(precision=14, scale=2), nullable=True)
    downtime_cost_per_hour = db.Column(db.Numeric(precision=14, scale=2), nullable=True)
    average_downtime_hours = db.Column(db.Integer, nullable=True)
    acceptable_risk_level = db.Column(db.String(20), nullable=True)
    has_cyber_insurance = db.Column(db.String(5), nullable=True)  # "yes" or "no"
    cyber_insurance_coverage = db.Column(db.Numeric(precision=14, scale=2), nullable=True)

    def calculate_financial_score(self):
        budget = float(self.annual_security_budget or 0)
        fine = float(self.potential_fine or 0)
        breach_cost = float(self.potential_breach_cost or 0)
        downtime_cost = float(self.downtime_cost_per_hour or 0)
        avg_downtime = float(self.average_downtime_hours or 0)

        # Combine potential risks
        total_risk = fine + breach_cost + (downtime_cost * avg_downtime)
        
        # Avoid division by zero if total_risk is 0
        if total_risk <= 0:
            ratio = 1.0 # Assign max ratio if no risk
        else:
            ratio = budget / total_risk

        # Scale ratio to a base score
        base_score = ratio * 100
        # Cap base score at 100 (budget can exceed risk)
        base_score = min(base_score, 100)


        # Bonus for cyber insurance
        if self.has_cyber_insurance == "yes":
            base_score += 10
        # Cap final score at 100
        base_score = min(base_score, 100)


        return round(base_score, 1)



    