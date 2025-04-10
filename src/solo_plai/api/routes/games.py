from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from solo_plai.data.database import get_db
from solo_plai.api.models import Game, GameCreate, GameDetail
import solo_plai.data.models as models

router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Game, status_code=status.HTTP_201_CREATED)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    """Create a new game session"""
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get("/", response_model=List[Game])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all games"""
    return db.query(models.Game).offset(skip).limit(limit).all()

@router.get("/{game_id}", response_model=GameDetail)
def read_game(game_id: str, db: Session = Depends(get_db)):
    """Get a game by ID"""
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@router.put("/{game_id}", response_model=Game)
def update_game(game_id: str, game: GameCreate, db: Session = Depends(get_db)):
    """Update a game"""
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Update game attributes
    for key, value in game.dict().items():
        setattr(db_game, key, value)
    
    db.commit()
    db.refresh(db_game)
    return db_game

@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: str, db: Session = Depends(get_db)):
    """Delete a game"""
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db.delete(db_game)
    db.commit()
    return None
