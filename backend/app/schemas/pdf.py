from pydantic import BaseModel
from datetime import datetime


class PdfUploadResponse(BaseModel):
    message: str
    room_id: int
    file_name: str
    indexing_started_at: datetime
