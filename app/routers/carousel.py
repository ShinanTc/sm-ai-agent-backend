from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os

from app.services.carousel_service import generate_carousel_images

router = APIRouter()

@router.post("/carousel")
async def create_carousel(
    file: UploadFile = File(...),
    bg_color: str = "green"
):
    """
    Generate carousel images from a text file.
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(
            status_code=400,
            detail="File must be a .txt file"
        )
    
    if bg_color not in ["green", "yellow"]:
        raise HTTPException(
            status_code=400,
            detail="Background color must be either 'green' or 'yellow'"
        )
    
    try:
        image_paths = await generate_carousel_images(file, bg_color)
        return {"message": "Carousel generated successfully", "images": image_paths}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )