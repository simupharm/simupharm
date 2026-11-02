"""Database Models — Users, Experiments, Progress, Quiz Results, Subscriptions, Usage"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    institution = Column(String(255), default="")
    role = Column(String(50), default="student")  # student, instructor, admin
    created_at = Column(DateTime, default=datetime.utcnow)

    # Email verification
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)

    # Password reset
    password_reset_token = Column(String(255), nullable=True)
    password_reset_token_expires = Column(DateTime, nullable=True)

    # Subscription / Billing
    plan = Column(String(50), default="free")  # free, pro, institution
    razorpay_customer_id = Column(String(255), nullable=True, unique=True)
    razorpay_subscription_id = Column(String(255), nullable=True)
    plan_expires_at = Column(DateTime, nullable=True)
    daily_simulation_count = Column(Integer, default=0)
    last_simulation_date = Column(String(10), nullable=True)  # YYYY-MM-DD for daily reset

    experiments = relationship("Experiment", back_populates="user")
    quiz_results = relationship("QuizResult", back_populates="user")
    progress = relationship("Progress", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    instrument = Column(String(50), nullable=False)
    compound_name = Column(String(255), default="")
    parameters = Column(JSON, default={})
    results = Column(JSON, default={})
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="experiments")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    instrument = Column(String(50), default="general")
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, default=0)
    time_taken_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_results")


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    instrument = Column(String(50), nullable=False)
    mastery_level = Column(Float, default=0.0)
    time_spent_minutes = Column(Integer, default=0)
    simulations_run = Column(Integer, default=0)
    concept_mastery_json = Column(JSON, default={})  # Per-concept mastery for adaptive learning
    events_json = Column(JSON, default=[])  # Learning event history
    last_accessed = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress")


class Subscription(Base):
    """Tracks subscription billing history and lifecycle events."""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    razorpay_subscription_id = Column(String(255), nullable=True)
    razorpay_checkout_session_id = Column(String(255), nullable=True)
    plan = Column(String(50), nullable=False)  # pro, institution_starter, institution_standard, etc.
    status = Column(String(50), nullable=False, default="pending")  # pending, active, canceled, past_due, expired
    billing_period = Column(String(20), default="monthly")  # monthly, semester, annual
    amount = Column(Integer, default=0)  # Amount in smallest currency unit (paise for INR)
    currency = Column(String(3), default="INR")
    started_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")
