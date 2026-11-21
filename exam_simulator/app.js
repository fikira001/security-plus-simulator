/**
 * CompTIA Security+ (SY0-701) Master Exam Simulator & Fast-Pass Prep
 * High-performance, offline-capable testing and acceleration engine.
 */

class SecPlusSimulator {
  constructor() {
    this.db = null;
    this.studyGuides = null;
    this.currentExamId = null;
    this.currentExamTitle = "";
    this.questions = [];
    this.currentIndex = 0;
    this.userAnswers = {}; // qId -> array of letters, or object for PBQ
    this.flagged = new Set();
    this.timerSeconds = 90 * 60;
    this.timerInterval = null;
    this.isPaused = false;
    this.examMode = "vue_exam"; // 'vue_exam' or 'study_drill'

    // History and statistics
    this.stats = this.loadStats();
    this.missedQuestions = this.loadMissedQuestions();

    // Acronym state & deck separation
    this.acronyms = [];
    this.filteredAcronyms = [];
    this.currentDeckMode = localStorage.getItem("secplus_acro_deck_mode") || "learning"; // 'learning', 'mastered', 'all'
    this.currentAcronymDomainFilter = localStorage.getItem("secplus_acro_domain_filter") || "all";
    this.currentAcronymIndex = 0;
    this.acronymsMastered = new Set(JSON.parse(localStorage.getItem("secplus_acro_mastered") || "[]"));
    this.acroQuizCurrent = null;
    this.acroQuizScore = { correct: 0, total: 0 };

    // Notes state
    this.currentDomainNote = 1;
    this.cachedGradedResults = null;

    this.init();
  }

  async init() {
    this.setupTheme();
    this.setupNavigation();
    this.setupKeyboardShortcuts();
    await this.loadDatabase();
    await this.loadStudyGuides();
    this.renderDashboardStats();
    this.renderPBQLab();
    this.renderAcronymFlashcard();
    this.renderMissedBank();
    this.showCheatTab("ports");
    this.selectDomainNotes(1);
  }

  // --- DATABASE & STUDY GUIDES LOADING ---
  async loadDatabase() {
    try {
      const res = await fetch("data/questions_db.json");
      this.db = await res.json();
      this.acronyms = this.db.acronyms || [];
      this.applySavedAcronymState();
      console.log(`Database loaded: ${this.db.all_mcqs.length} MCQs, ${this.db.pbqs.length} PBQs, ${this.acronyms.length} Acronyms`);
    } catch (err) {
      console.error("Failed to load question database:", err);
      alert("Failed to load question database. Please verify data/questions_db.json.");
    }
  }

  async loadStudyGuides() {
    try {
      const res = await fetch("data/domain_study_guides.json");
      this.studyGuides = await res.json();
      console.log("Domain study guides loaded successfully.");
    } catch (err) {
      console.warn("Domain study guides not yet available:", err);
    }
  }

