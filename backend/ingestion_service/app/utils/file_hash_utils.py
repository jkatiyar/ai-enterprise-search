# app/utils/file_hash_utils.py

import hashlib

def generate_file_hash(file_path: str) -> str:
    """
    Generate a stable document ID based on file content.
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()
