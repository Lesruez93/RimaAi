"""Scan router — server-side fallback inference for crop/livestock images."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.scan import ScanHistory
from app.schemas.scan import ScanResult
from app.services.inference import run_inference

router = APIRouter(prefix="/scan", tags=["scan"])


@router.post("", response_model=ScanResult)
async def scan_image(
    file: UploadFile = File(..., description="Crop or livestock photo"),
    scan_type: str = Form("crop"),
    language: str = Form("en"),
    farmer_id: int | None = Form(None),
    db: Session = Depends(get_db),
) -> ScanResult:
    """Classify an uploaded image and return trilingual treatment advice.

    This is the *fallback* path for devices that cannot run the on-device TFLite
    model; on-device scans do not hit the network. The result is stored in
    ``scan_history`` for the farmer's records and offline sync.
    """
    image_bytes = await file.read()
    result = run_inference(image_bytes, scan_type=scan_type, language=language)
    db.add(
        ScanHistory(
            farmer_id=farmer_id,
            scan_type=result.scan_type,
            label=result.label,
            confidence=result.confidence,
            advice=result.advice,
            source="server",
        )
    )
    db.commit()
    return result
