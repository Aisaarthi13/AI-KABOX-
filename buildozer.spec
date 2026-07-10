[app]

# (str) Title of your application
title = AI KABOX Pro

# (str) Package name
package.name = kabox

# (str) Package domain (needed for android/ios packaging)
package.domain = org.aisaarthi

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (BOHOT ZAROORI: isme 'kv' hona chahiye)
source.include_exts = py,png,jpg,jpeg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# Yahan humne requests aur pillow add kiya hai jo hamari API aur image compression ke liye chahiye
requirements = python3, kivy==2.3.0, kivymd==1.2.0, requests, pillow, urllib3, charset-normalizer, idna, certifi

# (str) Supported orientations (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# INTERNET Gemini ke liye, baaki Camera aur Gallery access ke liye
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
