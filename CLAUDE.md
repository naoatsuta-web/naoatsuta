# CLAUDE.md

## Project Overview

This is a Mario Kart-style 2D racing game built with vanilla HTML5, CSS3, and JavaScript. The game uses the HTML5 Canvas API for rendering and has zero external dependencies. No build tools, bundlers, or package managers are used.

**Language:** Japanese (UI text and code comments are in Japanese)

## Repository Structure

```
/
├── index.html   # Entry point – loads style.css and game.js
├── style.css    # All styling (UI overlays, start/result screens, HUD)
├── game.js      # Entire game logic (constants, state, physics, rendering, AI)
├── README.md    # Minimal project readme
└── CLAUDE.md    # This file
```

This is a flat, single-page application with no subdirectories for source code.

## How to Run

Open `index.html` directly in a browser, or serve the directory with any static file server:

```sh
# Example using Python
python3 -m http.server 8000
# Then visit http://localhost:8000
```

No install, build, or compile step is required.

## Architecture

### Game Loop Pattern

The game uses `requestAnimationFrame` for the main loop in `gameLoop()`:

1. **Render phase** — draws track, item boxes, karts, ground items, flying items, minimap
2. **Update phase** (only when `gameState === 'playing'`) — updates player, CPU karts, flying items, UI

### Game States

The `gameState` variable controls flow: `'menu'` → `'countdown'` → `'playing'` → `'finished'`

### Key Constants (game.js)

| Constant | Value | Description |
|---|---|---|
| `CANVAS_WIDTH` / `CANVAS_HEIGHT` | 800 / 600 | Canvas dimensions |
| `MAX_SPEED` | 8 | Top speed for karts |
| `ACCELERATION` | 0.15 | Speed increase per frame |
| `TURN_SPEED` | 0.05 | Steering rate |
| `TOTAL_LAPS` | 3 | Laps to complete the race |
| `TRACK_WIDTH` | 200 | Width of the drivable track area |

### Core Systems

- **Player input:** Arrow keys for acceleration/braking/steering, spacebar for item use. Tracked via `keys` object with `keydown`/`keyup` listeners.
- **Physics:** Acceleration, friction, off-track speed penalty (50%), distance-based collision detection.
- **AI (CPU karts):** 5 opponents with checkpoint-based pathfinding, targeting 70-90% of max speed with randomization.
- **Item system:** 4 power-up types — Banana (ground trap), Shell (projectile), Star (speed boost + invincibility), Mushroom (speed boost). Collected from item boxes on the track.
- **Track:** Defined by 8 `trackPoints` forming a circuit, with 8 `checkpoints` for lap counting.
- **Rendering:** Canvas 2D context draws everything — track, karts (as colored circles with direction indicators), minimap, HUD elements.

### UI Layers

HTML overlays on top of the canvas handle:
- Start screen with controls explanation
- Countdown display (3, 2, 1, GO!)
- In-game HUD: lap counter, position, item box, speed meter
- Result screen with finish time and position

## Development Conventions

### Code Style
- All game logic resides in a single `game.js` file using global scope
- Comments are written in Japanese
- ES6+ syntax (const/let, arrow functions, template literals)
- No modules, classes, or imports — pure procedural/functional style

### No Build Tooling
- No `package.json`, no npm dependencies
- No linter, formatter, or type checker configured
- No testing framework — test manually in-browser

### No CI/CD
- No GitHub Actions or other CI pipelines
- No deployment configuration

## Controls Reference

| Key | Action |
|---|---|
| Arrow Up | Accelerate |
| Arrow Down | Brake |
| Arrow Left/Right | Steer |
| Spacebar | Use item |

## Key Functions in game.js

| Function | Purpose |
|---|---|
| `gameLoop()` | Main loop — render + update |
| `updatePlayer()` | Player movement, input handling, collision |
| `updateCPU(cpu)` | AI kart behavior and pathfinding |
| `drawTrack()` | Renders the circuit on canvas |
| `checkCheckpoint()` | Lap progress and race completion |
| `useItem()` | Activates held power-up |
| `calculatePositions()` | Determines race standings |
| `drawMinimap()` | Renders the minimap overlay |
| `startCountdown()` | Initiates the pre-race countdown |

## Notes for AI Assistants

- This is a zero-dependency vanilla JS project. Do not introduce build tools or package managers unless explicitly requested.
- All game code is in one file (`game.js`). Keep it that way unless the user asks to refactor.
- UI text and comments are in Japanese. Maintain this convention when adding new UI text or comments.
- The game runs entirely client-side. There is no server component, database, or API.
- When testing changes, simply reload `index.html` in a browser.
