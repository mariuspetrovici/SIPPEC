from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    specializations = relationship("Specialization", back_populates="faculty")


class Specialization(Base):
    __tablename__ = "specializations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))
    faculty = relationship("Faculty", back_populates="specializations")
    students = relationship("User", back_populates="specialization")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # "student", "teacher", "secretary", "admin"
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    specialization_id = Column(Integer, ForeignKey("specializations.id"), nullable=True)
    specialization = relationship("Specialization", back_populates="students")
    sent_requests = relationship("Request", back_populates="requester", foreign_keys="Request.requester_id")
    handled_requests = relationship("Request", back_populates="handler", foreign_keys="Request.handler_id")


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # "exam_reschedule", "grade_review", etc.
    status = Column(String)  # "pending", "approved", "rejected"
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    requester_id = Column(Integer, ForeignKey("users.id"))
    handler_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=True)

    requester = relationship("User", foreign_keys=[requester_id], back_populates="sent_requests")
    handler = relationship("User", foreign_keys=[handler_id], back_populates="handled_requests")
    exam = relationship("Exam", back_populates="requests")


class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    date = Column(DateTime)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    proposed_by = Column(Integer, ForeignKey("users.id"))
    confirmed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    requests = relationship("Request", back_populates="exam")


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True) 