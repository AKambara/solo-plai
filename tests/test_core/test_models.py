import pytest
from solo_plai.core.models import UnitType, UnitAbility, UnitAbilityType, UnitInstance

def test_unit_type_creation():
    """Test creating a unit type with properties."""
    unit_type = UnitType(
        name="Liberator",
        move=5,
        health=2,
        save=4,
        control=1
    )
    
    assert unit_type.name == "Liberator"
    assert unit_type.move == 5
    assert unit_type.health == 2
    assert unit_type.save == 4
    assert unit_type.control == 1
    assert unit_type.abilities == []

def test_unit_ability_usage():
    """Test unit ability availability based on usage type."""
    # Create an ability
    ability = UnitAbility(
        name="Righteous Fury",
        description="Reroll hit rolls of 1",
        usage_type=UnitAbilityType.ONCE_PER_TURN,
        effect="Reroll"
    )
    
    # Create a unit type with the ability
    unit_type = UnitType(
        name="Liberator",
        move=5,
        health=2,
        save=4,
        control=1,
        abilities=[ability]
    )
    
    # Create a unit instance
    unit = UnitInstance(
        unit_type=unit_type,
        initial_models=5,
        models_remaining=5
    )
    
    # Test ability availability
    assert unit.is_ability_available("Righteous Fury") == True
    
    # Use the ability
    unit.used_abilities["Righteous Fury"] = True
    
    # Test ability is no longer available
    assert unit.is_ability_available("Righteous Fury") == False
