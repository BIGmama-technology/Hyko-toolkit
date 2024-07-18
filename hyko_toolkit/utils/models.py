from pydantic import BaseModel, Field


class Body(BaseModel):
    document_id: str = Field(alias="documentId")


class CreateResponse(BaseModel):
    success: bool
    body: Body


class Response(BaseModel):
    success: bool
    body: str
