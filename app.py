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
# BATTLE LOGIC
# ══════════════════════════════════════════════════════════════════════════════

async def calculate_damage(attacker: dict, defender: dict, move: dict, weather: str, critical: bool = False) -> tuple[float, str]:
    """Calculate damage for an attack. Returns (damage, effectiveness_text)."""
    power = move.get('power') or 50
    attack = attacker['stats'][1]['base_stat']  # Attack stat
    defense = defender['stats'][2]['base_stat']  # Defense stat
    
    # Critical hit multiplier
    crit_mult = 1.5 if critical else 1.0
    
    # Weather multiplier
    weather_mult = 1.0
    move_type = move['type']['name']
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
    
    # Damage formula
    damage = ((2 * 50 / 5 + 2) * power * (attack / defense) / 50 + 2) * effectiveness * weather_mult * crit_mult
    return max(1, int(damage)), effectiveness_text

async def run_battle(pokemon1_name: str, pokemon2_name: str, weather: str) -> list[dict]:
    """
    Run a complete battle and return a list of battle events.
    Each event is a dict with: type, message, p1_hp_percent, p2_hp_percent
    """
    pokemon1 = await fetch_pokemon_data(pokemon1_name)
    pokemon2 = await fetch_pokemon_data(pokemon2_name)
    
    if not pokemon1 or not pokemon2:
        return [{"type": "error", "message": "Failed to load Pokemon data!", "p1_hp": 0, "p2_hp": 0}]
    
    max_hp1 = pokemon1['stats'][0]['base_stat']
    max_hp2 = pokemon2['stats'][0]['base_stat']
    hp1 = max_hp1
    hp2 = max_hp2
    
    events = []
    
    # Weather announcement
    weather_icons = {"rain": "🌧️", "sun": "☀️", "none": "🌤️"}
    events.append({
        "type": "weather",
        "message": f"{weather_icons.get(weather, '')} Weather: {weather.capitalize()}",
        "p1_hp": 100,
        "p2_hp": 100
    })
    
    # Battle start
    events.append({
        "type": "start",
        "message": f"⚔️ {pokemon1['name'].upper()} vs {pokemon2['name'].upper()} - FIGHT!",
        "p1_hp": 100,
        "p2_hp": 100
    })
    
    turn = 0
    max_turns = 50  # Prevent infinite loops
    
    while hp1 > 0 and hp2 > 0 and turn < max_turns:
        turn += 1
        
        # Pokemon 1's turn
        if pokemon1['moves']:
            move1_choice = random.choice(pokemon1['moves'][:4])  # Limit to first 4 moves
            move1_data = await fetch_move_data(move1_choice['move']['url'])
            
            if move1_data:
                critical1 = random.random() < 0.0625  # 1/16 chance
                damage1, eff_text1 = await calculate_damage(pokemon1, pokemon2, move1_data, weather, critical1)
                hp2 = max(0, hp2 - damage1)
                
                msg = f"💥 {pokemon1['name'].capitalize()} uses {move1_data['name'].replace('-', ' ').title()}!"
                events.append({
                    "type": "attack",
                    "message": msg,
                    "p1_hp": int(hp1 / max_hp1 * 100),
                    "p2_hp": int(hp2 / max_hp2 * 100)
                })
                
                if critical1:
                    events.append({
                        "type": "critical",
                        "message": "🎯 A critical hit!",
                        "p1_hp": int(hp1 / max_hp1 * 100),
                        "p2_hp": int(hp2 / max_hp2 * 100)
                    })
                
                if eff_text1:
                    events.append({
                        "type": "effectiveness",
                        "message": f"✨ {eff_text1}",
                        "p1_hp": int(hp1 / max_hp1 * 100),
                        "p2_hp": int(hp2 / max_hp2 * 100)
                    })
                
                events.append({
                    "type": "damage",
                    "message": f"   → {damage1} damage to {pokemon2['name'].capitalize()}!",
                    "p1_hp": int(hp1 / max_hp1 * 100),
                    "p2_hp": int(hp2 / max_hp2 * 100)
                })
        
        if hp2 <= 0:
            events.append({
                "type": "victory",
                "message": f"🏆 {pokemon2['name'].capitalize()} fainted! {pokemon1['name'].capitalize()} WINS!",
                "p1_hp": int(hp1 / max_hp1 * 100),
                "p2_hp": 0,
                "winner": pokemon1['name']
            })
            break
        
        # Pokemon 2's turn
        if pokemon2['moves']:
            move2_choice = random.choice(pokemon2['moves'][:4])
            move2_data = await fetch_move_data(move2_choice['move']['url'])
            
            if move2_data:
                critical2 = random.random() < 0.0625
                damage2, eff_text2 = await calculate_damage(pokemon2, pokemon1, move2_data, weather, critical2)
                hp1 = max(0, hp1 - damage2)
                
                msg = f"💥 {pokemon2['name'].capitalize()} uses {move2_data['name'].replace('-', ' ').title()}!"
                events.append({
                    "type": "attack",
                    "message": msg,
                    "p1_hp": int(hp1 / max_hp1 * 100),
                    "p2_hp": int(hp2 / max_hp2 * 100)
                })
                
                if critical2:
                    events.append({
                        "type": "critical",
                        "message": "🎯 A critical hit!",
                        "p1_hp": int(hp1 / max_hp1 * 100),
                        "p2_hp": int(hp2 / max_hp2 * 100)
                    })
                
                if eff_text2:
                    events.append({
                        "type": "effectiveness",
                        "message": f"✨ {eff_text2}",
                        "p1_hp": int(hp1 / max_hp1 * 100),
                        "p2_hp": int(hp2 / max_hp2 * 100)
                    })
                
                events.append({
                    "type": "damage",
                    "message": f"   → {damage2} damage to {pokemon1['name'].capitalize()}!",
                    "p1_hp": int(hp1 / max_hp1 * 100),
                    "p2_hp": int(hp2 / max_hp2 * 100)
                })
        
        if hp1 <= 0:
            events.append({
                "type": "victory",
                "message": f"🏆 {pokemon1['name'].capitalize()} fainted! {pokemon2['name'].capitalize()} WINS!",
                "p1_hp": 0,
                "p2_hp": int(hp2 / max_hp2 * 100),
                "winner": pokemon2['name']
            })
            break
    
    return events

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

