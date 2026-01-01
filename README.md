# Pokemon Battle Simulator

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-5.0+-FF7C00?logo=gradio&logoColor=white)
![License](https://img.shields.io/github/license/ericmaddox/pokemon-battle)
![Stars](https://img.shields.io/github/stars/ericmaddox/pokemon-battle)
![Issues](https://img.shields.io/github/issues/ericmaddox/pokemon-battle)
![Last Commit](https://img.shields.io/github/last-commit/ericmaddox/pokemon-battle)
[![PWA Ready](https://img.shields.io/badge/PWA-Ready-5A0FC8?logo=pwa)](http://localhost:7860)

<div align="center">

# Pokemon Battle Simulator

![Charizard GIF](https://github.com/ericmaddox/pokemon-battle/blob/main/media/charizard.gif)

**A turn-based Pokemon battle simulator with authentic Nintendo-style UI and official game mechanics**

</div>

---

## Features

### Battle Mechanics
- **Official Pokemon Formulas** - HP and stats calculated using Gen 3+ formulas
- **Physical/Special Split** - Uses correct Attack/Defense or Sp.Atk/Sp.Def
- **STAB Bonus** - 1.5x damage for same-type moves
- **Type Effectiveness** - Full type chart from PokeAPI
- **Critical Hits** - 1/16 chance for 1.5x damage (ignores stat drops)
- **Speed-Based Turn Order** - Faster Pokemon attacks first
- **Move Priority** - Quick Attack, etc. go first regardless of speed

### Status Conditions
- **Burn** - 1/16 HP damage per turn, halves physical attack
- **Poison** - 1/8 HP damage per turn
- **Paralysis** - 25% chance to skip turn, 50% speed reduction
- **Sleep** - Can't move for 1-3 turns
- **Freeze** - Can't move, 20% thaw chance per turn

### Stat Stages
- **-6 to +6 stages** for Attack, Defense, Sp.Atk, Sp.Def, Speed
- **Accuracy/Evasion stages** affect hit chance
- Moves like Swords Dance, Growl affect stats

### Battle Animations
- **Sprite shake** when hit
- **Flash effects** on damage
- **Critical hit screen shake**
- **Faint animation** when defeated
- **Victory bounce** for the winner
- **Type-based VFX** - Fire glows orange, Electric flickers, etc.

### Audio
- **Pokemon Cries** - Click the speaker button on any Pokemon card
- Authentic cries from PokeAPI

### Weather Effects
- **Rain** - Boosts Water moves, weakens Fire
- **Sun** - Boosts Fire moves, weakens Water
- **None** - Normal battle conditions

### UI/UX
- **Nintendo-style UI** with Press Start 2P font
- **Live sprites** from PokeAPI (front/back views)
- **Animated HP bars** with color transitions
- **Progressive Web App (PWA)** - Install as desktop/mobile app

### Level Scaling
- **Automatic balance** for mismatched battles
- Weaker Pokemon get higher levels, stronger get lower
- Shows **matchup tier** indicator before battle
- Example: Pikachu (Lv61) vs Snorlax (Lv39) = fair fight!

---

## Quick Start

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

---

## Requirements

- Python 3.10+
- gradio
- httpx

Install with:
```bash
pip install -r requirements.txt
```

---

## How to Play

1. **Select your Pokemon** from the dropdown (all 151 Gen 1 Pokemon!)
2. **Click RANDOM** for an opponent (or select one)
3. **Click the speaker button** to hear their cries
4. **Click START BATTLE!**
5. **Choose a move** from the 4 buttons
6. Watch the turn play out with animations!
7. Repeat until one Pokemon faints!

---

## Battle Mechanics

| Feature | Description |
|---------|-------------|
| **HP Formula** | `((2*Base + IV + EV/4) * Lv)/100 + Lv + 10` |
| **Stat Formula** | `((2*Base + IV + EV/4) * Lv)/100 + 5` |
| **Damage Formula** | `((2*Lv/5+2) * Power * Atk/Def / 50 + 2) * modifiers` |
| **Speed** | Higher SPD attacks first (unless priority moves) |
| **STAB** | 1.5x damage if move type matches Pokemon type |
| **Critical** | 1/16 chance for 1.5x damage |
| **Weather** | Rain boosts Water 1.5x, Sun boosts Fire 1.5x |

---

## Project Structure

```
pokemon-battle/
├── app.py              # Gradio GUI application
├── pokemon_battle.py   # CLI version
├── theme.css           # Nintendo-style CSS + animations
├── requirements.txt    # Dependencies
└── README.md
```

---

## Roadmap

### Completed
- [x] Status effects (Burn, Poison, Paralysis, Sleep, Freeze)
- [x] Stat stages (+6/-6)
- [x] Move priority
- [x] Official HP/stat formulas
- [x] Battle animations
- [x] Pokemon cries
- [x] PWA support
- [x] Level scaling for balanced battles

### Planned
- [ ] Abilities (Intimidate, Levitate, etc.)
- [ ] Held items
- [ ] Multi-hit moves (Fury Attack, etc.)
- [ ] Healing moves (Recover, etc.)
- [ ] Team battles with switching
- [ ] Multiplayer mode

---

## Contributing

Contributions welcome! Open an issue or submit a PR.

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Acknowledgements

- [PokeAPI](https://pokeapi.co/) for Pokemon data and cries
- [Gradio](https://gradio.app/) for the GUI framework
- [The Pokemon Company](https://www.pokemon.com/) for the franchise

---

<div align="right">
  <img src="https://komarev.com/ghpvc/?username=ericmaddox&repo=pokemon-battle&style=for-the-badge&color=2d343c&labelColor=81c7ff&label=Repository%20Views" alt="Repository Views" />
</div>
