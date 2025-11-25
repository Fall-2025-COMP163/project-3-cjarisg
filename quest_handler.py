"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
import character_manager

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")
    
    quest = quest_data_dict[quest_id]
    
    if character['level'] < quest['required_level']:
        raise InsufficientLevelError(f"Level {quest['required_level']} required")
    
    if quest['prerequisite'] != 'NONE' and quest['prerequisite'] not in character['completed_quests']:
        raise QuestRequirementsNotMetError(f"Prerequisite not completed: {quest['prerequisite']}")
    
    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f"Quest already completed: {quest_id}")
    
    if quest_id in character['active_quests']:
        raise QuestRequirementsNotMetError(f"Quest already active: {quest_id}")
    
    character['active_quests'].append(quest_id)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")
    
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest not active: {quest_id}")
    
    quest = quest_data_dict[quest_id]
    
    # Remove from active
    character['active_quests'].remove(quest_id)
    
    # Add to completed
    character['completed_quests'].append(quest_id)
    
    # Grant rewards
    character_manager.gain_experience(character, quest['reward_xp'])
    character_manager.add_gold(character, quest['reward_gold'])
    
    return {
        'xp': quest['reward_xp'],
        'gold': quest['reward_gold']
    }

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest not active: {quest_id}")
    
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    quests = []
    for quest_id in character['active_quests']:
        if quest_id in quest_data_dict:
            quests.append(quest_data_dict[quest_id])
    return quests

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    quests = []
    for quest_id in character['completed_quests']:
        if quest_id in quest_data_dict:
            quests.append(quest_data_dict[quest_id])
    return quests

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    available = []
    for quest_id, quest in quest_data_dict.items():
        if (character['level'] >= quest['required_level'] and
            (quest['prerequisite'] == 'NONE' or quest['prerequisite'] in character['completed_quests']) and
            quest_id not in character['completed_quests'] and
            quest_id not in character['active_quests']):
            available.append(quest)
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    return quest_id in character['completed_quests']

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    return quest_id in character['active_quests']

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    if quest_id not in quest_data_dict:
        return False
    
    quest = quest_data_dict[quest_id]
    
    if character['level'] < quest['required_level']:
        return False
    
    if quest['prerequisite'] != 'NONE' and quest['prerequisite'] not in character['completed_quests']:
        return False
    
    if quest_id in character['completed_quests']:
        return False
    
    if quest_id in character['active_quests']:
        return False
    
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")
    
    chain = []
    current_id = quest_id
    
    while current_id is not None:
        chain.insert(0, current_id)
        
        if current_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest not found: {current_id}")
        
        current = quest_data_dict[current_id]
        prerequisite = current.get('prerequisite', 'NONE')
        
        if prerequisite == 'NONE':
            current_id = None
        else:
            current_id = prerequisite
    
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
    
    completed_quests = len(character['completed_quests'])
    return (completed_quests / total_quests) * 100

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0
    
    for quest_id in character['completed_quests']:
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += quest.get('reward_xp', 0)
            total_gold += quest.get('reward_gold', 0)
    
    return {'total_xp': total_xp, 'total_gold': total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    quests = []
    for quest in quest_data_dict.values():
        if min_level <= quest['required_level'] <= max_level:
            quests.append(quest)
    return quests

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Rewards: {quest_data['reward_xp']} XP, {quest_data['reward_gold']} Gold")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    for quest in quest_list:
        print(f"{quest['title']} (Level {quest['required_level']}) - {quest['reward_xp']} XP, {quest['reward_gold']} Gold")

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    completion_pct = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    
    print(f"\n=== QUEST PROGRESS ===")
    print(f"Active Quests: {len(character['active_quests'])}")
    print(f"Completed Quests: {len(character['completed_quests'])}")
    print(f"Completion: {completion_pct:.1f}%")
    print(f"Total Rewards: {rewards['total_xp']} XP, {rewards['total_gold']} Gold")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for quest_id, quest in quest_data_dict.items():
        prerequisite = quest.get('prerequisite', 'NONE')
        if prerequisite != 'NONE' and prerequisite not in quest_data_dict:
            raise QuestNotFoundError(f"Invalid prerequisite: {prerequisite}")
    
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
