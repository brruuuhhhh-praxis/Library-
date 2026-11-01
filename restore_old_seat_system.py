#!/usr/bin/env python3
"""Restore the previous seat-selection workflow from commit 6203771 only.
Keeps the current registration number and after-registration print/PDF flow.
Run from the repository root (e.g. ~/shri-shyam-library).
"""
from pathlib import Path
from datetime import datetime
import shutil, subprocess, sys

ROOT = Path.cwd()
REG = ROOT / 'src' / 'Registration.jsx'
if not (ROOT / '.git').exists() or not REG.exists():
    sys.exit('ERROR: Run this script from the ~/shri-shyam-library repository root.')

BASE = '6203771'
try:
    old = subprocess.check_output(['git', 'show', f'{BASE}:src/Registration.jsx'], text=True, encoding='utf-8')
except subprocess.CalledProcessError:
    sys.exit(f'ERROR: Could not read {BASE}:src/Registration.jsx from Git history.')
current = REG.read_text(encoding='utf-8')

# Extract only the previous seat-picker UI; do not restore the whole file.
start_token = '      <div className="booking-seat-head">'
end_token = '      {error && <div className="booking-error"'

def get_section(src):
    start = src.find(start_token)
    end = src.find(end_token, start + len(start_token)) if start >= 0 else -1
    if start < 0 or end < 0:
        return None
    return src[start:end]

old_seat_section = get_section(old)
cur_seat_section = get_section(current)
if old_seat_section is None or cur_seat_section is None:
    sys.exit('ERROR: Could not safely find the seat-selection section in both versions. No files changed.')

# Confirm key expected edits can be made before writing anything.
old_validation_lines = [ln for ln in old.splitlines() if 'if (!form.seat_no)' in ln]
if not old_validation_lines:
    sys.exit('ERROR: Old version did not contain the expected seat-required validation. No files changed.')
validation = old_validation_lines[0].strip()
if 'seat_no: null, status:' not in current:
    sys.exit('ERROR: Expected current seat_no:null payload not found; no files changed.')
if 'setReceipt({ id: submittedId, registration_no:' not in current:
    sys.exit('ERROR: Current Registration Number logic not found; no files changed.')
if 'const submittedId' not in current:
    sys.exit('ERROR: Could not find submission anchor; no files changed.')

updated = current.replace(cur_seat_section, old_seat_section, 1)
updated = updated.replace('seat_no: null, status:', 'seat_no: Number(form.seat_no), status:', 1)

# Re-enable the previous requirement that a seat be selected before submitting.
if 'if (!form.seat_no)' not in updated:
    anchor = 'const submittedId'
    pos = updated.find(anchor)
    if pos < 0:
        sys.exit('ERROR: Submission anchor moved during patching; no files changed.')
    line_start = updated.rfind('\n', 0, pos) + 1
    indent = updated[line_start:pos]
    updated = updated[:line_start] + indent + validation + '\n' + updated[line_start:]

# Keep the new registration number while recording the seat selected by the member.
marker = 'setReceipt({ id: submittedId, registration_no:'
p = updated.find(marker)
if p < 0:
    sys.exit('ERROR: Could not update receipt seat number safely; no files changed.')
q = updated.find('});', p)
if q < 0:
    sys.exit('ERROR: Could not find end of receipt expression; no files changed.')
snippet = updated[p:q]
if 'seat_no: null' not in snippet:
    sys.exit('ERROR: Receipt seat field did not match the expected pattern; no files changed.')
updated = updated[:p] + snippet.replace('seat_no: null', 'seat_no: payload.seat_no', 1) + updated[q:]

# Revert only seat-related explanatory copy; preserve registration number and print-button gating.
updated = updated.replace(
    'रजिस्ट्रेशन फॉर्म भरें। Registration Number मिलने के बाद PDF प्राप्त करें; सीट भुगतान के बाद आवंटित होगी।',
    'रजिस्ट्रेशन फॉर्म भरें और उपलब्ध 50 सीटों में से अपनी पसंद की सीट चुनें।',
    1,
)
updated = updated.replace(
    'सीट का आवंटन भुगतान सफल होने के बाद ही होगा।',
    'आपकी चुनी हुई सीट का नंबर फॉर्म और ID Card पर दिखेगा।',
    1,
)
updated = updated.replace(
    '<span>सीट आवंटन</span><b>भुगतान सफल होने के बाद आवंटित होगी</b>',
    '<span>आवंटित सीट नंबर</span><b>{form.seat_no ? `सीट ${form.seat_no}` : \'________________\'}</b>',
    1,
)
updated = updated.replace(
    '<p><b>रजिस्ट्रेशन नं.:</b> {receipt ? receipt.registration_no : \'जमा करने के बाद जारी होगा\'}</p><p><b>सीट नंबर:</b> भुगतान के बाद आवंटित होगी</p>',
    '<p><b>रजिस्ट्रेशन नं.:</b> {receipt ? receipt.registration_no : \'जमा करने के बाद जारी होगा\'}</p><p><b>सीट नंबर:</b> {form.seat_no || \'आवंटन बाकी\'}</p>',
    1,
)

# Keep the form disabled while the live seat list is still loading, as before.
updated = updated.replace('disabled={submitting || Boolean(receipt)}', 'disabled={submitting || loadingSeats || Boolean(receipt)}', 1)

# Ensure the print/PDF button still appears only after successful registration.
if 'receipt && <button className="booking-print"' not in updated:
    sys.exit('ERROR: After-registration PDF button changed unexpectedly; no files changed.')
if 'registration_no:' not in updated:
    sys.exit('ERROR: Registration Number logic was not preserved; no files changed.')

stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
backup_dir = Path.home() / '.shri-shyam-library-backups' / f'restore-seat-system-{stamp}'
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(REG, backup_dir / 'Registration.jsx')
REG.write_text(updated, encoding='utf-8')
print('SUCCESS: Previous seat-selection UI and seat-required validation restored from Git commit', BASE)
print('Preserved: current Registration Number logic and PDF/ID-card button gated on successful registration.')
print('Backup:', backup_dir / 'Registration.jsx')
print('NEXT: npm run build')
