from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from app import db
from app.models import System, Assessment, AssessmentResponse, FinancialSecurityAssessment
from app.forms import SystemForm, InitialAssessmentForm, FinancialSecurityForm
from app.utils import calculate_weighted_score, get_maturity_level, MATURITY_LEVELS
import json

from app.recommendations import generate_recommendations_with_timeline

from app.exports import (generate_pdf_report, generate_csv_export, generate_financial_pdf_report, generate_financial_csv_export, generate_combined_csv, generate_pdf_with_recommendations)


main = Blueprint('main', __name__)

@main.route('/')
def index():
    #Home page showing a list of systems and a possible financial assessment
    systems = System.query.all()

    # If you only have one financial assessment or you want the latest:
    financial_assessment = FinancialSecurityAssessment.query.order_by(
        FinancialSecurityAssessment.created_at.desc()
    ).first()

    return render_template('index.html', systems=systems, financial_assessment=financial_assessment)

@main.route('/compare-financial', methods=['GET', 'POST'])
def compare_financial():
    #Compare multiple financial assessments
    all_fsa = FinancialSecurityAssessment.query.order_by(FinancialSecurityAssessment.created_at.desc()).all()

    if request.method == 'POST':
        selected_ids = request.form.getlist('fsa_ids')
        if not selected_ids:
            flash('Please select at least one financial assessment.', 'error')
            return redirect(url_for('main.compare_financial'))

        # Fetch the selected assessments from the DB
        selected_assessments = []
        for sid in selected_ids:
            fsa = FinancialSecurityAssessment.query.get(int(sid))
            if fsa:
                selected_assessments.append(fsa)

        # Render a comparison page showing the selected assessments side by side
        return render_template('compare_financial.html', assessments=selected_assessments)

    # Show a form with checkboxes for all financial assessments
    return render_template('compare_financial_form.html', all_assessments=all_fsa)



@main.route('/system/<int:system_id>/delete', methods=['POST'])
def delete_system(system_id):
    system = System.query.get_or_404(system_id)
    db.session.delete(system)
    db.session.commit()
    flash('System deleted successfully!', 'success')
    return redirect(url_for('main.index'))


