
def calculate_dimension_score(responses):
    # Convert a list of 1-10 answers into a 0-100 score
    if not responses:
        return 0
    max_possible = len(responses) * 10
    return (sum(r.response for r in responses) / max_possible) * 100


def get_question_text(question_id):
    # Return the wording for a given question
    questions = {
        1: "How frequently are security patches applied?",
        2: "What authentication mechanisms are in place?",
        3: "How granular is the system's access control?",
        4: "What is the annual maintenance cost relative to business value?",
        5: "What is the return on investment for the system?",
        6: "How costly would replacing the system be?",
        7: "What is the system's uptime percentage?",
        8: "How does the system perform under load?",
        9: "How well does the system integrate with other systems?",
        10: "How compliant is the system with relevant regulations?",
        11: "How well is the system documented?",
        12: "What level of audit capabilities does the system have?",
        13: "What is the quality of the codebase?",
        14: "How modern is the infrastructure?",
        15: "How scalable is the system?",
        16: "Does the system meet regulatory compliance requirements?",
        17: "How frequently are security and operational risks assessed?",
        18: "How is system auditing and reporting handled?",
        19: "What level of documentation exists for governance and policies?",
        20: "How does the system ensure legal and contractual compliance?",
        21: "How well is the system documented?",
        22: "How easy is it to modify the system to meet new requirements?",
        23: "How actively is the system codebase maintained?",
        24: "What is the level of dependency on legacy technologies?",
        25: "How well does the system handle technical debt reduction?",
    }
    return questions.get(question_id, "Unknown question")


def calculate_weighted_score(responses, dimension):
    # Weighted 0-100 score for one dimension
    weights = {
        "security": {1: 0.25, 2: 0.20, 3: 0.15, 4: 0.20, 5: 0.20},
        "financial": {6: 0.30, 7: 0.25, 8: 0.20, 9: 0.15, 10: 0.10},
        "operational": {11: 0.30, 12: 0.20, 13: 0.15, 14: 0.20, 15: 0.15},
        "governance": {16: 0.40, 17: 0.20, 18: 0.15, 19: 0.15, 20: 0.10},
        "technical_debt": {21: 0.25, 22: 0.20, 23: 0.20, 24: 0.20, 25: 0.15},
    }
    total = 0
    for r in responses:
        if r.dimension == dimension:
            weight = weights[dimension].get(r.question_id, 0)
            total += ((r.response / 4) * 100) * weight
    return round(total)


MATURITY_LEVELS = [
    (0, 20, 1, "Ad Hoc",
     "Few formal processes exist. Security controls are reactive, budgeting is minimal, "
     "patches applied sporadically without structured plan."),
    (20, 40, 2, "Documented",
     "Basic policies are written down and some documentation exists but is incomplete. "
     "Budgeting is short-term and training ad-hoc."),
    (40, 60, 3, "Defined",
     "Formal governance in place and deliberate financial planning. Patching is systematic, "
     "some modernisation (e.g. virtualisation) but ROI metrics are limited."),
    (60, 80, 4, "Managed",
     "Comprehensive documentation and rigorous metrics guide security and budgeting. "
     "Patching on a predictable schedule, multi-year forecasts, routine staff training."),
    (80, 101, 5, "Optimised",
     "Continuous improvement aligns legacy systems with new tech. Strategic budgeting "
     "balances modernisation & operations, maximizing ROI over time.")
]

def get_maturity_level(score):
    # Given an overall score 0-100, return a tuple
    for low, high, lvl, name, desc in MATURITY_LEVELS:
        if low <= score < high:
            return lvl, name, desc
    # fallback
    return None, "Unknown", ""

def score_to_priority_0to4(choice):
    if choice == 0:
        return 'critical'
    elif choice == 1:
        return 'high'
    elif choice == 2:
        return 'medium' 
    elif choice == 3:
        return 'low'  
    else:
        return 'ok'