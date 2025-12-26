"""
Pokemon Battle GUI - Enterprise Grade Gradio Application
A professional, polished battle simulator with real-time sprites and animations.
"""

import gradio as gr
import httpx
import asyncio
import random
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

POKEAPI_BASE = "https://pokeapi.co/api/v2"
SPRITE_BASE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"

# Gen 1-3 Pokemon for selection (total 386)
GEN_1_POKEMON = [
    "bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard",
    "squirtle", "wartortle", "blastoise", "caterpie", "metapod", "butterfree",
    "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot", "rattata",
    "raticate", "spearow", "fearow", "ekans", "arbok", "pikachu", "raichu",
    "sandshrew", "sandslash", "nidoran-f", "nidorina", "nidoqueen", "nidoran-m",
    "nidorino", "nidoking", "clefairy", "clefable", "vulpix", "ninetales",
    "jigglypuff", "wigglytuff", "zubat", "golbat", "oddish", "gloom", "vileplume",
    "paras", "parasect", "venonat", "venomoth", "diglett", "dugtrio", "meowth",
    "persian", "psyduck", "golduck", "mankey", "primeape", "growlithe", "arcanine",
    "poliwag", "poliwhirl", "poliwrath", "abra", "kadabra", "alakazam", "machop",
    "machoke", "machamp", "bellsprout", "weepinbell", "victreebel", "tentacool",
    "tentacruel", "geodude", "graveler", "golem", "ponyta", "rapidash", "slowpoke",
    "slowbro", "magnemite", "magneton", "farfetchd", "doduo", "dodrio", "seel",
    "dewgong", "grimer", "muk", "shellder", "cloyster", "gastly", "haunter",
    "gengar", "onix", "drowzee", "hypno", "krabby", "kingler", "voltorb",
    "electrode", "exeggcute", "exeggutor", "cubone", "marowak", "hitmonlee",
    "hitmonchan", "lickitung", "koffing", "weezing", "rhyhorn", "rhydon",
    "chansey", "tangela", "kangaskhan", "horsea", "seadra", "goldeen", "seaking",
    "staryu", "starmie", "mr-mime", "scyther", "jynx", "electabuzz", "magmar",
    "pinsir", "tauros", "magikarp", "gyarados", "lapras", "ditto", "eevee",
    "vaporeon", "jolteon", "flareon", "porygon", "omanyte", "omastar", "kabuto",
    "kabutops", "aerodactyl", "snorlax", "articuno", "zapdos", "moltres",
    "dratini", "dragonair", "dragonite", "mewtwo", "mew"
]

POPULAR_POKEMON = [
    "pikachu", "charizard", "mewtwo", "gengar", "dragonite", "snorlax",
    "gyarados", "alakazam", "machamp", "blastoise", "venusaur", "arcanine",
    "lapras", "jolteon", "mew", "articuno", "zapdos", "moltres", "eevee"
]

TYPE_COLORS = {
    "normal": "#A8A878", "fire": "#F08030", "water": "#6890F0", "electric": "#F8D030",
    "grass": "#78C850", "ice": "#98D8D8", "fighting": "#C03028", "poison": "#A040A0",
    "ground": "#E0C068", "flying": "#A890F0", "psychic": "#F85888", "bug": "#A8B820",
    "rock": "#B8A038", "ghost": "#705898", "dragon": "#7038F8", "dark": "#705848",
    "steel": "#B8B8D0", "fairy": "#EE99AC"
}

WEATHER_EFFECTS = ["none", "rain", "sun"]

# ══════════════════════════════════════════════════════════════════════════════
# API HELPERS
# ══════════════════════════════════════════════════════════════════════════════

async def fetch_pokemon_data(pokemon_name: str) -> dict | None:
    """Fetch Pokemon data from PokeAPI."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{POKEAPI_BASE}/pokemon/{pokemon_name.lower()}",
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching {pokemon_name}: {e}")
    return None

async def fetch_move_data(move_url: str) -> dict | None:
    """Fetch move data from PokeAPI."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(move_url, timeout=10.0)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching move: {e}")
    return None

