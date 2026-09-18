import React, { useState, useEffect } from 'react';

// --- CUSTOM SVG ICONS ---
const ChartIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>;
const CheckIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>;
const DocumentIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2"></path></svg>;
const ChatIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>;
const MailIcon = () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>;
const UploadIcon = () => <svg className="w-10 h-10 mb-3 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>;

export default function App() {
  const [activeTab, setActiveTab] = useState('analyzer');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('careerpath_user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('careerpath_user');
    setUser(null);
  };

  if (!user) {
    return <AuthScreen onLogin={setUser} />;
  }

  return (
    <div className="flex h-screen bg-slate-100 font-sans text-slate-800 overflow-hidden">
      <aside className="w-72 bg-[#0f172a] text-slate-300 flex flex-col shadow-2xl z-20">
        <div className="p-8 border-b border-slate-800">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
              <span className="text-white font-bold text-xl">C</span>
            </div>
            <h1 className="text-2xl font-black text-white tracking-tight">CareerPath</h1>
          </div>
          <p className="text-xs text-indigo-400 font-semibold uppercase tracking-wider mt-2">AI Phase-I System</p>
        </div>

        <nav className="flex-1 p-6 space-y-4">
          <button onClick={() => setActiveTab('analyzer')} className={`w-full flex items-center gap-4 p-4 rounded-2xl text-sm font-bold transition-all duration-300 ${activeTab === 'analyzer' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/40 translate-x-2' : 'hover:bg-slate-800 hover:text-white'}`}>
            <ChartIcon /> Smart Analyzer
          </button>
          <button onClick={() => setActiveTab('interview')} className={`w-full flex items-center gap-4 p-4 rounded-2xl text-sm font-bold transition-all duration-300 ${activeTab === 'interview' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/40 translate-x-2' : 'hover:bg-slate-800 hover:text-white'}`}>
            <ChatIcon /> Mock Interview
          </button>
          <button onClick={() => setActiveTab('editor')} className={`w-full flex items-center gap-4 p-4 rounded-2xl text-sm font-bold transition-all duration-300 ${activeTab === 'editor' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/40 translate-x-2' : 'hover:bg-slate-800 hover:text-white'}`}>
            <CheckIcon /> ATS Resume Fixer
          </button>
          <button onClick={() => setActiveTab('templates')} className={`w-full flex items-center gap-4 p-4 rounded-2xl text-sm font-bold transition-all duration-300 ${activeTab === 'templates' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/40 translate-x-2' : 'hover:bg-slate-800 hover:text-white'}`}>
            <DocumentIcon /> Domain Templates
          </button>
          <button onClick={() => setActiveTab('coverletter')} className={`w-full flex items-center gap-4 p-4 rounded-2xl text-sm font-bold transition-all duration-300 ${activeTab === 'coverletter' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/40 translate-x-2' : 'hover:bg-slate-800 hover:text-white'}`}>
            <MailIcon /> AI Cover Letter
          </button>
        </nav>

        <div className="p-6 border-t border-slate-800 bg-slate-900/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center text-white font-bold border-2 border-indigo-500">
                {user.name.charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="text-sm font-bold text-white truncate w-24">{user.name}</p>
                <p className="text-xs text-slate-400">Authenticated</p>
              </div>
            </div>
            <button onClick={handleLogout} className="text-xs text-red-400 font-bold hover:text-red-300 transition-colors bg-red-400/10 px-3 py-2 rounded-lg">
              Logout
            </button>
          </div>
        </div>
      </aside>

      <main className="flex-1 overflow-y-auto bg-slate-50 relative">
        <header className="sticky top-0 bg-slate-50/80 backdrop-blur-md z-10 p-8 border-b border-slate-200">
          <h2 className="text-3xl font-extrabold text-slate-800">
            {activeTab === 'analyzer' && "AI Skill Gap Analyzer"}
            {activeTab === 'interview' && "Smart Interview Simulator"}
            {activeTab === 'editor' && "ATS Resume Optimizer"}
            {activeTab === 'templates' && "Industry Templates"}
            {activeTab === 'coverletter' && "GenAI Cover Letter Builder"}
          </h2>
          <p className="text-slate-500 font-medium mt-1">Welcome back, {user.name}. Let's optimize your profile.</p>
        </header>

        <div key={activeTab} className="p-8 pb-20 animate-slide-up max-w-6xl mx-auto">
          {activeTab === 'analyzer' && <AnalyzerTab />}
          {activeTab === 'interview' && <InterviewTab />}
          {activeTab === 'editor' && <ResumeEditorTab />}
          {activeTab === 'templates' && <TemplatesTab />}
          {activeTab === 'coverletter' && <CoverLetterTab />}
        </div>
      </main>
    </div>
  );
}

// ==========================================
// AUTHENTICATION SCREEN COMPONENT
// ==========================================
function AuthScreen({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const clearFields = () => {
    setErrorMsg('');
    setPassword('');
    setConfirmPassword('');
    setEmail('');
    setName('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    if (!isLogin && password !== confirmPassword) {
      setErrorMsg("Passwords do not match. Please try again.");
      return;
    }

    setLoading(true);

    const url = isLogin ? 'https://careerpath-ai-imzn.onrender.com/login' : 'https://careerpath-ai-imzn.onrender.com/register';
    const payload = isLogin ? { email, password } : { name, email, password };

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (res.ok) {
        localStorage.setItem('careerpath_user', JSON.stringify(data.user));
        onLogin(data.user);
      } else {
        setErrorMsg(data.error || "Authentication failed. Please check your details.");
      }
    } catch (err) {
      setErrorMsg("Failed to connect to the backend server.");
    }
    setLoading(false);
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    clearFields();
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-indigo-500/20 rounded-full blur-[100px]"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-blue-500/20 rounded-full blur-[100px]"></div>

      <div className="bg-white p-12 rounded-[3rem] shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-slate-100 max-w-md w-full relative z-10 animate-slide-up">
        <div className="text-center mb-10">
          <div className="w-16 h-16 mx-auto bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/30 mb-6">
            <span className="text-white font-black text-3xl">C</span>
          </div>
          <h2 className="text-3xl font-black text-slate-800 tracking-tight">CareerPath AI</h2>
          <p className="text-slate-500 font-medium mt-2">{isLogin ? 'Sign in to continue to your dashboard.' : 'Create an account to start optimizing.'}</p>
        </div>

        {errorMsg && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-600 p-4 rounded-2xl flex items-start justify-between shadow-sm animate-slide-up">
            <div className="flex gap-3">
              <span className="text-xl">⚠️</span>
              <span className="font-bold text-sm mt-0.5">{errorMsg}</span>
            </div>
            <button
              type="button"
              onClick={clearFields}
              className="text-red-400 hover:text-red-700 bg-red-100 hover:bg-red-200 rounded-full w-6 h-6 flex items-center justify-center transition-colors shrink-0"
            >
              ✕
            </button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {!isLogin && (
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">Full Name</label>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)} required className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 font-medium focus:border-indigo-500 outline-none transition-all" placeholder="John Doe" />
            </div>
          )}

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">Email Address</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 font-medium focus:border-indigo-500 outline-none transition-all" placeholder="name@example.com" />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 font-medium focus:border-indigo-500 outline-none transition-all" placeholder="••••••••" />
          </div>

          {!isLogin && (
            <div className="space-y-2 animate-slide-up">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">Confirm Password</label>
              <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 font-medium focus:border-indigo-500 outline-none transition-all" placeholder="••••••••" />
            </div>
          )}

          <button type="submit" disabled={loading} className="w-full py-5 bg-slate-800 text-white rounded-2xl text-lg font-black hover:bg-slate-900 hover:-translate-y-1 hover:shadow-xl transition-all duration-300 mt-4 disabled:opacity-50">
            {loading ? 'Authenticating...' : (isLogin ? 'Secure Sign In' : 'Create Account')}
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-slate-500 font-medium">
            {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
            <button type="button" onClick={toggleMode} className="text-indigo-600 font-bold hover:underline">
              {isLogin ? 'Sign up' : 'Log in'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

// ==========================================
// 1. SMART ANALYZER
// ==========================================
function AnalyzerTab() {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState('AI/ML Engineer');
  const [jdUrl, setJdUrl] = useState('');
  const [github, setGithub] = useState('');
  const [timeline, setTimeline] = useState('4');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please upload a PDF resume.");
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('role', role);
    formData.append('jd_url', jdUrl);
    formData.append('github_user', github);
    formData.append('timeline', timeline);

    try {
      const res = await fetch('https://careerpath-ai-imzn.onrender.com/analyze', { method: 'POST', body: formData });
      const data = await res.json();
      if (res.ok) setResults(data);
      else alert("Error: " + data.error);
    } catch (err) { alert("Failed to connect to backend."); }
    setLoading(false);
  };

  return (
    <div className="space-y-10">
      <div className="bg-white p-10 rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
        <form onSubmit={handleAnalyze} className="space-y-8">
          <div className="grid grid-cols-2 gap-8">
            <div className="space-y-2">
              <label className="text-sm font-bold text-slate-700 uppercase tracking-wider">Target Role</label>
              <select value={role} onChange={(e) => setRole(e.target.value)} className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 text-slate-700 font-semibold focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all outline-none shadow-inner cursor-pointer">
                <option value="AI/ML Engineer">AI/ML Engineer</option>
                <option value="Full-Stack Developer">Full-Stack Developer</option>
                <option value="Data Scientist">Data Scientist</option>
                <option value="Custom Job (Web Scraper)">Custom Job (Web Scraper)</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-bold text-slate-700 uppercase tracking-wider">Timeline</label>
              <select value={timeline} onChange={(e) => setTimeline(e.target.value)} className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 text-slate-700 font-semibold focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all outline-none shadow-inner cursor-pointer">
                <option value="2">2 Weeks (Crash Course)</option>
                <option value="4">4 Weeks (Intensive)</option>
                <option value="8">8 Weeks (Comprehensive)</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-8">
            {role === 'Custom Job (Web Scraper)' ? (
              <div className="space-y-2">
                <label className="text-sm font-bold text-slate-700 uppercase tracking-wider">Job Post URL</label>
                <input type="text" value={jdUrl} onChange={(e) => setJdUrl(e.target.value)} placeholder="https://..." className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 font-medium focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all outline-none shadow-inner" />
              </div>
            ) : (
              <div className="space-y-2">
                <label className="text-sm font-bold text-slate-700 uppercase tracking-wider flex justify-between">
                  <span>GitHub Username / Link</span> <span className="text-indigo-400 text-xs">Optional API</span>
                </label>
                <input type="text" value={github} onChange={(e) => setGithub(e.target.value)} placeholder="e.g., torvalds or full URL" className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 font-medium focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all outline-none shadow-inner" />
              </div>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-bold text-slate-700 uppercase tracking-wider">Document Upload</label>
            <div className="upload-glow relative border-2 border-dashed border-slate-300 rounded-[2rem] p-12 text-center bg-slate-50 transition-all cursor-pointer group">
              <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
              <div className="flex flex-col items-center justify-center">
                <UploadIcon />
                <p className="text-xl font-black text-slate-700 group-hover:text-indigo-600 transition-colors">Drag & Drop Resume</p>
                <p className="text-sm font-medium text-slate-400 mt-2">Maximum file size: 16MB (.PDF only)</p>
                {file && <div className="mt-6 px-6 py-3 bg-indigo-100 border border-indigo-200 text-indigo-700 rounded-xl font-bold flex items-center gap-2 shadow-sm"><CheckIcon /> {file.name}</div>}
              </div>
            </div>
          </div>

          <button type="submit" disabled={loading} className="w-full py-5 bg-gradient-to-r from-indigo-600 to-blue-500 text-white rounded-2xl text-xl font-black hover:from-indigo-500 hover:to-blue-400 hover:-translate-y-1 hover:shadow-2xl hover:shadow-indigo-500/40 transition-all duration-300 disabled:opacity-50 disabled:hover:translate-y-0">
            {loading ? 'Processing Data Pipeline...' : 'Run Advanced AI Analysis'}
          </button>
        </form>
      </div>

      {results && (
        <div className="space-y-10 animate-slide-up">
          {results.github_skills && results.github_skills.length > 0 && (
            <div className="bg-slate-800 p-6 rounded-2xl shadow-lg border border-slate-700 flex items-center gap-6 text-white transform hover:scale-[1.01] transition-transform">
              <div className="w-14 h-14 bg-slate-700 rounded-full flex items-center justify-center shadow-inner text-2xl">🐙</div>
              <div>
                <h4 className="text-sm font-bold text-indigo-400 uppercase tracking-widest mb-1">GitHub API Synced</h4>
                <p className="font-medium text-slate-300 leading-relaxed">
                  Automatically extracted <span className="font-bold text-white bg-slate-700 px-2 py-1 rounded mx-1">{results.github_skills.map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(", ")}</span> from your public repositories to boost your match score.
                </p>
              </div>
            </div>
          )}

          <div className="grid grid-cols-2 gap-8">
            <div className="bg-white p-10 rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex flex-col justify-center">
              <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Cosine Similarity Match</h3>
              <div className="flex items-center gap-6">
                <div className="text-7xl font-black text-slate-800 tracking-tighter">{results.match_score_percentage}<span className="text-4xl text-slate-400">%</span></div>
                <div className="flex-1 bg-slate-100 rounded-full h-4 overflow-hidden shadow-inner">
                  <div className={`h-full rounded-full transition-all duration-1000 ${results.match_score_percentage > 70 ? 'bg-emerald-500' : results.match_score_percentage > 40 ? 'bg-amber-500' : 'bg-red-500'}`} style={{ width: `${results.match_score_percentage}%` }}></div>
                </div>
              </div>
            </div>
            <div className="bg-white p-10 rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
              <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Required Skill Gaps</h3>
              <div className="flex flex-wrap gap-3">
                {results.skill_gaps.map(gap => (
                  <span key={gap} className="px-5 py-2.5 bg-red-50/50 text-red-600 border border-red-100 rounded-xl text-base font-bold shadow-sm">{gap}</span>
                ))}
                {results.skill_gaps.length === 0 && <span className="px-5 py-2.5 bg-emerald-50 text-emerald-600 border border-emerald-200 rounded-xl text-base font-bold">100% Match Identified!</span>}
              </div>
            </div>
          </div>

          <div className="bg-white p-10 rounded-[3rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
            <h3 className="text-2xl font-black text-slate-800 mb-10 border-b border-slate-100 pb-6 flex items-center gap-3">Strategic Roadmap</h3>
            <div className="space-y-0 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-1 before:bg-gradient-to-b before:from-indigo-500 before:to-blue-200">
              {results.study_plan.map((week, idx) => (
                <div key={idx} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active mb-12">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-indigo-500 shadow-xl shadow-indigo-500/30 text-white absolute left-5 md:left-1/2 -translate-x-1/2 font-bold z-10">{idx + 1}</div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-3rem)] p-8 rounded-3xl bg-slate-50 border border-slate-100 shadow-sm hover:shadow-xl hover:shadow-indigo-500/5 transition-all duration-300">
                    <div className="text-indigo-600 font-black text-xl mb-1">{week.week}</div>
                    <div className="text-slate-800 font-bold text-lg mb-4">{week.focus}</div>
                    <ul className="space-y-3">
                      {week.tasks.map((task, i) => (
                        <li key={i} className="flex items-start gap-3 text-slate-600 font-medium"><span className="text-indigo-400 mt-1">✦</span><span className="leading-relaxed">{task}</span></li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==========================================
// 2. MOCK INTERVIEW
// ==========================================
function InterviewTab() {
  const [skillInput, setSkillInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);

  const generateInterview = async () => {
    if (!skillInput.trim()) return alert("Enter at least one skill.");
    setLoading(true);
    const skillsArray = skillInput.includes(',')
      ? skillInput.split(',').map(s => s.trim()).filter(s => s)
      : skillInput.split(' ').map(s => s.trim()).filter(s => s);

    try {
      const res = await fetch('https://careerpath-ai-imzn.onrender.com/generate_interview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skills: skillsArray })
      });
      const data = await res.json();
      setQuestions(data.questions);
      setCurrentIndex(0);
      setShowAnswer(false);
    } catch (err) { alert("Failed to connect to backend."); }
    setLoading(false);
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setShowAnswer(false);
    } else {
      alert("🎉 Interview Complete! You survived.");
      setQuestions(null);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-10">
      {!questions ? (
        <div className="bg-white p-12 rounded-[3rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 text-center animate-slide-up">
          <div className="w-20 h-20 bg-indigo-50 rounded-3xl flex items-center justify-center mx-auto mb-6 text-indigo-500 shadow-inner"><ChatIcon /></div>
          <h2 className="text-3xl font-black text-slate-800 mb-4">Interactive Interview Simulator</h2>
          <p className="text-lg font-medium text-slate-500 mb-10 max-w-2xl mx-auto">Enter your skills below. We will simulate a live technical interview, one question at a time.</p>
          <div className="flex flex-col items-center gap-6 max-w-xl mx-auto">
            <div className="w-full text-left">
              <label className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-2 block">Skills to Practice</label>
              <input type="text" value={skillInput} onChange={(e) => setSkillInput(e.target.value)} placeholder="e.g. Python, Docker, SQL" className="w-full border-2 border-slate-200 p-5 rounded-2xl bg-slate-50 text-lg font-medium focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all outline-none" />
            </div>
            <button onClick={generateInterview} disabled={loading} className="w-full py-5 bg-indigo-600 text-white rounded-2xl text-xl font-black hover:bg-indigo-700 hover:-translate-y-1 hover:shadow-2xl hover:shadow-indigo-500/30 transition-all duration-300 disabled:opacity-50">
              {loading ? 'Booting Simulator...' : 'Start Live Interview'}
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-white p-12 rounded-[3rem] shadow-2xl border border-indigo-100 animate-slide-up relative overflow-hidden">
          <div className="absolute top-0 left-0 h-2 bg-indigo-500 transition-all duration-500" style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}></div>
          <div className="flex justify-between items-center mb-8">
            <span className="px-4 py-2 bg-indigo-50 text-indigo-700 rounded-xl font-bold uppercase tracking-wider text-sm">Topic: {questions[currentIndex].skill}</span>
            <span className="text-slate-400 font-bold">Question {currentIndex + 1} of {questions.length}</span>
          </div>
          <h3 className="text-3xl font-black text-slate-800 mb-10 leading-tight">"{questions[currentIndex].question}"</h3>
          {!showAnswer ? (
            <button onClick={() => setShowAnswer(true)} className="py-4 px-8 bg-slate-100 text-slate-600 rounded-xl font-bold hover:bg-slate-200 transition-colors border border-slate-200">Reveal Answer Guide 👀</button>
          ) : (
            <div className="animate-slide-up">
              <div className="bg-emerald-50 border border-emerald-200 p-8 rounded-2xl mb-8">
                <h4 className="text-emerald-800 font-black mb-2 flex items-center gap-2">💡 Ideal Answer Structure:</h4>
                <p className="text-emerald-700 font-medium text-lg">{questions[currentIndex].hint}</p>
              </div>
              <button onClick={handleNext} className="w-full py-5 bg-slate-800 text-white rounded-2xl text-xl font-black hover:bg-slate-900 transition-colors shadow-lg">
                {currentIndex === questions.length - 1 ? 'Finish Interview' : 'Next Question ➔'}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ==========================================
// 3. ATS RESUME FIXER
// ==========================================
function ResumeEditorTab() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handleReview = async () => {
    if (!file) return alert("Upload a PDF");
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('https://careerpath-ai-imzn.onrender.com/review_resume', { method: 'POST', body: formData });
      const data = await res.json();
      setFeedback(data);
    } catch (err) { alert("Error reaching backend."); }
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-10">
      <div className="bg-white p-12 rounded-[3rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 text-center">
        <div className="w-20 h-20 bg-indigo-50 rounded-3xl flex items-center justify-center mx-auto mb-6 text-indigo-500 shadow-inner"><CheckIcon /></div>
        <h2 className="text-3xl font-black text-slate-800 mb-4">ATS Compliance Scanner</h2>
        <p className="text-lg font-medium text-slate-500 mb-10 max-w-2xl mx-auto">75% of resumes are rejected by bots before a human sees them. Scan yours for critical missing sections and spelling errors.</p>
        <div className="flex flex-col items-center gap-6">
          <div className="relative border-2 border-dashed border-slate-300 rounded-[2rem] p-8 w-full max-w-xl bg-slate-50 hover:bg-indigo-50 hover:border-indigo-400 transition-all cursor-pointer">
            <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
            <p className="text-xl font-bold text-slate-600">Select PDF to Scan</p>
            {file && <p className="mt-4 font-bold text-indigo-600 bg-indigo-100 py-2 px-4 rounded-xl inline-block">{file.name}</p>}
          </div>
          <button onClick={handleReview} disabled={loading} className="w-full max-w-xl py-5 bg-slate-800 text-white rounded-2xl text-xl font-black hover:bg-slate-900 hover:-translate-y-1 hover:shadow-2xl hover:shadow-slate-900/30 transition-all duration-300 disabled:opacity-50">
            {loading ? 'Running Diagnostic...' : 'Execute Document Scan'}
          </button>
        </div>
      </div>
      {feedback && (
        <div className="bg-white p-12 rounded-[3rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 animate-slide-up">
          <div className="flex items-center justify-between mb-10 pb-10 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">Diagnostic Score</h3>
              <div className={`text-6xl font-black tracking-tighter ${feedback.score > 80 ? 'text-emerald-500' : 'text-orange-500'}`}>{feedback.score}<span className="text-3xl text-slate-400">/100</span></div>
            </div>
            <div className={`w-24 h-24 rounded-full flex items-center justify-center border-8 ${feedback.score > 80 ? 'border-emerald-100 text-emerald-500' : 'border-orange-100 text-orange-500'}`}>
              <span className="text-4xl font-black">{feedback.score > 80 ? 'A' : 'C'}</span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-10">
            <div>
              <h4 className="font-black text-xl text-slate-800 mb-6 flex items-center gap-2"><span className="text-orange-500">⚠️</span> Structural Issues</h4>
              <ul className="space-y-4">
                {feedback.structural_issues.length === 0 ? <li className="text-base font-bold text-emerald-700 bg-emerald-50 p-5 rounded-2xl border border-emerald-100 shadow-sm">All ATS sections found!</li> : feedback.structural_issues.map((issue, i) => (<li key={i} className="text-base font-semibold text-orange-800 bg-orange-50 p-5 rounded-2xl border border-orange-100 shadow-sm">{issue}</li>))}
              </ul>
            </div>
            <div>
              <h4 className="font-black text-xl text-slate-800 mb-6 flex items-center gap-2"><span className="text-red-500">📝</span> Spell Check</h4>
              <ul className="space-y-4">
                {feedback.spelling_alerts.length === 0 ? <li className="text-base font-bold text-emerald-700 bg-emerald-50 p-5 rounded-2xl border border-emerald-100 shadow-sm">No critical typos detected.</li> : feedback.spelling_alerts.map((alert, i) => (<li key={i} className="text-base font-semibold text-red-800 bg-red-50 p-5 rounded-2xl border border-red-100 shadow-sm">{alert}</li>))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==========================================
// 4. TEMPLATES 
// ==========================================
function TemplatesTab() {
  const templates = [
    { domain: "AI_ML_Engineer", display: "AI / ML Engineer", desc: "Focuses on Research Papers, Algorithms, and Models.", color: "from-purple-500 to-indigo-500", shadow: "shadow-purple-500/20" },
    { domain: "Full-Stack_Developer", display: "Full-Stack Developer", desc: "Prioritizes tech stacks, live portfolio links, and CI/CD.", color: "from-blue-500 to-cyan-500", shadow: "shadow-blue-500/20" },
    { domain: "Data_Scientist", display: "Data Scientist", desc: "Highlights visualizations, statistical modeling, and Kaggle.", color: "from-emerald-500 to-teal-500", shadow: "shadow-emerald-500/20" }
  ];

  const handleDownload = (domainID) => {
    window.open(`https://careerpath-ai-imzn.onrender.com/download_template/${domainID}`, '_blank');
  };

  return (
    <div className="max-w-6xl mx-auto space-y-10">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <h2 className="text-5xl font-black text-slate-800 mb-6 tracking-tight">Domain Templates</h2>
        <p className="text-xl font-medium text-slate-500">Stop using generic formats. Different tech roles require strictly different resume architectures to pass recruiters.</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
        {templates.map((temp) => (
          <div key={temp.domain} className="group bg-white rounded-[2.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden hover:-translate-y-2 hover:shadow-2xl transition-all duration-300 flex flex-col">
            <div className={`h-32 bg-gradient-to-br ${temp.color} w-full relative overflow-hidden`}>
              <div className="absolute -right-10 -bottom-10 w-40 h-40 bg-white/20 rounded-full blur-2xl"></div>
            </div>
            <div className="p-10 pt-8 flex-1 flex flex-col">
              <h3 className="font-black text-2xl mb-4 text-slate-800">{temp.display}</h3>
              <p className="text-base font-medium text-slate-500 mb-10 flex-1 leading-relaxed">{temp.desc}</p>
              <button onClick={() => handleDownload(temp.domain)} className={`w-full py-4 bg-slate-50 border-2 border-slate-100 rounded-2xl text-lg font-bold text-slate-700 group-hover:bg-slate-800 group-hover:text-white group-hover:border-slate-800 transition-colors shadow-lg ${temp.shadow}`}>
                Download .DOCX Template
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ==========================================
// 5. AI COVER LETTER
// ==========================================
function CoverLetterTab() {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState('');
  const [company, setCompany] = useState('');
  const [loading, setLoading] = useState(false);
  const [letter, setLetter] = useState('');

  const generateLetter = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please upload a PDF resume so the AI can extract your skills.");
    if (!role || !company) return alert("Please enter the Target Role and Company.");

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('role', role);
    formData.append('company', company);

    try {
      const res = await fetch('https://careerpath-ai-imzn.onrender.com/generate_cover_letter', { method: 'POST', body: formData });
      const data = await res.json();
      if (res.ok) { setLetter(data.cover_letter); } else { alert("Server Error: " + data.error); }
    } catch (err) { alert("Failed to connect to backend."); }
    setLoading(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(letter);
    alert("Copied to clipboard!");
  };

  return (
    <div className="max-w-5xl mx-auto space-y-10">
      <div className="bg-white p-10 rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100">
        <div className="mb-8 border-b border-slate-100 pb-6">
          <h2 className="text-3xl font-black text-slate-800 mb-2">Smart Cover Letter Generator</h2>
          <p className="text-slate-500 font-medium">Upload your resume. Our engine will extract your top skills and write a personalized cover letter instantly.</p>
        </div>
        <form onSubmit={generateLetter} className="space-y-8">
          <div className="grid grid-cols-2 gap-8">
            <div className="space-y-2">
              <label className="text-sm font-bold text-slate-700 uppercase tracking-wider">Target Job Title</label>
              <input type="text" value={role} onChange={(e) => setRole(e.target.value)} placeholder="e.g., Python Developer" className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 font-medium focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all" required />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-bold text-slate-700 uppercase tracking-wider">Target Company</label>
              <input type="text" value={company} onChange={(e) => setCompany(e.target.value)} placeholder="e.g., Google, TCS, Startup Inc" className="w-full border-2 border-slate-100 p-4 rounded-2xl bg-slate-50 font-medium focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all" required />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-bold text-slate-700 uppercase tracking-wider block">Upload Resume (PDF)</label>
            <div className="relative border-2 border-dashed border-slate-300 rounded-[2rem] p-8 text-center bg-slate-50 hover:bg-indigo-50 transition-all cursor-pointer">
              <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" required />
              <p className="text-lg font-bold text-slate-600">Drag & Drop Resume to extract skills</p>
              {file && <p className="mt-2 font-bold text-indigo-600">{file.name}</p>}
            </div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-5 bg-indigo-600 text-white rounded-2xl text-xl font-black hover:bg-indigo-700 hover:-translate-y-1 hover:shadow-xl transition-all duration-300 disabled:opacity-50">
            {loading ? 'Drafting Letter...' : 'Generate Personalized Cover Letter'}
          </button>
        </form>
      </div>
      {letter && (
        <div className="bg-white p-10 rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 animate-slide-up relative">
          <button onClick={copyToClipboard} className="absolute top-8 right-8 px-6 py-2 bg-slate-800 text-white font-bold rounded-xl hover:bg-slate-700 transition-colors">Copy to Clipboard</button>
          <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">Generated Document</h3>
          <div className="bg-slate-50 border border-slate-200 p-8 rounded-2xl text-slate-700 font-medium leading-relaxed whitespace-pre-wrap">{letter}</div>
        </div>
      )}
    </div>
  );
}