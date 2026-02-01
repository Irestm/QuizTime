from typing import List, Optional, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

def ensure_gte_zero(value: int) -> int:
    if value < 0:
        return 0
    return value

class Pagination(BaseModel):
    limit: int = Field(10, le=100)
    offset: int = Field(0, ge=0)

# --- USER MODELS ---

class UserLoginSchema(BaseModel):
    username: str
    password: str

class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    biography: Optional[str] = None

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    biography: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# --- LEARNING MODELS ---

class QuizItemSchema(BaseModel):
    question: str
    answers: List[str]
    true_answer: str

    model_config = ConfigDict(from_attributes=True)

class MemorizeItemSchema(BaseModel):
    word: str
    translate: str
    transcription: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ThemeBase(BaseModel):
    title: str
    type: Literal['Memorize', 'Quiz']

class ThemeCreate(ThemeBase):
    quiz_items: Optional[List[QuizItemSchema]] = None
    memorize_items: Optional[List[MemorizeItemSchema]] = None

class ThemeUpdate(BaseModel):
    title: Optional[str] = None


class ThemeResponse(ThemeBase):
    id: int
    folder_id: int
    quiz_items: List[QuizItemSchema] = []
    memorize_items: List[MemorizeItemSchema] = []

    model_config = ConfigDict(from_attributes=True)

class FolderCreate(BaseModel):
    title: str
    description: Optional[str] = None


class FolderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class FolderResponse(FolderCreate):
    id: int
    themes: List[ThemeResponse] = []

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str