@main.route('/system/new', methods=['GET', 'POST'])
def create_system():
    #Create a new system to assess
    form = SystemForm()
    if form.validate_on_submit():
        system = System(
            name=form.name.data,
            num_devices=form.num_devices.data,          
            device_details=form.device_details.data, 
            description=form.description.data
        )
        db.session.add(system)
        db.session.commit()
        flash('System created successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('system_form.html', form=form, title="Create New System")

@main.route('/system/<int:system_id>/view', methods=['GET'])
def view_system(system_id):
    system = System.query.get_or_404(system_id)
    form = SystemForm(obj=system)  # Prepopulate form with system data
    return render_template('view_system.html', system=system, form=form)


@main.route('/system/<int:system_id>/assess', methods=['GET', 'POST'])
def assess_system(system_id):
    system = System.query.get_or_404(system_id)
    form = InitialAssessmentForm()
    
    if form.validate_on_submit():
        # Create a new assessment tied to the chosen system
        assessment = Assessment(
            system_id=system.id
        )
        db.session.add(assessment)
        db.session.flush()
        
        # Store responses for each section using your weighted score logic
        all_responses = []
        
        # Security Controls (Weight: 100%)
        security_fields = [
            (form.security_patching, 1), (form.access_control, 2),
            (form.security_monitoring, 3), (form.data_encryption, 4),
            (form.security_testing, 5)
        ]
        
        # Financial Viability (Weight: 100%)
        financial_fields = [
            (form.maintenance_budget, 6), (form.cost_value_ratio, 7),
            (form.financial_risk, 8), (form.training_investment, 9),
            (form.modernisation_planning, 10)
        ]
        
        # Operational Performance (Weight: 100%)
        operational_fields = [
            (form.system_uptime, 11), (form.system_integration, 12),
            (form.performance_monitoring, 13), (form.incident_management, 14),
            (form.scalability, 15)
        ]
        
        # Governance & Compliance (Weight: 100%)
        governance_fields = [
            (form.regulatory_compliance, 16), (form.risk_assessment, 17),
            (form.system_auditing, 18), (form.documentation_governance, 19),
            (form.legal_compliance, 20)
        ]
        
        # Technical Debt (Weight: 100%)
        technical_debt_fields = [
            (form.system_documentation, 21), (form.system_modification, 22),
            (form.codebase_maintenance, 23), (form.legacy_dependency, 24),
            (form.technical_debt, 25)
        ]
        
        # Process each section and calculate weighted scores
        for fields, dimension in [
            (security_fields, 'security'),
            (financial_fields, 'financial'),
            (operational_fields, 'operational'),
            (governance_fields, 'governance'),
            (technical_debt_fields, 'technical_debt')
        ]:
            section_responses = []
            for field, question_id in fields:
                response = AssessmentResponse(
                    assessment_id=assessment.id,
                    question_id=question_id,
                    response=field.data,
                    dimension=dimension
                )
                section_responses.append(response)
            all_responses.extend(section_responses)
            
            # Calculate and assign the weighted score for the section
            score_attr = f"{dimension}_score"
            setattr(assessment, score_attr, calculate_weighted_score(section_responses, dimension))
        
        db.session.add_all(all_responses)
        db.session.commit()
        
        flash('Initial assessment completed successfully!', 'success')
        return redirect(url_for('main.assessment_results', assessment_id=assessment.id))
    
    return render_template('initial_assessment.html', form=form, system=system)

@main.route('/system/<int:system_id>/edit', methods=['GET', 'POST'])
def edit_system(system_id):
    system = System.query.get_or_404(system_id)
    form = SystemForm(obj=system)
    if form.validate_on_submit():
        system.name = form.name.data
        system.num_devices = form.num_devices.data
        system.device_details = form.device_details.data
        system.description = form.description.data
        db.session.commit()
        flash('System updated successfully!', 'success')
        return redirect(url_for('main.view_system', system_id=system.id))
    return render_template('edit_system.html', system=system, form=form)


@main.route('/assessment/<int:assessment_id>/results')
def assessment_results(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    system = assessment.system
    overall_level_num, overall_level_name, overall_level_desc = None, "N/A", ""
    dimension_levels = {} # Dictionary to hold levels for each dimension
    radar_data = {"labels": [], "datasets": []} # Default

    try:
        if assessment.overall_score is not None:
            overall_level_num, overall_level_name, overall_level_desc = get_maturity_level(assessment.overall_score)

        # Calculate levels for each dimension 
        dimensions = {
            'Security': assessment.security_score,
            'Financial Viability': assessment.financial_score,
            'Operational Performance': assessment.operational_score,
            'Governance & Compliance': assessment.governance_score,
            'Technical Debt': assessment.technical_debt_score
        }
        for name, score in dimensions.items():
            if score is not None:
                lvl, lname, _ = get_maturity_level(score)
                dimension_levels[name] = {'num': lvl, 'name': lname}
            else:
                dimension_levels[name] = {'num': None, 'name': 'N/A'}

        # Prepare radar data
        radar_data = {
            "labels": list(dimensions.keys()),
            "datasets": [{
                "label": f"Assessment on {assessment.timestamp.strftime('%Y-%m-%d')}",
                "data": [dimensions[label] or 0 for label in dimensions.keys()], 
                "backgroundColor": "rgba(123,93,189,0.2)",
                "borderColor": "rgba(123,93,189,1)",
                "pointBackgroundColor": "rgba(123,93,189,1)"
            }]
        }
    except Exception as e:
        flash(f"Error preparing results data: {e}", "error")
        print(f"Error in assessment_results: {e}")
        # Keep defaults set above

    return render_template(
        'results.html',
        assessment=assessment,
        system=system,
        radar_data=json.dumps(radar_data),
        maturity_level=(overall_level_num, overall_level_name, overall_level_desc), # Overall level
        dimension_levels=dimension_levels # Pass dimension levels dict
    )



@main.route('/dashboard')
def dashboard():
    #Main dashboard showing system overview, latest assessments, and financial summary.
    systems_data = []
    latest_assessment_ids = [] # To calculate total unique assessments shown
    security_scores = []
    overall_scores = []
    total_system_count = 0

    try:
        systems = System.query.order_by(System.name).all()
        total_system_count = len(systems)

        for system in systems:
            latest_assessment = Assessment.query.filter_by(system_id=system.id)\
                                            .order_by(Assessment.timestamp.desc())\
                                            .first()
            systems_data.append({
                'system': system,
                'latest_assessment': latest_assessment
            })
            if latest_assessment:
                latest_assessment_ids.append(latest_assessment.id)
                if latest_assessment.security_score is not None:
                    security_scores.append(latest_assessment.security_score)
                if latest_assessment.overall_score is not None:
                    overall_scores.append(latest_assessment.overall_score)

        # Calculate averages safely
        avg_security_score = round(sum(security_scores) / len(security_scores), 1) if security_scores else None
        avg_overall_score = round(sum(overall_scores) / len(overall_scores), 1) if overall_scores else None
        total_assessments_count = len(set(latest_assessment_ids)) # Count unique latest assessments

        # Financial data
        financial_assessments = FinancialSecurityAssessment.query.order_by(
            FinancialSecurityAssessment.created_at.desc()
        ).all()
        total_financial_count = len(financial_assessments)

        fin_scores = [fsa.calculate_financial_score() for fsa in financial_assessments if fsa.calculate_financial_score() is not None]
        avg_financial_score = round(sum(fin_scores) / len(fin_scores), 1) if fin_scores else None

    except Exception as e:
        flash(f"Error loading dashboard data: {e}", "error")
        print(f"Error in dashboard route: {e}")
        # Set defaults on error
        systems_data = []
        financial_assessments = []
        total_system_count = 0
        total_assessments_count = 0
        avg_security_score = None
        avg_overall_score = None
        total_financial_count = 0
        avg_financial_score = None


    return render_template(
        'dashboard.html',
        systems_data=systems_data, # Pass the combined list
        financial_assessments=financial_assessments,
        # Pass summary stats
        total_system_count=total_system_count,
        total_assessments_count=total_assessments_count,
        avg_security_score=avg_security_score,
        avg_overall_score=avg_overall_score,
        total_financial_count=total_financial_count,
        avg_financial_score=avg_financial_score
    )

    

@main.route('/api/assessment/<int:assessment_id>')
def api_assessment(assessment_id):
    #API endpoint to get assessment data for charts
    assessment = Assessment.query.get_or_404(assessment_id)
    return jsonify(assessment.to_dict())

@main.route('/api/system/<int:system_id>/history')
def api_system_history(system_id):
    #API endpoint to get assessment history for a system
    assessments = Assessment.query.filter_by(system_id=system_id).order_by(Assessment.timestamp).all()
    return jsonify([a.to_dict() for a in assessments])

@main.route('/assessment/<int:assessment_id>/pdf')
def generate_pdf(assessment_id):
    #Generate and download a PDF report for an assessment
    assessment = Assessment.query.get_or_404(assessment_id)
    system = System.query.get(assessment.system_id)
    
    pdf_path = generate_pdf_report(assessment, system)
    return send_file(pdf_path, as_attachment=True, download_name=f"{system.name}_assessment_{assessment.id}.pdf")

@main.route('/assessment/<int:assessment_id>/csv')
def export_csv(assessment_id):
    #Export assessment data as CSV
    assessment = Assessment.query.get_or_404(assessment_id)
    system = System.query.get(assessment.system_id)
    
    csv_path = generate_csv_export(assessment, system)
    return send_file(csv_path, as_attachment=True, download_name=f"{system.name}_assessment_{assessment.id}.csv")



@main.route('/system/<int:system_id>/compare', methods=['GET', 'POST'])
def compare_assessments(system_id):
    #Compare multiple maturity assessments for a system
    system = System.query.get_or_404(system_id)

    # POST Request Logic 
    if request.method == 'POST':
        assessment_ids = request.form.getlist('assessment_ids') # Get list of selected IDs

        # Handle if nothing was selected
        if not assessment_ids:
            flash('Please select at least one assessment to compare or view.', 'error')
            return redirect(url_for('main.compare_assessments', system_id=system_id))

        try:
            if len(assessment_ids) == 1:
                flash('Showing results for the selected assessment.', 'info')
                return redirect(url_for('main.assessment_results', assessment_id=int(assessment_ids[0])))
            else:
                # Logic for Comparing 2+ Assessments
                radar_data = {
                    "labels": ["Security", "Financial", "Operational", "Governance", "Technical Debt"],
                    "datasets": []
                }
                assessments_to_compare = []
                valid_ids_count = 0
                for aid in assessment_ids:
                    try:
                        assessment_id_int = int(aid)
                        a = Assessment.query.get(assessment_id_int)
                        # Ensure assessment exists and belongs to the correct system
                        if a and a.system_id == system_id:
                            assessments_to_compare.append(a)
                            valid_ids_count += 1
                            label = f"{a.timestamp.strftime('%Y-%m-%d')} (ID={a.id})"
                            dataset = {
                                "label": label,
                                "data": [ a.security_score or 0, a.financial_score or 0, a.operational_score or 0, a.governance_score or 0, a.technical_debt_score or 0 ],
                                "fill": True
                            }
                            radar_data["datasets"].append(dataset)
                    except ValueError:
                        flash(f"Invalid assessment ID format received: {aid}", "warning")
                        continue # Skip invalid IDs

                # Check if enough valid assessments were found for comparison
                if valid_ids_count < 2:
                    flash('Please select at least two valid assessments belonging to this system to compare.', 'warning')
                    return redirect(url_for('main.compare_assessments', system_id=system_id))

                # Sort assessments and datasets for consistency
                assessments_to_compare.sort(key=lambda x: x.timestamp)
                radar_data["datasets"].sort(key=lambda x: x["label"])

                comparison_data = json.dumps(radar_data)
                return render_template('compare.html',
                                    assessments=assessments_to_compare,
                                    comparison_data=comparison_data,
                                    system=system)

        except Exception as e:
            flash(f"An error occurred while processing your request: {e}", "error")
            print(f"Error in compare_assessments POST: {e}")
            # Redirect back to selection form on general error
            return redirect(url_for('main.compare_assessments', system_id=system_id))
    


    assessments_with_levels = []
    try:
        all_assessments_query = Assessment.query.filter_by(system_id=system_id)\
                                        .order_by(Assessment.timestamp.desc())\
                                        .all()

        for assessment in all_assessments_query:
            level_num, level_name, _ = get_maturity_level(assessment.overall_score)
            assessments_with_levels.append({
                'assessment': assessment,
                'level_num': level_num,
                'level_name': level_name
            })
    except Exception as e:
        flash(f"Error loading assessment history: {e}", "error")
        print(f"Error in compare_assessments GET: {e}")
        assessments_with_levels = [] # Pass empty list on error

    # Pass the enhanced list to the template
    return render_template('compare_form.html',
                        assessments_data=assessments_with_levels,
                        system=system)



@main.route('/save-section', methods=['POST'])
def save_section():
    data = request.json
    section = data.get('section')
    responses = data.get('responses')
    
    try:
        # Store in session for now (you might want to store in database instead)
        if 'assessment_data' not in session:
            session['assessment_data'] = {}
        
        session['assessment_data'][section] = responses
        
        return jsonify({
            'success': True,
            'message': f'{section.capitalize()} section saved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@main.route('/financial-security', methods=['GET', 'POST'])
def financial_security():
    # Create or update an organisation-wide Financial Security Assessment
    form = FinancialSecurityForm()
    if form.validate_on_submit():
        fsa = FinancialSecurityAssessment(
            annual_security_budget=form.annual_security_budget.data,
            planned_security_investment=form.planned_security_investment.data,
            security_staff_training=form.security_staff_training.data,
            annual_revenue=form.annual_revenue.data,
            potential_fine=form.potential_fine.data,
            potential_breach_cost=form.potential_breach_cost.data,
            downtime_cost_per_hour=form.downtime_cost_per_hour.data,
            average_downtime_hours=form.average_downtime_hours.data,
            acceptable_risk_level=form.acceptable_risk_level.data,
            has_cyber_insurance=form.has_cyber_insurance.data,
            cyber_insurance_coverage=form.cyber_insurance_coverage.data
        )
        db.session.add(fsa)
        db.session.commit()

        flash("Financial Security Assessment saved!", "success")
        return redirect(url_for('main.view_financial_security', assessment_id=fsa.id))
    return render_template('financial_security.html', form=form)


@main.route('/financial-security/<int:assessment_id>')
def view_financial_security(assessment_id):
    #Display the results of a specific Financial Security Assessment.
    fsa = FinancialSecurityAssessment.query.get_or_404(assessment_id)
    score = None
    fin_level_num = None # Default value
    fin_level_name = "N/A" # Default value

    try:
        score = fsa.calculate_financial_score()
        if score is not None:
            # Calculate level info in the route 
            level_num, level_name, _ = get_maturity_level(score) # Get level, name, desc
            fin_level_num = level_num
            fin_level_name = level_name
    except Exception as e:
        flash(f"Error calculating financial score or level: {e}", "error")
        print(f"Error calculating score/level for FSA ID {assessment_id}: {e}")

    # Pass the calculated level info to the template 
    return render_template(
        'financial_security_results.html',
        assessment=fsa,
        score=score,
        fin_level_num=fin_level_num,
        fin_level_name=fin_level_name
    )



@main.route(
    "/system/<int:system_id>/assessment/<int:assessment_id>/recommendations"
)
@main.route("/system/<int:system_id>/assessment/<int:assessment_id>/recommendations")
def recommendations(system_id, assessment_id):
    #Displays the critical/high/medium/low recommendations, the timeline,

    system = System.query.get_or_404(system_id)
    assessment = Assessment.query.get_or_404(assessment_id)

    financial_assessment = (
        FinancialSecurityAssessment.query
        .order_by(FinancialSecurityAssessment.created_at.desc())
        .first()
    )

    level_num = None
    level_name = "Unknown"
    level_desc = ""
    if assessment.overall_score is not None: # Check if score exists
        try:
            # Call the function which returns 3 values
            lvl, name, desc = get_maturity_level(assessment.overall_score)
            level_num = lvl
            level_name = name
            level_desc = desc 
        except Exception as e:
            # Log error if something unexpected happens in get_maturity_level
            print(f"Error getting maturity level: {e}")
            # Keep default values (None, "Unknown", "")
            pass

    # Unpack return values 
    recs, timeline, financial_metrics = generate_recommendations_with_timeline(
        assessment, financial_assessment
    )

    return render_template(
        "recommendations.html",
        system=system,
        assessment=assessment,
        financial_assessment=financial_assessment,
        recommendations=recs,
        timeline=timeline,
        # Pass calculated maturity level info
        maturity_level_num=level_num,
        maturity_level_name=level_name,
        # Pass calculated financial metrics
        budget_adequacy_ratio=financial_metrics.get("budget_adequacy_ratio"),
        insurance_adequacy_ratio=financial_metrics.get("insurance_adequacy_ratio"),
        is_insurance_inadequate=financial_metrics.get("is_insurance_inadequate", False)
    )



@main.app_template_filter('format_number')
def format_number(value):
    return "{:,.2f}".format(value)

@main.route('/system/<int:system_id>/assessment/<int:assessment_id>/report')
def generate_report(system_id, assessment_id):
    system = System.query.get_or_404(system_id)
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Get the most recent financial assessment
    financial_assessment = FinancialSecurityAssessment.query.order_by(
        FinancialSecurityAssessment.created_at.desc()
    ).first()
    
    # Use generate_pdf_with_recommendations
    pdf_path = generate_pdf_with_recommendations(assessment, system, financial_assessment)
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"{system.name}_assessment_{assessment.id}.pdf"
    )

@main.route('/choose-recommendation')
def choose_recommendation():
    systems = System.query.all()
    return render_template('choose_recommendation.html', systems=systems)


@main.route('/redirect-to-latest-assessment')
def redirect_to_latest_assessment():
    system_id = request.args.get('system_id', type=int)
    if not system_id:
        flash("Please choose a system.")
        return redirect(url_for('main.choose_recommendation'))
    
    latest_assessment = Assessment.query.filter_by(system_id=system_id).order_by(Assessment.timestamp.desc()).first()
    if not latest_assessment:
        flash("No assessments found for the selected system. Please create an assessment first.")
        return redirect(url_for('main.view_system', system_id=system_id))
    
    return redirect(url_for('main.recommendations', system_id=system_id, assessment_id=latest_assessment.id))

# financial exports 
@main.route("/financial-security/<int:assessment_id>/pdf")
def financial_pdf(assessment_id):
    fsa = FinancialSecurityAssessment.query.get_or_404(assessment_id)
    pdf_path = generate_financial_pdf_report(fsa)
    return send_file(pdf_path, as_attachment=True, download_name=f"financial_assessment_{assessment_id}.pdf")

@main.route("/financial-security/<int:assessment_id>/csv")
def financial_csv(assessment_id):
    fsa = FinancialSecurityAssessment.query.get_or_404(assessment_id)
    csv_path = generate_financial_csv_export(fsa)
    return send_file(csv_path, as_attachment=True, download_name=f"financial_assessment_{assessment_id}.csv")


# combined CSV (maturity + financial + recs)
@main.route("/system/<int:system_id>/assessment/<int:assessment_id>/combined_csv")
def combined_csv(system_id, assessment_id):
    system = System.query.get_or_404(system_id)
    assessment = Assessment.query.get_or_404(assessment_id)

    # latest org-wide financial assessment
    financial_assessment = FinancialSecurityAssessment.query.order_by(
        FinancialSecurityAssessment.created_at.desc()
    ).first()

    recs, _, _ = generate_recommendations_with_timeline(assessment, financial_assessment)

    csv_path = generate_combined_csv(assessment, system,
                                    financial_assessment, recs)
    return send_file(csv_path,
                    as_attachment=True,
                    download_name=f"{system.name}_assessment_{assessment.id}_combined.csv")



@main.route('/maturity-levels')
def maturity_levels_explained():
    #Displays a page explaining the different maturity levels.

    return render_template('maturity_levels.html', levels=MATURITY_LEVELS)

@main.route('/scoring-methodology')
def scoring_methodology():
    return render_template('scoring_methodology.html')

@main.route('/recommendations-explained')
def recommendations_explained():
    return render_template('recommendations_explained.html')

@main.route('/about')
def about():
    version = "1.0 (Prototype)"
    date = "April 2025"
    return render_template('about.html', version=version, date=date)