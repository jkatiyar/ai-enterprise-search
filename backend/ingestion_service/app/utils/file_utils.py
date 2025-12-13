import os

UPLOAD_DIR = "uploaded_files"

# Create directory if not exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_temp_file(file):
    """Save uploaded file temporarily."""
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    
    return file_path
