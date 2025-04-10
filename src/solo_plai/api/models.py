from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
import uuid


class UnitAbilityBase(BaseModel):
    name: str
    description: str
    usage_type: str
    effect: str


class UnitAbilityCreate(UnitAbilityBase):
    pass


class UnitAbility(UnitAbilityBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class UnitTypeBase(BaseModel):
    name: str
    move: int
    health: int
    save: int
    control: int
    army: str


class UnitTypeCreate(UnitTypeBase):
    abilities: List[str] = []  # List of ability IDs


class UnitType(UnitTypeBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    abilities: List[UnitAbility] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    name: str
    army_name: str
    is_ai: bool = False


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class UnitInstanceBase(BaseModel):
    unit_type_id: str
    player_id: str
    initial_models: int
    models_remaining: int
    position_x: Optional[int] = None
    position_y: Optional[int] = None
    used_abilities: Dict[str, bool] = {}
    used_once_per_battle: List[str] = []


class UnitInstanceCreate(UnitInstanceBase):
    pass


class UnitInstance(UnitInstanceBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class BoardBase(BaseModel):
    board_type: str
    terrain: Dict[str, str] = {}  # Key is "x,y" coordinate, value is terrain type
    objectives: List[str] = []  # List of "x,y" coordinates


class BoardCreate(BoardBase):
    pass


class Board(BoardBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class TwistCardBase(BaseModel):
    name: str
    description: str
    effect: str


class TwistCardCreate(TwistCardBase):
    pass


class TwistCard(TwistCardBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    player_id: str
    ai_id: str
    board_id: str
    current_twist_id: Optional[str] = None
    current_turn: int = 0
    max_turns: int = 4
    victory_points: Dict[str, int] = {}
    game_state: Optional[Dict] = None


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class GameDetail(Game):
    player: Player
    ai_opponent: Player
    board: Board
    current_twist: Optional[TwistCard] = None

    class Config:
        orm_mode = True
