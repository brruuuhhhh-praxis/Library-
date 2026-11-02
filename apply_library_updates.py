from pathlib import Path

root = Path.cwd()
ca_path = root / 'src/CurrentAffairs.jsx'
css_path = root / 'src/CurrentAffairs.css'
admin_path = root / 'src/Admin.jsx'
for p in (ca_path, css_path, admin_path):
    if not p.exists():
        raise SystemExit(f'ERROR: {p} not found. Run this script from the repository root.')

ca = '''import React from 'react';
import { ArrowLeft, CalendarDays, Clock3, Newspaper } from 'lucide-react';
import './CurrentAffairs.css';
import LibraryBrand from './LibraryBrand.jsx';

export default function CurrentAffairs({ onHome }) {
  return (
    <main className="ca-page">
      <header className="ca-topbar">
        <a className="ca-brand" href="#/" onClick={onHome} aria-label="श्री श्याम लाइब्रेरी होम">
          <LibraryBrand variant="compact-light" tagline="A PLACE FOR FOCUSED MINDS" caption="DAILY CURRENT AFFAIRS" />
        </a>
        <a className="ca-back-link" href="#/" onClick={onHome}><ArrowLeft size={17} /> होम पेज</a>
      </header>
      <section className="ca-coming-soon">
        <div className="ca-coming-icon"><Newspaper size={32} /></div>
        <span className="ca-coming-kicker"><Clock3 size={14} /> COMING SOON</span>
        <h1>करंट अफेयर्स<br /><em>शीघ्र ही उपलब्ध होगा</em></h1>
        <p>श्री श्याम लाइब्रेरी पर UPSC, RPSC और RSSB की तैयारी के लिए राष्ट्रीय, राजस्थान और अंतरराष्ट्रीय समसामयिकी जल्द उपलब्ध कराई जाएगी।</p>
        <div className="ca-coming-note"><CalendarDays size={18} /><span>तथ्य-जाँची हुई खबरें और परीक्षा-उपयोगी क्विज़ तैयार किए जा रहे हैं।</span></div>
        <a className="ca-coming-home" href="#/" onClick={onHome}>होम पेज पर वापस जाएँ <ArrowLeft size={16} /></a>
      </section>
      <footer className="ca-footer"><a href="#/" onClick={onHome}><ArrowLeft size={15} /> श्री श्याम लाइब्रेरी पर वापस जाएँ</a><span>© {new Date().getFullYear()} श्री श्याम लाइब्रेरी</span></footer>
    </main>
  );
}
'''
ca_path.write_text(ca, encoding='utf-8')

css_add = '''\n/* Current Affairs temporary launch state */
.ca-coming-soon{max-width:850px;min-height:58vh;margin:0 auto;padding:70px 28px 84px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.ca-coming-icon{width:76px;height:76px;border-radius:24px;display:grid;place-items:center;background:linear-gradient(145deg,#203a33,#314e43);color:#e7bd73;box-shadow:0 16px 34px #203a3324;margin-bottom:23px}
.ca-coming-kicker{display:inline-flex;align-items:center;gap:7px;color:#9a7436;font-size:10px;font-weight:900;letter-spacing:.17em}
.ca-coming-soon h1{font-size:clamp(34px,6vw,58px);line-height:1.45;letter-spacing:-.04em;margin:16px 0;color:#203a33}
.ca-coming-soon h1 em{font-style:normal;color:#a77b36}
.ca-coming-soon>p{max-width:620px;color:#5c6862;font-size:15px;line-height:2;margin:0}
.ca-coming-note{display:flex;align-items:center;justify-content:center;gap:10px;max-width:620px;margin-top:24px;padding:14px 18px;border:1px solid #e4d7bd;border-radius:13px;background:#fffdf8;color:#52615a;font-size:12px;line-height:1.8}
.ca-coming-note svg{flex-shrink:0;color:#a77b36}
.ca-coming-home{display:inline-flex;align-items:center;gap:9px;margin-top:28px;padding:13px 18px;border-radius:11px;background:#203a33;color:#fff;text-decoration:none;font-size:12px;font-weight:800}
.ca-coming-home svg{transform:rotate(180deg)}
@media(max-width:700px){.ca-coming-soon{min-height:62vh;padding:48px 20px 60px}.ca-coming-soon>p{font-size:13px}.ca-coming-note{align-items:flex-start;text-align:left}}
'''
css = css_path.read_text(encoding='utf-8')
if '.ca-coming-soon{' not in css:
    css_path.write_text(css + css_add, encoding='utf-8')

admin = admin_path.read_text(encoding='utf-8')
needle = '''      await loadData();
    } catch {
      setError('नेटवर्क समस्या के कारण कार्रवाई नहीं हो सकी। कृपया फिर प्रयास करें।');'''
replacement = '''      let whatsappWarning = '';
      if (action === 'confirm') {
        const registrationNo = `SS-${String(record.created_at || new Date().toISOString()).slice(0, 4)}-${String(record.id).replaceAll('-', '').slice(0, 8).toUpperCase()}`;
        const { error: whatsappError } = await supabase.functions.invoke('send-seat-confirmation', {
          body: { registration_id: record.id, registration_no: registrationNo },
        });
        if (whatsappError) {
          console.error('Seat confirmation WhatsApp notification failed:', whatsappError);
          whatsappWarning = 'सदस्यता Confirm हो गई, लेकिन WhatsApp संदेश नहीं भेजा जा सका। WhatsApp Cloud API secrets और approved template जाँचें।';
        }
      }
      await loadData();
      if (whatsappWarning) setError(whatsappWarning);
    } catch {
      setError('नेटवर्क समस्या के कारण कार्रवाई नहीं हो सकी। कृपया फिर प्रयास करें।');'''
if 'send-seat-confirmation' not in admin:
    if needle not in admin:
        raise SystemExit('ERROR: Admin insertion point not found; no Admin.jsx change applied.')
    admin_path.write_text(admin.replace(needle, replacement, 1), encoding='utf-8')

print('SUCCESS: Current Affairs coming-soon page and admin WhatsApp invocation patched.')
print('NEXT: Deploy the Supabase Edge Function and configure WhatsApp Cloud API secrets/template before live WhatsApp messages can send.')