async def fetch_type_data(type_name: str) -> dict | None:
    """Fetch type effectiveness data."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{POKEAPI_BASE}/type/{type_name}",
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching type data: {e}")
    return None

def get_sprite_url(pokemon_id: int, back: bool = False) -> str:
    """Get sprite URL for a Pokemon."""
    if back:
        return f"{SPRITE_BASE}/back/{pokemon_id}.png"
    return f"{SPRITE_BASE}/{pokemon_id}.png"

def get_animated_sprite_url(pokemon_id: int, back: bool = False) -> str:
    """Get animated sprite URL (if available)."""
    if back:
        return f"{SPRITE_BASE}/versions/generation-v/black-white/animated/back/{pokemon_id}.gif"
    return f"{SPRITE_BASE}/versions/generation-v/black-white/animated/{pokemon_id}.gif"

# ══════════════════════════════════════════════════════════════════════════════
# BATTLE LOGIC - ENHANCED
# ══════════════════════════════════════════════════════════════════════════════

# Stat stage multipliers (from actual Pokemon games)
STAT_STAGE_MULTIPLIERS = {
    -6: 2/8, -5: 2/7, -4: 2/6, -3: 2/5, -2: 2/4, -1: 2/3,
    0: 1.0,
    1: 3/2, 2: 4/2, 3: 5/2, 4: 6/2, 5: 7/2, 6: 8/2
}

def get_stat_multiplier(stage: int) -> float:
    """Get the stat multiplier for a given stage (-6 to +6)."""
    return STAT_STAGE_MULTIPLIERS.get(max(-6, min(6, stage)), 1.0)

async def get_pokemon_moves(pokemon_data: dict, limit: int = 4) -> list[dict]:
    """Fetch best damaging moves for a Pokemon by searching through all moves."""
    all_moves = pokemon_data.get('moves', [])
    damaging_moves = []
    
    # Try to find good damaging moves by checking more moves
    sample_size = min(20, len(all_moves))  # Check up to 20 moves
    sampled = random.sample(all_moves, sample_size) if len(all_moves) >= sample_size else all_moves
    
    for move_entry in sampled:
        if len(damaging_moves) >= 4:
            break
        move_data = await fetch_move_data(move_entry['move']['url'])
        if move_data and move_data.get('power') and move_data.get('power') > 0:
            damaging_moves.append({
                'name': move_data['name'].replace('-', ' ').title(),
                'power': move_data.get('power', 50),
                'accuracy': move_data.get('accuracy', 100) or 100,
                'type': move_data['type']['name'],
                'category': move_data.get('damage_class', {}).get('name', 'physical'),
                'pp': move_data.get('pp', 10),
            })
    
    # Sort by power (strongest first)
    damaging_moves.sort(key=lambda m: m['power'], reverse=True)
    
    # Fill remaining slots with Struggle
    while len(damaging_moves) < 4:
        damaging_moves.append({
            'name': 'Struggle',
            'power': 50,
            'accuracy': 100,
            'type': 'normal',
            'category': 'physical',
            'pp': 999
        })
    
    return damaging_moves[:4]

def get_stab_multiplier(pokemon: dict, move_type: str) -> float:
    """Check if move gets STAB (Same-Type Attack Bonus)."""
    pokemon_types = [t['type']['name'] for t in pokemon.get('types', [])]
    if move_type in pokemon_types:
        return 1.5  # STAB bonus
    return 1.0

def get_speed(pokemon: dict) -> int:
    """Get Pokemon's speed stat."""
    return pokemon['stats'][5]['base_stat']

async def calculate_damage_enhanced(
    attacker: dict, 
    defender: dict, 
    move: dict, 
    weather: str, 
    critical: bool = False
) -> tuple[int, str, bool]:
    """
    Enhanced damage calculation with STAB and Physical/Special split.
    Returns (damage, effectiveness_text, stab_applied)
    """
    power = move.get('power') or 50
    move_type = move.get('type', 'normal')
    category = move.get('category', 'physical')
    
    # Physical vs Special split
    if category == 'physical':
        attack = attacker['stats'][1]['base_stat']   # Attack
        defense = defender['stats'][2]['base_stat']  # Defense
    else:  # special
        attack = attacker['stats'][3]['base_stat']   # Sp. Atk
        defense = defender['stats'][4]['base_stat']  # Sp. Def
    
    # STAB (Same-Type Attack Bonus)
    stab = get_stab_multiplier(attacker, move_type)
    stab_applied = stab > 1.0
    
    # Critical hit multiplier
    crit_mult = 1.5 if critical else 1.0
    
    # Weather multiplier
    weather_mult = 1.0
    if weather == 'rain' and move_type == 'water':
        weather_mult = 1.5
    elif weather == 'sun' and move_type == 'fire':
        weather_mult = 1.5
    elif weather == 'rain' and move_type == 'fire':
        weather_mult = 0.5
    elif weather == 'sun' and move_type == 'water':
        weather_mult = 0.5
    
    # Type effectiveness
    effectiveness = 1.0
    effectiveness_text = ""
    
    type_data = await fetch_type_data(move_type)
    if type_data:
        damage_relations = type_data['damage_relations']
        for def_type in defender['types']:
            def_type_name = def_type['type']['name']
            if def_type_name in [t['name'] for t in damage_relations['double_damage_to']]:
                effectiveness *= 2
            elif def_type_name in [t['name'] for t in damage_relations['half_damage_to']]:
                effectiveness *= 0.5
            elif def_type_name in [t['name'] for t in damage_relations['no_damage_to']]:
                effectiveness *= 0
    
    if effectiveness > 1:
        effectiveness_text = "It's super effective!"
    elif effectiveness < 1 and effectiveness > 0:
        effectiveness_text = "It's not very effective..."
    elif effectiveness == 0:
        effectiveness_text = "It has no effect!"
    
    # Damage formula (Gen V+)
    level = 50  # Fixed level for now
    base_damage = ((2 * level / 5 + 2) * power * (attack / defense) / 50 + 2)
    final_damage = base_damage * stab * effectiveness * weather_mult * crit_mult
    
    # Random variance (0.85 to 1.0)
    variance = random.uniform(0.85, 1.0)
    final_damage *= variance
    
    return max(1, int(final_damage)), effectiveness_text, stab_applied

