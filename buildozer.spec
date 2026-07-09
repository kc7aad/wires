[app]

# (str) Title of your application
title = Wires

# (str) Package name
package.name = wires

# (str) Package domain (needed for android/ios packaging)
package.domain = org.wires

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source includes (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source excludes (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of exclusions using pattern matching
#source.exclude_patterns = tests/*,bin/*

# (list) Garden requirements
#garden_requirements =

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (list) List of service to declare
#services = MyService

#############################################
# Python for android (p4a) specific
#############################################

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash of the application (image or text+image)
# presplash.filename = %(source.dir)s/data/presplash.png

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19c

# (bool) Use -- only make the code in src/ and main.py accessable from the apk
#android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (bool) Indicate if the screen should stay on
android.screenontime = 0

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

# (bool) Disable name space check
android.allow_backup = True

#############################################
# Python for android (p4a) requirements
#############################################

# (list) python for android (p4a) modules (see pygame_sdl2 wiki)
# leave empty to let python for android choose defaults
# you can use this variable to install custom recipes from different repos
p4a.bootstrap = sdl2

# (list) Modules to compile with python for android
p4a.local_recipes = ./recipes

# (list) requirements
# comma seperated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#############################################
# Android specific
#############################################

# (bool) Indicate if the application should request the WRITE_EXTERNAL_STORAGE permission
#android.permissions = WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (int) overrides automatic versionCode generation
android.numeric_version = 1

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

# (bool) fopen write mode will be changed to 'a' if possible
android.allow_backup = True

#############################################
# Build
#############################################

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning upon buildozer run if buildozer.spec differs from the last build config
warn_on_root = 1
