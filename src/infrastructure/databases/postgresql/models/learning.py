from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from ..base import Base


class Folder(Base):
    __tablename__ = "folders"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="folders")

    themes: Mapped[List["Theme"]] = relationship(back_populates="folder", cascade="all, delete-orphan")


class Theme(Base):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(50))

    folder_id: Mapped[int] = mapped_column(ForeignKey("folders.id"))
    folder: Mapped["Folder"] = relationship(back_populates="themes")

    quiz_items: Mapped[List["QuizItem"]] = relationship(
        back_populates="theme",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    memorize_items: Mapped[List["MemorizeItem"]] = relationship(
        back_populates="theme",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class QuizItem(Base):
    __tablename__ = "quiz_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String)
    answers: Mapped[List[str]] = mapped_column(ARRAY(String))
    true_answer: Mapped[str] = mapped_column(String)

    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id", ondelete="CASCADE"))
    theme: Mapped["Theme"] = relationship(back_populates="quiz_items")


class MemorizeItem(Base):
    __tablename__ = "memorize_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(100))
    translate: Mapped[str] = mapped_column(String(100))
    transcription: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id", ondelete="CASCADE"))
    theme: Mapped["Theme"] = relationship(back_populates="memorize_items")