async def execute_turn(
    attacker: dict,
    defender: dict,
    move: dict,
    weather: str,
    attacker_name: str,
    defender_name: str
) -> tuple[int, list[dict]]:
    """Execute a single turn and return (damage_dealt, events)."""
    events = []
    
    # Check accuracy
    accuracy = move.get('accuracy', 100)
    if random.randint(1, 100) > accuracy:
        events.append({
            "type": "miss",
            "message": f"{attacker_name}'s attack missed!"
        })
        return 0, events
    
    # Calculate damage
    critical = random.random() < 0.0625  # 1/16 chance
    damage, eff_text, stab_applied = await calculate_damage_enhanced(
        attacker, defender, move, weather, critical
    )
    
    # Attack message
    events.append({
        "type": "attack",
        "message": f"{attacker_name} used {move['name']}!"
    })
    
    # STAB message
    if stab_applied:
        events.append({
            "type": "stab",
            "message": f"STAB bonus applied!"
        })
    
    # Critical hit message
    if critical:
        events.append({
            "type": "critical",
            "message": "A critical hit!"
        })
    
    # Effectiveness message
    if eff_text:
        events.append({
            "type": "effectiveness",
            "message": eff_text
        })
    
    # Damage message
    category_label = "physical" if move.get('category') == 'physical' else "special"
    events.append({
        "type": "damage",
        "message": f"   {damage} damage ({category_label})!"
    })
    
    return damage, events

async def run_battle_turn(
    player_pokemon: dict,
    opponent_pokemon: dict,
    player_move: dict,
    weather: str,
    player_hp: int,
    opponent_hp: int,
    max_player_hp: int,
    max_opponent_hp: int,
    turn_number: int = 1
) -> tuple[int, int, list[dict], str | None]:
    """
    Run a single battle turn with player move selection.
    Returns (new_player_hp, new_opponent_hp, events, winner)
    """
    events = []
    winner = None
    
    player_name = player_pokemon['name'].capitalize()
    opponent_name = opponent_pokemon['name'].capitalize()
    
    # Determine turn order based on Speed
    player_speed = get_speed(player_pokemon)
    opponent_speed = get_speed(opponent_pokemon)
    
    if player_speed > opponent_speed:
        first = "player"
    elif opponent_speed > player_speed:
        first = "opponent"
    else:
        first = random.choice(["player", "opponent"])
    
    # Opponent selects a random move
    opponent_moves = await get_pokemon_moves(opponent_pokemon)
    opponent_move = random.choice(opponent_moves)
    
    # Helper to add turn number to events
    def tag_events(event_list):
        for e in event_list:
            e['turn'] = turn_number
        return event_list
    
    # Execute turns in speed order
    if first == "player":
        # Player attacks first
        damage, turn_events = await execute_turn(
            player_pokemon, opponent_pokemon, player_move, weather,
            player_name, opponent_name
        )
        events.extend(tag_events(turn_events))
        opponent_hp = max(0, opponent_hp - damage)
        
        if opponent_hp <= 0:
            events.append({
                "type": "victory",
                "message": f"{opponent_name} fainted! {player_name} wins!",
                "turn": turn_number
            })
            return player_hp, 0, events, "player"
        
        # Opponent attacks
        damage, turn_events = await execute_turn(
            opponent_pokemon, player_pokemon, opponent_move, weather,
            opponent_name, player_name
        )
        events.extend(tag_events(turn_events))
        player_hp = max(0, player_hp - damage)
        
        if player_hp <= 0:
            events.append({
                "type": "defeat",
                "message": f"{player_name} fainted! {opponent_name} wins!",
                "turn": turn_number
            })
            return 0, opponent_hp, events, "opponent"
    else:
        # Opponent attacks first
        damage, turn_events = await execute_turn(
            opponent_pokemon, player_pokemon, opponent_move, weather,
            opponent_name, player_name
        )
        events.extend(tag_events(turn_events))
        player_hp = max(0, player_hp - damage)
        
        if player_hp <= 0:
            events.append({
                "type": "defeat",
                "message": f"{player_name} fainted! {opponent_name} wins!",
                "turn": turn_number
            })
            return 0, opponent_hp, events, "opponent"
        
        # Player attacks
        damage, turn_events = await execute_turn(
            player_pokemon, opponent_pokemon, player_move, weather,
            player_name, opponent_name
        )
        events.extend(tag_events(turn_events))
        opponent_hp = max(0, opponent_hp - damage)
        
        if opponent_hp <= 0:
            events.append({
                "type": "victory",
                "message": f"{opponent_name} fainted! {player_name} wins!",
                "turn": turn_number
            })
            return player_hp, 0, events, "player"
    
    # Add prompt for next turn
    events.append({
        "type": "prompt",
        "message": f"What will {player_name} do?",
        "turn": turn_number
    })
    
    return player_hp, opponent_hp, events, None

