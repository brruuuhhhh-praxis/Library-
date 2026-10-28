import React, { useEffect, useMemo, useState } from 'react';
import {
  ArrowLeft, ArrowUpRight, CalendarDays, CheckCircle2, ChevronRight,
  ExternalLink, FileQuestion, Filter, LoaderCircle, Newspaper, Search, ShieldCheck
} from 'lucide-react';
import { isSupabaseConfigured, supabase } from './lib/supabase.js';
import './CurrentAffairs.css';

const CATEGORIES = [
  { id: 'national', label: 'राष्ट्रीय समसामयिकी', short: 'राष्ट्रीय', emoji: '🇮🇳' },
  { id: 'international', label: 'अंतरराष्ट्रीय समसामयिकी', short: 'अंतरराष्ट्रीय', emoji: '🌐' },
  { id: 'rajasthan', label: 'राजस्थान समसामयिकी', short: 'राजस्थान', emoji: '🏜️' },
];

function istDateString(date = new Date()) {
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Kolkata', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(date);
  const value = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}`;
}

function shiftDate(dateString, amount) {
  const [year, month, day] = dateString.split('-').map(Number);
  const value = new Date(Date.UTC(year, month - 1, day + amount));
  return `${value.getUTCFullYear()}-${String(value.getUTCMonth() + 1).padStart(2, '0')}-${String(value.getUTCDate()).padStart(2, '0')}`;
}

function prettyDate(dateString) {
  if (!dateString) return '—';
  const [year, month, day] = dateString.split('-').map(Number);
  return new Intl.DateTimeFormat('hi-IN', {
    day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Asia/Kolkata',
  }).format(new Date(Date.UTC(year, month - 1, day, 6)));
}

function sourceHost(url) {
  try { return new URL(url).hostname.replace(/^www\./, ''); }
  catch { return 'मूल स्रोत'; }
}

export default function CurrentAffairs({ onHome }) {
  const today = useMemo(() => istDateString(), []);
  const [editionDate, setEditionDate] = useState(today);
  const [activeCategory, setActiveCategory] = useState('national');
  const [searchTerm, setSearchTerm] = useState('');
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState('');
  const [quizIndex, setQuizIndex] = useState(0);
  const [chosenOption, setChosenOption] = useState(null);
  const [answerChecked, setAnswerChecked] = useState(false);
  const [quizScore, setQuizScore] = useState(0);

  useEffect(() => {
    let isCurrent = true;
    async function loadEdition() {
      setLoading(true);
      setLoadError('');
      setStories([]);
      if (!isSupabaseConfigured || !supabase) {
        setLoading(false);
        return;
      }
      const { data, error } = await supabase
        .from('current_affairs')
        .select('id, edition_date, event_date, category, headline, one_liner, source_name, source_url, quiz_questions, priority, published_at')
        .eq('edition_date', editionDate)
        .eq('status', 'published')
        .order('priority', { ascending: true })
        .order('created_at', { ascending: false });
      if (!isCurrent) return;
      if (error) setLoadError(error.message || 'समसामयिकी लोड नहीं हो पाई।');
      else setStories(Array.isArray(data) ? data : []);
      setLoading(false);
    }
    loadEdition();
    return () => { isCurrent = false; };
  }, [editionDate]);

  const visibleStories = useMemo(() => {
    const query = searchTerm.trim().toLocaleLowerCase('hi-IN');
    return stories.filter((story) => story.category === activeCategory && (!query ||
      `${story.headline || ''} ${story.one_liner || ''} ${story.source_name || ''}`.toLocaleLowerCase('hi-IN').includes(query)));
  }, [stories, activeCategory, searchTerm]);

  const quizQuestions = useMemo(() => stories.flatMap((story) => {
    if (!Array.isArray(story.quiz_questions)) return [];
    return story.quiz_questions
      .filter((question) => question && typeof question.question === 'string' && Array.isArray(question.options) && Number.isInteger(question.answer_index))
      .map((question, index) => ({ ...question, storyHeadline: story.headline, sourceUrl: story.source_url, id: `${story.id}-${index}` }));
  }), [stories]);
  const currentQuestion = quizQuestions[quizIndex];

  function chooseCategory(category) {
    setActiveCategory(category);
    setSearchTerm('');
  }

  function changeEdition(value) {
    setEditionDate(value);
    setQuizIndex(0);
    setChosenOption(null);
    setAnswerChecked(false);
    setQuizScore(0);
  }

  function checkAnswer() {
    if (chosenOption === null || !currentQuestion || answerChecked) return;
    if (chosenOption === currentQuestion.answer_index) setQuizScore((score) => score + 1);
    setAnswerChecked(true);
  }

  function nextQuestion() {
    setQuizIndex((index) => (index + 1) % quizQuestions.length);
    setChosenOption(null);
    setAnswerChecked(false);
  }

  const sourceDate = shiftDate(editionDate, -1);

  return (
    <main className="ca-page">
      <header className="ca-topbar">
        <a className="ca-brand" href="#/" onClick={onHome} aria-label="श्री श्याम लाइब्रेरी होम">
          <span className="ca-brand-mark"><Newspaper size={22} /></span>
          <span><b>श्री श्याम लाइब्रेरी</b><small>DAILY CURRENT AFFAIRS</small></span>
        </a>
        <a className="ca-back-link" href="#/" onClick={onHome}><ArrowLeft size={17} /> होम पेज</a>
      </header>

      <section className="ca-hero">
        <div className="ca-hero-copy">
          <span className="ca-kicker"><span /> EXAM-READY ONE LINERS</span>
          <h1>आज की खबरें,<br /><em>सीधी और सटीक।</em></h1>
          <p>RPSC, RSSB और राजस्थान की अन्य प्रतियोगी परीक्षाओं के लिए राष्ट्रीय, अंतरराष्ट्रीय और राजस्थान समसामयिकी—संक्षिप्त हिंदी वन-लाइनर में।</p>
          <div className="ca-trust-row"><span><CheckCircle2 size={15} /> स्रोत लिंक सहित</span><span><ShieldCheck size={15} /> तथ्य-जाँच के लिए मूल स्रोत</span></div>
        </div>
        <div className="ca-hero-stamp"><CalendarDays size={25} /><span>EDITION DATE</span><b>{prettyDate(editionDate)}</b><small>समाचार अवधि: {prettyDate(sourceDate)}</small></div>
      </section>

      <section className="ca-content-wrap">
        <div className="ca-edition-bar">
          <div><CalendarDays size={18} /><label htmlFor="ca-edition-date">समसामयिकी एडिशन चुनें</label></div>
          <input id="ca-edition-date" aria-label="एडिशन की तारीख" type="date" value={editionDate} max={today} onChange={(event) => changeEdition(event.target.value)} />
        </div>
        <div className="ca-date-note">नियम: एडिशन की तारीख से पिछले दिन (रात 12:00 से 11:59 तक, भारतीय समय) की खबरें इसमें शामिल होंगी।</div>

        <div className="ca-category-tabs" role="tablist" aria-label="समसामयिकी श्रेणियाँ">
          {CATEGORIES.map((category) => (
            <button key={category.id} type="button" role="tab" aria-selected={activeCategory === category.id}
              className={activeCategory === category.id ? 'is-active' : ''} onClick={() => chooseCategory(category.id)}>
              <span>{category.emoji}</span>{category.label}
            </button>
          ))}
        </div>

        <div className="ca-list-heading">
          <div><span className="ca-section-tag"><Filter size={13} /> {CATEGORIES.find((item) => item.id === activeCategory)?.short}</span><h2>वन-लाइनर अपडेट्स</h2></div>
          <label className="ca-search"><Search size={17} /><input value={searchTerm} onChange={(event) => setSearchTerm(event.target.value)} placeholder="खबर खोजें…" aria-label="खबर खोजें" /></label>
        </div>

        {loading && <div className="ca-status"><LoaderCircle className="ca-spin" size={24} /><p>समसामयिकी लोड हो रही है…</p></div>}
        {!loading && loadError && <div className="ca-status ca-status-error"><p>डेटा लोड नहीं हुआ: {loadError}</p><small>Supabase connection और current_affairs table की policy जाँचें।</small></div>}
        {!loading && !loadError && !isSupabaseConfigured && (
          <div className="ca-status ca-empty-setup"><span className="ca-empty-icon"><Newspaper size={26} /></span><h3>समसामयिकी फ़ीड कनेक्ट करना बाकी है</h3><p>वेबसाइट का Current Affairs पेज तैयार है। लाइव एडिशन दिखाने के लिए Supabase में migration चलाएँ, फिर GitHub repository के Actions secrets में <code>VITE_SUPABASE_URL</code> और <code>VITE_SUPABASE_ANON_KEY</code> जोड़ें।</p><small>यहाँ कोई बनावटी या अपुष्ट खबर नहीं दिखाई जाएगी।</small></div>
        )}
        {!loading && !loadError && isSupabaseConfigured && visibleStories.length === 0 && (
          <div className="ca-status ca-empty"><span className="ca-empty-icon"><Newspaper size={25} /></span><h3>इस श्रेणी में अभी प्रकाशित खबरें नहीं हैं</h3><p>{prettyDate(editionDate)} के एडिशन में {CATEGORIES.find((item) => item.id === activeCategory)?.label} की खबरें प्रकाशित होने पर यहाँ दिखेंगी।</p><small>एडिशन की तारीख: {prettyDate(editionDate)} · कवर की गई खबरें: {prettyDate(sourceDate)}</small></div>
        )}
        {!loading && !loadError && visibleStories.length > 0 && (
          <div className="ca-story-list">
            {visibleStories.map((story, index) => (
              <article className="ca-story-card" key={story.id}>
                <div className="ca-story-number">{String(index + 1).padStart(2, '0')}</div>
                <div className="ca-story-main">
                  <div className="ca-story-meta"><span>{CATEGORIES.find((item) => item.id === story.category)?.short || story.category}</span><time dateTime={story.event_date}>घटना की तारीख: {prettyDate(story.event_date)}</time></div>
                  <h3>{story.headline}</h3>
                  <p>{story.one_liner}</p>
                  <a className="ca-source-link" href={story.source_url} target="_blank" rel="noopener noreferrer">
                    <ExternalLink size={14} /> स्रोत: {story.source_name || sourceHost(story.source_url)} <ArrowUpRight size={14} />
                  </a>
                </div>
              </article>
            ))}
          </div>
        )}

        <section className="ca-quiz-panel">
          <div className="ca-quiz-intro"><span className="ca-quiz-icon"><FileQuestion size={21} /></span><div><span className="ca-section-tag">REVISION MODE</span><h2>आज का क्विज़</h2><p>प्रकाशित खबरों के साथ सेव किए गए प्रश्नों से अभ्यास करें।</p></div></div>
          {quizQuestions.length === 0 ? (
            <div className="ca-quiz-empty">इस एडिशन में अभी quiz प्रश्न उपलब्ध नहीं हैं। प्रश्न खबरों के साथ सेव होने पर यहीं अभ्यास कर सकेंगे।</div>
          ) : (
            <div className="ca-quiz-body">
              <div className="ca-quiz-progress">प्रश्न {quizIndex + 1} / {quizQuestions.length}<span>स्कोर: {quizScore}</span></div>
              <h3>{currentQuestion.question}</h3>
              <div className="ca-options">
                {currentQuestion.options.map((option, index) => {
                  let optionClass = chosenOption === index ? 'is-selected' : '';
                  if (answerChecked && index === currentQuestion.answer_index) optionClass += ' is-correct';
                  else if (answerChecked && chosenOption === index) optionClass += ' is-wrong';
                  return <button type="button" key={`${currentQuestion.id}-${index}`} className={optionClass}
                    disabled={answerChecked} onClick={() => setChosenOption(index)}><span>{String.fromCharCode(65 + index)}</span>{option}</button>;
                })}
              </div>
              {answerChecked && <div className="ca-explanation"><b>{chosenOption === currentQuestion.answer_index ? 'सही जवाब!' : 'सही उत्तर देखें'}</b><p>{currentQuestion.explanation || `सही उत्तर: ${currentQuestion.options[currentQuestion.answer_index]}`}</p>{currentQuestion.sourceUrl && <a href={currentQuestion.sourceUrl} target="_blank" rel="noopener noreferrer">स्रोत खोलें <ExternalLink size={13} /></a>}</div>}
              <div className="ca-quiz-actions">{!answerChecked ? <button type="button" className="ca-primary-button" disabled={chosenOption === null} onClick={checkAnswer}>उत्तर जाँचें <ChevronRight size={17} /></button> : <button type="button" className="ca-primary-button" onClick={nextQuestion}>अगला प्रश्न <ChevronRight size={17} /></button>}</div>
            </div>
          )}
          <div className="ca-quiz-footnote">क्विज़ stored questions पर चलता है—यह ब्राउज़र में कोई AI/API call नहीं करता।</div>
        </section>
      </section>

      <footer className="ca-footer"><a href="#/" onClick={onHome}><ArrowLeft size={15} /> श्री श्याम लाइब्रेरी पर वापस जाएँ</a><span>© {new Date().getFullYear()} श्री श्याम लाइब्रेरी · ज्ञान रोज़, तैयारी रोज़</span></footer>
    </main>
  );
}
