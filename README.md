# Racing Game — Freeplay Prototype

This repository is a starting point for a freeplay racing game. It includes a small Python + Pygame prototype showing a top-down freeplay mode with simple AI traffic and a controllable car.

## Run the prototype (local)

1. Create a virtual environment and install dependencies.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the demo

```bash
python -m game
```

Controls:
- Arrow keys: accelerate/steer
- R: reset player position
- T: spawn a new AI car
- D: toggle debug info

## Goals / Next steps
- Replace the prototype with Godot for better quality visuals and export options.
- Improve physics: tire friction, drifting, collision
- Add sound, UI, day/night, weather
- Add map, checkpoints, and mission generator for freeplay objectives

If you want to use the prototype as a code reference while building a higher quality game, I can help port it to Godot/Unity and guide asset and testing setup.

Shareable link
 - The repository is already hosted at: `https://github.com/s-madelynmbarksdale-ops/racing-game`
 - I'll push the latest changes to `main` so you can share that URL. After I push, open that link to view or share the project.

Quick headless smoke-test (CI-friendly)
```bash
# run for 2 seconds headless to ensure imports and main loop run without a display
GAME_TEST_SECONDS=2 SDL_VIDEODRIVER=dummy python -m game
```