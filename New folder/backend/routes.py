from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    name: str
    address: str
    details: str


@router.get("/")
def root():
    return {
        "application": "LegalEase",
        "version": "1.0.0",
        "status": "running",
        "message": "LegalEase API is running."
    }


@router.get("/api/health")
def health():
    return {
        "status": "OK"
    }


@router.post("/api/generate-document")
def generate_document(request: DocumentRequest):
    document = f"""
LEGAL DOCUMENT

Document Type: {request.document_type}

Name: {request.name}

Address: {request.address}

Details:
{request.details}

This document was generated using LegalEase.
"""

    return {
        "status": "success",
        "document": document
    }