# ══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def create_pokemon_info_html(pokemon_data: dict | None, is_player: bool = True) -> str:
    """Generate HTML for Pokemon info card - Nintendo style."""
    if not pokemon_data:
        placeholder = "YOUR POKEMON" if is_player else "ENEMY"
        return f"""
        <div class="pokemon-card-wrapper" style="background: linear-gradient(180deg, #e0e0e0 0%, #c8c8c8 100%);
            border: 4px solid #404040; border-radius: 12px; padding: 20px;
            box-shadow: inset -3px -3px 0 #909090, inset 3px 3px 0 #f8f8f8, 5px 5px 0 #303030;
            text-align: center; min-height: 280px;">
            <div style="font-family: 'Press Start 2P', monospace; font-size: 48px; color: #a0a0a0; margin: 40px 0;">?</div>
            <p style="font-family: 'Press Start 2P', monospace; font-size: 10px; color: #606060;">SELECT {placeholder}</p>
        </div>
        """
    
    name = pokemon_data['name'].upper()
    pokemon_id = pokemon_data['id']
    types = pokemon_data['types']
    stats = pokemon_data['stats']
    hp = stats[0]['base_stat']
    
    # Generate type badges - Pokemon style
    type_badges = ""
    for t in types:
        type_name = t['type']['name']
        type_badges += f'<span class="type-badge type-{type_name}" style="font-family: \'Press Start 2P\', monospace; font-size: 8px; padding: 4px 8px; border-radius: 4px; text-transform: uppercase; display: inline-block; margin: 2px; box-shadow: inset -1px -1px 0 rgba(0,0,0,0.3), inset 1px 1px 0 rgba(255,255,255,0.3);">{type_name}</span> '
    
    # Sprite URL - use front sprite for opponent, back for player (battle perspective)
    sprite_url = get_sprite_url(pokemon_id, back=is_player)
    
    # Stats bars - Pokemon style
    stat_data = [
        ("HP", stats[0]['base_stat'], "#20d070"),
        ("ATK", stats[1]['base_stat'], "#f08030"),
        ("DEF", stats[2]['base_stat'], "#f8d030"),
        ("SP.A", stats[3]['base_stat'], "#6890f0"),
        ("SP.D", stats[4]['base_stat'], "#78c850"),
        ("SPD", stats[5]['base_stat'], "#f85888")
    ]
    
    stats_html = ""
    for stat_name, value, color in stat_data:
        percent = min(100, value / 255 * 100)
        stats_html += f"""
        <div style="display: flex; align-items: center; margin: 3px 0;">
            <span style="font-family: 'Press Start 2P', monospace; font-size: 8px; width: 40px; color: #303030;">{stat_name}</span>
            <div style="flex: 1; height: 10px; background: #484848; border-radius: 2px; padding: 2px; box-shadow: inset 1px 1px 0 #202020;">
                <div style="width: {percent}%; height: 100%; background: linear-gradient(180deg, {color}88, {color}); border-radius: 1px;"></div>
            </div>
            <span style="font-family: 'Press Start 2P', monospace; font-size: 8px; width: 30px; text-align: right; color: #303030;">{value}</span>
        </div>
        """
    
    side_label = "YOUR" if is_player else "ENEMY"
    
    return f"""
    <div class="pokemon-card-wrapper" style="background: linear-gradient(180deg, #e0e0e0 0%, #c8c8c8 100%);
        border: 4px solid #404040; border-radius: 12px; padding: 12px;
        box-shadow: inset -3px -3px 0 #909090, inset 3px 3px 0 #f8f8f8, 5px 5px 0 #303030;">
        
        <!-- HP Box Header -->
        <div style="background: linear-gradient(180deg, #f0f0f0 0%, #d8d8d8 100%); border: 3px solid #404040;
            border-radius: 8px; padding: 8px 12px; margin-bottom: 8px;
            box-shadow: inset -2px -2px 0 #a0a0a0, inset 2px 2px 0 #ffffff;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-family: 'Press Start 2P', monospace; font-size: 12px; color: #303030;">{name}</span>
                <span style="font-family: 'Press Start 2P', monospace; font-size: 10px; color: #505050;">Lv50</span>
            </div>
            <div style="display: flex; align-items: center; margin-top: 6px;">
                <span style="font-family: 'Press Start 2P', monospace; font-size: 8px; color: #f08030; margin-right: 4px;">HP</span>
                <div style="flex: 1; height: 8px; background: #484848; border-radius: 4px; padding: 2px; box-shadow: inset 1px 1px 0 #202020;">
                    <div class="hp-bar-green" style="width: 100%; height: 100%; background: linear-gradient(180deg, #70f880 0%, #20d070 50%, #18a050 100%); border-radius: 2px;"></div>
                </div>
            </div>
            <div style="text-align: right; margin-top: 4px;">
                <span style="font-family: 'Press Start 2P', monospace; font-size: 10px; color: #303030;">{hp}/{hp}</span>
            </div>
        </div>
        
        <!-- Sprite Area -->
        <div style="text-align: center; padding: 10px; background: linear-gradient(180deg, #b8e0a8 0%, #88c070 100%); 
            border-radius: 8px; margin-bottom: 8px; min-height: 140px; display: flex; justify-content: center; align-items: center;
            position: relative;">
            <div style="position: absolute; bottom: 10px; width: 100px; height: 20px; background: radial-gradient(ellipse at center, rgba(0,0,0,0.3) 0%, transparent 70%);"></div>
            <img src="{sprite_url}" style="width: 120px; height: 120px; image-rendering: pixelated; filter: drop-shadow(2px 2px 0 rgba(0,0,0,0.3)); position: relative; z-index: 1;" />
        </div>
        
        <!-- Type Badges -->
        <div style="text-align: center; margin-bottom: 8px;">{type_badges}</div>
        
        <!-- Stats Panel -->
        <div style="background: #f8f8f8; border: 2px solid #808080; border-radius: 6px; padding: 8px;
            box-shadow: inset -1px -1px 0 #c0c0c0, inset 1px 1px 0 #ffffff;">
            <div style="font-family: 'Press Start 2P', monospace; font-size: 8px; color: #404040; margin-bottom: 6px; text-transform: uppercase;">BASE STATS</div>
            {stats_html}
        </div>
    </div>
    """

