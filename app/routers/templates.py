from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Literal
import shutil
import os

from app.services.template_service import save_template

router = APIRouter()

TemplateType = Literal["daily", "monday", "weekend"]

@router.post("/templates/{template_type}")
async def replace_template(
    template_type: TemplateType,
    file: UploadFile = File(...)
):
    """
    Replace a template image for motivational quotes.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    try:
        result = await save_template(template_type, file)
        return {"message": f"Template {template_type} updated successfully", "path": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )