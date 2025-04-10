from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from solo_plai.data.database import Base

# Association table for many-to-many relationship between unit types and abilities
unit_type_abilities = Table(
    "unit_type_abilities",
    Base.metadata,
    Column("unit_type_id", String, ForeignKey("unit_types.id")),
    Column("ability_id", String, ForeignKey("unit_abilities.id")),
)

class UnitAbility(Base):
    """ORM model for unit abilities"""
    __tablename__ = "unit_abilities"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    usage_type = Column(String, nullable=False)  # 'once_per_turn', 'once_per_battle', 'passive'
    effect = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship
    unit_types = relationship("UnitType", secondary=unit_type_abilities, back_populates="abilities")

class UnitType(Base):
    """ORM model for unit types"""
    __tablename__ = "unit_types"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    move = Column(Integer, nullable=False)
    health = Column(Integer, nullable=False)
    save = Column(Integer, nullable=False)
    control = Column(Integer, nullable=False)
    army = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    abilities = relationship("UnitAbility", secondary=unit_type_abilities, back_populates="unit_types")
    instances = relationship("UnitInstance", back_populates="unit_type")

class Player(Base):
    """ORM model for players"""
    __tablename__ = "players"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    army_name = Column(String, nullable=False)
    is_ai = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    game_player = relationship("Game", foreign_keys="Game.player_id", back_populates="player")
    game_ai = relationship("Game", foreign_keys="Game.ai_id", back_populates="ai_opponent")
    units = relationship("UnitInstance", back_populates="player")

class UnitInstance(Base):
    """ORM model for unit instances in a game"""
    __tablename__ = "unit_instances"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    unit_type_id = Column(String, ForeignKey("unit_types.id"), nullable=False)
    player_id = Column(String, ForeignKey("players.id"), nullable=False)
    initial_models = Column(Integer, nullable=False)
    models_remaining = Column(Integer, nullable=False)
    position_x = Column(Integer, nullable=True)
    position_y = Column(Integer, nullable=True)
    used_abilities = Column(JSON, default={})
    used_once_per_battle = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    unit_type = relationship("UnitType", back_populates="instances")
    player = relationship("Player", back_populates="units")

class Board(Base):
    """ORM model for game boards"""
    __tablename__ = "boards"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    board_type = Column(String, nullable=False)
    terrain = Column(JSON, default={})
    objectives = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    games = relationship("Game", back_populates="board")

class TwistCard(Base):
    """ORM model for twist cards"""
    __tablename__ = "twist_cards"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    effect = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    games = relationship("Game", back_populates="current_twist")

class Game(Base):
    """ORM model for game sessions"""
    __tablename__ = "games"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    player_id = Column(String, ForeignKey("players.id"), nullable=False)
    ai_id = Column(String, ForeignKey("players.id"), nullable=False)
    board_id = Column(String, ForeignKey("boards.id"), nullable=False)
    current_twist_id = Column(String, ForeignKey("twist_cards.id"), nullable=True)
    current_turn = Column(Integer, default=0)
    max_turns = Column(Integer, default=4)
    victory_points = Column(JSON, default={})
    game_state = Column(JSON, nullable=True)  # For storing additional state
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    player = relationship("Player", foreign_keys=[player_id], back_populates="game_player")
    ai_opponent = relationship("Player", foreign_keys=[ai_id], back_populates="game_ai")
    board = relationship("Board", back_populates="games")
    current_twist = relationship("TwistCard", back_populates="games")