def create_hp_bar_html(name: str, hp_percent: int, is_player: bool) -> str:
    """Create a Pokemon-style HP bar."""
    if hp_percent > 50:
        bar_color = "linear-gradient(180deg, #70f880 0%, #20d070 50%, #18a050 100%)"
        bar_class = "hp-bar-green"
    elif hp_percent > 20:
        bar_color = "linear-gradient(180deg, #f8e870 0%, #f8c830 50%, #c8a028 100%)"
        bar_class = "hp-bar-yellow"
    else:
        bar_color = "linear-gradient(180deg, #f88070 0%, #f85030 50%, #c03020 100%)"
        bar_class = "hp-bar-red"
    
    return f"""
    <div style="background: linear-gradient(180deg, #f0f0f0 0%, #d8d8d8 100%); border: 3px solid #404040;
        border-radius: 8px; padding: 8px 12px; margin: 4px 0;
        box-shadow: inset -2px -2px 0 #a0a0a0, inset 2px 2px 0 #ffffff, 4px 4px 0 #303030;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #303030;">{name.upper()}</span>
            <span style="font-family: 'Press Start 2P', monospace; font-size: 9px; color: #505050;">Lv50</span>
        </div>
        <div style="display: flex; align-items: center;">
            <span style="font-family: 'Press Start 2P', monospace; font-size: 8px; color: #f08030; margin-right: 6px;">HP</span>
            <div style="flex: 1; height: 8px; background: #484848; border-radius: 4px; padding: 2px; box-shadow: inset 1px 1px 0 #202020;">
                <div class="{bar_class}" style="width: {hp_percent}%; height: 100%; background: {bar_color}; border-radius: 2px; transition: width 0.5s ease-out;"></div>
            </div>
        </div>
        <div style="text-align: right; margin-top: 4px;">
            <span style="font-family: 'Press Start 2P', monospace; font-size: 10px; color: #303030;">{hp_percent}/100</span>
        </div>
    </div>
    """

def format_battle_log(events: list[dict], turn_number: int = 0, player_name: str = "") -> str:
    """Format battle events into Pokemon game-style HTML with turn separators."""
    if not events:
        prompt = f"What will {player_name} do?" if player_name else "What will you do?"
        return f"""<div style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #303030; 
            text-align: center; padding: 20px; line-height: 2;">{prompt}</div>"""
    
    html = ""
    current_turn = 0
    
    for event in events:
        event_type = event.get("type", "info")
        message = event.get("message", "")
        turn = event.get("turn", 0)
        
        # Add turn separator when turn changes
        if turn > current_turn:
            current_turn = turn
            html += f"""<div style="font-family: 'Press Start 2P', monospace; font-size: 10px; 
                color: #6890f0; padding: 8px 0 4px; margin-top: 8px; 
                border-top: 2px dashed #a0a0a0;">─── TURN {turn} ───</div>"""
        
        # Style based on event type - Pokemon game colors
        styles = {
            "turn_start": "color: #6890f0; font-size: 10px;",
            "speed": "color: #808080; font-size: 9px; padding-left: 8px;",
            "attack": "color: #303030; margin-top: 6px;",
            "stab": "color: #78c850; padding-left: 16px; font-size: 9px;",
            "critical": "color: #f08030; padding-left: 16px;",
            "effectiveness": "color: #78c850; padding-left: 16px;" if "super" in message.lower() else "color: #a040a0; padding-left: 16px;",
            "damage": "color: #505050; padding-left: 16px; font-size: 10px;",
            "miss": "color: #808080; padding-left: 16px;",
            "victory": "color: #20d070; font-weight: bold; background: #e8f8e8; padding: 12px; border: 3px solid #20d070; border-radius: 8px; margin-top: 12px; text-align: center;",
            "defeat": "color: #e03838; font-weight: bold; background: #f8e8e8; padding: 12px; border: 3px solid #e03838; border-radius: 8px; margin-top: 12px; text-align: center;",
            "prompt": "color: #303030; margin-top: 12px; padding-top: 8px; border-top: 2px solid #c0c0c0;",
        }
        
        style = styles.get(event_type, "color: #303030;")
        html += f'<div style="font-family: \'Press Start 2P\', monospace; font-size: 11px; padding: 2px 0; line-height: 1.8; {style}">{message}</div>'
    
    # Wrap in scrollable container
    return f"""<div style="background: #f8f8f8; border: 4px solid #404040; border-radius: 12px; padding: 16px;
        box-shadow: inset -3px -3px 0 #c0c0c0, inset 3px 3px 0 #ffffff, 5px 5px 0 #303030;
        max-height: 350px; overflow-y: auto;">
        {html}
    </div>"""

# ══════════════════════════════════════════════════════════════════════════════
# GRADIO APP
# ══════════════════════════════════════════════════════════════════════════════

# Load custom CSS
css_path = Path(__file__).parent / "theme.css"
custom_css = ""
if css_path.exists():
    custom_css = css_path.read_text()

