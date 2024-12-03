import requests
import random
import time

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {pokemon_name.capitalize()} not found.")
        return None

def get_move_data(move_url):
    response = requests.get(move_url)
    return response.json()

def calculate_damage(attacker, defender, move, weather_effect, critical_hit=False):
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
    type_data = requests.get(type_url).json()
    effectiveness = 1
    for type_info in defender['types']:
        if type_info['type']['name'] in [type['name'] for type in type_data['damage_relations']['double_damage_to']]:
            effectiveness *= 2
        if type_info['type']['name'] in [type['name'] for type in type_data['damage_relations']['half_damage_to']]:
            effectiveness *= 0.5
        if type_info['type']['name'] in [type['name'] for type in type_data['damage_relations']['no_damage_to']]:
            effectiveness *= 0

    # More detailed damage calculation
    damage = ((2 * 50 / 5 + 2) * power * (attack / defense) / 50 + 2) * effectiveness * weather_multiplier * crit_multiplier
    return max(1, damage)

def evolve_pokemon(pokemon):
    evolution_url = pokemon['species']['url']
    species_data = requests.get(evolution_url).json()
    if species_data['evolution_chain']:
        evolution_chain_url = species_data['evolution_chain']['url']
        chain_data = requests.get(evolution_chain_url).json()
        current_stage = chain_data['chain']
        while current_stage['species']['name'] != pokemon['name']:
            current_stage = current_stage['evolves_to'][0]
        if current_stage['evolves_to']:
            next_stage = current_stage['evolves_to'][0]['species']['name']
            return get_pokemon_data(next_stage)
    return pokemon

def battle(pokemon1, pokemon2):
    hp1 = pokemon1['stats'][0]['base_stat']
    hp2 = pokemon2['stats'][0]['base_stat']
    level1 = 50
    level2 = 50
    exp1 = 0
    exp2 = 0
    status1 = None
    status2 = None

    weather_effect = random.choice(['rain', 'sun', 'none'])
    battle_log = []

    battle_log.append(f"Weather: {weather_effect.capitalize()}")

    while hp1 > 0 and hp2 > 0:
        # Pokemon 1's turn
        move1 = random.choice(pokemon1['moves'])
        move1_data = get_move_data(move1['move']['url'])
        critical_hit1 = random.random() < 0.1
        damage_to_2 = calculate_damage(pokemon1, pokemon2, move1_data, weather_effect, critical_hit1)
        hp2 -= damage_to_2
        log_entry = f"{pokemon1['name'].capitalize()} uses {move1['move']['name']} and deals {damage_to_2} damage."
        if critical_hit1:
            log_entry += " Critical hit!"
        battle_log.append(log_entry)
        print(log_entry)
        time.sleep(2)

        if hp2 <= 0:
            faint_log = f"{pokemon2['name'].capitalize()} faints! {pokemon1['name'].capitalize()} wins!"
            battle_log.append(faint_log)
            print(faint_log)
            exp1 += 50  # Award experience points
            if exp1 >= 100:
                battle_log.append(f"{pokemon1['name'].capitalize()} is evolving!")
                print(f"{pokemon1['name'].capitalize()} is evolving!")
                pokemon1 = evolve_pokemon(pokemon1)
                exp1 = 0
            break

        # Pokemon 2's turn
        move2 = random.choice(pokemon2['moves'])
        move2_data = get_move_data(move2['move']['url'])
        critical_hit2 = random.random() < 0.1
        damage_to_1 = calculate_damage(pokemon2, pokemon1, move2_data, weather_effect, critical_hit2)
        hp1 -= damage_to_1
        log_entry = f"{pokemon2['name'].capitalize()} uses {move2['move']['name']} and deals {damage_to_1} damage."
        if critical_hit2:
            log_entry += " Critical hit!"
        battle_log.append(log_entry)
        print(log_entry)
        time.sleep(2)

        if hp1 <= 0:
            faint_log = f"{pokemon1['name'].capitalize()} faints! {pokemon2['name'].capitalize()} wins!"
            battle_log.append(faint_log)
            print(faint_log)
            exp2 += 50  # Award experience points
            if exp2 >= 100:
                battle_log.append(f"{pokemon2['name'].capitalize()} is evolving!")
                print(f"{pokemon2['name'].capitalize()} is evolving!")
                pokemon2 = evolve_pokemon(pokemon2)
                exp2 = 0
            break

    # Display levels and experience
    print(f"\n{pokemon1['name'].capitalize()} Level: {level1} Exp: {exp1}")
    print(f"{pokemon2['name'].capitalize()} Level: {level2} Exp: {exp2}")

def main():
    while True:
        pokemon_name = input("Enter the name of the Pokémon you want to use: ")
        pokemon1 = get_pokemon_data(pokemon_name)
        if pokemon1:
            break
        print("Please enter a valid Pokémon name.")

    random_id = random.randint(1, 151)  # You can adjust the range as needed
    random_pokemon_name = str(random_id)
    pokemon2 = get_pokemon_data(random_pokemon_name)
    if not pokemon2:
        return

    print(f"Your Pokémon: {pokemon1['name'].capitalize()}")
    print(f"Opponent: {pokemon2['name'].capitalize()}")

    battle(pokemon1, pokemon2)

if __name__ == "__main__":
    main()
