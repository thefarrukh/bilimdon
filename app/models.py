from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, Date, Integer, Boolean, ForeignKey
from datetime import datetime, date, timezone
from typing import Optional, List
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    birthdate: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str] = mapped_column(String(50), default="user")

    owned_games: Mapped[List["Game"]] = relationship("Game", back_populates="owner")
    submissions: Mapped[List["Submission"]] = relationship("Submission", back_populates="owner")


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id"))
    # score: Mapped[int] = mapped_column(Integer, default=0)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="owned_games")
    questions: Mapped[List["GameQuestion"]] = relationship("GameQuestion", back_populates="game")


class GameQuestion(Base):
    __tablename__ = "game_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"))
    score: Mapped[int] = mapped_column(Integer, default=0)

    question: Mapped["Question"] = relationship("Question", back_populates="games")
    game: Mapped["Game"] = relationship("Game", back_populates="questions")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    option_ids: Mapped[List["Option"]] = relationship("Option", back_populates="question")
    games: Mapped[List["GameQuestion"]] = relationship("GameQuestion", back_populates="question")
    submissions: Mapped[List["Submission"]] = relationship("Submission", back_populates="question")


class Participation(Base):
    __tablename__ = "participations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    gained_score: Mapped[int] = mapped_column(Integer, default=0)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))


class Option(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"))
    title: Mapped[str] = mapped_column(String(100))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    question = relationship("Question", back_populates="option_ids")
    submissions: Mapped[List["Submission"]] = relationship("Submission", back_populates="option")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"))
    option_id: Mapped[int] = mapped_column(Integer, ForeignKey("options.id"))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    owner = relationship("User", back_populates="submissions")
    question = relationship("Question", back_populates="submissions")
    option = relationship("Option", back_populates="submissions")
