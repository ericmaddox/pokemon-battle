import aiohttp
import asyncio
import random
import time

async def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error: {pokemon_name.capitalize()} not found.")
                return None

async def get_move_data(move_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(move_url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error fetching move data from {move_url}")
                return None

async def calculate_damage(attacker, defender, move, weather_effect, critical_hit=False):
    power = move['power'] if move['power'] else 50  # Default power if not specified
    attack = attacker['stats'][1]['base_stat']
    defense = defender['stats'][2]['base_stat']

    # Critical hit multiplier
    crit_multiplier = 1.5 if critical_hit else 1

    # Weather effect multiplier
    weather_multiplier = 1
    if weather_effect == 'rain' and move['type']['name'] == 'water':
        weather_multiplier = 1.5
    elif weather_effect == 'sun' and move['type']['name'] == 'fire':
        weather_multiplier = 1.5

    # Type effectiveness multiplier
    type_url = f"https://pokeapi.co/api/v2/type/{move['type']['name']}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(type_url) as response:
            if response.status == 200:
                type_data_json = await response.json()
            else:
                print(f"Error fetching type data for {move['type']['name']}")
                return 1  # Default minimal damage if data is unavailable

    effectiveness = 1
    for type_info in defender['types']:
        if type_info['type']['name'] in [type['name'] for type in type_data_json['damage_relations']['double_damage_to']]:
            effectiveness *= 2
        if type_info['type']['name'] in [type['name'] for type in type_data_json['damage_relations']['half_damage_to']]:
            effectiveness *= 0.5
        if type_info['type']['name'] in [type['name'] for type in type_data_json['damage_relations']['no_damage_to']]:
            effectiveness *= 0

    # More detailed damage calculation
    damage = ((2 * 50 / 5 + 2) * power * (attack / defense) / 50 + 2) * effectiveness * weather_multiplier * crit_multiplier
    return max(1, damage)

async def evolve_pokemon(pokemon, level):
    if level >= 16 and pokemon['name'] == 'bulbasaur':  # Example: Bulbasaur evolves at level 16
        return await get_pokemon_data('ivysaur')
    elif level >= 32 and pokemon['name'] == 'ivysaur':  # Ivysaur evolves at level 32
        return await get_pokemon_data('venusaur')
    # Add more evolution rules here as needed
    return pokemon

async def battle(pokemon1, pokemon2):
    hp1 = pokemon1['stats'][0]['base_stat']
    hp2 = pokemon2['stats'][0]['base_stat']
    level1 = 5  # Starting level for simplicity, this should be dynamic
    level2 = 5
    exp1 = 0
    exp2 = 0

    weather_effect = random.choice(['rain', 'sun', 'none'])
    battle_log = []

    battle_log.append(f"Weather: {weather_effect.capitalize()}")

    while hp1 > 0 and hp2 > 0:
        # Pokemon 1's turn
        move1 = random.choice(pokemon1['moves'])
        move1_data = await get_move_data(move1['move']['url'])
        critical_hit1 = random.random() < (0.1 + 0.02 * pokemon1['stats'][4]['base_stat'])  # Critical hit chance
        damage_to_2 = await calculate_damage(pokemon1, pokemon2, move1_data, weather_effect, critical_hit1)
        hp2 -= damage_to_2
        log_entry = f"{pokemon1['name'].capitalize()} uses {move1['move']['name']} and deals {damage_to_2} damage."
        if critical_hit1:
            log_entry += " Critical hit!"
        battle_log.append(log_entry)
        print(log_entry)
        await asyncio.sleep(2)

        if hp2 <= 0:
            faint_log = f"{pokemon2['name'].capitalize()} faints! {pokemon1['name'].capitalize()} wins!"
            battle_log.append(faint_log)
            print(faint_log)
            exp1 += 50  # Award experience points
            if exp1 >= 100:
                level1 += 1
                battle_log.append(f"{pokemon1['name'].capitalize()} is now level {level1}!")
                print(f"{pokemon1['name'].capitalize()} is now level {level1}!")
                pokemon1 = await evolve_pokemon(pokemon1, level1)
                exp1 = 0
            break

        # Pokemon 2's turn
        move2 = random.choice(pokemon2['moves'])
        move2_data = await get_move_data(move2['move']['url'])
        critical_hit2 = random.random() < (0.1 + 0.02 * pokemon2['stats'][4]['base_stat'])
        damage_to_1 = await calculate_damage(pokemon2, pokemon1, move2_data, weather_effect, critical_hit2)
        hp1 -= damage_to_1
        log_entry = f"{pokemon2['name'].capitalize()} uses {move2['move']['name']} and deals {damage_to_1} damage."
        if critical_hit2:
            log_entry += " Critical hit!"
        battle_log.append(log_entry)
        print(log_entry)
        await asyncio.sleep(2)

        if hp1 <= 0:
            faint_log = f"{pokemon1['name'].capitalize()} faints! {pokemon2['name'].capitalize()} wins!"
            battle_log.append(faint_log)
            print(faint_log)
            exp2 += 50  # Award experience points
            if exp2 >= 100:
                level2 += 1
                battle_log.append(f"{pokemon2['name'].capitalize()} is now level {level2}!")
                print(f"{pokemon2['name'].capitalize()} is now level {level2}!")
                pokemon2 = await evolve_pokemon(pokemon2, level2)
                exp2 = 0
            break

    # Display levels and experience
    print(f"\n{pokemon1['name'].capitalize()} Level: {level1} Exp: {exp1}")
    print(f"{pokemon2['name'].capitalize()} Level: {level2} Exp: {exp2}")

async def main():
    while True:
        pokemon_name = input("Enter the name of the Pokémon you want to use: ")
        pokemon1 = await get_pokemon_data(pokemon_name)
        if pokemon1:
            break
        print("Please enter a valid Pokémon name.")

    random_id = random.randint(1, 151)  # You can adjust the range as needed
    random_pokemon_name = str(random_id)
    pokemon2 = await get_pokemon_data(random_pokemon_name)
    if not pokemon2:
        return

    print(f"Your Pokémon: {pokemon1['name'].capitalize()}")
    print(f"Opponent: {pokemon2['name'].capitalize()}")

    await battle(pokemon1, pokemon2)

if __name__ == "__main__":
    asyncio.run(main())
