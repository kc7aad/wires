# Wires - Android Puzzle Game

A fun wire untangling puzzle game for Android. Drag and pull colored wires to untangle them. Progress through 5 increasingly difficult levels!

## Game Overview

**Objective:** Untangle all colored wires in each level to complete it.

- **5 Levels** with progressive difficulty
- **Multiple colored wires** (each a different color)
- **Touch controls** - tap and drag wires to move them
- **Physics-based interactions** - wires resist being pushed through each other
- **Visual feedback** - wires highlight their untangled status

## Level Progression

| Level | Wires | Difficulty | Wire Length |
|-------|-------|-----------|------------|
| 1 | 3 | Easy | 150-250px |
| 2 | 4 | Medium | 200-300px |
| 3 | 5 | Hard | 250-350px |
| 4 | 5 | Very Hard | 300-400px |
| 5 | 6 | Expert | 300-450px |

## How to Play

1. **Main Menu** - Select a level from the menu (you can start at any level)
2. **Gameplay** - The game board shows tangled colored wires
3. **Untangle** - Tap and drag any part of a wire to move it
4. **Objective** - Separate all wires so they don't overlap
5. **Level Complete** - Once all wires are untangled, you'll see a completion message
6. **Next Level** - Progress to the next level or retry the current one

## Technical Details

### Architecture

- **Wire Class** - Manages individual wire geometry, physics, and state
- **Point Class** - Represents 2D points along a wire's path
- **WireGameWidget** - Core game logic, physics, and rendering
- **GameScreen** - UI and level management
- **MenuScreen** - Main menu and navigation

### Game Mechanics

1. **Wire Generation** - Each wire is generated as a series of connected points forming a path
2. **Tangling Algorithm** - Wires are tangled by pushing intersection points apart
3. **Drag Mechanics** - Touching a wire applies force to that point and nearby points
4. **Untangle Detection** - Wires are considered untangled when they cross less than 5 times
5. **Difficulty Scaling** - Later levels have more wires, longer wires, and stronger tangles

## Building for Android

### Prerequisites

1. **Python 3.8+**
2. **Kivy** - Install with: `pip install kivy`
3. **Buildozer** - Install with: `pip install buildozer`
4. **Android SDK** - Required for APK building
5. **Java Development Kit (JDK)** - Required for building

### Quick Build

```bash
# Navigate to the game directory
cd /path/to/wires

# Build the APK
buildozer -u python3,kivy android debug

# The APK will be in ./bin/wires-0.1-debug.apk
```

### Install on Device

```bash
# Connect your Android device via USB (with USB debugging enabled)
adb install bin/wires-0.1-debug.apk

# Or use buildozer to deploy directly
buildozer android debug deploy run
```

### Troubleshooting Build Issues

**Issue: BuildozerException: ./buildozer.spec not found**
- Solution: Make sure you're in the directory with `buildozer.spec`

**Issue: Java/SDK not found**
- Solution: Install Android SDK and set `ANDROID_SDK_ROOT` environment variable

**Issue: Build fails due to missing dependencies**
- Solution: Try `buildozer android clean` then rebuild

## Running on Desktop (Development)

For quick testing on desktop:

```bash
# Install dependencies
pip install kivy

# Run the game
python3 wires_game.py
```

The game will run in a window. Touch controls work with mouse clicks.

## Code Structure

```
wires_game.py
├── Point                  # 2D point class
├── Wire                   # Wire physics and state
├── WireGameWidget         # Game board and logic
├── GameScreen             # Level UI
├── MenuScreen             # Main menu
└── WiresGame              # App root
```

## Features

### Current Features
- ✅ 5 levels with increasing difficulty
- ✅ 3-6 wires per level
- ✅ Color-coded wires
- ✅ Touch-based drag mechanics
- ✅ Physics-based wire interactions
- ✅ Untangle detection
- ✅ Level progression
- ✅ Reset level functionality
- ✅ How to play instructions

### Potential Enhancements
- 🎨 Particle effects for untangling
- 🎵 Sound effects and background music
- ⏱️ Timer for speedrun challenges
- 🏆 High scores and statistics
- 🎯 Hint system
- 📈 Dynamic difficulty based on player performance
- 🎨 Customizable themes

## System Requirements

### Mobile
- Android 5.0 (API 21) or higher
- 50MB free space
- Touch screen

### Desktop (Development)
- Python 3.8+
- 100MB free space
- Any OS (Windows, macOS, Linux)

## Game Performance

- **Target FPS:** 60
- **Render Updates:** 10 FPS (UI)
- **Physics Updates:** 60 FPS (game logic)

The game is optimized for mobile devices with lower specifications while maintaining smooth gameplay on modern devices.

## Tips for Players

1. **Start Slow** - Take your time on early levels to understand the mechanics
2. **Small Movements** - Large drags can make tangles worse
3. **Work One Wire** - Focus on untangling one wire at a time
4. **Use the Endpoints** - The start and end of wires are easier to drag
5. **Watch for Intersections** - Look for where wires cross and pull them apart
6. **Don't Give Up** - Later levels are challenging but always solvable!

## Known Limitations

- Wire rendering is simplified (single line) rather than 3D-style
- No persistent save state (progress resets on app close)
- Limited to portrait orientation
- No online leaderboards

## License

This game is free to use and modify for personal and educational purposes.

## Contact & Support

For issues or suggestions, feel free to reach out!

Enjoy untangling! 🎮✨
