# Wires - Quick Start Guide

## Test on Desktop (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the game
python main.py
```

Click and drag wires on the game board to untangle them!

## Build for Android (30 minutes)

### Setup (One-time)

1. **Install Buildozer:**
   ```bash
   pip install buildozer
   ```

2. **Install Android tools** (if not already installed):
   ```bash
   # macOS
   brew install android-sdk android-ndk openjdk@11
   
   # Ubuntu/Debian
   sudo apt-get install android-sdk android-ndk openjdk-11-jdk
   
   # Windows - Download from:
   # - Android Studio: https://developer.android.com/studio
   # - Java SDK: https://www.oracle.com/java/technologies/downloads/
   ```

3. **Set environment variables:**
   ```bash
   # macOS/Linux
   export ANDROID_SDK_ROOT=/path/to/android-sdk
   export ANDROID_NDK_ROOT=/path/to/android-ndk
   
   # Windows (in Command Prompt as Administrator)
   set ANDROID_SDK_ROOT=C:\path\to\android-sdk
   set ANDROID_NDK_ROOT=C:\path\to\android-ndk
   ```

### Build & Deploy

```bash
# Build debug APK
buildozer android debug

# The APK is in: bin/wires-0.1-debug.apk

# Deploy to connected device
adb install bin/wires-0.1-debug.apk

# Or use buildozer one-command deploy
buildozer android debug deploy run
```

### Enable USB Debugging on Android

1. Go to **Settings → About Phone**
2. Tap **Build Number** 7 times
3. Go to **Settings → Developer Options**
4. Enable **USB Debugging**
5. Connect via USB and allow the connection prompt

## Game Controls

- **Tap and drag** any part of a wire to move it
- **Reset button** restarts the current level
- **Swipe up** to return to the level selection menu (in some builds)

## Testing Features

### Level 1 (Easy)
- 3 wires, minimal tangling
- Perfect for learning controls

### Levels 2-3 (Medium)
- 4-5 wires, moderate complexity
- Requires strategy

### Levels 4-5 (Hard)
- 5-6 wires, heavy tangling
- Challenging physics interactions

## Troubleshooting

**"Python module not found"**
→ Run `pip install -r requirements.txt`

**Game runs slowly on desktop**
→ Reduce window size or run on a device

**Build fails**
→ Run `buildozer android clean` then retry

**APK won't install**
→ Uninstall previous version: `adb uninstall org.wires.wires`

## File Structure

```
wires_game/
├── main.py                 # Entry point
├── wires_game.py          # Game code
├── buildozer.spec         # Android build config
├── requirements.txt       # Python dependencies
├── README.md              # Full documentation
└── QUICKSTART.md          # This file
```

## Next Steps

1. Test on desktop
2. Customize difficulty (edit `get_difficulty_params()` in wires_game.py)
3. Build and test on Android device
4. Adjust wire colors, physics, or game mechanics as desired

Enjoy the game! 🎮
