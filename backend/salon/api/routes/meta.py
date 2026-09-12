"""Non-secret build/runtime metadata."""

from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel

from salon import __version__


class MetaResponse(BaseModel):
    name: str
    version: str
    environment: str
    verification_adapter: str
    payment_adapter: str


router = APIRouter(tags=["meta"])


@router.get("/meta", response_model=MetaResponse)
def meta(request: Request) -> MetaResponse:
    settings = request.app.state.settings
    data = settings.build_metadata()
    return MetaResponse(name="sotto-salon", version=__version__, **data)
