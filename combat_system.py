"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    valid_types = ['goblin', 'orc', 'dragon']
    
    if enemy_type.lower() not in valid_types:
        raise InvalidTargetError(f"Invalid enemy type: {enemy_type}")
    
    enemy_type = enemy_type.lower()
    
    enemies = {
        'goblin': {
            'name': 'Goblin',
            'health': 50,
            'max_health': 50,
            'strength': 8,
            'magic': 2,
            'xp_reward': 25,
            'gold_reward': 10
        },
        'orc': {
            'name': 'Orc',
            'health': 80,
            'max_health': 80,
            'strength': 12,
            'magic': 5,
            'xp_reward': 50,
            'gold_reward': 25
        },
        'dragon': {
            'name': 'Dragon',
            'health': 200,
            'max_health': 200,
            'strength': 25,
            'magic': 15,
            'xp_reward': 200,
            'gold_reward': 100
        }
    }
    
    return enemies[enemy_type].copy()

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        return create_enemy('goblin')
    elif character_level <= 5:
        return create_enemy('orc')
    else:
        return create_enemy('dragon')

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = False
        self.turn_counter = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is dead")
        
        self.combat_active = True
        self.turn_counter = 0
        
        while self.combat_active:
            self.player_turn()
            if not self.combat_active:
                break
            self.enemy_turn()
            
            winner = self.check_battle_end()
            if winner:
                self.combat_active = False
                if winner == 'player':
                    rewards = get_victory_rewards(self.enemy)
                    return {'winner': 'player', 'xp_gained': rewards['xp'], 'gold_gained': rewards['gold']}
                else:
                    return {'winner': 'enemy', 'xp_gained': 0, 'gold_gained': 0}
        
        return {'winner': 'escaped', 'xp_gained': 0, 'gold_gained': 0}
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active")
        
        display_combat_stats(self.character, self.enemy)
        print("\n1. Attack")
        print("2. Special Ability")
        print("3. Run")
        
        choice = input("Choose action (1-3): ").strip()
        
        if choice == '1':
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character['name']} attacks for {damage} damage!")
        elif choice == '2':
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == '3':
            if self.attempt_escape():
                display_battle_log("Escaped successfully!")
                self.combat_active = False
            else:
                display_battle_log("Failed to escape!")
        else:
            print("Invalid choice, attacking instead...")
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character['name']} attacks for {damage} damage!")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active")
        
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks for {damage} damage!")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        damage = attacker['strength'] - (defender['strength'] // 4)
        return max(1, damage)
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target['health'] = max(0, target['health'] - damage)
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy['health'] <= 0:
            return 'player'
        if self.character['health'] <= 0:
            return 'enemy'
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        return random.random() < 0.5

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    character_class = character['class']
    
    if character_class == 'Warrior':
        return warrior_power_strike(character, enemy)
    elif character_class == 'Mage':
        return mage_fireball(character, enemy)
    elif character_class == 'Rogue':
        return rogue_critical_strike(character, enemy)
    elif character_class == 'Cleric':
        return cleric_heal(character)
    else:
        return "Unknown ability!"

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = character['strength'] * 2 - (enemy['strength'] // 4)
    damage = max(1, damage)
    enemy['health'] = max(0, enemy['health'] - damage)
    return f"Warrior uses Power Strike for {damage} damage!"

def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = character['magic'] * 2
    damage = max(1, damage)
    enemy['health'] = max(0, enemy['health'] - damage)
    return f"Mage casts Fireball for {damage} damage!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:
        damage = character['strength'] * 3 - (enemy['strength'] // 4)
        damage = max(1, damage)
        enemy['health'] = max(0, enemy['health'] - damage)
        return f"Rogue lands Critical Strike for {damage} damage!"
    else:
        return "Rogue's attack missed!"

def cleric_heal(character):
    """Cleric special ability"""
    healed = min(30, character['max_health'] - character['health'])
    character['health'] = min(character['health'] + 30, character['max_health'])
    return f"Cleric heals for {healed} health!"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    return character['health'] > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