with gr.Blocks(
    title="Pokemon Battle Simulator",
) as app:
    
    # State
    player_pokemon_state = gr.State(None)
    opponent_pokemon_state = gr.State(None)
    battle_events_state = gr.State([])
    
    # Turn-based battle state
    player_hp_state = gr.State(100)
    opponent_hp_state = gr.State(100)
    max_player_hp_state = gr.State(100)
    max_opponent_hp_state = gr.State(100)
    player_moves_state = gr.State([])  # List of 4 moves with full data
    battle_active_state = gr.State(False)
    turn_counter_state = gr.State(0)  # Track current turn number
    
    # ══════════════════════════════════════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════════════════════════════════════
    
    with gr.Row(elem_id="app-header"):
        gr.HTML("""
            <div style="text-align: center; padding: 16px 0;">
                <h1 id="app-title" style="font-family: 'Press Start 2P', monospace; font-size: 20px; 
                    color: #f8d030;
                    text-shadow: 3px 3px 0 #3068a8, -1px -1px 0 #3068a8, 1px -1px 0 #3068a8, -1px 1px 0 #3068a8, 0 4px 0 #305090;
                    letter-spacing: -1px; margin: 0;">
                    POKEMON BATTLE!
                </h1>
                <p id="app-subtitle" style="font-family: 'Press Start 2P', monospace; font-size: 9px; color: #f8f8f8; 
                    text-shadow: 1px 1px 0 #303030; margin-top: 8px;">
                    GEN I EDITION
                </p>
            </div>
        """)
    
    # ══════════════════════════════════════════════════════════════════════════
    # POKEMON SELECTION
    # ══════════════════════════════════════════════════════════════════════════
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML("<div style='font-family: Press Start 2P, monospace; color: #f8f8f8; font-size: 10px; text-shadow: 1px 1px 0 #303030; margin-bottom: 8px;'>YOUR POKEMON</div>")
            player_dropdown = gr.Dropdown(
                choices=GEN_1_POKEMON,
                value="pikachu",
                label="Select Pokemon",
                filterable=True,
                elem_classes=["pokemon-dropdown"]
            )
            player_info = gr.HTML(
                value=create_pokemon_info_html(None, is_player=True),
                elem_id="player-info"
            )
        
        with gr.Column(scale=1):
            gr.HTML("<div style='font-family: Press Start 2P, monospace; color: #f8f8f8; font-size: 10px; text-shadow: 1px 1px 0 #303030; margin-bottom: 8px;'>ENEMY POKEMON</div>")
            with gr.Row():
                opponent_dropdown = gr.Dropdown(
                    choices=GEN_1_POKEMON,
                    value=None,
                    label="Select Pokemon (or Random)",
                    filterable=True,
                    elem_classes=["pokemon-dropdown"]
                )
                random_btn = gr.Button("RANDOM", size="sm", elem_classes=["pokemon-btn"])
            opponent_info = gr.HTML(
                value=create_pokemon_info_html(None, is_player=False),
                elem_id="opponent-info"
            )
    
    # ══════════════════════════════════════════════════════════════════════════
    # BATTLE CONTROLS
    # ══════════════════════════════════════════════════════════════════════════
    
    with gr.Row():
        with gr.Column(scale=1):
            weather_dropdown = gr.Dropdown(
                choices=WEATHER_EFFECTS,
                value="none",
                label="Weather",
                elem_classes=["pokemon-dropdown"]
            )
        with gr.Column(scale=2):
            with gr.Row():
                start_battle_btn = gr.Button(
                    "START BATTLE!",
                    variant="primary",
                    size="lg",
                    elem_classes=["pokemon-btn", "pokemon-btn-primary"]
                )
                reset_btn = gr.Button(
                    "RUN",
                    size="lg",
                    elem_classes=["pokemon-btn"]
                )
    
    # ══════════════════════════════════════════════════════════════════════════
    # BATTLE ARENA (HP BARS)
    # ══════════════════════════════════════════════════════════════════════════
    
    with gr.Row(visible=False) as battle_arena:
        with gr.Column(scale=1):
            player_hp_bar = gr.HTML(value="")
        with gr.Column(scale=1):
            opponent_hp_bar = gr.HTML(value="")
    
    # ══════════════════════════════════════════════════════════════════════════
    # MOVE SELECTION (2x2 Grid - Pokemon style)
    # ══════════════════════════════════════════════════════════════════════════
    
    gr.HTML("<div style='font-family: Press Start 2P, monospace; color: #f8f8f8; font-size: 10px; text-shadow: 1px 1px 0 #303030; margin: 16px 0 8px;'>SELECT A MOVE:</div>")
    
    with gr.Row(visible=False) as move_selection_area:
        with gr.Column(scale=1):
            with gr.Row():
                move_btn_1 = gr.Button("Move 1", elem_classes=["move-btn"])
                move_btn_2 = gr.Button("Move 2", elem_classes=["move-btn"])
            with gr.Row():
                move_btn_3 = gr.Button("Move 3", elem_classes=["move-btn"])
                move_btn_4 = gr.Button("Move 4", elem_classes=["move-btn"])
    
    # ══════════════════════════════════════════════════════════════════════════
    # BATTLE LOG
    # ══════════════════════════════════════════════════════════════════════════
    
    battle_log = gr.HTML(
        value="""<div style="background: #f8f8f8; border: 4px solid #404040; border-radius: 12px; padding: 16px;
            box-shadow: inset -3px -3px 0 #c0c0c0, inset 3px 3px 0 #ffffff, 5px 5px 0 #303030;
            min-height: 120px;">
            <div style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #303030; line-height: 2;">
                Select both Pokemon and click START BATTLE!
            </div>
        </div>""",
        elem_id="battle-log"
    )
    
    # ══════════════════════════════════════════════════════════════════════════
    # EVENT HANDLERS
    # ══════════════════════════════════════════════════════════════════════════
    
    async def load_player_pokemon(pokemon_name):
        """Load player's Pokemon data and update display."""
        if not pokemon_name:
            return create_pokemon_info_html(None, is_player=True), None
        data = await fetch_pokemon_data(pokemon_name)
        return create_pokemon_info_html(data, is_player=True), data
    
    async def load_opponent_pokemon(pokemon_name):
        """Load opponent's Pokemon data and update display."""
        if not pokemon_name:
            return create_pokemon_info_html(None, is_player=False), None
        data = await fetch_pokemon_data(pokemon_name)
        return create_pokemon_info_html(data, is_player=False), data
    
    async def random_opponent():
        """Select a random opponent Pokemon."""
        choice = random.choice(GEN_1_POKEMON)
        data = await fetch_pokemon_data(choice)
        return choice, create_pokemon_info_html(data, is_player=False), data
    
    async def initialize_battle(player_data, opponent_data, weather):
        """Initialize battle and show move selection."""
        if not player_data or not opponent_data:
            error_msg = """<div style="background: #f8f8f8; border: 4px solid #404040; border-radius: 12px; padding: 16px;
                box-shadow: inset -3px -3px 0 #c0c0c0, inset 3px 3px 0 #ffffff, 5px 5px 0 #303030;">
                <div style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #e03838; line-height: 2;">
                    Select both Pokemon first!
                </div>
            </div>"""
            return (
                error_msg,
                "", "",
                gr.update(visible=False),  # battle_arena
                gr.update(visible=False),  # move_selection_area
                gr.update(value="Move 1"),
                gr.update(value="Move 2"),
                gr.update(value="Move 3"),
                gr.update(value="Move 4"),
                [],  # player_moves_state
                False,  # battle_active
                100, 100, 100, 100,  # HP states
                []  # events
            )
        
        # Get player moves
        player_moves = await get_pokemon_moves(player_data)
        
        # Initialize HP
        max_p1_hp = player_data['stats'][0]['base_stat']
        max_p2_hp = opponent_data['stats'][0]['base_stat']
        
        player_name = player_data['name'].capitalize()
        opponent_name = opponent_data['name'].capitalize()
        player_speed = get_speed(player_data)
        opponent_speed = get_speed(opponent_data)
        
        # Create move button labels with type info
        move_labels = []
        for m in player_moves:
            label = f"{m['name']} ({m['type'].upper()})"
            move_labels.append(label)
        
        # Initialize battle log
        init_msg = f"""<div style="background: #f8f8f8; border: 4px solid #404040; border-radius: 12px; padding: 16px;
            box-shadow: inset -3px -3px 0 #c0c0c0, inset 3px 3px 0 #ffffff, 5px 5px 0 #303030;">
            <div style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #303030; line-height: 2;">
                {player_name} vs {opponent_name}!<br>
                Your SPD: {player_speed} | Enemy SPD: {opponent_speed}<br>
                Weather: {weather.capitalize()}<br><br>
                What will {player_name} do?
            </div>
        </div>"""
        
        return (
            init_msg,
            create_hp_bar_html(player_name, 100, is_player=True),
            create_hp_bar_html(opponent_name, 100, is_player=False),
            gr.update(visible=True),   # battle_arena
            gr.update(visible=True),   # move_selection_area
            gr.update(value=move_labels[0]),
            gr.update(value=move_labels[1]),
            gr.update(value=move_labels[2]),
            gr.update(value=move_labels[3]),
            player_moves,  # player_moves_state
            True,  # battle_active
            max_p1_hp, max_p2_hp, max_p1_hp, max_p2_hp,  # HP states
            []  # events
        )
    
    async def use_move(move_index, player_data, opponent_data, weather, player_hp, opponent_hp, max_p_hp, max_o_hp, player_moves, prev_events, battle_active, turn_counter):
        """Execute a turn with the selected move."""
        if not battle_active or not player_data or not opponent_data or not player_moves:
            return (
                format_battle_log(prev_events) if prev_events else "Select Pokemon and start battle!",
                create_hp_bar_html("???", 100, is_player=True),
                create_hp_bar_html("???", 100, is_player=False),
                gr.update(visible=False),
                player_hp, opponent_hp, prev_events, battle_active, turn_counter
            )
        
        # Increment turn counter
        new_turn = turn_counter + 1
        
        selected_move = player_moves[move_index]
        player_name = player_data['name'].capitalize()
        
        # Execute the turn
        new_p_hp, new_o_hp, events, winner = await run_battle_turn(
            player_data, opponent_data, selected_move, weather,
            player_hp, opponent_hp, max_p_hp, max_o_hp, new_turn
        )
        
        # Combine with previous events
        all_events = prev_events + events
        
        opponent_name = opponent_data['name'].capitalize()
        
        # Check if battle ended
        if winner:
            return (
                format_battle_log(all_events, new_turn, player_name),
                create_hp_bar_html(player_name, int(new_p_hp / max_p_hp * 100), is_player=True),
                create_hp_bar_html(opponent_name, int(new_o_hp / max_o_hp * 100), is_player=False),
                gr.update(visible=False),  # Hide move selection
                new_p_hp, new_o_hp, all_events, False, new_turn  # battle_active = False
            )
        
        return (
            format_battle_log(all_events, new_turn, player_name),
            create_hp_bar_html(player_name, int(new_p_hp / max_p_hp * 100), is_player=True),
            create_hp_bar_html(opponent_name, int(new_o_hp / max_o_hp * 100), is_player=False),
            gr.update(visible=True),  # Keep move selection visible
            new_p_hp, new_o_hp, all_events, battle_active, new_turn
        )
    
    def reset_battle():
        """Reset the battle state."""
        return (
            """<div style="background: #f8f8f8; border: 4px solid #404040; border-radius: 12px; padding: 16px;
                box-shadow: inset -3px -3px 0 #c0c0c0, inset 3px 3px 0 #ffffff, 5px 5px 0 #303030;
                min-height: 120px;">
                <div style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #303030; line-height: 2;">
                    Select both Pokemon and click START BATTLE!
                </div>
            </div>""",
            "", "",
            gr.update(visible=False),  # battle_arena
            gr.update(visible=False),  # move_selection
            100, 100, 100, 100,  # HP states
            [],  # events
            False,  # battle_active
            [],  # player_moves
            0  # turn_counter reset
        )
    
    # Wire up events
    player_dropdown.change(
        fn=load_player_pokemon,
        inputs=[player_dropdown],
        outputs=[player_info, player_pokemon_state]
    )
    
    opponent_dropdown.change(
        fn=load_opponent_pokemon,
        inputs=[opponent_dropdown],
        outputs=[opponent_info, opponent_pokemon_state]
    )
    
    random_btn.click(
        fn=random_opponent,
        inputs=[],
        outputs=[opponent_dropdown, opponent_info, opponent_pokemon_state]
    )
    
    start_battle_btn.click(
        fn=initialize_battle,
        inputs=[player_pokemon_state, opponent_pokemon_state, weather_dropdown],
        outputs=[
            battle_log, player_hp_bar, opponent_hp_bar,
            battle_arena, move_selection_area,
            move_btn_1, move_btn_2, move_btn_3, move_btn_4,
            player_moves_state, battle_active_state,
            player_hp_state, opponent_hp_state, max_player_hp_state, max_opponent_hp_state,
            battle_events_state
        ]
    )
    
    # Move button handlers - create wrapper functions for each move
    async def use_move_1(*args):
        return await use_move(0, *args)
    
    async def use_move_2(*args):
        return await use_move(1, *args)
    
    async def use_move_3(*args):
        return await use_move(2, *args)
    
    async def use_move_4(*args):
        return await use_move(3, *args)
    
    move_inputs = [
        player_pokemon_state, opponent_pokemon_state, weather_dropdown,
        player_hp_state, opponent_hp_state, max_player_hp_state, max_opponent_hp_state,
        player_moves_state, battle_events_state, battle_active_state, turn_counter_state
    ]
    move_outputs = [
        battle_log, player_hp_bar, opponent_hp_bar, move_selection_area,
        player_hp_state, opponent_hp_state, battle_events_state, battle_active_state, turn_counter_state
    ]
    
    move_btn_1.click(
        fn=use_move_1,
        inputs=move_inputs,
        outputs=move_outputs
    )
    move_btn_2.click(
        fn=use_move_2,
        inputs=move_inputs,
        outputs=move_outputs
    )
    move_btn_3.click(
        fn=use_move_3,
        inputs=move_inputs,
        outputs=move_outputs
    )
    move_btn_4.click(
        fn=use_move_4,
        inputs=move_inputs,
        outputs=move_outputs
    )
    
    reset_btn.click(
        fn=reset_battle,
        inputs=[],
        outputs=[
            battle_log, player_hp_bar, opponent_hp_bar,
            battle_arena, move_selection_area,
            player_hp_state, opponent_hp_state, max_player_hp_state, max_opponent_hp_state,
            battle_events_state, battle_active_state, player_moves_state, turn_counter_state
        ]
    )
    
    # Load initial Pokemon on app start
    app.load(
        fn=load_player_pokemon,
        inputs=[player_dropdown],
        outputs=[player_info, player_pokemon_state]
    )


# ══════════════════════════════════════════════════════════════════════════════
# LAUNCH
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import signal
    import sys
    import atexit
    
    def cleanup():
        """Cleanup function called on exit."""
        print("\n  Shutting down server...")
    
    def signal_handler(sig, frame):
        """Handle interrupt signals gracefully."""
        print("\n\n  ⚡ Server stopped. Goodbye! ⚡\n")
        sys.exit(0)
    
    # Register cleanup and signal handlers
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("\n" + "═" * 60)
    print("  ⚡ POKEMON BATTLE SIMULATOR - Enterprise Edition ⚡")
    print("═" * 60)
    print("\n  Starting server...")
    print("  Press Ctrl+C to stop the server.\n")
    
    try:
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            inbrowser=True,  # Automatically open browser
            theme=gr.themes.Base(
                primary_hue=gr.themes.colors.cyan,
                secondary_hue=gr.themes.colors.pink,
                neutral_hue=gr.themes.colors.slate,
            ),
            css=custom_css
        )
    except KeyboardInterrupt:
        print("\n\n  ⚡ Server stopped. Goodbye! ⚡\n")
