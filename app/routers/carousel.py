from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import os
import zipfile
import io

from app.services.carousel_service import generate_carousel_images

router = APIRouter()

@router.post("/carousel")
async def create_carousel(
    file: UploadFile = File(...),  # this should be given as multipart/form-data
    bg_color: str = "green"  # this should be given as parameter, if given on body it will take the default value "green"
):
    """
    Generate carousel images from a text file and return a zip file.
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="File must be a .txt file")
    
    if bg_color not in ["green", "yellow"]:
        raise HTTPException(status_code=400, detail="Background color must be either 'green' or 'yellow'")

    print("bg_color", bg_color)
    
    try:
        image_paths = await generate_carousel_images(file, bg_color)

        # Create an in-memory zip buffer
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for image_path in image_paths:
                filename = os.path.basename(image_path)
                zipf.write(image_path, arcname=filename)
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": "attachment; filename=carousel_images.zip"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