  // --- THEME ---
  setupTheme() {
    const saved = localStorage.getItem("secplus_theme") || "light";
    const sunIcon = document.getElementById("theme-icon-sun");
    const moonIcon = document.getElementById("theme-icon-moon");

    const applyTheme = (theme) => {
      if (theme === "dark") {
        document.body.classList.remove("theme-light");
        document.body.classList.add("theme-dark");
        if (sunIcon) sunIcon.classList.remove("hidden");
        if (moonIcon) moonIcon.classList.add("hidden");
      } else {
        document.body.classList.remove("theme-dark");
        document.body.classList.add("theme-light");
        if (sunIcon) sunIcon.classList.add("hidden");
        if (moonIcon) moonIcon.classList.remove("hidden");
      }
    };

    applyTheme(saved);

    const toggleBtn = document.getElementById("theme-toggle-btn");
    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        const isDark = document.body.classList.contains("theme-dark");
        const next = isDark ? "light" : "dark";
        localStorage.setItem("secplus_theme", next);
        applyTheme(next);
      });
    }
  }

  // --- NAVIGATION ---
  setupNavigation() {
    document.querySelectorAll(".nav-item-btn, .nav-tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        if (btn.dataset.tab) {
          this.switchTab(btn.dataset.tab);
        }
      });
    });

    const mobileToggle = document.getElementById("mobile-toggle-btn");
    if (mobileToggle) {
      mobileToggle.addEventListener("click", () => {
        const sidebar = document.getElementById("app-sidebar");
        if (sidebar) sidebar.classList.toggle("mobile-open");
      });
    }

    // Review grid filter buttons
    document.querySelectorAll(".review-filter-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".review-filter-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.renderReviewGrid(btn.dataset.filter);
      });
    });

    // Flag checkbox in header
    const flagCb = document.getElementById("vue-flag-checkbox");
    if (flagCb) {
      flagCb.addEventListener("change", () => {
        this.toggleFlag(flagCb.checked);
      });
    }

    // Flag button in question body
    const flagBtn = document.getElementById("exam-flag-btn");
    if (flagBtn) {
      flagBtn.addEventListener("click", () => {
        const q = this.questions[this.currentIndex];
        if (q) {
          const isFlagged = !this.flagged.has(q.id);
          this.toggleFlag(isFlagged);
        }
      });
    }

    // Prev / Next buttons
    const prevBtn = document.getElementById("exam-prev-btn");
    if (prevBtn) prevBtn.addEventListener("click", () => this.prevQuestion());

    const nextBtn = document.getElementById("exam-next-btn");
    if (nextBtn) nextBtn.addEventListener("click", () => this.nextQuestion());

    const finishBtn = document.getElementById("exam-finish-btn");
    if (finishBtn) finishBtn.addEventListener("click", () => this.openReviewScreen());

    const vueReviewBtn = document.getElementById("vue-review-screen-btn");
    if (vueReviewBtn) vueReviewBtn.addEventListener("click", () => this.openReviewScreen());

    // Timer control
    const pauseBtn = document.getElementById("exam-pause-btn");
    if (pauseBtn) pauseBtn.addEventListener("click", () => this.togglePauseTimer());

    // Instant check button (for study mode)
    const checkBtn = document.getElementById("exam-instant-check-btn");
    if (checkBtn) checkBtn.addEventListener("click", () => this.checkInstantAnswer());

    // Quick random exam button in header
    const quickMockBtn = document.getElementById("quick-random-exam-btn");
    if (quickMockBtn) quickMockBtn.addEventListener("click", () => this.startRandomExam(90));

    // Close search dropdown on click outside
    document.addEventListener("click", (e) => {
      const searchBox = document.querySelector(".topbar-search-box");
      const resultsContainer = document.getElementById("global-search-results");
      if (searchBox && !searchBox.contains(e.target) && resultsContainer) {
        resultsContainer.classList.add("hidden");
      }
    });
  }

  setupKeyboardShortcuts() {
    window.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "SELECT" || e.target.tagName === "TEXTAREA") {
        return;
      }

      // In active exam view
      if (document.getElementById("view-exam").classList.contains("active")) {
        if (e.key === "ArrowRight") {
          this.nextQuestion();
        } else if (e.key === "ArrowLeft") {
          this.prevQuestion();
        } else if (e.key.toLowerCase() === "f") {
          const q = this.questions[this.currentIndex];
          if (q) this.toggleFlag(!this.flagged.has(q.id));
        } else if (["1", "2", "3", "4", "5", "6", "7", "a", "b", "c", "d", "e", "f", "g"].includes(e.key.toLowerCase())) {
          this.handleOptionKey(e.key.toLowerCase());
        }
      }

      // In Acronym Flashcard view
      if (document.getElementById("view-acronyms").classList.contains("active") && !document.getElementById("acro-flashcard-view").classList.contains("hidden")) {
        if (e.code === "Space") {
          e.preventDefault();
          this.flipFlashcard();
        } else if (e.key === "ArrowRight") {
          this.nextFlashcard();
        } else if (e.key === "ArrowLeft") {
          this.prevFlashcard();
        } else if (e.key.toLowerCase() === "m") {
          this.toggleAcronymMastered();
        }
      }
    });
  }

  handleOptionKey(key) {
    const q = this.questions[this.currentIndex];
    if (!q || !q.options) return;
    const mapping = { "1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "6": "F", "7": "G" };
    const letter = (mapping[key] || key).toUpperCase();
    const opt = q.options.find(o => o.letter === letter);
    if (opt) {
      this.selectOption(opt.letter);
    }
  }

  switchTab(tabId) {
    document.querySelectorAll(".nav-item-btn, .nav-tab-btn").forEach(b => {
      b.classList.toggle("active", b.dataset.tab === tabId);
    });
    document.querySelectorAll(".view-panel").forEach(p => p.classList.remove("active"));
    const target = document.getElementById(`view-${tabId}`);
    if (target) {
      target.classList.add("active");
    }

    // Close mobile sidebar if open
    const sidebar = document.getElementById("app-sidebar");
    if (sidebar) sidebar.classList.remove("mobile-open");

    // Hide Pearson VUE top bar if leaving active exam
    const vueBar = document.getElementById("vue-exam-bar");
    if (vueBar && tabId !== "exam" && tabId !== "review-grid") {
      vueBar.classList.add("hidden");
    }

    if (tabId === "dashboard") {
      this.renderDashboardStats();
    } else if (tabId === "missed") {
      this.renderMissedBank();
    } else if (tabId === "notes") {
      this.selectDomainNotes(this.currentDomainNote);
    } else if (tabId === "acronyms") {
      this.renderAcronymFlashcard();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // --- GLOBAL SEARCH SYSTEM ---
  handleGlobalSearch(query) {
    const resultsContainer = document.getElementById("global-search-results");
    if (!resultsContainer) return;
    
    query = (query || "").toLowerCase().trim();
    if (query.length < 2) {
      resultsContainer.classList.add("hidden");
      resultsContainer.innerHTML = "";
      return;
    }

    const matches = {
      acronyms: [],
      notes: [],
      pbqs: [],
      mcqs: []
    };

    // 1. Search Acronyms
    if (this.acronyms) {
      for (const a of this.acronyms) {
        if (a.term.toLowerCase().includes(query) || (a.definition && a.definition.toLowerCase().includes(query))) {
          matches.acronyms.push(a);
          if (matches.acronyms.length >= 4) break;
        }
      }
    }

    // 2. Search Domain Study Guides
    if (this.studyGuides) {
      for (const domKey in this.studyGuides) {
        const dom = this.studyGuides[domKey];
        if (dom.objectives) {
          for (const obj of dom.objectives) {
            if (obj.code.toLowerCase().includes(query) || obj.title.toLowerCase().includes(query)) {
              matches.notes.push({ domain: dom.domain, code: obj.code, title: obj.title });
              if (matches.notes.length >= 4) break;
            }
          }
        }
        if (matches.notes.length >= 4) break;
      }
    }

    // 3. Search PBQs
    if (this.db && this.db.pbqs) {
      for (const pbq of this.db.pbqs) {
        if (pbq.title.toLowerCase().includes(query) || (pbq.scenario && pbq.scenario.toLowerCase().includes(query))) {
          matches.pbqs.push(pbq);
          if (matches.pbqs.length >= 3) break;
        }
      }
    }

    // 4. Search MCQs
    if (this.db && this.db.all_mcqs) {
      for (const q of this.db.all_mcqs) {
        if (q.stem && q.stem.toLowerCase().includes(query)) {
          matches.mcqs.push(q);
          if (matches.mcqs.length >= 3) break;
        }
      }
    }

    const totalMatches = matches.acronyms.length + matches.notes.length + matches.pbqs.length + matches.mcqs.length;
    if (totalMatches === 0) {
      resultsContainer.innerHTML = `<div style="padding: 12px 16px; font-size: 0.85rem; color: var(--text-muted); text-align: center;">No matches found for "${query}"</div>`;
      resultsContainer.classList.remove("hidden");
      return;
    }

    let html = "";

    if (matches.acronyms.length > 0) {
      html += `<div class="search-result-group"><div class="search-result-group-title">Acronyms</div>`;
      matches.acronyms.forEach(a => {
        html += `
          <div class="search-result-item" onclick="app.jumpToAcronym('${a.term}')">
            <span class="search-result-text"><strong>${a.term}</strong> — ${a.definition}</span>
            <span class="search-result-badge">D${a.domain || 'All'}</span>
          </div>
        `;
      });
      html += `</div>`;
    }

    if (matches.notes.length > 0) {
      html += `<div class="search-result-group"><div class="search-result-group-title">Domain Study Guides</div>`;
      matches.notes.forEach(n => {
        html += `
          <div class="search-result-item" onclick="app.jumpToNote(${n.domain}, '${n.code}')">
            <span class="search-result-text"><strong>${n.code}</strong> ${n.title}</span>
            <span class="search-result-badge">Domain ${n.domain}.0</span>
          </div>
        `;
      });
      html += `</div>`;
    }

    if (matches.pbqs.length > 0) {
      html += `<div class="search-result-group"><div class="search-result-group-title">PBQ Lab</div>`;
      matches.pbqs.forEach(p => {
        html += `
          <div class="search-result-item" onclick="app.jumpToPBQ('${p.id}')">
            <span class="search-result-text"><strong>${p.title}</strong></span>
            <span class="search-result-badge">Domain ${p.domain}.0 PBQ</span>
          </div>
        `;
      });
      html += `</div>`;
    }

    if (matches.mcqs.length > 0) {
      html += `<div class="search-result-group"><div class="search-result-group-title">Practice Questions</div>`;
      matches.mcqs.forEach(q => {
        const shortStem = q.stem.split('\n')[0].substring(0, 75).replace(/"/g, '&quot;');
        html += `
          <div class="search-result-item" onclick="app.startTargetedQuestionDrill('${q.id}')">
            <span class="search-result-text">${shortStem}...</span>
            <span class="search-result-badge">D${q.domain}.0 MCQ</span>
          </div>
        `;
      });
      html += `</div>`;
    }

    resultsContainer.innerHTML = html;
    resultsContainer.classList.remove("hidden");
  }

  jumpToAcronym(term) {
    const res = document.getElementById("global-search-results");
    if (res) res.classList.add("hidden");
    this.switchTab("acronyms");
    this.setAcronymMode("table");
    const searchInp = document.getElementById("acronym-search-input");
    if (searchInp) {
      searchInp.value = term;
      this.searchAcronyms(term);
    }
  }

  jumpToNote(domainNum, objCode) {
    const res = document.getElementById("global-search-results");
    if (res) res.classList.add("hidden");
    this.switchTab("notes");
    this.selectDomainNotes(domainNum);
    setTimeout(() => {
      const card = document.getElementById(`note-card-${objCode.replace('.', '-')}`);
      if (card) {
        card.classList.add("open");
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 120);
  }

  jumpToPBQ(pbqId) {
    const res = document.getElementById("global-search-results");
    if (res) res.classList.add("hidden");
    this.switchTab("pbqs");
    setTimeout(() => {
      const el = document.getElementById(`pbq-card-${pbqId}`);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 120);
  }

  startTargetedQuestionDrill(qId) {
    const res = document.getElementById("global-search-results");
    if (res) res.classList.add("hidden");
    const q = this.db.all_mcqs.find(m => m.id === qId);
    if (!q) return;

    this.questions = [q];
    this.currentExamId = `targeted_${qId}`;
    this.currentExamTitle = `Targeted Question Review (${q.id})`;
    this.currentIndex = 0;
    this.userAnswers = {};
    this.flagged.clear();
    this.timerSeconds = 120;
    this.isPaused = false;
    this.examMode = "study_drill";
    this.launchExamSession();
  }
  // --- STATS & LOCALSTORAGE ---
  loadStats() {
    const s = localStorage.getItem("secplus_stats");
    return s ? JSON.parse(s) : { attempts: [], domainPerformance: { 1: { c: 0, t: 0 }, 2: { c: 0, t: 0 }, 3: { c: 0, t: 0 }, 4: { c: 0, t: 0 }, 5: { c: 0, t: 0 } }, totalAnswered: 0 };
  }

  saveStats() {
    localStorage.setItem("secplus_stats", JSON.stringify(this.stats));
  }

  loadMissedQuestions() {
    const m = localStorage.getItem("secplus_missed");
    return m ? JSON.parse(m) : {};
  }

  saveMissedQuestions() {
    localStorage.setItem("secplus_missed", JSON.stringify(this.missedQuestions));
    const cnt = Object.keys(this.missedQuestions).length;
    const badge = document.getElementById("missed-count-badge");
    if (badge) badge.innerText = cnt;
    const totalStat = document.getElementById("total-missed-stat");
    if (totalStat) totalStat.innerText = cnt;
  }

  renderDashboardStats() {
    const totalAttempted = this.stats.totalAnswered || 0;
    document.getElementById("total-attempted-stat").innerText = totalAttempted;
    const missedCnt = Object.keys(this.missedQuestions).length;
    document.getElementById("total-missed-stat").innerText = missedCnt;
    document.getElementById("missed-count-badge").innerText = missedCnt;

    let totalScoreWeight = 0;
    const weights = { 1: 0.12, 2: 0.22, 3: 0.18, 4: 0.28, 5: 0.20 };
    let hasData = false;

    for (let d = 1; d <= 5; d++) {
      const data = this.stats.domainPerformance[d] || { c: 0, t: 0 };
      const pct = data.t > 0 ? Math.round((data.c / data.t) * 100) : 0;
      if (data.t > 0) hasData = true;

      const pEl = document.getElementById(`d${d}-progress`);
      const txtEl = document.getElementById(`d${d}-pct`);
      if (pEl) pEl.style.width = `${pct}%`;
      if (txtEl) txtEl.innerText = `${pct}% (${data.c}/${data.t})`;

      totalScoreWeight += (pct / 100) * weights[d];
    }

    const readinessPct = hasData ? Math.round(totalScoreWeight * 100) : 0;
    document.getElementById("readiness-pct").innerText = `${readinessPct}%`;
    const circle = document.getElementById("readiness-circle");
    if (circle) {
      circle.setAttribute("stroke-dasharray", `${readinessPct}, 100`);
    }

    const predicted = hasData ? Math.round(100 + (totalScoreWeight * 800)) : "--";
    document.getElementById("predicted-score").innerText = `${predicted} / 900`;

    const sidebarLabel = document.getElementById("sidebar-readiness-label");
    if (sidebarLabel) {
      sidebarLabel.innerText = `Readiness: ${readinessPct}%`;
    }

    const exams = ["exam_a", "exam_b", "exam_c", "exam_gibson_post", "exam_polynko"];
    exams.forEach(eid => {
      const attempts = this.stats.attempts.filter(a => a.examId === eid);
      const el = document.getElementById(`${eid.replace(/_/g, '-')}-best`);
      if (el && attempts.length > 0) {
        const best = Math.max(...attempts.map(a => a.scaledScore));
        el.innerText = `Best: ${best}/900 (${best >= 750 ? 'PASS' : 'FAIL'})`;
        el.style.color = best >= 750 ? 'var(--accent-green)' : 'var(--accent-red)';
      }
    });
  }

  // --- EXAM LAUNCHERS ---
  startExam(examKey) {
    if (!this.db || !this.db.exams[examKey]) {
      alert("Exam not found in database.");
      return;
    }

    const examData = this.db.exams[examKey];
    this.currentExamId = examKey;
    this.currentExamTitle = examData.title;
    this.questions = JSON.parse(JSON.stringify(examData.questions));
    this.currentIndex = 0;
    this.userAnswers = {};
    this.flagged.clear();
    this.timerSeconds = (examData.duration_minutes || 90) * 60;
    this.isPaused = false;
    this.examMode = "vue_exam";

    this.launchExamSession();
  }

  startRandomExam(size = 90) {
    if (!this.db || !this.db.all_mcqs) return;
    this.currentExamId = "random_exam";
    this.currentExamTitle = `CompTIA Security+ Dynamic Exam (${size} Questions)`;
    this.examMode = "vue_exam";

    const dWeights = { 1: 0.12, 2: 0.22, 3: 0.18, 4: 0.28, 5: 0.20 };
    const domainBuckets = { 1: [], 2: [], 3: [], 4: [], 5: [] };

    this.db.all_mcqs.forEach(q => {
      const d = q.domain || 1;
      if (domainBuckets[d]) domainBuckets[d].push(q);
    });

    let selected = [];

    // Include 2-3 PBQs if full mock
    if (size >= 60 && this.db.pbqs && this.db.pbqs.length > 0) {
      const shuffledPbqs = [...this.db.pbqs].sort(() => 0.5 - Math.random());
      selected.push(...shuffledPbqs.slice(0, 3));
    }

    const remainingCount = size - selected.length;
    for (let d = 1; d <= 5; d++) {
      const quota = Math.round(remainingCount * dWeights[d]);
      const pool = [...domainBuckets[d]].sort(() => 0.5 - Math.random());
      selected.push(...pool.slice(0, quota));
    }

    if (selected.length < size) {
      const extra = [...this.db.all_mcqs].filter(q => !selected.some(s => s.id === q.id)).sort(() => 0.5 - Math.random());
      selected.push(...extra.slice(0, size - selected.length));
    } else if (selected.length > size) {
      selected = selected.slice(0, size);
    }

    const pbqs = selected.filter(q => q.items);
    const mcqs = selected.filter(q => !q.items).sort(() => 0.5 - Math.random());
    this.questions = [...pbqs, ...mcqs];

    this.currentIndex = 0;
    this.userAnswers = {};
    this.flagged.clear();
    this.timerSeconds = size * 60;
    this.isPaused = false;

    this.launchExamSession();
  }

  startDomainDrill(domainNum) {
    document.getElementById("drill-domain-select").value = domainNum.toString();
    this.switchTab("drills");
  }

  launchCustomDrill() {
    const domainVal = document.getElementById("drill-domain-select").value;
    const size = parseInt(document.getElementById("drill-size-select").value);
    const mode = document.getElementById("drill-mode-select").value;

    let pool = [];
    if (domainVal === "all") {
      pool = [...this.db.all_mcqs];
    } else {
      const d = parseInt(domainVal);
      pool = this.db.all_mcqs.filter(q => q.domain === d);
    }

    if (pool.length === 0) {
      alert("No questions found for the selected domain.");
      return;
    }

    pool.sort(() => 0.5 - Math.random());
    this.questions = pool.slice(0, size);
    this.currentExamId = `drill_d${domainVal}`;
    this.currentExamTitle = domainVal === "all" ? `Mixed Domain Drill (${size} Qs)` : `Domain ${domainVal} Targeted Drill (${size} Qs)`;
    this.currentIndex = 0;
    this.userAnswers = {};
    this.flagged.clear();
    this.timerSeconds = size * 90;
    this.isPaused = false;
    this.examMode = mode === "study" ? "study_drill" : "vue_exam";

    this.launchExamSession();
  }

  drillMissedQuestions() {
    const missedIds = Object.keys(this.missedQuestions);
    if (missedIds.length === 0) {
      alert("No missed questions in your bank! Outstanding!");
      return;
    }

    const pool = [];
    missedIds.forEach(id => {
      const q = this.db.all_mcqs.find(m => m.id === id);
      if (q) pool.push(q);
    });

    if (pool.length === 0) {
      alert("Missed questions could not be found in active database.");
      return;
    }

    pool.sort(() => 0.5 - Math.random());
    this.questions = pool;
    this.currentExamId = "missed_drill";
    this.currentExamTitle = `Missed Questions Recovery Drill (${pool.length} Qs)`;
    this.currentIndex = 0;
    this.userAnswers = {};
    this.flagged.clear();
    this.timerSeconds = pool.length * 90;
    this.isPaused = false;
    this.examMode = "study_drill";

    this.launchExamSession();
  }

  launchExamSession() {
    const vueBar = document.getElementById("vue-exam-bar");
    vueBar.classList.remove("hidden");
    document.querySelector(".vue-exam-title").innerText = this.currentExamTitle;

    const checkBtn = document.getElementById("exam-instant-check-btn");
    if (this.examMode === "study_drill") {
      checkBtn.classList.remove("hidden");
    } else {
      checkBtn.classList.add("hidden");
    }

    this.switchTab("exam");
    this.startTimer();
    this.renderCurrentQuestion();
  }

  // --- TIMER ---
  startTimer() {
    clearInterval(this.timerInterval);
    this.updateTimerDisplay();

    this.timerInterval = setInterval(() => {
      if (!this.isPaused) {
        this.timerSeconds--;
        this.updateTimerDisplay();

        if (this.timerSeconds <= 0) {
          clearInterval(this.timerInterval);
          alert("Time has expired! Submitting your exam for grading now.");
          this.submitExamForGrading();
        }
      }
    }, 1000);
  }

  updateTimerDisplay() {
    const mins = Math.floor(this.timerSeconds / 60);
    const secs = this.timerSeconds % 60;
    const str = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    const el = document.getElementById("vue-timer");
    if (el) {
      el.innerText = str;
      if (this.timerSeconds <= 300) {
        el.style.color = "var(--accent-red)";
      } else {
        el.style.color = "#38bdf8";
      }
    }
  }

  togglePauseTimer() {
    this.isPaused = !this.isPaused;
    const btn = document.getElementById("exam-pause-btn");
    btn.innerText = this.isPaused ? "▶" : "⏸";
    btn.title = this.isPaused ? "Resume Timer" : "Pause Timer";
  }

  // --- FORMAT QUESTION STEM WITH TERMINAL LOGS & BULLETS ---
  formatStemHTML(stem) {
    if (!stem) return "";

    // Split text into lines
    const lines = stem.split('\n');
    let html = "";
    let inLogBlock = false;
    let logBuffer = [];
    let inBulletList = false;
    let bulletBuffer = [];

    const flushLog = () => {
      if (logBuffer.length > 0) {
        html += `
          <div class="terminal-card">
            <div class="terminal-header">
              <div class="terminal-dots">
                <span class="red"></span>
                <span class="yellow"></span>
                <span class="green"></span>
              </div>
              <span class="terminal-title">SECURITY EVENT LOG / PACKET CAPTURE</span>
              <span class="terminal-badge">SYS/NET</span>
            </div>
            <pre class="terminal-body"><code>${logBuffer.join('\n')}</code></pre>
          </div>
        `;
        logBuffer = [];
      }
      inLogBlock = false;
    };

    const flushBullets = () => {
      if (bulletBuffer.length > 0) {
        html += `
          <ul class="q-stem-bullet-list">
            ${bulletBuffer.map(b => `
              <li class="q-stem-bullet-item">
                <span class="bullet-dot">▪</span>
                <span>${b}</span>
              </li>
            `).join('')}
          </ul>
        `;
        bulletBuffer = [];
      }
      inBulletList = false;
    };

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;

      // Detect log line triggers
      const isLogLine = /^(ALERT|UTC\s+\d+|Frame\s+\d+|Ethernet\s+II|Internet\s+Protocol|Transmission\s+Control|Application\s+Data|Rule\s+#|\d+\.\d+\.\d+\.\d+|URL\/|User\s+Agent:|Detail:|Gateway\s+Anti-Virus|Method\s+(GET|POST|PUT|DELETE)|SELECT\s+\*\s+FROM|USER\d+['"])/i.test(line) ||
                        (/\d+\.\d+\.\d+\.\d+.*?(->|:\d+)/.test(line) && !line.includes('?'));

      // Detect bullet line
      const isBulletLine = /^([•–\-\*]|\d+\.)\s+/.test(line);

      if (isLogLine) {
        flushBullets();
        inLogBlock = true;
        logBuffer.push(line);
      } else if (isBulletLine) {
        flushLog();
        inBulletList = true;
        bulletBuffer.push(line.replace(/^[•–\-\*]\s+|\d+\.\s+/, ''));
      } else {
        // Normal paragraph text
        flushLog();
        flushBullets();
        html += `<p class="q-stem-paragraph">${line}</p>`;
      }
    }

    flushLog();
    flushBullets();

    return html;
  }

  // --- CURRENT QUESTION RENDERING ---
  renderCurrentQuestion() {
    const q = this.questions[this.currentIndex];
    if (!q) return;

    // Counter & Badges
    document.getElementById("vue-q-current").innerText = this.currentIndex + 1;
    document.getElementById("vue-q-total").innerText = this.questions.length;
    document.getElementById("exam-q-badge").innerText = `Question ${this.currentIndex + 1} of ${this.questions.length}`;

    const dTag = document.getElementById("exam-q-domain");
    dTag.innerText = `Domain ${q.domain || 1}.0`;

    // Flag checkbox sync
    const isFlagged = this.flagged.has(q.id);
    const cb = document.getElementById("vue-flag-checkbox");
    if (cb) cb.checked = isFlagged;
    const flagBtn = document.getElementById("exam-flag-btn");
    if (flagBtn) {
      flagBtn.classList.toggle("flagged", isFlagged);
      document.getElementById("flag-btn-text").innerText = isFlagged ? "Flagged" : "Flag for Review";
    }

    // Hide instant feedback initially
    const feedbackBox = document.getElementById("instant-feedback-card");
    feedbackBox.classList.add("hidden");

    // Render formatted stem with terminal logs
    const stemBox = document.getElementById("exam-q-stem-box");
    stemBox.innerHTML = this.formatStemHTML(q.stem || q.title);

    const isPBQ = !!q.items;
    const qTypeBadge = document.getElementById("exam-q-type");
    const multiHint = document.getElementById("exam-multi-select-hint");
    const optionsContainer = document.getElementById("exam-options-container");
    const pbqContainer = document.getElementById("exam-pbq-container");

    if (isPBQ) {
      qTypeBadge.innerText = "Performance-Based Question (PBQ)";
      qTypeBadge.style.background = "rgba(139, 92, 246, 0.2)";
      qTypeBadge.style.color = "#c4b5fd";
      multiHint.classList.add("hidden");
      optionsContainer.classList.add("hidden");
      pbqContainer.classList.remove("hidden");
      this.renderPBQQuestion(q);
    } else {
      // Reliable multi-select detection
      const requiredCount = q.requiredCount || (q.correct && q.correct.length > 1 ? q.correct.length : 1);
      const isMulti = q.isMulti || requiredCount > 1;

      if (isMulti) {
        qTypeBadge.innerText = `Multi-Select (${requiredCount} Answers)`;
        qTypeBadge.style.background = "rgba(245, 158, 11, 0.2)";
        qTypeBadge.style.color = "#fbbf24";

        const currentAns = this.userAnswers[q.id] || [];
        multiHint.innerHTML = `
          <span>⚠️ <strong>Multi-Select Question:</strong> Please select <strong>${requiredCount} options</strong>.</span>
          <span class="multi-select-counter">${currentAns.length} of ${requiredCount} selected</span>
        `;
        multiHint.classList.remove("hidden");
      } else {
        qTypeBadge.innerText = "Single Choice";
        qTypeBadge.style.background = "rgba(59, 130, 246, 0.15)";
        qTypeBadge.style.color = "var(--accent-blue)";
        multiHint.classList.add("hidden");
      }

      optionsContainer.classList.remove("hidden");
      pbqContainer.classList.add("hidden");
      this.renderMCQQuestion(q, isMulti, requiredCount);
    }

    // Live progress
    const answeredCount = Object.keys(this.userAnswers).length;
    const progressPct = Math.round((answeredCount / this.questions.length) * 100);
    document.getElementById("exam-live-progress").style.width = `${progressPct}%`;
    document.getElementById("exam-progress-text").innerText = `${answeredCount} / ${this.questions.length} Answered`;

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  renderMCQQuestion(q, isMulti, requiredCount) {
    const container = document.getElementById("exam-options-container");
    container.innerHTML = "";

    const currentAnswer = this.userAnswers[q.id] || [];

    q.options.forEach(opt => {
      const item = document.createElement("div");
      item.className = `option-item ${isMulti ? 'multi-choice' : 'single-choice'}`;
      const isSelected = currentAnswer.includes(opt.letter);
      if (isSelected) item.classList.add("selected");

      const badgeContent = isMulti ? (isSelected ? "✓" : opt.letter) : opt.letter;

      item.innerHTML = `
        <div class="option-letter-badge">${badgeContent}</div>
        <div class="option-text">${opt.text}</div>
      `;

      item.addEventListener("click", () => {
        this.selectOption(opt.letter);
      });

      container.appendChild(item);
    });
  }

  selectOption(letter) {
    const q = this.questions[this.currentIndex];
    const requiredCount = q.requiredCount || (q.correct && q.correct.length > 1 ? q.correct.length : 1);
    const isMulti = q.isMulti || requiredCount > 1;

    if (isMulti) {
      let cur = this.userAnswers[q.id] ? [...this.userAnswers[q.id]] : [];

      if (cur.includes(letter)) {
        // Toggle off
        cur = cur.filter(l => l !== letter);
      } else {
        // Add option
        if (cur.length < requiredCount) {
          cur.push(letter);
        } else {
          // If already at required count, replace the first selected option
          cur.shift();
          cur.push(letter);
        }
      }

      if (cur.length > 0) {
        this.userAnswers[q.id] = cur;
      } else {
        delete this.userAnswers[q.id];
      }
    } else {
      // Single choice
      this.userAnswers[q.id] = [letter];
    }

    this.renderCurrentQuestion();
  }

  renderPBQQuestion(q) {
    const container = document.getElementById("exam-pbq-container");
    container.innerHTML = "";

    const currentAnswerMap = this.userAnswers[q.id] || {};

    const scenarioBox = document.createElement("div");
    scenarioBox.className = "pbq-scenario-box";
    scenarioBox.innerText = q.scenario;
    container.appendChild(scenarioBox);

    const table = document.createElement("table");
    table.className = "pbq-items-table";
    table.innerHTML = `
      <thead>
        <tr>
          <th style="width: 55%">Prompt / Configuration Item</th>
          <th style="width: 45%">Select Security Configuration</th>
        </tr>
      </thead>
      <tbody>
        ${q.items.map((item, idx) => `
          <tr>
            <td><strong>Item ${idx + 1}:</strong> ${item.prompt}</td>
            <td>
              <select class="pbq-select" data-idx="${idx}">
                <option value="">-- Choose Option --</option>
                ${q.options.map(opt => `
                  <option value="${opt}" ${currentAnswerMap[idx] === opt ? 'selected' : ''}>${opt}</option>
                `).join('')}
              </select>
            </td>
          </tr>
        `).join('')}
      </tbody>
    `;

    container.appendChild(table);

    table.querySelectorAll(".pbq-select").forEach(sel => {
      sel.addEventListener("change", (e) => {
        const idx = e.target.dataset.idx;
        const val = e.target.value;
        if (!this.userAnswers[q.id]) this.userAnswers[q.id] = {};
        if (val) {
          this.userAnswers[q.id][idx] = val;
        } else {
          delete this.userAnswers[q.id][idx];
        }

        const answeredCount = Object.keys(this.userAnswers).length;
        const progressPct = Math.round((answeredCount / this.questions.length) * 100);
        document.getElementById("exam-live-progress").style.width = `${progressPct}%`;
        document.getElementById("exam-progress-text").innerText = `${answeredCount} / ${this.questions.length} Answered`;
      });
    });
  }

  toggleFlag(isFlagged) {
    const q = this.questions[this.currentIndex];
    if (isFlagged) {
      this.flagged.add(q.id);
    } else {
      this.flagged.delete(q.id);
    }
    const cb = document.getElementById("vue-flag-checkbox");
    if (cb) cb.checked = isFlagged;
    const flagBtn = document.getElementById("exam-flag-btn");
    if (flagBtn) {
      flagBtn.classList.toggle("flagged", isFlagged);
      document.getElementById("flag-btn-text").innerText = isFlagged ? "Flagged" : "Flag for Review";
    }
  }

  prevQuestion() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderCurrentQuestion();
    }
  }

  nextQuestion() {
    if (this.currentIndex < this.questions.length - 1) {
      this.currentIndex++;
      this.renderCurrentQuestion();
    } else {
      this.openReviewScreen();
    }
  }

  // Study mode instant check
  checkInstantAnswer() {
    const q = this.questions[this.currentIndex];
    const isPBQ = !!q.items;
    const feedbackBox = document.getElementById("instant-feedback-card");
    const verdictBadge = document.getElementById("feedback-verdict-badge");
    const objTag = document.getElementById("feedback-obj-tag");
    const expText = document.getElementById("feedback-explanation-text");

    let isCorrect = false;

    if (isPBQ) {
      const userMap = this.userAnswers[q.id] || {};
      let allMatch = true;
      q.items.forEach((it, idx) => {
        if (userMap[idx] !== it.answer) allMatch = false;
      });
      isCorrect = allMatch && Object.keys(userMap).length === q.items.length;
    } else {
      const userAns = (this.userAnswers[q.id] || []).sort().join(',');
      const correctAns = (q.correct || []).sort().join(',');
      isCorrect = userAns === correctAns && userAns.length > 0;

      const items = document.querySelectorAll(".option-item");
      items.forEach(it => {
        const letter = it.querySelector(".option-letter-badge").innerText.trim();
        if (q.correct.includes(letter)) {
          it.style.borderColor = "var(--accent-green)";
          it.style.background = "rgba(16, 185, 129, 0.2)";
        } else if (userAns.includes(letter)) {
          it.style.borderColor = "var(--accent-red)";
          it.style.background = "rgba(239, 68, 68, 0.2)";
        }
      });
    }

    verdictBadge.innerText = isCorrect ? "✓ Correct" : "✗ Incorrect";
    verdictBadge.className = `verdict-badge ${isCorrect ? 'correct' : 'incorrect'}`;
    objTag.innerText = q.objective || "CompTIA SY0-701";
    expText.innerText = q.explanation;
    feedbackBox.classList.remove("hidden");

    if (!isCorrect) {
      this.missedQuestions[q.id] = {
        stem: q.stem || q.title,
        domain: q.domain || 1,
        source: q.source || "Drill",
        explanation: q.explanation
      };
      this.saveMissedQuestions();
    }
  }

  // --- REVIEW GRID SCREEN ---
  openReviewScreen() {
    this.switchTab("review-grid");
    this.renderReviewGrid("all");
  }

  renderReviewGrid(filter = "all") {
    const grid = document.getElementById("review-grid-items");
    grid.innerHTML = "";

    let answeredCnt = 0;
    let unansweredCnt = 0;
    let flaggedCnt = this.flagged.size;

    this.questions.forEach((q, idx) => {
      const hasAnswer = this.userAnswers[q.id] !== undefined && Object.keys(this.userAnswers[q.id]).length > 0;
      const isFlagged = this.flagged.has(q.id);

      if (hasAnswer) answeredCnt++;
      else unansweredCnt++;

      if (filter === "unanswered" && hasAnswer) return;
      if (filter === "flagged" && !isFlagged) return;

      const btn = document.createElement("button");
      btn.className = "grid-q-btn";
      if (hasAnswer) btn.classList.add("answered");
      if (isFlagged) btn.classList.add("flagged");

      btn.innerHTML = `<span>Q${idx + 1}</span>`;
      btn.addEventListener("click", () => {
        this.currentIndex = idx;
        this.switchTab("exam");
        this.renderCurrentQuestion();
      });

      grid.appendChild(btn);
    });

    document.getElementById("count-answered").innerText = answeredCnt;
    document.getElementById("count-unanswered").innerText = unansweredCnt;
    document.getElementById("count-flagged").innerText = flaggedCnt;
  }

  returnToActiveExam() {
    this.switchTab("exam");
    this.renderCurrentQuestion();
  }

  // --- SUBMIT & SCORING ---
  submitExamForGrading() {
    clearInterval(this.timerInterval);

    let correctCount = 0;
    const totalCount = this.questions.length;
    const domainScores = { 1: { c: 0, t: 0 }, 2: { c: 0, t: 0 }, 3: { c: 0, t: 0 }, 4: { c: 0, t: 0 }, 5: { c: 0, t: 0 } };

    const gradedResults = [];

    this.questions.forEach((q, idx) => {
      const d = q.domain || 1;
      if (!domainScores[d]) domainScores[d] = { c: 0, t: 0 };
      domainScores[d].t++;

      let isCorrect = false;
      const isPBQ = !!q.items;

      if (isPBQ) {
        const userMap = this.userAnswers[q.id] || {};
        let matches = 0;
        q.items.forEach((it, i) => {
          if (userMap[i] === it.answer) matches++;
        });
        isCorrect = matches === q.items.length;
        if (isCorrect) correctCount++;
      } else {
        const userAns = (this.userAnswers[q.id] || []).sort().join(',');
        const correctAns = (q.correct || []).sort().join(',');
        isCorrect = userAns === correctAns && userAns.length > 0;
        if (isCorrect) correctCount++;
      }

      if (isCorrect) {
        domainScores[d].c++;
        delete this.missedQuestions[q.id];
      } else {
        this.missedQuestions[q.id] = {
          stem: q.stem || q.title,
          domain: d,
          source: q.source || this.currentExamTitle,
          explanation: q.explanation
        };
      }

      gradedResults.push({
        qIndex: idx + 1,
        question: q,
        userAnswer: this.userAnswers[q.id] || [],
        isCorrect: isCorrect,
        isFlagged: this.flagged.has(q.id)
      });
    });

    this.saveMissedQuestions();

    const rawPct = Math.round((correctCount / totalCount) * 100);
    const scaledScore = Math.round(100 + ((correctCount / totalCount) * 800));
    const passed = scaledScore >= 750;

    // Update stats
    this.stats.totalAnswered += totalCount;
    for (let d = 1; d <= 5; d++) {
      this.stats.domainPerformance[d].c += domainScores[d].c;
      this.stats.domainPerformance[d].t += domainScores[d].t;
    }
    this.stats.attempts.push({
      date: new Date().toISOString(),
      examId: this.currentExamId,
      examTitle: this.currentExamTitle,
      scaledScore: scaledScore,
      passed: passed,
      rawPct: rawPct
    });
    this.saveStats();

    this.renderResultsView(scaledScore, passed, rawPct, correctCount, totalCount, domainScores, gradedResults);
  }

  // --- POST-EXAM DETAILED RESULTS & REVIEW ---
  renderResultsView(scaledScore, passed, rawPct, correctCount, totalCount, domainScores, gradedResults) {
    this.switchTab("results");
    document.getElementById("vue-exam-bar").classList.add("hidden");

    // Banner
    const banner = document.getElementById("results-banner");
    banner.className = `results-header-banner ${passed ? 'pass' : 'fail'}`;

    const badge = document.getElementById("results-status-badge");
    badge.innerText = passed ? "CONGRATULATIONS: PASS" : "DID NOT PASS";
    badge.className = `pass-fail-badge ${passed ? 'pass' : 'fail'}`;

    document.getElementById("results-status-text").innerText = passed ? "Exam Passed (Above 750)" : "Passing Score is 750/900";
    document.getElementById("results-status-text").style.color = passed ? "var(--accent-green)" : "var(--accent-red)";

    document.getElementById("results-exam-title").innerText = this.currentExamTitle;
    document.getElementById("results-score-num").innerText = scaledScore;
    document.getElementById("results-raw-pct").innerText = `${rawPct}%`;
    document.getElementById("results-correct-count").innerText = correctCount;
    document.getElementById("results-total-count").innerText = totalCount;

    // Domain breakdown
    const barsContainer = document.getElementById("results-domain-bars");
    barsContainer.innerHTML = "";
    const domainNames = {
      1: "Domain 1.0: General Security Concepts (12%)",
      2: "Domain 2.0: Threats, Vulnerabilities, & Mitigations (22%)",
      3: "Domain 3.0: Security Architecture (18%)",
      4: "Domain 4.0: Security Operations (28%)",
      5: "Domain 5.0: Program Management & Oversight (20%)"
    };

    for (let d = 1; d <= 5; d++) {
      const data = domainScores[d];
      const dpct = data.t > 0 ? Math.round((data.c / data.t) * 100) : 0;

      const row = document.createElement("div");
      row.className = "domain-result-row";
      row.innerHTML = `
        <div class="dr-top">
          <span>${domainNames[d]}</span>
          <span style="color: ${dpct >= 83 ? 'var(--accent-green)' : 'var(--accent-red)'}">${dpct}% (${data.c}/${data.t})</span>
        </div>
        <div class="dr-bar">
          <div class="dr-fill" style="width: ${dpct}%; background: ${dpct >= 83 ? 'var(--accent-green)' : 'var(--accent-red)'}"></div>
        </div>
      `;
      barsContainer.appendChild(row);
    }

    // Render Question Navigator Jump Grid
    const jumpGrid = document.getElementById("results-jump-grid");
    jumpGrid.innerHTML = "";
    gradedResults.forEach(item => {
      const btn = document.createElement("button");
      btn.className = `jump-btn ${item.isCorrect ? 'correct' : 'incorrect'}`;
      btn.innerHTML = `<span>Q${item.qIndex}</span>`;
      btn.title = `Question ${item.qIndex}: ${item.isCorrect ? 'Correct' : 'Incorrect'}`;
      btn.addEventListener("click", () => {
        const target = document.getElementById(`review-card-${item.qIndex}`);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
          target.style.boxShadow = "0 0 0 3px var(--accent-blue)";
          setTimeout(() => target.style.boxShadow = "", 1500);
        }
      });
      jumpGrid.appendChild(btn);
    });

    this.cachedGradedResults = gradedResults;
    this.filterResultsReview("all");
  }

  filterResultsReview(filter = "all") {
    if (!this.cachedGradedResults) return;

    document.querySelectorAll(".filter-pills .pill-btn").forEach(b => {
      b.classList.toggle("active", b.dataset.resfilter === filter);
    });

    const feed = document.getElementById("results-questions-feed");
    feed.innerHTML = "";

    let filtered = this.cachedGradedResults;
    if (filter === "incorrect") {
      filtered = this.cachedGradedResults.filter(i => !i.isCorrect);
    } else if (filter === "flagged") {
      filtered = this.cachedGradedResults.filter(i => i.isFlagged);
    } else if (filter.startsWith("d")) {
      const dNum = parseInt(filter.substring(1));
      filtered = this.cachedGradedResults.filter(i => i.question.domain === dNum);
    }

    document.getElementById("res-all-cnt").innerText = this.cachedGradedResults.length;
    document.getElementById("res-incorrect-cnt").innerText = this.cachedGradedResults.filter(i => !i.isCorrect).length;
    document.getElementById("res-flagged-cnt").innerText = this.cachedGradedResults.filter(i => i.isFlagged).length;

    filtered.forEach(item => {
      const q = item.question;
      const isPBQ = !!q.items;

      const card = document.createElement("div");
      card.id = `review-card-${item.qIndex}`;
      card.className = `result-card ${item.isCorrect ? 'correct' : 'incorrect'}`;

      let optionsHTML = "";

      if (isPBQ) {
        optionsHTML = `
          <div style="background: var(--bg-card); padding: 14px; border-radius: var(--radius-sm); margin: 12px 0;">
            <h5 style="margin-bottom: 8px; color: var(--accent-purple)">Performance-Based Question Results:</h5>
            ${q.items.map((it, idx) => {
              const uVal = item.userAnswer[idx] || "None selected";
              const isMatch = uVal === it.answer;
              return `
                <div style="margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid var(--border-subtle); font-size: 0.9rem">
                  <div><strong>Item ${idx + 1}:</strong> ${it.prompt}</div>
                  <div>Your Selection: <strong style="color: ${isMatch ? 'var(--accent-green)' : 'var(--accent-red)'}">${uVal}</strong></div>
                  <div>Correct Configuration: <strong style="color: var(--accent-green)">${it.answer}</strong></div>
                </div>
              `;
            }).join('')}
          </div>
        `;
      } else {
        // Full options display with user's selection and correct answer clearly highlighted
        const userSelectedLetters = Array.isArray(item.userAnswer) ? item.userAnswer : [item.userAnswer];
        const correctLetters = Array.isArray(q.correct) ? q.correct : [q.correct];

        optionsHTML = `
          <div class="rc-options-review-list">
            ${q.options.map(opt => {
              const isUserChoice = userSelectedLetters.includes(opt.letter);
              const isCorrectKey = correctLetters.includes(opt.letter);

              let itemClass = "rc-option-item";
              let badgeHTML = "";

              if (isUserChoice && isCorrectKey) {
                itemClass += " user-correct";
                badgeHTML = `<span class="rc-user-tag correct">✓ Your Choice (Correct)</span>`;
              } else if (isUserChoice && !isCorrectKey) {
                itemClass += " user-incorrect";
                badgeHTML = `<span class="rc-user-tag incorrect">✗ Your Choice (Incorrect)</span>`;
              } else if (isCorrectKey) {
                itemClass += " answer-key";
                badgeHTML = `<span class="rc-user-tag key">★ Correct Answer</span>`;
              }

              return `
                <div class="${itemClass}">
                  <div class="rc-option-badge-wrap">
                    <span class="rc-opt-letter">${opt.letter}</span>
                    ${badgeHTML}
                  </div>
                  <div class="rc-opt-text" style="font-size: 1rem; line-height: 1.5">${opt.text}</div>
                </div>
              `;
            }).join('')}
          </div>
        `;
      }

      card.innerHTML = `
        <div class="rc-header">
          <div class="rc-meta">
            <span class="rc-qnum">Question ${item.qIndex}</span>
            <span class="domain-badge d${q.domain || 1}">Domain ${q.domain || 1}.0</span>
            <span style="font-size: 0.8rem; color: var(--text-muted)">${q.source || ''}</span>
          </div>
          <span class="rc-status ${item.isCorrect ? 'correct' : 'incorrect'}">
            ${item.isCorrect ? '✓ Correct' : '✗ Incorrect'}
          </span>
        </div>

        <div class="rc-stem">
          ${this.formatStemHTML(q.stem || q.title)}
        </div>

        ${optionsHTML}

        <div class="rc-exp-container">
          <div class="rc-exp-title">Official In-Depth Explanation & Rationale:</div>
          <div class="rc-exp-body">${q.explanation}</div>
          <div class="rc-obj-link">Exam Blueprint Reference: <strong>${q.objective || `Domain ${q.domain}.0`}</strong></div>
        </div>
      `;

      feed.appendChild(card);
    });
  }

  retakeMissedFromResults() {
    this.drillMissedQuestions();
  }

  // --- DOMAIN STUDY GUIDES VIEWER ---
  selectDomainNotes(domainNum) {
    this.currentDomainNote = domainNum;
    document.querySelectorAll(".notes-domain-btn").forEach(b => {
      b.classList.toggle("active", parseInt(b.dataset.d) === domainNum);
    });

    const viewer = document.getElementById("notes-viewer-area");
    if (!viewer || !this.studyGuides) return;

    const data = this.studyGuides[domainNum.toString()];
    if (!data) {
      viewer.innerHTML = `<div style="text-align: center; padding: 40px;">Study guide loading...</div>`;
      return;
    }

    viewer.innerHTML = `
      <div class="notes-domain-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
          <span class="domain-badge d${data.domain}">${data.weight} Weight on Exam</span>
          <button class="primary-pill-btn" onclick="app.startDomainDrill(${data.domain})">⚡ Drill Domain ${data.domain} Questions</button>
        </div>
        <h2 class="ndb-title">${data.title}</h2>
        <p class="ndb-summary">${data.summary}</p>
      </div>

      <div class="notes-objective-accordion">
        ${data.objectives.map((obj, idx) => `
          <div class="note-obj-card ${idx === 0 ? 'open' : ''}" id="note-card-${obj.code.replace('.', '-')}">
            <div class="note-obj-header" onclick="this.parentElement.classList.toggle('open')">
              <div class="noh-left">
                <span class="noh-code">${obj.code}</span>
                <span class="noh-title">${obj.title}</span>
              </div>
              <span class="noh-toggle">▼</span>
            </div>
            <div class="note-obj-content">
              ${obj.sections.map(sec => {
                if (sec.type === "heading") {
                  return `<h4 class="note-subheading">${sec.text}</h4>`;
                } else if (sec.type === "bullets") {
                  return `
                    <ul class="note-bullets">
                      ${sec.items.map(it => `<li class="note-bullet-li">${it}</li>`).join('')}
                    </ul>
                  `;
                }
                return "";
              }).join('')}
              <div class="note-drill-action">
                <button class="secondary-pill-btn" onclick="app.startDomainDrill(${data.domain})">Practice ${obj.code} Questions →</button>
              </div>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  searchNotes(keyword) {
    keyword = keyword.toLowerCase().trim();
    if (!keyword) {
      this.selectDomainNotes(this.currentDomainNote);
      return;
    }

    const cards = document.querySelectorAll(".note-obj-card");
    cards.forEach(card => {
      const text = card.innerText.toLowerCase();
      if (text.includes(keyword)) {
        card.style.display = "block";
        card.classList.add("open");
      } else {
        card.style.display = "none";
      }
    });
  }

  // --- PBQ LABORATORY ---
  renderPBQLab() {
    const grid = document.getElementById("pbq-catalog-grid");
    if (!grid || !this.db || !this.db.pbqs) return;
    grid.innerHTML = "";

    this.db.pbqs.forEach(pbq => {
      const card = document.createElement("div");
      card.className = "pbq-lab-card";
      card.innerHTML = `
        <div class="pbq-lab-top">
          <span class="pbq-tag">PBQ #${pbq.id}</span>
          <span style="font-size: 0.8rem; color: var(--text-muted)">Domain ${pbq.domain}.0</span>
        </div>
        <h4 class="pbq-lab-title">${pbq.title}</h4>
        <p class="pbq-lab-desc">${pbq.scenario.substring(0, 120)}...</p>
        <button class="pbq-launch-btn">Practice This PBQ ▶</button>
      `;

      card.querySelector(".pbq-launch-btn").addEventListener("click", () => {
        this.questions = [pbq];
        this.currentExamId = `pbq_${pbq.id}`;
        this.currentExamTitle = pbq.title;
        this.currentIndex = 0;
        this.userAnswers = {};
        this.flagged.clear();
        this.timerSeconds = 15 * 60;
        this.isPaused = false;
        this.examMode = "study_drill";
        this.launchExamSession();
      });

      grid.appendChild(card);
    });
  }

  // --- ACRONYM BLITZ & TERM EXPLAINER SUITE ---
  applySavedAcronymState() {
    this.currentDeckMode = localStorage.getItem("secplus_acro_deck_mode") || "learning";
    this.currentAcronymDomainFilter = localStorage.getItem("secplus_acro_domain_filter") || "all";

    // Set active deck button
    document.querySelectorAll(".deck-tab-btn").forEach(b => {
      b.classList.toggle("active", b.id === `deck-tab-${this.currentDeckMode}`);
    });

    // Set active domain filter pill
    document.querySelectorAll(".acro-filter-pill").forEach(p => {
      p.classList.toggle("active", p.dataset.acroDom === this.currentAcronymDomainFilter.toString());
    });

    this.updateAcronymDeckList();

    // Restore saved card term if available
    const savedTerm = localStorage.getItem("secplus_acro_resume_term");
    if (savedTerm && this.filteredAcronyms.length > 0) {
      const foundIdx = this.filteredAcronyms.findIndex(a => a.acronym === savedTerm);
      this.currentAcronymIndex = foundIdx !== -1 ? foundIdx : 0;
    } else {
      this.currentAcronymIndex = 0;
    }
  }

  setAcronymDeck(mode) {
    this.currentDeckMode = mode;
    localStorage.setItem("secplus_acro_deck_mode", mode);

    document.querySelectorAll(".deck-tab-btn").forEach(b => {
      b.classList.toggle("active", b.id === `deck-tab-${mode}`);
    });

    this.updateAcronymDeckList();
    this.currentAcronymIndex = 0;
    this.renderAcronymFlashcard();

    if (!document.getElementById("acro-table-view").classList.contains("hidden")) {
      this.renderAcronymTable();
    }
  }

  updateAcronymDeckList() {
    if (!this.acronyms || this.acronyms.length === 0) return;

    // Base deck filter
    let baseList = [];
    if (this.currentDeckMode === "learning") {
      baseList = this.acronyms.filter(a => !this.acronymsMastered.has(a.acronym));
    } else if (this.currentDeckMode === "mastered") {
      baseList = this.acronyms.filter(a => this.acronymsMastered.has(a.acronym));
    } else {
      baseList = [...this.acronyms];
    }

    // Domain filter
    if (this.currentAcronymDomainFilter === "all") {
      this.filteredAcronyms = baseList;
    } else {
      const dNum = parseInt(this.currentAcronymDomainFilter);
      this.filteredAcronyms = baseList.filter(a => a.domain === dNum);
    }

    // Update Deck Pill Counts
    const unmasteredTotal = this.acronyms.filter(a => !this.acronymsMastered.has(a.acronym)).length;
    const masteredTotal = this.acronymsMastered.size;
    const allTotal = this.acronyms.length;

    const learnCountEl = document.getElementById("learning-deck-count");
    if (learnCountEl) learnCountEl.innerText = unmasteredTotal;

    const masterCountEl = document.getElementById("mastered-deck-count");
    if (masterCountEl) masterCountEl.innerText = masteredTotal;

    const allCountEl = document.getElementById("all-deck-count");
    if (allCountEl) allCountEl.innerText = allTotal;
  }

  setAcronymMode(mode) {
    document.querySelectorAll(".mode-toggle-group .pill-btn").forEach(b => b.classList.remove("active"));
    const activeBtn = document.getElementById(`acro-${mode}-mode-btn`);
    if (activeBtn) activeBtn.classList.add("active");

    document.getElementById("acro-flashcard-view").classList.toggle("hidden", mode !== "flashcard");
    document.getElementById("acro-quiz-view").classList.toggle("hidden", mode !== "quiz");
    document.getElementById("acro-table-view").classList.toggle("hidden", mode !== "table");

    if (mode === "flashcard") {
      this.renderAcronymFlashcard();
    } else if (mode === "quiz") {
      this.startAcronymQuiz();
    } else if (mode === "table") {
      this.renderAcronymTable();
    }
  }

  filterAcronymsByDomain(domain) {
    this.currentAcronymDomainFilter = domain;
    localStorage.setItem("secplus_acro_domain_filter", domain);

    document.querySelectorAll(".acro-filter-pill").forEach(p => {
      p.classList.toggle("active", p.dataset.acroDom === domain.toString());
    });

    this.updateAcronymDeckList();
    this.currentAcronymIndex = 0;
    this.renderAcronymFlashcard();

    if (!document.getElementById("acro-table-view").classList.contains("hidden")) {
      this.renderAcronymTable();
    }
  }

  renderAcronymFlashcard() {
    const list = this.filteredAcronyms;
    const mainCard = document.getElementById("main-flashcard");
    const controls = document.querySelector(".flashcard-controls");
    const emptyState = document.getElementById("fc-empty-state");
    const counterText = document.getElementById("fc-counter-text");
    const progressFill = document.getElementById("fc-progress-fill");
    const statusBadge = document.getElementById("fc-deck-status");
    const resumeText = document.getElementById("acro-resume-text");

    if (statusBadge) {
      statusBadge.innerText = `${this.acronymsMastered.size} Mastered`;
    }

    // Handle Empty Decks (e.g. all mastered, or 0 mastered cards)
    if (!list || list.length === 0) {
      if (mainCard) mainCard.classList.add("hidden");
      if (controls) controls.classList.add("hidden");
      if (emptyState) {
        emptyState.classList.remove("hidden");
        const titleEl = document.getElementById("fc-empty-title");
        const descEl = document.getElementById("fc-empty-desc");
        const iconEl = document.getElementById("fc-empty-icon");
        const actionsEl = document.getElementById("fc-empty-actions");

        if (this.currentDeckMode === "learning") {
          if (iconEl) iconEl.innerText = "🏆";
          if (titleEl) titleEl.innerText = "All Active Cards Mastered!";
          if (descEl) descEl.innerText = "Incredible work! You have marked all acronyms in this selection as mastered. Review them in the Mastered Deck or reset to practice again.";
          if (actionsEl) {
            actionsEl.innerHTML = `
              <button class="btn-primary-action" onclick="app.setAcronymDeck('mastered')">Review Mastered Deck</button>
              <button class="btn-secondary-action" onclick="app.resetCurrentDeckMastery()">Reset Mastery for this Deck</button>
            `;
          }
        } else if (this.currentDeckMode === "mastered") {
          if (iconEl) iconEl.innerText = "🎯";
          if (titleEl) titleEl.innerText = "No Mastered Cards Yet";
          if (descEl) descEl.innerText = "Cards you mark as mastered in the Learning Deck will be placed here for later revision.";
          if (actionsEl) {
            actionsEl.innerHTML = `
              <button class="btn-primary-action" onclick="app.setAcronymDeck('learning')">Go to Learning Deck</button>
            `;
          }
        } else {
          if (iconEl) iconEl.innerText = "🔍";
          if (titleEl) titleEl.innerText = "No Acronyms Found";
          if (descEl) descEl.innerText = "No acronyms match the active domain filter.";
          if (actionsEl) {
            actionsEl.innerHTML = `
              <button class="btn-primary-action" onclick="app.filterAcronymsByDomain('all')">Show All Domains</button>
            `;
          }
        }
      }

      if (counterText) counterText.innerText = `0 Cards`;
      if (progressFill) progressFill.style.width = this.currentDeckMode === 'learning' ? '100%' : '0%';
      if (resumeText) resumeText.innerText = "Deck Complete";
      return;
    }

    // Active cards available
    if (mainCard) mainCard.classList.remove("hidden");
    if (controls) controls.classList.remove("hidden");
    if (emptyState) emptyState.classList.add("hidden");

    if (this.currentAcronymIndex >= list.length) {
      this.currentAcronymIndex = 0;
    }

    const item = list[this.currentAcronymIndex];
    if (!item) return;

    // FRONT OF CARD
    const frontTerm = document.getElementById("card-acro-term");
    if (frontTerm) frontTerm.innerText = item.acronym;

    const frontDomain = document.getElementById("card-acro-domain");
    if (frontDomain) frontDomain.innerText = `Domain ${item.domain || 1}.0`;

    const frontCat = document.getElementById("card-acro-category");
    if (frontCat) frontCat.innerText = item.category || "General Security";

    // BACK OF CARD
    const backTerm = document.getElementById("card-acro-back-term");
    if (backTerm) backTerm.innerText = item.acronym;

    const backDomain = document.getElementById("card-acro-back-domain");
    if (backDomain) backDomain.innerText = `Domain ${item.domain || 1}.0`;

    const backCat = document.getElementById("card-acro-back-category");
    if (backCat) backCat.innerText = item.category || "General Security";

    const backDef = document.getElementById("card-acro-def");
    if (backDef) backDef.innerText = item.expansion || item.definition;

    const backExp = document.getElementById("card-acro-explanation");
    if (backExp) {
      backExp.innerText = item.explanation || `The standard abbreviation for ${item.expansion || item.definition} in the CompTIA Security+ blueprint.`;
    }

    const backCue = document.getElementById("card-acro-exam-tip");
    if (backCue) {
      backCue.innerText = item.exam_tip || `Recognize ${item.acronym} under Domain ${item.domain || 1}.0 objectives.`;
    }

    // COUNTER & PROGRESS
    if (counterText) {
      counterText.innerText = `Card ${this.currentAcronymIndex + 1} of ${list.length}`;
    }

    const pct = Math.round(((this.currentAcronymIndex + 1) / list.length) * 100);
    if (progressFill) progressFill.style.width = `${pct}%`;

    // RESUME NOTIFICATION / TRACKING
    localStorage.setItem("secplus_acro_resume_term", item.acronym);
    if (resumeText) {
      const modeLabel = this.currentDeckMode === 'learning' ? 'Learning' : (this.currentDeckMode === 'mastered' ? 'Mastered' : 'All');
      resumeText.innerText = `Resumed at Card ${this.currentAcronymIndex + 1}: ${item.acronym} (${modeLabel})`;
    }

    // MASTERED / UNMASTER BUTTON STATE
    const isMastered = this.acronymsMastered.has(item.acronym);
    const masterBtn = document.getElementById("fc-master-btn");
    const masterText = document.getElementById("fc-master-btn-text");

    if (masterBtn && masterText) {
      masterBtn.classList.remove("is-mastered", "unmaster");
      if (this.currentDeckMode === "mastered") {
        masterBtn.classList.add("unmaster");
        masterText.innerText = "Unmaster (Move to Learning)";
      } else if (this.currentDeckMode === "learning") {
        masterText.innerText = "Mark Mastered";
      } else {
        masterBtn.classList.toggle("is-mastered", isMastered);
        masterText.innerText = isMastered ? "Mastered ✓ (Click to Unmaster)" : "Mark Mastered";
      }
    }

    // Unflip card
    if (mainCard) mainCard.classList.remove("flipped");
  }

  flipFlashcard() {
    const cardEl = document.getElementById("main-flashcard");
    if (cardEl) cardEl.classList.toggle("flipped");
  }

  nextFlashcard() {
    const list = this.filteredAcronyms;
    if (!list || list.length === 0) return;
    if (this.currentAcronymIndex < list.length - 1) {
      this.currentAcronymIndex++;
    } else {
      this.currentAcronymIndex = 0; // Loop back
    }
    this.renderAcronymFlashcard();
  }

  prevFlashcard() {
    const list = this.filteredAcronyms;
    if (!list || list.length === 0) return;
    if (this.currentAcronymIndex > 0) {
      this.currentAcronymIndex--;
    } else {
      this.currentAcronymIndex = list.length - 1; // Loop back
    }
    this.renderAcronymFlashcard();
  }

  toggleAcronymMastered() {
    const list = this.filteredAcronyms;
    if (!list || list.length === 0) return;

    const item = list[this.currentAcronymIndex];
    if (!item) return;

    const wasMastered = this.acronymsMastered.has(item.acronym);
    if (wasMastered) {
      this.acronymsMastered.delete(item.acronym);
    } else {
      this.acronymsMastered.add(item.acronym);
    }

    localStorage.setItem("secplus_acro_mastered", JSON.stringify([...this.acronymsMastered]));

    // Update deck list because membership changed
    this.updateAcronymDeckList();

    if (this.currentDeckMode === "learning" || this.currentDeckMode === "mastered") {
      // The card has been moved out of this active deck!
      if (this.currentAcronymIndex >= this.filteredAcronyms.length) {
        this.currentAcronymIndex = Math.max(0, this.filteredAcronyms.length - 1);
      }
      this.renderAcronymFlashcard();
    } else {
      // All cards deck: stay or advance
      this.nextFlashcard();
    }
  }

  resetCurrentDeckMastery() {
    if (!confirm("Are you sure you want to reset mastery for these acronyms? They will all return to your Learning Deck.")) return;

    if (this.currentAcronymDomainFilter === "all") {
      this.acronymsMastered.clear();
    } else {
      const dNum = parseInt(this.currentAcronymDomainFilter);
      this.acronyms.filter(a => a.domain === dNum).forEach(a => {
        this.acronymsMastered.delete(a.acronym);
      });
    }

    localStorage.setItem("secplus_acro_mastered", JSON.stringify([...this.acronymsMastered]));
    this.updateAcronymDeckList();
    this.currentAcronymIndex = 0;
    this.renderAcronymFlashcard();
  }

  startAcronymQuiz() {
    this.acroQuizScore = { correct: 0, total: 0 };
    this.nextAcronymQuizQuestion();
  }

  nextAcronymQuizQuestion() {
    const pool = this.filteredAcronyms.length >= 4 ? this.filteredAcronyms : this.acronyms;
    if (!pool || pool.length === 0) return;

    const target = pool[Math.floor(Math.random() * pool.length)];
    const targetDef = target.expansion || target.definition;

    const distractors = this.acronyms
      .filter(a => a.acronym !== target.acronym)
      .sort(() => 0.5 - Math.random())
      .slice(0, 3)
      .map(a => a.expansion || a.definition);

    const choices = [targetDef, ...distractors].sort(() => 0.5 - Math.random());
    this.acroQuizCurrent = { target, choices, correct: targetDef };

    document.getElementById("acro-quiz-score").innerText = `Score: ${this.acroQuizScore.correct} / ${this.acroQuizScore.total}`;
    document.getElementById("acro-quiz-term").innerHTML = `What is the official term for <strong style="color:var(--accent-blue)">${target.acronym}</strong>?`;

    const container = document.getElementById("acro-quiz-options-container");
    container.innerHTML = "";
    document.getElementById("acro-quiz-feedback").classList.add("hidden");
    document.getElementById("acro-quiz-next-btn").classList.add("hidden");

    choices.forEach(c => {
      const btn = document.createElement("button");
      btn.className = "option-item";
      btn.style.width = "100%";
      btn.style.cursor = "pointer";
      btn.innerHTML = `<span style="font-weight: 600">${c}</span>`;
      btn.addEventListener("click", () => {
        this.checkAcronymQuizChoice(c, targetDef, btn, target);
      });
      container.appendChild(btn);
    });
  }

  checkAcronymQuizChoice(selected, correct, clickedBtn, target) {
    const isCorrect = selected === correct;
    this.acroQuizScore.total++;
    if (isCorrect) this.acroQuizScore.correct++;

    document.getElementById("acro-quiz-score").innerText = `Score: ${this.acroQuizScore.correct} / ${this.acroQuizScore.total}`;

    document.querySelectorAll("#acro-quiz-options-container .option-item").forEach(b => {
      b.disabled = true;
      if (b.innerText.trim() === correct) {
        b.style.borderColor = "var(--accent-green)";
        b.style.backgroundColor = "rgba(16, 185, 129, 0.15)";
      } else if (b === clickedBtn && !isCorrect) {
        b.style.borderColor = "var(--accent-red)";
        b.style.backgroundColor = "rgba(239, 68, 68, 0.15)";
      }
    });

    const fb = document.getElementById("acro-quiz-feedback");
    fb.className = `quiz-feedback-box ${isCorrect ? 'correct' : 'incorrect'}`;
    const expText = target.explanation ? `<br><small style="margin-top:6px; display:block; font-weight:normal; color:var(--text-secondary)">💡 ${target.explanation}</small>` : '';
    fb.innerHTML = isCorrect
      ? `<strong>✓ Correct!</strong> ${target.acronym} = ${correct}${expText}`
      : `<strong>✗ Incorrect!</strong> ${target.acronym} = <strong>${correct}</strong>${expText}`;
    fb.classList.remove("hidden");

    document.getElementById("acro-quiz-next-btn").classList.remove("hidden");
  }

  renderAcronymTable(query = "") {
    const tbody = document.getElementById("acronym-table-body");
    if (!tbody || !this.acronyms) return;
    tbody.innerHTML = "";

    const q = query.toLowerCase().trim();
    let pool = this.filteredAcronyms.length > 0 && this.currentAcronymDomainFilter !== "all"
      ? this.filteredAcronyms
      : this.acronyms;

    let filtered = pool;
    if (q) {
      filtered = pool.filter(a =>
        a.acronym.toLowerCase().includes(q) ||
        (a.expansion && a.expansion.toLowerCase().includes(q)) ||
        (a.definition && a.definition.toLowerCase().includes(q)) ||
        (a.explanation && a.explanation.toLowerCase().includes(q)) ||
        (a.exam_tip && a.exam_tip.toLowerCase().includes(q))
      );
    }

    filtered.forEach(a => {
      const tr = document.createElement("tr");
      const isMastered = this.acronymsMastered.has(a.acronym);
      tr.innerHTML = `
        <td class="acro-col-term">${a.acronym} ${isMastered ? '<span style="color:#10b981" title="Mastered">✓</span>' : ''}</td>
        <td class="acro-col-name">${a.expansion || a.definition}</td>
        <td>
          <span class="domain-badge d${a.domain || 1}">D${a.domain || 1}.0</span>
          <div style="font-size:0.7rem; color:var(--text-muted); margin-top:4px">${a.category || 'General'}</div>
        </td>
        <td class="acro-col-desc">${a.explanation || ''}</td>
        <td><div class="acro-col-cue">${a.exam_tip || ''}</div></td>
      `;
      tbody.appendChild(tr);
    });
  }

  searchAcronyms(query) {
    if (!document.getElementById("acro-table-view").classList.contains("hidden")) {
      this.renderAcronymTable(query);
    } else {
      const q = query.toLowerCase().trim();
      if (!q) return;
      const pool = this.filteredAcronyms.length > 0 ? this.filteredAcronyms : this.acronyms;
      const idx = pool.findIndex(a =>
        a.acronym.toLowerCase().includes(q) ||
        (a.expansion && a.expansion.toLowerCase().includes(q)) ||
        (a.definition && a.definition.toLowerCase().includes(q))
      );
      if (idx !== -1) {
        this.currentAcronymIndex = idx;
        this.renderAcronymFlashcard();
      }
    }
  }

  // --- CHEAT SHEETS ---
  showCheatTab(tabKey) {
    document.querySelectorAll(".cs-tab-btn").forEach(b => b.classList.remove("active"));
    const activeBtn = Array.from(document.querySelectorAll(".cs-tab-btn")).find(b => b.getAttribute("onclick")?.includes(tabKey));
    if (activeBtn) activeBtn.classList.add("active");

    const area = document.getElementById("cheat-content-area");
    if (!this.db || !this.db.cheatsheet) return;

    if (tabKey === "ports") {
      const ports = this.db.cheatsheet.ports || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">Core Security+ Ports & Protocols (TCP/UDP)</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">Essential for network firewall rules, PBQs, and traffic triage</span>
        </div>
        <table class="styled-table">
          <thead>
            <tr><th style="width:14%">Port</th><th style="width:20%">Protocol</th><th>Description & Security Context</th></tr>
          </thead>
          <tbody>
            ${ports.map(p => `
              <tr>
                <td style="font-family: var(--font-mono); font-weight: 700; color: var(--accent-cyan)">${p.port}</td>
                <td><strong>${p.proto}</strong></td>
                <td>${p.desc}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    } else if (tabKey === "crypto") {
      const crypto = this.db.cheatsheet.crypto || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">High-Yield Cryptography & Ciphers</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">Symmetric vs Asymmetric, Hashing, Key Stretching & Quantum-Resistant</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 14px">
          ${crypto.map(c => `
            <div style="background: var(--bg-card); padding: 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-color)">
              <h4 style="color: var(--accent-blue); margin-bottom: 6px">${c.term}</h4>
              <p style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6">${c.details}</p>
            </div>
          `).join('')}
        </div>
      `;
    } else if (tabKey === "volatility") {
      const vol = this.db.cheatsheet.volatility || [];
      const principles = this.db.cheatsheet.forensics_principles || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">RFC 3227 Order of Volatility & Digital Forensics</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">Must be collected in order from most volatile to least volatile</span>
        </div>

        <table class="styled-table" style="margin-bottom: 24px">
          <thead>
            <tr>
              <th style="width: 14%">Volatility Rank</th>
              <th style="width: 32%">Evidence Target</th>
              <th style="width: 18%">Typical Lifespan</th>
              <th>Forensic Acquisition Context</th>
            </tr>
          </thead>
          <tbody>
            ${vol.map((v, i) => `
              <tr>
                <td>
                  <span class="cs-rank-pill ${i === 0 ? 'high' : (i <= 2 ? 'med' : 'low')}">${v.rank}</span>
                </td>
                <td style="font-weight: 700; color: var(--text-primary)">${v.target}</td>
                <td style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary)">${v.lifespan}</td>
                <td style="font-size: 0.88rem; color: var(--text-secondary)">${v.context}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <h4 style="margin: 20px 0 12px; color: var(--text-primary)">Core Digital Forensics Principles & Standards</h4>
        <div class="cs-card-grid">
          ${principles.map(p => `
            <div class="cs-feature-card">
              <div class="cs-card-header">
                <h5 class="cs-card-title">${p.concept}</h5>
                <span class="cs-tag">${p.rule}</span>
              </div>
              <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.55; margin: 0">${p.details}</p>
            </div>
          `).join('')}
        </div>
      `;
    } else if (tabKey === "attacks") {
      const attacks = this.db.cheatsheet.attacks || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">Network & Application Attacks, Indicators & Mitigations</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">Common attack vectors, diagnostic signs, and primary defensive controls</span>
        </div>

        <div class="cs-card-grid">
          ${attacks.map(a => `
            <div class="cs-feature-card">
              <div class="cs-card-header">
                <h5 class="cs-card-title">${a.attack}</h5>
                <span class="cs-tag">${a.vector}</span>
              </div>
              <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; margin: 0">${a.mechanism}</p>
              
              <div class="cs-row-label">Key Indicators / Log Evidence:</div>
              <div class="cs-indicator-box">${a.indicators}</div>

              <div class="cs-row-label">Primary Exam Mitigation:</div>
              <div class="cs-mitigation-box">${a.mitigation}</div>
            </div>
          `).join('')}
        </div>
      `;
    } else if (tabKey === "iam") {
      const iam = this.db.cheatsheet.iam || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">Authentication, IAM & Federation Standards</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">RADIUS vs TACACS+, Kerberos, SAML, OAuth 2.0, OIDC, SCIM, and Access Control Models</span>
        </div>

        <div style="display: flex; flex-direction: column; gap: 14px">
          ${iam.map(item => `
            <div style="background: var(--bg-card); padding: 18px; border-radius: var(--radius-sm); border: 1px solid var(--border-color)">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
                <h4 style="color: var(--accent-blue); margin: 0">${item.protocol}</h4>
                <span class="cs-tag">${item.category}</span>
              </div>
              <p style="font-size: 0.92rem; color: var(--text-secondary); line-height: 1.6; margin: 0">${item.summary}</p>
            </div>
          `).join('')}
        </div>
      `;
    } else if (tabKey === "cloud") {
      const cloud = this.db.cheatsheet.cloud || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">Cloud Architecture, SASE & Zero Trust Principles</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">Shared Responsibility, CASB, SASE, NIST SP 800-207 Zero Trust, and Cloud Storage</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px">
          ${cloud.map(c => `
            <div style="background: var(--bg-card); padding: 18px; border-radius: var(--radius-sm); border: 1px solid var(--border-color); display: flex; flex-direction: column; gap: 8px">
              <h4 style="color: var(--accent-cyan); margin: 0">${c.pillar}</h4>
              <p style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin: 0">${c.details}</p>
            </div>
          `).join('')}
        </div>
      `;
    } else if (tabKey === "compliance") {
      const compliance = this.db.cheatsheet.compliance || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">Governance, Regulatory Compliance & Security Frameworks</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">GDPR, HIPAA, PCI-DSS, SOX, NIST CSF 2.0, NIST SP 800-53, ISO 27001/2, SOC 2, and CIS Controls</span>
        </div>

        <table class="styled-table">
          <thead>
            <tr>
              <th style="width: 24%">Standard / Regulation</th>
              <th style="width: 22%">Applicability & Scope</th>
              <th>Core Mandates & Security Requirements</th>
            </tr>
          </thead>
          <tbody>
            ${compliance.map(c => `
              <tr>
                <td style="font-weight: 700; color: var(--accent-purple)">${c.standard}</td>
                <td><span class="cs-tag" style="background:rgba(168, 85, 247, 0.1); color:var(--accent-purple); border-color:rgba(168,85,247,0.3)">${c.scope}</span></td>
                <td style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.55">${c.mandates}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    } else if (tabKey === "resilience") {
      const raid = this.db.cheatsheet.resilience || [];
      const dr = this.db.cheatsheet.dr_metrics || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">RAID Configurations, High Availability & Disaster Recovery Metrics</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">Fault tolerance levels, RTO, RPO, MTBF, MTTR, and recovery site tiers</span>
        </div>

        <table class="styled-table" style="margin-bottom: 24px">
          <thead>
            <tr>
              <th style="width: 16%">RAID Level</th>
              <th style="width: 12%">Min Disks</th>
              <th style="width: 18%">Fault Tolerance</th>
              <th style="width: 14%">Usable Cap.</th>
              <th>Optimal Exam Use Case</th>
            </tr>
          </thead>
          <tbody>
            ${raid.map(r => `
              <tr>
                <td style="font-weight: 700; font-family: var(--font-mono); color: var(--accent-green)">${r.level}</td>
                <td>${r.min_disks}</td>
                <td><span class="cs-tag" style="background:rgba(16, 185, 129, 0.1); color:#059669; border-color:rgba(16,185,129,0.3)">${r.fault_tolerance}</span></td>
                <td style="font-family: var(--font-mono); font-weight: 600">${r.usable_capacity}</td>
                <td style="font-size: 0.88rem; color: var(--text-secondary)">${r.best_use}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <h4 style="margin: 20px 0 12px; color: var(--text-primary)">Disaster Recovery & Continuity Metrics</h4>
        <div class="cs-card-grid">
          ${dr.map(d => `
            <div class="cs-feature-card">
              <h5 class="cs-card-title" style="color: var(--accent-blue)">${d.metric}</h5>
              <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.55; margin: 0">${d.definition}</p>
            </div>
          `).join('')}
        </div>
      `;
    } else if (tabKey === "ir") {
      const ir = this.db.cheatsheet.incident_response || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">NIST / CompTIA Incident Response Lifecycle (PICERL)</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px">
          ${ir.map(step => `
            <div style="background: var(--bg-card); padding: 16px; border-radius: var(--radius-sm); border-left: 4px solid var(--accent-purple)">
              <h4 style="margin-bottom: 4px">${step.phase}</h4>
              <p style="color: var(--text-secondary); font-size: 0.9rem">${step.focus}</p>
            </div>
          `).join('')}
        </div>
      `;
    } else if (tabKey === "risk") {
      const formulas = this.db.cheatsheet.risk_formulas || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">Quantitative Risk Management Formulas</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">ALE, SLE, ARO, MTBF, MTTR calculations</span>
        </div>
        <table class="styled-table">
          <thead>
            <tr><th>Formula / Acronym</th><th>Concept</th><th>Definition</th></tr>
          </thead>
          <tbody>
            ${formulas.map(f => `
              <tr>
                <td style="font-family: var(--font-mono); font-weight: 700; color: var(--accent-green)">${f.formula}</td>
                <td><strong>${f.name}</strong></td>
                <td>${f.desc}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    } else if (tabKey === "controls") {
      const controls = this.db.cheatsheet.security_controls || [];
      area.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px">
          <h3 style="margin:0">CompTIA Security Control Categories & Types</h3>
          <span style="font-size:0.8rem; color:var(--text-muted)">Technical, Managerial, Operational, Physical & Functional Controls</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px">
          ${controls.map(c => `
            <div style="background: var(--bg-card); padding: 18px; border-radius: var(--radius-sm); border: 1px solid var(--border-color)">
              <h4 style="color: var(--accent-amber); margin-bottom: 8px">${c.category} Controls</h4>
              <p style="font-size: 0.9rem; color: var(--text-secondary)">${c.desc}</p>
            </div>
          `).join('')}
        </div>
      `;
    }
  }

  // --- MISSED QUESTIONS REPOSITORY ---
  renderMissedBank() {
    const list = document.getElementById("missed-questions-list");
    if (!list) return;
    list.innerHTML = "";

    const missedIds = Object.keys(this.missedQuestions);
    document.getElementById("missed-total-count").innerText = missedIds.length;
    document.getElementById("missed-count-badge").innerText = missedIds.length;

    if (missedIds.length === 0) {
      list.innerHTML = `
        <div style="text-align: center; padding: 48px; color: var(--text-muted); background: var(--bg-secondary); border-radius: var(--radius-md)">
          🎉 <strong>Missed Bank is completely clear!</strong><br>
          Any questions you answer incorrectly during mock exams or drills appear here for targeted practice.
        </div>
      `;
      return;
    }

    missedIds.forEach((id, idx) => {
      const item = this.missedQuestions[id];
      const card = document.createElement("div");
      card.className = "result-card incorrect";
      card.innerHTML = `
        <div class="rc-header">
          <span class="rc-qnum">Missed Item #${idx + 1} (${item.source || 'Drill'})</span>
          <span class="domain-badge d${item.domain || 1}">Domain ${item.domain || 1}.0</span>
        </div>
        <div class="rc-stem">${this.formatStemHTML(item.stem)}</div>
        <div class="rc-exp-container">
          <div class="rc-exp-title">Key Explanation:</div>
          <div class="rc-exp-body">${item.explanation}</div>
        </div>
      `;
      list.appendChild(card);
    });
  }

  clearMissedQuestions() {
    if (confirm("Are you sure you want to clear your missed questions repository?")) {
      this.missedQuestions = {};
      this.saveMissedQuestions();
      this.renderMissedBank();
    }
  }
}

// Global instance
let app;
window.addEventListener("DOMContentLoaded", () => {
  app = new SecPlusSimulator();
});
