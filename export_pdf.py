import os
import textwrap
from fpdf import FPDF

def export_logs():
    log_file = 'suspicious_events.log'
    
    if not os.path.exists(log_file):
        print("Log file not found!")
        return

    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    sessions = {}
    current_session = None

    for line in lines:
        line = line.strip()
        if not line: continue
        
        if "SECTION START: SESSION" in line:
            try:
                current_session = int(line.split("SESSION")[1].split("*")[0].strip())
                sessions[current_session] = []
            except: continue
            
        if current_session is not None:
            sessions[current_session].append(line)

    if not sessions:
        print("No valid sessions found.")
        return

    print("\n" + "="*30 + "\n LOG EXPORT TOOL \n" + "="*30)
    for sec_num in sorted(sessions.keys()):
        print(f" - Session {sec_num}")
    
    choice = input("\nSession number (or 'all'): ").strip().lower()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, text="AI Proctoring System - Log Report", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", size=10)

    # Function to safely add lines to PDF
    def add_safe_lines(line_list):
        for line in line_list:
            # We manually wrap the text to 80 characters 
            # This prevents the "Not enough horizontal space" error
            wrapped_lines = textwrap.wrap(line, width=80)
            if not wrapped_lines: # For empty lines/spacing
                pdf.ln(5)
                continue
            for w_line in wrapped_lines:
                pdf.cell(0, 6, text=w_line, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1) # Tiny gap between log entries

    export_filename = "Proctoring_Report.pdf"

    if choice == 'all':
        export_filename = "Complete_Proctoring_Logs.pdf"
        for sec_num in sorted(sessions.keys()):
            add_safe_lines(sessions[sec_num])
            pdf.ln(10)
    elif choice.isdigit() and int(choice) in sessions:
        sec_num = int(choice)
        export_filename = f"Session_{sec_num}_Logs.pdf"
        add_safe_lines(sessions[sec_num])
    else:
        print("Invalid choice.")
        return

    pdf.output(export_filename)
    print(f"\nSUCCESS: Logs exported to '{export_filename}'")

if __name__ == "__main__":
    export_logs()