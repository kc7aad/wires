# Automated APK Build with GitHub Actions

The lazy person's guide to building your APK! 🚀

## Setup (2 minutes)

### 1. Create a GitHub Repository

- Go to https://github.com/new
- Name it `wires` (or whatever you like)
- Make it **Public** (free builds require public repos)
- Click "Create repository"

### 2. Push the Code

```bash
# Clone the new repo
git clone https://github.com/YOUR_USERNAME/wires.git
cd wires

# Copy all the game files here
# (wires_game.py, main.py, buildozer.spec, requirements.txt, etc.)

# Initialize and push
git add .
git commit -m "Initial commit: Wires game"
git push origin main
```

## Build It! (5-15 minutes)

### 1. Trigger the Build

Once you push, GitHub Actions automatically starts building. You can also manually trigger it:

1. Go to your repo: `https://github.com/YOUR_USERNAME/wires`
2. Click **"Actions"** tab
3. Click **"Build Wires APK"** on the left
4. Click **"Run workflow"** → **"Run workflow"**

### 2. Watch the Build

- The build takes 10-15 minutes
- You'll see a yellow ⏳ icon while building
- It turns 🟢 green when done
- It turns 🔴 red if something fails (unlikely)

### 3. Download Your APK

Once the build finishes:

1. Click the completed workflow run
2. Scroll down to **"Artifacts"** section
3. Click **"wires-apk"**
4. Download `wires-0.1-debug.apk`

## Install on Your Phone

### Option A: Direct Download (Easiest)
```bash
# After downloading the APK, move it to your Android phone
# Open Files app → Downloads → wires-0.1-debug.apk
# Tap to install (may need to enable "Install from unknown sources")
```

### Option B: ADB (If you have USB debugging)
```bash
adb install ~/Downloads/wires-0.1-debug.apk
```

## Troubleshooting

### Build Failed? 
Check the build log:
1. Click the failed workflow run
2. Click **"build"** 
3. Scroll through the output to see the error

Common fixes:
- Make sure `buildozer.spec` is in the root directory
- Make sure `requirements.txt` has kivy listed
- Make sure `main.py` exists and imports wires_game correctly

### APK Won't Install?
- **"Unknown sources"** - Go to Settings → Apps → enable "Install unknown apps" for your file manager
- **"App already installed"** - Uninstall the old version first
- **"Incompatible"** - Make sure your phone is Android 5.0+ (check Settings → About)

### Want to Make Changes?

Just edit the Python code and push again:

```bash
# Edit wires_game.py to change difficulty/colors/etc
nano wires_game.py

# Push the changes
git add .
git commit -m "Tweaked difficulty"
git push origin main

# GitHub Actions builds automatically again!
```

## What the Workflow Does

The GitHub Actions workflow (`.github/workflows/build.yml`) automatically:

1. ✅ Sets up Java + Android SDK + Android NDK
2. ✅ Installs Python + Buildozer
3. ✅ Runs `buildozer android debug`
4. ✅ Uploads the APK as a downloadable artifact
5. ✅ Creates a Release (if pushing to main branch)

This happens completely on GitHub's servers—nothing needed on your machine!

## Pro Tips

### Automatic Releases
Every time you push to the `main` branch, GitHub automatically creates a Release with your APK. You can download old versions from the **Releases** tab.

### Share with Friends
You can share the APK directly:
1. Go to **Releases** tab
2. Share the download link
3. They can install it on their Android phone

### Keep Testing
You can push as often as you want:
```bash
# Make changes
git add .
git commit -m "Tweaked wire physics"
git push origin main

# APK rebuilds automatically!
```

### View Build Logs
If you want to see what's happening during the build:
1. Click **Actions** tab
2. Click the workflow run
3. Click **build** to see the full log

## Files You Need

Make sure these files are in your repo:
```
wires/
├── .github/workflows/build.yml   ← GitHub Actions config
├── wires_game.py                 ← Main game code
├── main.py                       ← Entry point
├── buildozer.spec                ← Build config
├── requirements.txt              ← Python deps
├── README.md                     ← Documentation
└── QUICKSTART.md                 ← Setup guide
```

## Questions?

If the build fails:
1. Check the error message in the build log
2. Make sure all files are committed: `git status`
3. Try pushing again (sometimes transient issues)
4. Check that buildozer.spec exists and is properly formatted

## Summary

```
Code on GitHub → GitHub Actions → APK ready → Download → Install on phone
            (automatic)        (10-15 min)
```

That's it! You're lazy, and that's fine—GitHub does the work now. 😎

Enjoy your Wires game! 🎮
