"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    
    while True:
        choice = input("Choose option (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return int(choice)
        print("Invalid choice. Please select 1-3.")

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    print("\n=== CREATE CHARACTER ===")
    name = input("Enter character name: ").strip()
    
    print("\nAvailable classes:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")
    
    while True:
        choice = input("Choose class (1-4): ").strip()
        class_map = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue', '4': 'Cleric'}
        if choice in class_map:
            character_class = class_map[choice]
            break
        print("Invalid choice. Please select 1-4.")
    
    try:
        current_character = character_manager.create_character(name, character_class)
        print(f"\nCharacter created: {name} the {character_class}")
        save_game()
        game_loop()
    except InvalidCharacterClassError as e:
        print(f"Error: {e}")

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    saved = character_manager.list_saved_characters()
    
    if not saved:
        print("No saved characters found.")
        return
    
    print("\n=== SAVED CHARACTERS ===")
    for i, name in enumerate(saved, 1):
        print(f"{i}. {name}")
    print(f"{len(saved) + 1}. Back")
    
    while True:
        choice = input(f"Select character (1-{len(saved) + 1}): ").strip()
        try:
            idx = int(choice) - 1
            if idx == len(saved):
                return
            if 0 <= idx < len(saved):
                break
        except ValueError:
            pass
        print(f"Invalid choice. Please select 1-{len(saved) + 1}.")
    
    try:
        current_character = character_manager.load_character(saved[idx])
        print(f"Loaded: {current_character['name']}")
        game_loop()
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file is corrupted")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running and current_character:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Goodbye!")
            game_running = False
        else:
            print("Invalid choice.")

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print(f"\n=== {current_character['name']} - Level {current_character['level']} ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")
    
    while True:
        choice = input("Choose option (1-6): ").strip()
        if choice in ['1', '2', '3', '4', '5', '6']:
            return int(choice)
        print("Invalid choice. Please select 1-6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print(f"\n=== CHARACTER STATS ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character['level']}")
    print(f"Experience: {current_character['experience']}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Strength: {current_character['strength']}")
    print(f"Magic: {current_character['magic']}")
    print(f"Gold: {current_character['gold']}")
    
    if current_character.get('equipped_weapon'):
        print(f"Equipped Weapon: {current_character['equipped_weapon']}")
    if current_character.get('equipped_armor'):
        print(f"Equipped Armor: {current_character['equipped_armor']}")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    if not current_character['inventory']:
        print("\nInventory is empty.")
        return
    
    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character, all_items)

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (Testing)")
        print("7. Back")
        
        choice = input("Choose option (1-7): ").strip()
        
        if choice == '1':
            active = quest_handler.get_active_quests(current_character, all_quests)
            if active:
                print("\nActive Quests:")
                for q in active:
                    print(f"- {q['title']}")
            else:
                print("No active quests.")
        
        elif choice == '2':
            available = quest_handler.get_available_quests(current_character, all_quests)
            if available:
                print("\nAvailable Quests:")
                for i, q in enumerate(available, 1):
                    print(f"{i}. {q['title']} (Level {q['required_level']})")
            else:
                print("No available quests.")
        
        elif choice == '3':
            completed = quest_handler.get_completed_quests(current_character, all_quests)
            if completed:
                print("\nCompleted Quests:")
                for q in completed:
                    print(f"- {q['title']}")
            else:
                print("No completed quests.")
        
        elif choice == '4':
            available = quest_handler.get_available_quests(current_character, all_quests)
            if available:
                print("\nAvailable Quests:")
                for i, q in enumerate(available, 1):
                    print(f"{i}. {q['title']}")
                try:
                    idx = int(input("Select quest (1-...): ")) - 1
                    if 0 <= idx < len(available):
                        quest_id = available[idx]['quest_id']
                        quest_handler.accept_quest(current_character, quest_id, all_quests)
                        print("Quest accepted!")
                except (ValueError, IndexError):
                    print("Invalid selection.")
            else:
                print("No available quests.")
        
        elif choice == '5':
            if current_character['active_quests']:
                print("\nActive Quests:")
                for i, qid in enumerate(current_character['active_quests'], 1):
                    if qid in all_quests:
                        print(f"{i}. {all_quests[qid]['title']}")
                try:
                    idx = int(input("Select quest to abandon (1-...): ")) - 1
                    if 0 <= idx < len(current_character['active_quests']):
                        qid = current_character['active_quests'][idx]
                        quest_handler.abandon_quest(current_character, qid)
                        print("Quest abandoned.")
                except (ValueError, IndexError):
                    print("Invalid selection.")
            else:
                print("No active quests to abandon.")
        
        elif choice == '6':
            if current_character['active_quests']:
                qid = current_character['active_quests'][0]
                try:
                    quest_handler.complete_quest(current_character, qid, all_quests)
                    print(f"Quest '{all_quests[qid]['title']}' completed!")
                except QuestNotActiveError:
                    print("Quest not active.")
            else:
                print("No active quests to complete.")
        
        elif choice == '7':
            break

