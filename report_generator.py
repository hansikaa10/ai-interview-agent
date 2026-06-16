# report_generator.py
from fpdf import FPDF

def generate_pdf_transcript(state):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- Document Header Title ---
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 41, 59) # Deep dark blue/slate
    pdf.cell(0, 15, "AI Interview Performance Report", ln=True, align="C")
    pdf.ln(5)
    
    # --- Profile Summary Metadata ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 7, f"Achieved Track Difficulty: {state.get('difficulty', 'easy').upper()}", ln=True)
    
    skills_list = ", ".join(state.get("resume_skills", [])) if state.get("resume_skills") else "None Detected"
    pdf.cell(0, 7, f"Target Candidate Skills: {skills_list}", ln=True)
    pdf.ln(6)
    
    # --- Matrix Metrics Section ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Topic Assessment Matrix Overview", ln=True)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(51, 65, 85)
    
    # Multi-line strings for strong and weak topic dictionary dumps
    strong_str = ", ".join([f"{k} ({v}x)" for k, v in state.get("strong_topics", {}).items() if v > 0])
    weak_str = ", ".join([f"{k} ({v}x)" for k, v in state.get("weak_topics", {}).items() if v > 0])
    
    pdf.multi_cell(0, 6, f"Demonstrated Proficiencies: {strong_str if strong_str else 'None recorded yet.'}")
    pdf.multi_cell(0, 6, f"Flagged Growth Areas: {weak_str if weak_str else 'None recorded yet.'}")
    pdf.ln(8)
    
    # --- Chronological Timeline Logs ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Detailed Question & Evaluation Log Timeline", ln=True)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(4)
    
    for idx, entry in enumerate(state.get("history", []), 1):
        # Card Header block background coloring simulation
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(37, 99, 235) # Vibrant Blue
        pdf.cell(0, 7, f"Round {idx}: Focus Category -> [{entry['topic'].upper()}]", ln=True)
        
        pdf.set_font("Helvetica", "I", 11)
        pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(0, 6, f"Question Posed: \"{entry['question']}\"")
        
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(40, 6, f"Assigned Score: {entry['score']} / 5")
        pdf.cell(0, 6, f"Calculated Grade Level: {entry['grade']}", ln=True)
        pdf.ln(4)
        
    # Return output string binary stream buffer safely for the browser download prompt
    return pdf.output()
