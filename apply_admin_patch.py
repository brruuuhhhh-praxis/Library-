#!/usr/bin/env python3
"""Apply Confirm/Reject/Cancel UI patch to src/Admin.jsx.
Run from the repository root: python apply_admin_patch.py
Creates src/Admin.jsx.before-security-patch as a backup first.
"""
from pathlib import Path
import sys

path = Path("src/Admin.jsx")
if not path.exists():
    sys.exit("ERROR: src/Admin.jsx not found. Run this script from the Library repository root.")

s = path.read_text(encoding="utf-8")
if "admin_confirm_library_registration" in s:
    sys.exit("Patch appears already applied; no changes made.")

old = """  async function changeSeat(seat) {
    if (!supabase) return;
    setError('');
    const nextStatus = seat.status === 'booked' ? 'available' : 'booked';
    if (nextStatus === 'available') {
      const ok = window.confirm(`सीट ${seat.seat_no} खाली करने पर इसका pending/active रजिस्ट्रेशन cancelled हो जाएगा। जारी रखें?`);
      if (!ok) return;
    }
    setLoading(true);
    try {
      const { error: updateError } = await supabase.rpc('admin_set_library_seat_status', {
        p_seat_no: seat.seat_no,
        p_status: nextStatus,
      });
      if (updateError) {
        setError('सीट अपडेट नहीं हुई। Supabase में नवीनतम atomic-seat migration चलाएँ और एडमिन अनुमति जाँचें।');
        return;
      }
      await loadData();
    } catch {
      setError('नेटवर्क समस्या के कारण सीट अपडेट नहीं हो सकी। कृपया फिर प्रयास करें।');
    } finally {
      setLoading(false);
    }
  }


"""
new = old + """  async function registrationAction(record, action) {
    if (!supabase || !record?.id) return;
    const labels = {
      confirm: 'इस आवेदन को Confirm करके सदस्य सक्रिय करना है?',
      reject: 'इस pending आवेदन को Reject करना है? सीट खाली हो जाएगी।',
      cancel: 'इस सक्रिय सदस्यता को Cancel करना है?'
    };
    if (!window.confirm(labels[action])) return;

    const rpcNames = {
      confirm: 'admin_confirm_library_registration',
      reject: 'admin_reject_library_registration',
      cancel: 'admin_cancel_library_membership'
    };
    setLoading(true);
    setError('');
    try {
      const { error: actionError } = await supabase.rpc(rpcNames[action], {
        p_registration_id: record.id
      });
      if (actionError) {
        console.error('Admin registration action failed:', actionError);
        setError(actionError.message || 'कार्रवाई नहीं हो सकी। एडमिन अनुमति और migration जाँचें।');
        return;
      }
      await loadData();
    } catch {
      setError('नेटवर्क समस्या के कारण कार्रवाई नहीं हो सकी। कृपया फिर प्रयास करें।');
    } finally {
      setLoading(false);
    }
  }


"""
if old not in s:
    sys.exit("ERROR: Could not find expected changeSeat() block. No file changed.")

# Keep a backup before modifying the source file.
backup = path.with_name(path.name + ".before-security-patch")
if not backup.exists():
    backup.write_text(s, encoding="utf-8")

s = s.replace(old, new, 1)

old_buttons = """</div></details><button className="booking-print admin-record-print" type="button" onClick={()=>{setPrintRecord(r);setTimeout(()=>window.print(),150);}}>आवेदन प्रिंट करें</button></article>)}</div>}"""
new_buttons = """</div></details><div className="admin-record-actions">{r.status === 'pending' && <><button className="booking-submit admin-action-confirm" type="button" disabled={loading} onClick={() => registrationAction(r, 'confirm')}>✓ Confirm</button><button className="booking-print admin-action-reject" type="button" disabled={loading} onClick={() => registrationAction(r, 'reject')}>✕ Reject</button></>}{r.status === 'active' && <button className="booking-print admin-action-reject" type="button" disabled={loading} onClick={() => registrationAction(r, 'cancel')}>Membership Cancel करें</button>}<button className="booking-print admin-record-print" type="button" onClick={()=>{setPrintRecord(r);setTimeout(()=>window.print(),150);}}>आवेदन प्रिंट करें</button></div></article>)}</div>}"""
if old_buttons not in s:
    sys.exit("ERROR: Could not find expected registration record button block. Backup created; source was not changed.")

s = s.replace(old_buttons, new_buttons, 1)
path.write_text(s, encoding="utf-8")
print("Patch applied to src/Admin.jsx")
print(f"Backup saved at: {backup}")
print("Next: run npm run build")
