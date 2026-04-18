"""Team model representing football clubs."""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    short_name = Column(String(10), nullable=True)
    founded_year = Column(Integer, nullable=True)
    stadium = Column(String(100), nullable=True)
    city = Column(String(50), nullable=True)
    country = Column(String(50), default="England")
    league = Column(String(50), default="Premier League")
    manager = Column(String(100), nullable=True)
    budget_millions = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"
