Siri Library liquid-glass patch — corrected package

Run only from the project root: ~/shri-shyam-library

  unzip -o siri_library_liquid_v2_fixed.zip -d siri-patch-v2-fixed
  python siri-patch-v2-fixed/apply_patch.py
  npm run build
  git diff --check

The apply script checks the expected feature layout and creates a backup before writing.
Do not push until the local site has been inspected on mobile.
