# Pokemon Battle Simulator

![License](https://img.shields.io/github/license/ericmaddox/pokemon-battle.svg)
![Issues](https://img.shields.io/github/issues/ericmaddox/pokemon-battle.svg)
![Stars](https://img.shields.io/github/stars/ericmaddox/pokemon-battle.svg)

<div align="center">

# ⚡ Pokémon Battle Simulator ⚡

![Charizard GIF](https://github.com/ericmaddox/pokemon-battle/blob/main/media/charizard.gif)

**A turn-based Pokemon battle simulator with authentic Nintendo-style UI**

</div>

---

## 🎮 Features

### GUI Mode (NEW!)
- **Nintendo-style UI** with Press Start 2P font
- **Turn-based battles** - Choose from 4 moves each turn
- **Speed-based turn order** - Faster Pokemon attacks first
- **STAB bonus** - 1.5x damage for same-type moves
- **Physical/Special split** - Uses correct stats for damage
- **Live sprites** from PokeAPI
- **Weather effects** - Rain, Sun, or None
- **Type effectiveness** - Super effective/not very effective
- **Critical hits** with 1/16 chance

### CLI Mode
- Classic terminal-based battles
- Leveling and evolution system
- Async API requests for speed

---

## 🚀 Quick Start

### GUI Mode (Recommended)
```bash
# Clone the repo
git clone https://github.com/ericmaddox/pokemon-battle.git
cd pokemon-battle

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the GUI
python app.py
```
Opens automatically at **http://localhost:7860**

### CLI Mode
```bash
python pokemon_battle.py
```

---

## 📦 Requirements

- Python 3.x
- gradio
- httpx
- aiohttp
- Pillow

Install with:
```bash
pip install -r requirements.txt
```

---

## 🎯 How to Play (GUI)

1. **Select your Pokemon** from the dropdown
2. **Click RANDOM** for an opponent (or select one)
3. **Click START BATTLE!**
4. **Choose a move** from the 4 buttons
5. Watch the turn play out based on speed
6. Repeat until one Pokemon faints!

---

## 🔧 Battle Mechanics

| Feature | Description |
|---------|-------------|
| **Speed** | Higher SPD attacks first |
| **STAB** | 1.5x damage if move type matches Pokemon type |
| **Physical** | Uses Attack vs Defense |
| **Special** | Uses Sp.Atk vs Sp.Def |
| **Critical** | 1/16 chance for 1.5x damage |
| **Weather** | Rain boosts Water, Sun boosts Fire |

---

## 📁 Project Structure

```
pokemon-battle/
├── app.py              # Gradio GUI application
├── pokemon_battle.py   # CLI version
├── theme.css           # Nintendo-style CSS
├── requirements.txt    # Dependencies
└── README.md
```

---

## 🗺️ Roadmap

- [ ] Status effects (Burn, Poison, Paralysis)
- [ ] Stat stages (+6/-6 from moves like Swords Dance)
- [ ] Team battles with Pokemon switching
- [ ] Abilities (Intimidate, Levitate, etc.)
- [ ] Held items
- [ ] Multiplayer mode

---

## 🤝 Contributing

Contributions welcome! Open an issue or submit a PR.

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgements

- [PokéAPI](https://pokeapi.co/) for Pokemon data
- [Gradio](https://gradio.app/) for the GUI framework
- [The Pokémon Company](https://www.pokemon.com/) for the franchise

---

<div align="right">
  <img src="https://komarev.com/ghpvc/?username=ericmaddox&repo=pokemon-battle&style=for-the-badge&color=2d343c&labelColor=81c7ff&label=Repository%20Views" alt="Repository Views" />
</div>
