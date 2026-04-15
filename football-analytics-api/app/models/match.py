"""Match model representing football matches."""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    season = Column(String(20), nullable=False, index=True)
    matchday = Column(Integer, nullable=True)
    match_date = Column(Date, nullable=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    home_goals = Column(Integer, nullable=False)
    away_goals = Column(Integer, nullable=False)
    home_possession = Column(Float, nullable=True)
    away_possession = Column(Float, nullable=True)
    home_shots = Column(Integer, nullable=True)
    away_shots = Column(Integer, nullable=True)
    home_shots_on_target = Column(Integer, nullable=True)
    away_shots_on_target = Column(Integer, nullable=True)
    home_corners = Column(Integer, nullable=True)
    away_corners = Column(Integer, nullable=True)
    home_fouls = Column(Integer, nullable=True)
    away_fouls = Column(Integer, nullable=True)
    referee = Column(String(100), nullable=True)
    venue = Column(String(100), nullable=True)
    attendance = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")

    @property
    def result(self):
        """Determine match result."""
        if self.home_goals > self.away_goals:
            return "HOME_WIN"
        elif self.home_goals < self.away_goals:
            return "AWAY_WIN"
        return "DRAW"

    def __repr__(self):
        return f"<Match(id={self.id}, home={self.home_team_id} vs away={self.away_team_id})>"
