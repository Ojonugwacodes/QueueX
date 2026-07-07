from datetime import datetime, timezone

from typing import Optional
from app.database import Base
from sqlalchemy.dialects.postgresql import JSONB, UUID
import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, DateTime
import uuid


class ServiceType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    ACCOUNT_ENQUIRY = "account_enquiry"
    LOAN = "loan"
    ACCOUNT_OPENING = "account_opening"
    

class QueueStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    QUEUED = "queued"
    COMPLETED = "completed"
    RUNNING = "running"
    CANCELLED = "cancelled"
    RETRYING = "retrying"

class Priority(str, enum.Enum):
    PREMIUM = "premium"
    SENIOR = "senior"
    REGULAR = "regular"

class Customer(Base):
    __tablename__= "customers"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))

class Teller(Base):
    __tablename__= "tellers"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    counter_number: Mapped[int] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))

class Queue_entries(Base):
    __tablename__= "queue_entries"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    teller_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("tellers.id"), nullable=True)
    service_type: Mapped[ServiceType] = mapped_column(String(20), nullable=False)
    priority: Mapped[Priority] = mapped_column(String(20), nullable=False)
    status: Mapped[QueueStatus] = mapped_column(String(20), nullable=False)
    queue_entry_no: Mapped[int] = mapped_column(nullable=False)
    check_in_details: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    called_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)