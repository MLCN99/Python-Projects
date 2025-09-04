from datetime import datetime, timedelta
from pathlib import Path
from pypdf import PdfWriter

# --- Setup logging ---
def log(message):
    """Log to console and file"""
    print(message)
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Log file path (daily log file)
log_dir = Path.cwd() / "Logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / f"log_{datetime.now().strftime('%d%m%Y')}.txt"
log_file = open(log_path, "a", encoding="utf-8")

# --- Main Script ---
current_date = datetime.now().date()
formatted_date = current_date.strftime("%d%m%Y")  # Example: 02092025

target_path = Path.cwd() / "Folders-To-Merge" / formatted_date
merge_pdf = PdfWriter()

if target_path.exists():
    log("Folder with current date exists.")
    file_index = 1

    for file in target_path.iterdir():
        if file.is_file() and file.suffix.lower() == ".pdf":
            log(f"   Found PDF ({file_index}): {file}")
            merge_pdf.append(str(file))
            file_index += 1

    if file_index > 1:  # At least one PDF found
        merge_path = target_path / f"Merged-{formatted_date}.pdf"
        merge_pdf.write(str(merge_path))
        merge_pdf.close()

        if merge_path.exists():
            log(f"PDFs merged successfully: {merge_path}")
        else:
            log(f"An issue occurred, merged file not found: {merge_path}")

        # Create tomorrow's folder
        tomorrow_date = current_date + timedelta(days=1)
        tomorrow_folder = Path.cwd() / "Folders-To-Merge" / tomorrow_date.strftime("%d%m%Y")
        tomorrow_folder.mkdir(parents=True, exist_ok=True)
        log(f"Prepared folder for tomorrow: {tomorrow_folder}")
    else:
        log(f"No PDF files found in {target_path}. Nothing to merge.")

else:
    # If today's folder doesn't exist, create it
    target_path.mkdir(parents=True, exist_ok=True)
    log(f"Folder for today did not exist, so it was created: {target_path}")
    log("Please place your PDFs inside this folder and re-run the script.")

# --- Close log file ---
log_file.close()
