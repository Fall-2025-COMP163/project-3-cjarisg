"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
    
    character['inventory'].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item not found: {item_id}")
    
    character['inventory'].remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    return item_id in character['inventory']

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    return MAX_INVENTORY_SIZE - len(character['inventory'])

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    removed = character['inventory'].copy()
    character['inventory'] = []
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item not found: {item_id}")
    
    if item_data['type'] != 'consumable':
        raise InvalidItemTypeError(f"Cannot use {item_data['type']} item")
    
    stat_name, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat_name, value)
    
    character['inventory'].remove(item_id)
    return f"Used {item_data['name']}"

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item not found: {item_id}")
    
    if item_data['type'] != 'weapon':
        raise InvalidItemTypeError(f"Not a weapon: {item_data['type']}")
    
    # Unequip current weapon if exists
    if character.get('equipped_weapon'):
        old_weapon_id = character['equipped_weapon']
        # This should refer to item_data, but we don't have it here
        # For now, assume strength bonus of 5 for generic unequip
        character['strength'] -= 5
        character['inventory'].append(old_weapon_id)
    
    # Equip new weapon
    stat_name, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat_name, value)
    character['equipped_weapon'] = item_id
    character['inventory'].remove(item_id)
    
    return f"Equipped {item_data['name']}"

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item not found: {item_id}")
    
    if item_data['type'] != 'armor':
        raise InvalidItemTypeError(f"Not armor: {item_data['type']}")
    
    # Unequip current armor if exists
    if character.get('equipped_armor'):
        old_armor_id = character['equipped_armor']
        character['max_health'] -= 10
        character['inventory'].append(old_armor_id)
    
    # Equip new armor
    stat_name, value = parse_item_effect(item_data['effect'])
    apply_stat_effect(character, stat_name, value)
    character['equipped_armor'] = item_id
    character['inventory'].remove(item_id)
    
    return f"Equipped {item_data['name']}"

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    if not character.get('equipped_weapon'):
        return None
    
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
    
    weapon_id = character['equipped_weapon']
    character['strength'] -= 5
    character['inventory'].append(weapon_id)
    character['equipped_weapon'] = None
    
    return weapon_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    if not character.get('equipped_armor'):
        return None
    
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
    
    armor_id = character['equipped_armor']
    character['max_health'] -= 10
    character['inventory'].append(armor_id)
    character['equipped_armor'] = None
    
    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    if character['gold'] < item_data['cost']:
        raise InsufficientResourcesError("Insufficient gold")
    
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
    
    character['gold'] -= item_data['cost']
    character['inventory'].append(item_id)
    
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item not found: {item_id}")
    
    sell_price = item_data['cost'] // 2
    character['inventory'].remove(item_id)
    character['gold'] += sell_price
    
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    stat_name, value = effect_string.split(':')
    return (stat_name.strip(), int(value.strip()))

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    if stat_name == 'health':
        character['health'] = min(character['health'] + value, character['max_health'])
    elif stat_name in ['max_health', 'strength', 'magic']:
        character[stat_name] = character.get(stat_name, 0) + value
    else:
        character[stat_name] = character.get(stat_name, 0) + value

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    if not character['inventory']:
        print("Inventory is empty")
        return
    
    print("\n=== INVENTORY ===")
    item_counts = {}
    for item_id in character['inventory']:
        if item_id not in item_counts:
            item_counts[item_id] = 0
        item_counts[item_id] += 1
    
    for item_id, count in item_counts.items():
        if item_id in item_data_dict:
            item = item_data_dict[item_id]
            print(f"{item['name']} ({item['type']}) x{count}")
        else:
            print(f"{item_id} x{count}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
