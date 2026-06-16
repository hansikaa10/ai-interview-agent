# report_generator.py
from fpdf import FPDF

def generate_pdf_transcript(state):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Get the exact printable width dynamically (usually 190mm on A4)
    full_width = pdf.epw 
    
    # --- Document Header Title ---
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 41, 59) # Deep slate blue
    pdf.cell(full_width, 15, "AI Interview Performance Report", align="C", ln=1)
    pdf.ln(5)
    
    # --- Profile Summary Metadata ---
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(full_width, 6, f"Achieved Track Difficulty: {state.get('difficulty', 'easy').upper()}", ln=1)
    
    skills_list = ", ".join(state.get("resume_skills", [])) if state.get("resume_skills") else "None Detected"
    pdf.cell(full_width, 6, f"Target Candidate Skills: {skills_list}", ln=1)
    pdf.ln(8)
    
    # --- Matrix Metrics Section ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(full_width, 8, "Topic Assessment Matrix Overview", ln=1)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + full_width, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    
    strong_str = ", ".join([f"{k} ({v}x)" for k, v in state.get("strong_topics", {}).items() if v > 0])
    weak_str = ", ".join([f"{k} ({v}x)" for k, v in state.get("weak_topics", {}).items() if v > 0])
    
    pdf.multi_cell(full_width, 6, f"Demonstrated Proficiencies: {strong_str if strong_str else 'None recorded yet.'}")
    pdf.multi_cell(full_width, 6, f"Flagged Growth Areas: {weak_str if weak_str else 'None recorded yet.'}")
    pdf.ln(6)
    
    # --- Chronological Timeline Logs ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(full_width, 8, "Detailed Question & Evaluation Log Timeline", ln=1)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + full_width, pdf.get_y())
    pdf.ln(5)
    
    for idx, entry in enumerate(state.get("history", []), 1):
        # Round Header
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(37, 99, 235) # Vibrant Blue
        pdf.cell(full_width, 6, f"Round {idx}: Focus Category -> [{entry['topic'].upper()}]", ln=1)
        
        # Question Posed
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(full_width, 5, f"Question Posed: \"{entry['question']}\"")
        pdf.ln(1)
        
        # Scores & Grades (Split cleanly into exact column widths)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(60, 6, f"Assigned Score: {entry['score']} / 5")
        pdf.cell(60, 6, f"Calculated Grade Level: {entry['grade']}", ln=1)
        pdf.ln(4) # Spacing before the next card block
        
    return pdf.output()
