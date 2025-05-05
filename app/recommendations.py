from app.dic_recomentations import QUESTION_RECOMMENDATIONS
from app.utils import score_to_priority_0to4


def generate_recommendations_with_timeline(assessment, financial_assessment):
    recommendations = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": [],
    }
    CRITICAL_BUDGET_RATIO = 0.05   # Budget covers <5 % of total risk
    LOW_BUDGET_RATIO      = 0.15   # Budget covers <15 % of total risk
    LOW_INVESTMENT_RATIO  = 0.20   # <20 % of budget planned for new investment
    LOW_STAFFING_RATIO    = 0.25   # <25 % of budget for staff / training

    INADEQUATE_INS_RATIO  = 0.50   # Insurance covers < 50 % of breach cost

    HIGH_FINE_RISK   = 50_000      # Potential fine  > £50 k
    HIGH_BREACH_RISK = 100_000     # Potential breach > £100 k
    HIGH_DOWN_RISK   = 50_000      # Annual downtime > £50 k


    budget = fine = breach_cost = downtime_hourly = downtime_hours = 0.0
    coverage = investment = staff_training_budget = 0.0
    risk_tolerance = "medium"

    total_risk = annual_downtime_cost = 0.0

    budget_ratio  = 999.0
    inv_ratio     = 1.0
    staff_ratio   = 1.0
    ins_ratio     = 999.0

    is_high_fine  = is_high_breach = is_high_downtime = False
    crit_budget   = low_budget = low_inv = low_staff = False
    has_insurance = False
    ins_inadequate = False

    if financial_assessment:
        budget    = float(financial_assessment.annual_security_budget or 0)
        fine      = float(financial_assessment.potential_fine or 0)
        breach_cost = float(financial_assessment.potential_breach_cost or 0)
        downtime_hourly = float(financial_assessment.downtime_cost_per_hour or 0)
        downtime_hours  = float(financial_assessment.average_downtime_hours or 0)
        coverage  = float(financial_assessment.cyber_insurance_coverage or 0)
        investment = float(financial_assessment.planned_security_investment or 0)
        staff_training_budget = float(financial_assessment.security_staff_training or 0)
        risk_tolerance = financial_assessment.acceptable_risk_level or "medium"
        has_insurance  = financial_assessment.has_cyber_insurance == "yes"

        annual_downtime_cost = downtime_hourly * downtime_hours
        total_risk           = fine + breach_cost + annual_downtime_cost

        budget_ratio = budget / total_risk if total_risk else 999.0
        inv_ratio    = investment / budget if budget else 0.0
        staff_ratio  = staff_training_budget / budget if budget else 0.0
        ins_ratio    = coverage / breach_cost if breach_cost else 999.0

        is_high_fine     = fine > HIGH_FINE_RISK
        is_high_breach   = breach_cost > HIGH_BREACH_RISK
        is_high_downtime = annual_downtime_cost > HIGH_DOWN_RISK

        crit_budget = budget_ratio < CRITICAL_BUDGET_RATIO
        low_budget  = budget_ratio < LOW_BUDGET_RATIO
        low_inv     = inv_ratio   < LOW_INVESTMENT_RATIO
        low_staff   = staff_ratio < LOW_STAFFING_RATIO
        ins_inadequate = has_insurance and (ins_ratio < INADEQUATE_INS_RATIO)

    for resp in assessment.responses:
        qid         = resp.question_id
        user_choice = resp.response           

        if qid not in QUESTION_RECOMMENDATIONS:
            continue

        rec_entry = QUESTION_RECOMMENDATIONS[qid]
        base_priority  = score_to_priority_0to4(user_choice)
        final_priority = base_priority

        dimension = rec_entry["dimension"]
        rec_text  = rec_entry["text"]
        estimated_cost = rec_entry.get("cost", "N/A")
        modified_text = rec_text
        context_notes  = []

        
        # Check if specific high risks exist OR if TD score is low to potentially elevate OK items
        needs_elevate_check = (
            (qid == 1 and is_high_breach)   or  # patching vs breach risk
            (qid == 11 and is_high_downtime) or # uptime vs downtime risk
            (qid == 21 and (assessment.technical_debt_score or 100) < 40) # Documentation check if tech debt low
        )
        if base_priority == "ok" and not needs_elevate_check:
            continue # Skip OK items unless a specific risk warrants review

        def elevate_priority(current_priority, reason):
            new_priority = current_priority
            if current_priority == 'low':
                new_priority = 'medium'
            elif current_priority == 'medium':
                new_priority = 'high'
            elif current_priority == 'high':
                new_priority = 'critical'
            # Critical stays critical
            if new_priority != current_priority:
                context_notes.append(reason)
            return new_priority

        # Risk-based Elevations
        if dimension == "security" and is_high_breach and qid in {1, 2, 4}: # Patching, Access Control, Encryption
            if base_priority in {'low', 'medium', 'high'}:
                 final_priority = elevate_priority(final_priority, f"Elevated due to high potential breach cost (£{breach_cost:,.0f}).")

        if dimension == "operational" and is_high_downtime and qid in {11, 14, 15}: # Uptime, Incident Mgmt, Scalability
             if base_priority in {'low', 'medium', 'high'}:
                 final_priority = elevate_priority(final_priority, f"Elevated due to high annual downtime impact (£{annual_downtime_cost:,.0f}).")

        if dimension == "governance" and is_high_fine and qid in {16, 18, 20}: # Compliance, Auditing, Legal
             if base_priority in {'low', 'medium', 'high'}:
                 final_priority = elevate_priority(final_priority, f"Elevated due to high potential fine (£{fine:,.0f}).")


        # Budget-driven Adjustments
        costly_qids = {3, 5, 11, 12, 15, 22, 24} # SIEM, PenTest, Redundancy, APIs, Scale, Refactor, Dependencies
        if qid in costly_qids and low_budget and base_priority != "ok":
            context_notes.append(f"Budget challenge: High cost item & budget covers only {budget_ratio*100:.0f}% of risk.")


        # If budget is critical, elevate low-cost foundational items
        if crit_budget:
            low_cost_qids = {1, 6, 7, 8, 10, 14, 19, 20, 21, 25} # Patching, FinPlan, OpsPlan, GovPlan, Docs, TDPlan
            if qid in low_cost_qids and estimated_cost == 'Low':
                # Jump potentially multiple steps if needed
                if base_priority == 'low': final_priority = 'high'
                if base_priority == 'medium': final_priority = 'critical'
                if base_priority == 'high': final_priority = 'critical' # Already high, make critical
                if final_priority != base_priority: # Only add note if changed
                     context_notes.append("Elevated: Foundational/Low-cost fix needed urgently due to critical budget.")


        # Investment/Staffing Notes 
        if dimension == "technical_debt" and low_inv and qid in {22, 23, 24, 25}: # Refactor, Maint, Deps, TD Mgmt
             context_notes.append(f"Slow progress may link to low planned investment ({inv_ratio*100:.0f}% of budget).")
             # Slightly boost TD items if investment low and score poor
             if (assessment.technical_debt_score or 100) < 40 and base_priority == "low":
                 final_priority = 'medium'
                 if final_priority != base_priority:
                     context_notes.append("Elevated slightly due to low TD score & low investment.")

        skill_intensive_qids = {3, 5, 12, 17, 22, 23} # SIEM, PenTest, APIs, RiskAssess, Refactor, Maint
        if qid in skill_intensive_qids and low_staff and base_priority != "ok":
             context_notes.append(f"Requires skilled staff; training gap suspected ({staff_ratio*100:.0f}% budget for staff/training).")


        # Insurance Inadequacy 
        if dimension == "security" and ins_inadequate and qid in {1, 2, 4, 5} and base_priority == "low": # Key security controls
             final_priority = "medium" # Elevate from low to medium
             if final_priority != base_priority:
                 context_notes.append(f"Increased importance as insurance coverage is low ({ins_ratio*100:.0f}% of potential breach cost).")

        # Risk Tolerance Adjustments
        if risk_tolerance == "low" and base_priority == "low":
            final_priority = "medium" # Elevate low to medium
            if final_priority != base_priority:
                context_notes.append("Elevated due to low organisational risk tolerance.")

        if base_priority == "ok" and needs_elevate_check: # Check again using the flag
            elevate = False
            reason_ok = ""
            # Determine specific reason based on which condition triggered needs_elevate_check
            if qid == 1 and is_high_breach:
                reason_ok = f"Review patching effectiveness given high breach risk (£{breach_cost:,.0f})."
                elevate = True
            elif qid == 11 and is_high_downtime:
                reason_ok = f"Review uptime measures given high downtime impact (£{annual_downtime_cost:,.0f})."
                elevate = True
            elif qid == 21 and (assessment.technical_debt_score or 100) < 40:
                reason_ok = "Verify documentation adequacy given overall low technical debt score."
                elevate = True

            if elevate:
                final_priority = "low" # Elevate OK to LOW for review
                modified_text = f"Review / Verify: {rec_text}" # Prepend review instruction
                context_notes.append(reason_ok)


    
        moved  = final_priority != base_priority
        reason = "; ".join(context_notes) if moved else ""
        display_text = modified_text

        if final_priority != "ok":  # Only add actionable recommendations
            recommendations.setdefault(final_priority, []).append({
                "dimension": dimension.replace("_", " ").title(),
                "text": display_text,
                "moved": moved,
                "reason": reason,
                "cost": estimated_cost
            })


    if financial_assessment:
        rec_cost_low = "Low"
        rec_cost_med = "Medium" # Potential cost of increasing budget/insurance

        # Critical Budget Shortfall -> Remains Critical
        if crit_budget:
            recommendations["critical"].append({
                "dimension": "Financial", "text": f"CRITICAL BUDGET SHORTFALL: Budget (£{budget:,.0f}) covers only {budget_ratio*100:.0f}% of risk (£{total_risk:,.0f}). Urgent review required.",
                "moved": False, "reason": "", "cost": rec_cost_low
            })
        # Low Budget -> Remains High
        elif low_budget:
            recommendations["high"].append({
                "dimension": "Financial", "text": f"Security budget (£{budget:,.0f}) appears low ({budget_ratio*100:.0f}% of risk £{total_risk:,.0f}). Consider increasing.",
                "moved": False, "reason": "", "cost": rec_cost_low
            })

        # No Insurance -> Remains High
        if not has_insurance:
            recommendations["high"].append({
                "dimension": "Financial", "text": "Obtain cyber-insurance quotation to mitigate financial exposure.",
                "moved": False, "reason": "", "cost": rec_cost_low
            })
        # Inadequate Insurance -> Now Medium (Review needed, but less urgent than none)
        elif ins_inadequate:
            recommendations["medium"].append({ # <-- CHANGED TO MEDIUM
                "dimension": "Financial", "text": f"Review cyber-insurance coverage (£{coverage:,.0f}). Currently covers < {INADEQUATE_INS_RATIO*100:.0f}% of potential breach cost (£{breach_cost:,.0f}).",
                "moved": False, "reason": "", "cost": rec_cost_low
            })

        # Low Investment -> Now Medium
        if low_inv:
            recommendations["medium"].append({ # <-- CHANGED TO MEDIUM
                "dimension": "Financial", "text": f"Planned investment ({inv_ratio*100:.0f}% of budget) seems low for proactive modernisation. Review investment strategy.",
                "moved": False, "reason": "", "cost": rec_cost_low
            })

        # Low Staffing/Training Budget -> Now Medium
        if low_staff:
            recommendations["medium"].append({ # <-- CHANGED TO MEDIUM
                "dimension": "Financial", "text": f"Budget allocation for security staff / training ({staff_ratio*100:.0f}%) appears low. Ensure adequate skilled resources.",
                "moved": False, "reason": "", "cost": rec_cost_low
            })

    implementation_plan = [
        {
            "phase": "Phase 1: Immediate Actions (e.g., Within 30 Days)",
            "tasks": [
                "Triage and begin addressing all 'Critical' priority recommendations.",
                "Focus on foundational fixes identified as Critical.",
                "Verify robust auditing and logging if identified as Critical.",
            ],
        },
        {
            "phase": "Phase 2: High Priority Remediation (e.g., Within 90 Days)",
            "tasks": [
                "Address all 'High' priority recommendations.",
                "Implement remaining Critical items if not completed in Phase 1.",
                "Complete structured patching implementation (if High/Critical).",
                "Enhance access controls (RBAC, MFA) if identified as High/Critical.",
            ],
        },
        {
            "phase": "Phase 3: Medium Priority Improvements (e.g., Within 6 Months)", #
            "tasks": [
                "Address 'Medium' priority recommendations.", 
                "Begin tackling high-priority technical debt.",
                "Formalise incident response plans and conduct training.",
            ],
        },
        {
            "phase": "Phase 4: Consolidation & Long-Term Planning (e.g., Within 12 Months / Ongoing)", 
            "tasks": [
                "Address 'Low' priority items (including reviews of 'OK' items flagged).", 
                "Develop/refine and execute longer-term modernisation roadmap.",
                "Schedule regular re-assessments (e.g., quarterly or bi-annually).",
            ],
        },
    ]

    financial_metrics = {
        "budget_adequacy_ratio": budget_ratio if financial_assessment else None,
        "insurance_adequacy_ratio": ins_ratio if financial_assessment else None,
        "total_risk": total_risk if financial_assessment else None,
        "is_insurance_inadequate": ins_inadequate,
    }

    return recommendations, implementation_plan, financial_metrics