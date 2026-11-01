SIRI LIBRARY - LIQUID GLASS + 3D SEATS PATCH

Termux-safe install:
1) cd ~/shri-shyam-library
2) mkdir -p siri-patch-v2
3) unzip -o /sdcard/Download/siri_library_liquid_v2.zip -d siri-patch-v2
4) python siri-patch-v2/apply_patch.py
5) npm run build
6) git diff --check

The installer creates a timestamped backup and leaves registration/seat-selection logic intact. Review on localhost before push.
