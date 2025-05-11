from fastapi import UploadFile
import os
import shutil

TEMPLATE_PATHS = {
    "daily": "templates/motivation-quotes/generic.png",
    "monday": "templates/motivation-quotes/freakin-monday.png",
    "weekend": "templates/motivation-quotes/weekend-mode.png"
}

async def save_template(template_type: str, file: UploadFile) -> str:
    """
    Save an uploaded template file to the appropriate location.
    """
    if template_type not in TEMPLATE_PATHS:
        raise ValueError(f"Invalid template type: {template_type}")
    
    template_path = TEMPLATE_PATHS[template_type]
    os.makedirs(os.path.dirname(template_path), exist_ok=True)
    
    try:
        with open(template_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return template_path
    finally:
        file.file.close()
    
    return template_path