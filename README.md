# Pokémon Battle Simulator ![Charizard GIF](https://github.com/ericmaddox/pokemon-battle/blob/main/media/charizard.gif)

Welcome to the Pokémon Battle Simulator! This project allows you to simulate Pokémon battles using data from the PokéAPI. You can choose your Pokémon, battle against random opponents, and experience dynamic battle features including weather effects, status effects, critical hits, healing moves, evolution, and now an enhanced leveling system!

## Features

- Choose Your Pokémon: Select your favorite Pokémon to battle with.
- Random Opponents: Battle against randomly selected Pokémon.
- Dynamic Battle Mechanics: Experience battles with weather effects, critical hits, and more.
- Evolution: Watch your Pokémon evolve after gaining enough experience.
- Leveling System: Pokémon level up and evolve based on experience points (EXP).
- Critical Hit Enhancements: Critical hit chances are now dynamically calculated based on stats.
- Detailed Battle Log: Follow the battle with a detailed log of each move and event.
- Turn-based Strategy: Players and opponents take turns choosing moves with type effectiveness and weather factors influencing the battle.
- Asynchronous Requests: API calls are now faster thanks to asynchronous requests.

## Requirements

- Python 3.x
- requests library
- asyncio for asynchronous requests

You can install the necessary dependencies using pip:

```sh
pip install -r requirements.txt
```

## How to Run

1. Clone the repository:
```sh
git clone https://github.com/ericmaddox/pokemon-battle.git
```

2. Navigate to the project directory:
```sh
cd pokemon-battle
```

3. Run the script:
```sh
python pokemon_battle.py
```

4. Enter the name of the Pokémon you want to use and enjoy the battle!

## Usage

When you run the script, you'll be prompted to enter the name of your Pokémon. The script will then randomly select an opponent and simulate a battle. The battle log will be displayed in the terminal, showing each move and the resulting damage.

## Future Enhancements Roadmap

- Trainer Customization: Customize your trainer's name and appearance.
- Battle Arenas: Add different battle arenas with unique effects.
- Multiplayer Mode: Implement local or online multiplayer battles.
- AI Opponents: Create AI opponents with varying difficulty levels.
- Item Usage: Allow trainers to use items during battles.
- Special Moves: Introduce special moves like Z-Moves or Mega Evolutions.
- Battle Animations: Add animations for moves and status effects.

## Release Notes for `pokemon_battle.py`

### **Version 1.0.1 - Asynchronous Requests and Code Improvements**  
**Release Date:** [December 7th, 2024]

This release introduces several major updates to the Pokémon Battle script, improving gameplay mechanics, performance, and overall code structure.

#### New Features:
1. **Leveling System**: Pokémon now level up and evolve based on experience points (EXP). Evolution is triggered at specific levels (e.g., Bulbasaur evolves into Ivysaur at level 16).
2. **Critical Hit Enhancements**: Pokémon now have a dynamically calculated critical hit chance based on their stats (e.g., Speed). Critical hits provide a 1.5x damage multiplier.
3. **Asynchronous Requests**: API calls (e.g., to fetch Pokémon data or move data) are now asynchronous, reducing wait times during battle and data retrieval.
4. **Battle Logic**: Turn-based strategy is now implemented, with players and opponents taking turns choosing moves. The battle UI displays important information like health and move choices, and type effectiveness and weather effects are factored into damage calculations.
5. **Expanded Evolution Logic**: Evolution now respects Pokémon evolutionary chains and handles missing evolutions properly. Additional evolutionary rules can easily be added.
6. **Damage Variance**: Damage calculations now have slight randomness to add variability, making each battle feel more dynamic.

#### Code Improvements:
1. **Modularized Functions**: Functions like `battle()` and `calculate_damage()` were broken down into smaller, reusable components for better readability and maintainability.
2. **Error Handling**: More robust error handling was added for API requests to ensure stability and smooth user experience, even in case of failed requests.
3. **Caching**: Implemented LRU (Least Recently Used) caching for type data to minimize redundant API calls and speed up data retrieval.
4. **Constants and Validation**: Introduced constants for common values (e.g., experience thresholds) to make the code more maintainable. Added validation for missing or invalid data to prevent crashes during runtime.

### Dependencies:
- `requests==2.26.0`
- `asyncio` for asynchronous requests.

### Installation:
To install the dependencies, run the following command:

```sh
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! If you have any ideas or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ericmaddox/pokemon-battle/blob/main/LICENSE) file for details.

## Acknowledgements

- [PokéAPI](https://pokeapi.co/) for providing the Pokémon data.
- [Python Requests](https://pypi.org/project/requests/) for making HTTP requests easy.
- [asyncio](https://docs.python.org/3/library/asyncio.html) for simplifying asynchronous programming in Python.
- [The Pokémon Company](https://www.pokemon.com/us/) for creating and owning the Pokémon franchise. You can find more information about them at The Pokémon Company.

Enjoy battling!