def format_battle_log(events: list[dict]) -> str:
    """Format battle events into Pokemon game-style HTML."""
    if not events:
        return """<div style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #303030; 
            text-align: center; padding: 20px; line-height: 2;">What will you do?</div>"""
    
    html = ""
    for event in events:
        event_type = event.get("type", "info")
        message = event.get("message", "").replace("💥 ", "").replace("🎯 ", "").replace("✨ ", "").replace("🏆 ", "").replace("⚔️ ", "").replace("🌧️ ", "").replace("☀️ ", "").replace("🌤️ ", "")
        
        # Style based on event type - Pokemon game colors
        styles = {
            "weather": "color: #6890f0;",
            "start": "color: #303030; font-weight: bold;",
            "attack": "color: #303030;",
            "critical": "color: #f08030;",
            "effectiveness": "color: #78c850;" if "super" in message.lower() else "color: #a040a0;",
            "damage": "color: #505050; padding-left: 16px;",
            "victory": "color: #e03838; font-weight: bold; background: #f8f8c0; padding: 8px; border: 2px solid #c0a000; margin-top: 8px;",
            "error": "color: #e03838;"
        }
        
        style = styles.get(event_type, "color: #303030;")
        html += f'<div style="font-family: \'Press Start 2P\', monospace; font-size: 11px; padding: 4px 0; line-height: 1.8; {style}">{message}</div>'
    
    # Wrap in scrollable container
    return f"""<div style="background: #f8f8f8; border: 4px solid #404040; border-radius: 12px; padding: 16px;
        box-shadow: inset -3px -3px 0 #c0c0c0, inset 3px 3px 0 #ffffff, 5px 5px 0 #303030;
        max-height: 300px; overflow-y: auto;">
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
                battle_btn = gr.Button(
                    "FIGHT!",
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
    # BATTLE ARENA
    # ══════════════════════════════════════════════════════════════════════════
    
    with gr.Row(visible=False) as battle_arena:
        with gr.Column(scale=1):
            player_hp_bar = gr.HTML(value="")
        with gr.Column(scale=1):
            opponent_hp_bar = gr.HTML(value="")
    
    # ══════════════════════════════════════════════════════════════════════════
    # BATTLE LOG
    # ══════════════════════════════════════════════════════════════════════════
    
    gr.HTML("")
    battle_log = gr.HTML(
        value="""<div style="background: #f8f8f8; border: 4px solid #404040; border-radius: 12px; padding: 16px;
            box-shadow: inset -3px -3px 0 #c0c0c0, inset 3px 3px 0 #ffffff, 5px 5px 0 #303030;
            min-height: 120px;">
            <div style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #303030; line-height: 2;">
                What will you do?
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
    
    async def start_battle(player_data, opponent_data, weather):
        """Execute the battle and return results."""
        if not player_data or not opponent_data:
            return (
                "<div style='color: #ff4757; text-align: center; padding: 1rem;'>⚠️ Please select both Pokemon before battling!</div>",
                "", "",
                gr.update(visible=False),
                []
            )
        
        player_name = player_data['name'].capitalize()
        opponent_name = opponent_data['name'].capitalize()
        
        # Run battle
        events = await run_battle(player_data['name'], opponent_data['name'], weather)
        
        # Get final HP values
        final_event = events[-1] if events else {"p1_hp": 100, "p2_hp": 100}
        p1_hp = final_event.get("p1_hp", 0)
        p2_hp = final_event.get("p2_hp", 0)
        
        return (
            format_battle_log(events),
            create_hp_bar_html(player_name, p1_hp, is_player=True),
            create_hp_bar_html(opponent_name, p2_hp, is_player=False),
            gr.update(visible=True),
            events
        )
    
    def reset_battle():
        """Reset the battle state."""
        return (
            """<div style="background: #f8f8f8; border: 4px solid #404040; border-radius: 12px; padding: 16px;
                box-shadow: inset -3px -3px 0 #c0c0c0, inset 3px 3px 0 #ffffff, 5px 5px 0 #303030;
                min-height: 120px;">
                <div style="font-family: 'Press Start 2P', monospace; font-size: 11px; color: #303030; line-height: 2;">
                    What will you do?
                </div>
            </div>""",
            "", "",
            gr.update(visible=False),
            []
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
    
    battle_btn.click(
        fn=start_battle,
        inputs=[player_pokemon_state, opponent_pokemon_state, weather_dropdown],
        outputs=[battle_log, player_hp_bar, opponent_hp_bar, battle_arena, battle_events_state]
    )
    
    reset_btn.click(
        fn=reset_battle,
        inputs=[],
        outputs=[battle_log, player_hp_bar, opponent_hp_bar, battle_arena, battle_events_state]
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
