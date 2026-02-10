from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from datetime import datetime, timezone
from app.schemas.pdf import PdfUploadResponse
from app.services.pdf_service import start_pdf_indexing
from app.api.dep import get_current_user
from app.models.users import User

router = APIRouter(prefix="/rooms", tags=["PDF"])


@router.post("/{room_id}/upload", response_model=PdfUploadResponse)
async def upload_pdf(
    room_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    await start_pdf_indexing(
        room_id=room_id,
        user_id=current_user.id,
        file=file,
    )

    return PdfUploadResponse(
        message="Indexing started",
        room_id=room_id,
        file_name=file.filename,
        indexing_started_at=datetime.now(timezone.utc),
    ) 
