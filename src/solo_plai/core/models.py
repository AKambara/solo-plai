from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime


class UnitAbilityType(Enum):
    ONCE_PER_TURN = "once_per_turn"
    ONCE_PER_BATTLE = "once_per_battle"
    PASSIVE = "passive"


@dataclass
class UnitAbility:
    """Represents a special ability a unit can use"""
    name: str
    description: str
    usage_type: UnitAbilityType
    effect: str


@dataclass
class UnitType:
    """Base class representing a unit type in the game"""
    name: str
    move: int  # Movement in inches
    health: int  # Health per model
    save: int  # Save roll needed (e.g., 4+ would be 4)
    control: int  # Control value per model
    abilities: List[UnitAbility] = field(default_factory=list)


@dataclass
class UnitInstance:
    """An actual instance of a unit in a game with current status"""
    unit_type: UnitType
    initial_models: int
    models_remaining: int
    position: Optional[Tuple[int, int]] = None
    used_abilities: Dict[str, bool] = field(default_factory=dict)
    used_once_per_battle: Set[str] = field(default_factory=set)

    def __post_init__(self):
        """Initialize used_abilities dictionary based on unit type abilities"""
        self.used_abilities = {ability.name: False for ability in self.unit_type.abilities}

    def is_ability_available(self, ability_name: str) -> bool:
        """Check if an ability can be used based on usage type"""
        for ability in self.unit_type.abilities:
            if ability.name == ability_name:
                if ability.usage_type == UnitAbilityType.ONCE_PER_BATTLE:
                    return ability_name not in self.used_once_per_battle
                elif ability.usage_type == UnitAbilityType.ONCE_PER_TURN:
                    return not self.used_abilities.get(ability_name, False)
                return True
        return False


@dataclass
class Player:
    """Represents a player in the game"""
    name: str
    army_name: str
    is_ai: bool = False
    units: List[UnitInstance] = field(default_factory=list)


@dataclass
class Board:
    """Represents the physical game board (30" x 22.4")"""
    board_type: str
    terrain: Dict[Tuple[int, int], str] = field(default_factory=dict)
    objectives: List[Tuple[int, int]] = field(default_factory=list)


@dataclass
class TwistCard:
    """Represents a twist card that modifies game rules"""
    name: str
    description: str
    effect: str


@dataclass
class GameState:
    """Core class for managing the complete state of a Spearhead game session"""
    id: str
    player: Player
    ai_opponent: Player
    board: Board
    current_turn: int = 0
    max_turns: int = 4  # Spearhead is played over 4 turns
    current_twist: Optional[TwistCard] = None
    victory_points: Dict[str, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Initialize victory points if not provided"""
        if not self.victory_points:
            self.victory_points = {
                self.player.name: 0,
                self.ai_opponent.name: 0
            }

    def advance_turn(self) -> None:
        """Move the game to the next turn"""
        self.current_turn += 1
        self.updated_at = datetime.now()
        
        # Reset once-per-turn abilities
        for player in [self.player, self.ai_opponent]:
            for unit in player.units:
                for ability_name in unit.used_abilities:
                    unit.used_abilities[ability_name] = False

    def get_winner(self) -> Optional[Player]:
        """Determine the winner based on victory points"""
        if self.victory_points[self.player.name] > self.victory_points[self.ai_opponent.name]:
            return self.player
        elif self.victory_points[self.player.name] < self.victory_points[self.ai_opponent.name]:
            return self.ai_opponent
        return None  # Draw
