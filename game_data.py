"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except Exception:
        raise CorruptedDataError(f"Cannot read quest file: {filename}")
    
    quests = {}
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        if not block.strip():
            continue
        
        try:
            quest = parse_quest_block(block.strip().split('\n'))
            quests[quest['quest_id']] = quest
        except (KeyError, ValueError) as e:
            raise InvalidDataFormatError(f"Invalid quest format: {e}")
    
    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except Exception:
        raise CorruptedDataError(f"Cannot read item file: {filename}")
    
    items = {}
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        if not block.strip():
            continue
        
        try:
            item = parse_item_block(block.strip().split('\n'))
            items[item['item_id']] = item
        except (KeyError, ValueError) as e:
            raise InvalidDataFormatError(f"Invalid item format: {e}")
    
    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required = ['quest_id', 'title', 'description', 'reward_xp', 
                'reward_gold', 'required_level', 'prerequisite']
    
    for field in required:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing field: {field}")
    
    if not isinstance(quest_dict['reward_xp'], int):
        raise InvalidDataFormatError("reward_xp must be integer")
    if not isinstance(quest_dict['reward_gold'], int):
        raise InvalidDataFormatError("reward_gold must be integer")
    if not isinstance(quest_dict['required_level'], int):
        raise InvalidDataFormatError("required_level must be integer")
    
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required = ['item_id', 'name', 'type', 'effect', 'cost', 'description']
    valid_types = ['weapon', 'armor', 'consumable']
    
    for field in required:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing field: {field}")
    
    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(f"Invalid type: {item_dict['type']}")
    
    if not isinstance(item_dict['cost'], int):
        raise InvalidDataFormatError("cost must be integer")
    
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists('data/save_games'):
        os.makedirs('data/save_games')

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest = {}
    
    for line in lines:
        if ':' not in line:
            continue
        
        key, value = line.split(':', 1)
        key = key.strip().lower()
        value = value.strip()
        
        if key in ['reward_xp', 'reward_gold', 'required_level']:
            try:
                quest[key] = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Cannot convert {key} to int: {value}")
        else:
            quest[key] = value
    
    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}
    
    for line in lines:
        if ':' not in line:
            continue
        
        key, value = line.split(':', 1)
        key = key.strip().lower()
        value = value.strip()
        
        if key == 'cost':
            try:
                item[key] = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Cannot convert cost to int: {value}")
        else:
            item[key] = value
    
    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")