def explore():
    """Find and fight random enemies"""
    global current_character
    
    if current_character['health'] <= 0:
        print("You are dead!")
        return
    
    print("\nYou venture out to explore...")
    enemy = combat_system.get_random_enemy_for_level(current_character['level'])
    print(f"You encounter a {enemy['name']}!")
    
    battle = combat_system.SimpleBattle(current_character, enemy)
    try:
        result = battle.start_battle()
        
        if result['winner'] == 'player':
            print(f"\nVictory! Gained {result['xp_gained']} XP and {result['gold_gained']} Gold!")
            character_manager.gain_experience(current_character, result['xp_gained'])
            character_manager.add_gold(current_character, result['gold_gained'])
        elif result['winner'] == 'enemy':
            print("\nYou were defeated!")
            current_character['health'] = 0
        else:
            print("\nYou escaped!")
    except CharacterDeadError:
        print("You are too weak to fight!")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    while True:
        print(f"\n=== SHOP === Gold: {current_character['gold']}")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            print("\nAvailable Items:")
            items_list = list(all_items.items())
            for i, (iid, item) in enumerate(items_list, 1):
                print(f"{i}. {item['name']} - {item['cost']} Gold ({item['type']})")
            
            try:
                idx = int(input("Select item (1-...): ")) - 1
                if 0 <= idx < len(items_list):
                    iid, item = items_list[idx]
                    inventory_system.purchase_item(current_character, iid, item)
                    print(f"Purchased {item['name']}!")
            except (ValueError, IndexError, InsufficientResourcesError, InventoryFullError) as e:
                print(f"Cannot purchase: {e}")
        
        elif choice == '2':
            if current_character['inventory']:
                print("\nYour Items:")
                for i, iid in enumerate(current_character['inventory'], 1):
                    if iid in all_items:
                        print(f"{i}. {all_items[iid]['name']}")
                
                try:
                    idx = int(input("Select item to sell (1-...): ")) - 1
                    if 0 <= idx < len(current_character['inventory']):
                        iid = current_character['inventory'][idx]
                        gold = inventory_system.sell_item(current_character, iid, all_items[iid])
                        print(f"Sold for {gold} Gold!")
                except (ValueError, IndexError, ItemNotFoundError) as e:
                    print(f"Cannot sell: {e}")
            else:
                print("You have no items to sell.")
        
        elif choice == '3':
            break

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    if current_character:
        try:
            character_manager.save_character(current_character)
        except Exception as e:
            print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        try:
            all_quests = game_data.load_quests()
            all_items = game_data.load_items()
        except Exception as e:
            print(f"Error loading game data: {e}")
            raise
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        raise

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
    except Exception as e:
        print(f"Fatal error loading game data: {e}")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game_menu()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
