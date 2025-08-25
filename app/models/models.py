from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    photos: Mapped[list["UserPhoto"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sessions: Mapped[list["TryOnSession"]] = relationship(back_populates="user")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="user")


class UserPhoto(Base):
    photo_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"), index=True)
    image_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="photos")
    sessions: Mapped[list["TryOnSession"]] = relationship(back_populates="photo")


class Outfit(Base):
    outfit_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    image_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    meta: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    sessions: Mapped[list["TryOnSession"]] = relationship(back_populates="outfit")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="outfit")
    model3d: Mapped[Optional["Outfit3D"]] = relationship(back_populates="outfit", uselist=False, cascade="all, delete-orphan")


class TryOnSession(Base):
    session_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"), index=True)
    photo_id: Mapped[int] = mapped_column(ForeignKey("userphoto.photo_id", ondelete="SET NULL"), nullable=True, index=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfit.outfit_id", ondelete="SET NULL"), nullable=True, index=True)
    result_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="sessions")
    photo: Mapped["UserPhoto"] = relationship(back_populates="sessions")
    outfit: Mapped["Outfit"] = relationship(back_populates="sessions")


class Recommendation(Base):
    __table_args__ = (
        UniqueConstraint("user_id", "outfit_id", name="uq_recommendation_user_outfit"),
    )

    rec_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"), index=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfit.outfit_id", ondelete="CASCADE"), index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="recommendations")
    outfit: Mapped["Outfit"] = relationship(back_populates="recommendations")


class Outfit3D(Base):
    __table_args__ = (
        UniqueConstraint("outfit_id", name="uq_outfit3d_outfit"),
    )

    model_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    outfit_id: Mapped[int] = mapped_column(ForeignKey("outfit.outfit_id", ondelete="CASCADE"), nullable=False, index=True)
    file_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    format: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    outfit: Mapped["Outfit"] = relationship(back_populates="model3d")

