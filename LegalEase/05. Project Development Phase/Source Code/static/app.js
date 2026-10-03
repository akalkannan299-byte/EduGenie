// --- EduGenie Application Logic ---

// State Management
const state = {
  currentTab: 'tab-learn',
  currentTask: 'qa',
  lastResponseText: '',
  lastHistoryId: null,
  activeQuizData: null,
  activeQuizTopic: '',
  selectedQuizAnswers: {},
  isRecording: false,
  recognition: null,
};

// DOM Elements
const elements = {
  // Navigation
  navButtons: document.querySelectorAll('.nav-btn'),
  tabPanes: document.querySelectorAll('.tab-pane'),

  // Learning Hub
  taskPills: document.querySelectorAll('.task-pill'),
  levelContainer: document.getElementById('levelSelectorContainer'),
  learnerLevel: document.getElementById('learnerLevel'),
  hubInput: document.getElementById('hubInput'),
  hubInputLabel: document.getElementById('hubInputLabel'),
  charCount: document.getElementById('charCount'),
  quickChips: document.getElementById('quickChips'),
  voiceBtn: document.getElementById('voiceBtn'),
  clearInputBtn: document.getElementById('clearInputBtn'),
  generateBtn: document.getElementById('generateBtn'),
  generateBtnText: document.getElementById('generateBtnText'),
  responseStatus: document.getElementById('responseStatus'),
  responseContainer: document.getElementById('responseContainer'),
  speakBtn: document.getElementById('speakBtn'),
  copyBtn: document.getElementById('copyBtn'),
  bookmarkBtn: document.getElementById('bookmarkBtn'),
  saveNoteBtn: document.getElementById('saveNoteBtn'),

  // Quiz Arena
  quizTopicInput: document.getElementById('quizTopicInput'),
  startQuizBtn: document.getElementById('startQuizBtn'),
  quizStageContainer: document.getElementById('quizStageContainer'),
  quizControls: document.getElementById('quizControls'),
  submitQuizBtn: document.getElementById('submitQuizBtn'),
  quizTimer: document.getElementById('quizTimer'),
  timerCount: document.getElementById('timerCount'),
  quizHistoryContainer: document.getElementById('quizHistoryContainer'),
  refreshQuizHistoryBtn: document.getElementById('refreshQuizHistoryBtn'),

  // Learning Paths
  pathTopicInput: document.getElementById('pathTopicInput'),
  pathLevelSelect: document.getElementById('pathLevelSelect'),
  buildPathBtn: document.getElementById('buildPathBtn'),
  pathResultContainer: document.getElementById('pathResultContainer'),
  savePathNoteBtn: document.getElementById('savePathNoteBtn'),
  copyPathBtn: document.getElementById('copyPathBtn'),

  // Notes & History
  subTabButtons: document.querySelectorAll('.sub-tab-btn'),
  subviews: document.querySelectorAll('.subview'),
  historySearchInput: document.getElementById('historySearchInput'),
  filterChips: document.querySelectorAll('.filter-chip'),
  historyListContainer: document.getElementById('historyListContainer'),
  bookmarksListContainer: document.getElementById('bookmarksListContainer'),
  notesListContainer: document.getElementById('notesListContainer'),
  clearHistoryBtn: document.getElementById('clearHistoryBtn'),
  newNoteModalBtn: document.getElementById('newNoteModalBtn'),

  // Note Modal
  noteModal: document.getElementById('noteModal'),
  closeNoteModalBtn: document.getElementById('closeNoteModalBtn'),
  cancelNoteBtn: document.getElementById('cancelNoteBtn'),
  saveNewNoteSubmitBtn: document.getElementById('saveNewNoteSubmitBtn'),
  modalNoteTitle: document.getElementById('modalNoteTitle'),
  modalNoteCategory: document.getElementById('modalNoteCategory'),
  modalNoteContent: document.getElementById('modalNoteContent'),

  // Analytics
  statQueries: document.getElementById('statQueries'),
  statQuizzes: document.getElementById('statQuizzes'),
  statScore: document.getElementById('statScore'),
  statNotes: document.getElementById('statNotes'),
  taskBreakdownBars: document.getElementById('taskBreakdownBars'),
  refreshStatsBtn: document.getElementById('refreshStatsBtn'),

  // Status & Toasts
  aiStatusBadge: document.getElementById('aiStatusBadge'),
  aiStatusText: document.getElementById('aiStatusText'),
  toastContainer: document.getElementById('toastContainer'),
};

// Suggestion Prompts Library
const PROMPT_SUGGESTIONS = {
  qa: [
    "What is the difference between TCP and UDP?",
    "Explain how public-key cryptography works.",
    "What is Big-O notation and why is it important?",
    "How does the browser rendering engine work?",
    "What is the difference between SQL and NoSQL?"
  ],
  explain: [
    "TCP three-way handshake",
    "Gradient Descent in Machine Learning",
    "Object-Oriented Programming (OOP) Principles",
    "Binary Search Tree operations",
    "Docker containers vs Virtual Machines"
  ],
  summarize: [
    "Artificial intelligence is transforming education by enabling personalized learning paths, automated grading, intelligent tutoring, and rapid revision. Learners can study at their own pace while intelligent agents identify knowledge gaps and provide tailored exercises.",
    "Cloud computing provides on-demand computing services—including servers, storage, databases, networking, software, and analytics—over the internet with pay-as-you-go pricing, enabling organizations to scale rapidly while reducing infrastructure overhead."
  ]
};

// Helper: Escape HTML
function escapeHTML(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Built-in Markdown Formatter
function renderMarkdown(md) {
  if (!md) return '';
  let html = escapeHTML(md);

  // Code blocks ```code```
  html = html.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre><code class="lang-${lang}">${code.trim()}</code></pre>`;
  });

  // Inline code `code`
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Headings # ## ### ####
  html = html.replace(/^#### (.*?)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');

  // Bold & Italic
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // Blockquotes > quote
  html = html.replace(/^>\s*(.*?)$/gm, '<blockquote>$1</blockquote>');

  // Horizontal rules
  html = html.replace(/^---$/gm, '<hr>');

  // Unordered list items - item or * item
  html = html.replace(/^\s*[-*]\s+(.*?)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  // Numbered list items
  html = html.replace(/^\s*(\d+)\.\s+(.*?)$/gm, '<li><strong>$1.</strong> $2</li>');

  // Paragraphs
  const paragraphs = html.split(/\n\n+/);
  html = paragraphs.map(p => {
    p = p.trim();
    if (!p) return '';
    if (p.startsWith('<h') || p.startsWith('<pre') || p.startsWith('<ul>') || p.startsWith('<block') || p.startsWith('<hr')) {
      return p;
    }
    return `<p>${p.replace(/\n/g, '<br>')}</p>`;
  }).join('\n');

  return `<div class="markdown-content">${html}</div>`;
}

// Toast Notifications
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  elements.toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3500);
}

// --- Tab Switching ---
function switchTab(tabId) {
  state.currentTab = tabId;
  elements.navButtons.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabId);
  });
  elements.tabPanes.forEach(pane => {
    pane.classList.toggle('active', pane.id === tabId);
  });

  if (tabId === 'tab-quiz') {
    loadQuizHistory();
  } else if (tabId === 'tab-notes') {
    loadHistory();
  } else if (tabId === 'tab-analytics') {
    loadAnalytics();
  }
}

elements.navButtons.forEach(btn => {
  btn.addEventListener('click', () => switchTab(btn.dataset.tab));
});

// --- Learning Hub Interactions ---
function updateTaskView(task) {
  state.currentTask = task;

  // Update pills UI
  elements.taskPills.forEach(pill => {
    const radio = pill.querySelector('input');
    pill.classList.toggle('active', radio.value === task);
  });

  // Level selector visibility
  if (task === 'explain') {
    elements.levelContainer.classList.remove('hidden');
    elements.hubInputLabel.textContent = 'Topic or Concept to Explain';
    elements.hubInput.placeholder = 'Example: TCP three-way handshake, Gradient Descent, Recursion...';
  } else if (task === 'summarize') {
    elements.levelContainer.classList.add('hidden');
    elements.hubInputLabel.textContent = 'Educational Passage to Summarize';
    elements.hubInput.placeholder = 'Paste a long chapter, article, or lecture notes here...';
  } else {
    elements.levelContainer.classList.add('hidden');
    elements.hubInputLabel.textContent = 'Your Academic or Conceptual Question';
    elements.hubInput.placeholder = 'Example: What is the difference between TCP and UDP?';
  }

  // Populate suggestion chips
  renderSuggestionChips(task);
}

function renderSuggestionChips(task) {
  const suggestions = PROMPT_SUGGESTIONS[task] || [];
  elements.quickChips.innerHTML = suggestions.map(s => `
    <button type="button" class="chip-btn" data-text="${escapeHTML(s)}">${escapeHTML(s)}</button>
  `).join('');

  elements.quickChips.querySelectorAll('.chip-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      elements.hubInput.value = btn.dataset.text;
      updateCharCount();
      elements.hubInput.focus();
    });
  });
}

function updateCharCount() {
  const len = elements.hubInput.value.length;
  elements.charCount.textContent = `${len} character${len === 1 ? '' : 's'}`;
}

elements.hubInput.addEventListener('input', updateCharCount);

elements.taskPills.forEach(pill => {
  const radio = pill.querySelector('input');
  radio.addEventListener('change', () => updateTaskView(radio.value));
});

elements.clearInputBtn.addEventListener('click', () => {
  elements.hubInput.value = '';
  updateCharCount();
  elements.hubInput.focus();
});

// Quick suggestion chips for Quiz Arena and Learning Paths
document.querySelectorAll('[data-quiz-topic]').forEach(btn => {
  btn.addEventListener('click', () => {
    elements.quizTopicInput.value = btn.dataset.quizTopic;
    elements.quizTopicInput.focus();
  });
});

document.querySelectorAll('[data-path-topic]').forEach(btn => {
  btn.addEventListener('click', () => {
    elements.pathTopicInput.value = btn.dataset.pathTopic;
    elements.pathTopicInput.focus();
  });
});

// --- Speech-to-Text (Voice Recognition) ---
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  state.recognition = new SpeechRecognition();
  state.recognition.continuous = false;
  state.recognition.interimResults = false;

  state.recognition.onstart = () => {
    state.isRecording = true;
    elements.voiceBtn.classList.add('recording');
    showToast('Listening... Speak clearly.', 'info');
  };

  state.recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    elements.hubInput.value += (elements.hubInput.value ? ' ' : '') + transcript;
    updateCharCount();
  };

  state.recognition.onerror = () => {
    state.isRecording = false;
    elements.voiceBtn.classList.remove('recording');
  };

  state.recognition.onend = () => {
    state.isRecording = false;
    elements.voiceBtn.classList.remove('recording');
  };

  elements.voiceBtn.addEventListener('click', () => {
    if (state.isRecording) {
      state.recognition.stop();
    } else {
      state.recognition.start();
    }
  });
} else {
  elements.voiceBtn.style.display = 'none';
}

// --- Text-to-Speech (Audio Read Out) ---
elements.speakBtn.addEventListener('click', () => {
  if (!state.lastResponseText) {
    showToast('No response text to read.', 'info');
    return;
  }
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    // Strip markdown formatting for cleaner speech
    const cleanSpeech = state.lastResponseText.replace(/[#*`>-]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
    showToast('🔊 Reading response aloud...', 'info');
  } else {
    showToast('Text-to-speech not supported in this browser.', 'error');
  }
});

// --- Copy to Clipboard ---
elements.copyBtn.addEventListener('click', async () => {
  if (!state.lastResponseText) return;
  try {
    await navigator.clipboard.writeText(state.lastResponseText);
    showToast('📋 Copied to clipboard!', 'success');
  } catch (err) {
    showToast('Failed to copy to clipboard.', 'error');
  }
});

elements.copyPathBtn.addEventListener('click', async () => {
  const text = elements.pathResultContainer.innerText;
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    showToast('📋 Learning path copied!', 'success');
  } catch (err) {
    showToast('Failed to copy.', 'error');
  }
});

// --- Bookmark Current Result ---
elements.bookmarkBtn.addEventListener('click', async () => {
  if (!state.lastHistoryId) {
    showToast('Generate a response first to bookmark.', 'info');
    return;
  }
  try {
    const res = await fetch(`/api/history/${state.lastHistoryId}/bookmark`, { method: 'POST' });
    const data = await res.json();
    if (res.ok) {
      showToast(data.is_bookmarked ? '⭐ Added to bookmarks!' : 'Removed from bookmarks', 'success');
    }
  } catch (err) {
    showToast('Failed to bookmark.', 'error');
  }
});

// --- Save to Notes ---
elements.saveNoteBtn.addEventListener('click', () => {
  if (!state.lastResponseText) {
    showToast('Generate a response first to save note.', 'info');
    return;
  }
  openNoteModal(`Note: ${elements.hubInput.value.slice(0, 40)}...`, state.currentTask.toUpperCase(), state.lastResponseText);
});

elements.savePathNoteBtn.addEventListener('click', () => {
  const text = elements.pathResultContainer.innerText;
  if (!text) return;
  openNoteModal(`Roadmap: ${elements.pathTopicInput.value}`, 'Roadmap', text);
});

// --- Note Modal Handling ---
function openNoteModal(title = '', category = 'General', content = '') {
  elements.modalNoteTitle.value = title;
  elements.modalNoteCategory.value = category;
  elements.modalNoteContent.value = content;
  elements.noteModal.classList.remove('hidden');
}

function closeNoteModal() {
  elements.noteModal.classList.add('hidden');
}

elements.newNoteModalBtn.addEventListener('click', () => openNoteModal());
elements.closeNoteModalBtn.addEventListener('click', closeNoteModal);
elements.cancelNoteBtn.addEventListener('click', closeNoteModal);

elements.saveNewNoteSubmitBtn.addEventListener('click', async () => {
  const title = elements.modalNoteTitle.value.trim();
  const category = elements.modalNoteCategory.value.trim() || 'General';
  const content = elements.modalNoteContent.value.trim();

  if (!title || !content) {
    showToast('Title and content are required.', 'error');
    return;
  }

  try {
    const res = await fetch('/api/notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, category, content })
    });
    if (res.ok) {
      showToast('💾 Note saved successfully!', 'success');
      closeNoteModal();
      loadNotes();
    } else {
      showToast('Failed to save note.', 'error');
    }
  } catch (err) {
    showToast('Network error while saving note.', 'error');
  }
});

// --- AI Generation (Learning Hub) ---
elements.generateBtn.addEventListener('click', async () => {
  const text = elements.hubInput.value.trim();
  if (text.length < 3) {
    showToast('Please enter at least 3 characters.', 'error');
    return;
  }

  elements.generateBtn.disabled = true;
  elements.generateBtnText.textContent = 'EduGenie is thinking...';
  elements.responseStatus.textContent = 'Generating...';
  elements.responseContainer.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">⏳</div>
      <h3>Generating educational response...</h3>
      <p>Analyzing principles, synthesizing analogies, and verifying clarity.</p>
    </div>
  `;

  let url = '/qa';
  let body = { text };

  if (state.currentTask === 'explain') {
    url = '/explain';
    body = { text, level: elements.learnerLevel.value };
  } else if (state.currentTask === 'summarize') {
    url = '/summarize';
    body = { text };
  }

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || 'Generation request failed');
    }

    state.lastResponseText = data.result;
    state.lastHistoryId = data.history_id;
    elements.responseContainer.innerHTML = renderMarkdown(data.result);
    elements.responseStatus.textContent = 'Complete';
    showToast('✅ Response generated!', 'success');
  } catch (err) {
    elements.responseContainer.innerHTML = `<p class="loading-text" style="color: var(--danger)">Error: ${escapeHTML(err.message)}</p>`;
    elements.responseStatus.textContent = 'Error';
    showToast(err.message, 'error');
  } finally {
    elements.generateBtn.disabled = false;
    elements.generateBtnText.textContent = 'Generate with AI';
  }
});

// --- TAB 2: Quiz Arena Logic ---
elements.startQuizBtn.addEventListener('click', async () => {
  const topic = elements.quizTopicInput.value.trim();
  if (topic.length < 2) {
    showToast('Enter a topic or paste a passage for the quiz.', 'error');
    return;
  }

  elements.startQuizBtn.disabled = true;
  elements.startQuizBtn.innerHTML = '<span>🎲 Generating Quiz...</span>';
  elements.quizStageContainer.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">🎲</div>
      <h3>Creating customized questions...</h3>
      <p>Formulating questions, verifying distractors, and creating explanations.</p>
    </div>
  `;

  try {
    const res = await fetch('/quiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: topic })
    });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || 'Quiz creation failed');

    state.activeQuizData = data.quiz;
    state.activeQuizTopic = topic;
    state.selectedQuizAnswers = {};

    renderQuizStage(data.quiz);
    elements.quizControls.classList.remove('hidden');
    showToast('🎯 Quiz ready! Select your answers below.', 'success');
  } catch (err) {
    elements.quizStageContainer.innerHTML = `<p class="loading-text" style="color: var(--danger)">Error: ${escapeHTML(err.message)}</p>`;
    elements.quizControls.classList.add('hidden');
    showToast(err.message, 'error');
  } finally {
    elements.startQuizBtn.disabled = false;
    elements.startQuizBtn.innerHTML = '<span>🎲 Generate Quiz</span>';
  }
});

function renderQuizStage(questions) {
  elements.quizStageContainer.innerHTML = questions.map((q, qIndex) => `
    <div class="quiz-card" data-q-index="${qIndex}">
      <h3 class="quiz-question-title">${qIndex + 1}. ${escapeHTML(q.question)}</h3>
      <div class="quiz-options">
        ${q.options.map((opt, optIndex) => `
          <button type="button" class="quiz-option-btn" data-q="${qIndex}" data-opt="${escapeHTML(opt)}">
            <span class="option-marker">${String.fromCharCode(65 + optIndex)}</span>
            <span class="option-text">${escapeHTML(opt)}</span>
          </button>
        `).join('')}
      </div>
      <div class="quiz-feedback hidden"></div>
    </div>
  `).join('');

  // Attach option click listeners
  elements.quizStageContainer.querySelectorAll('.quiz-option-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const qIndex = btn.dataset.q;
      const optVal = btn.dataset.opt;

      // Unselect siblings
      const card = btn.closest('.quiz-card');
      card.querySelectorAll('.quiz-option-btn').forEach(b => b.classList.remove('selected'));

      btn.classList.add('selected');
      state.selectedQuizAnswers[qIndex] = optVal;
    });
  });
}

// Submit Quiz
elements.submitQuizBtn.addEventListener('click', async () => {
  if (!state.activeQuizData || state.activeQuizData.length === 0) return;

  const total = state.activeQuizData.length;
  const answeredCount = Object.keys(state.selectedQuizAnswers).length;

  if (answeredCount < total) {
    if (!confirm(`You answered ${answeredCount} of ${total} questions. Submit anyway?`)) {
      return;
    }
  }

  const payload = {
    topic: state.activeQuizTopic,
    answers: state.activeQuizData.map((q, idx) => ({
      question: q.question,
      selected_answer: state.selectedQuizAnswers[idx] || '(Not answered)',
      correct_answer: q.correct_answer,
      explanation: q.explanation || ''
    }))
  };

  try {
    elements.submitQuizBtn.disabled = true;
    const res = await fetch('/api/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();

    if (!res.ok) throw new Error(result.detail || 'Submission failed');

    // Display Score Summary & highlight questions
    displayQuizResults(result);
    loadQuizHistory();
    showToast(`Quiz completed! Score: ${result.score}/${result.total_questions} (${result.percentage}%)`, 'success');
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    elements.submitQuizBtn.disabled = false;
  }
});

function displayQuizResults(result) {
  // Hide submit button
  elements.quizControls.classList.add('hidden');

  // Insert score card at the top of quiz stage
  const scoreCard = document.createElement('div');
  scoreCard.className = 'score-summary-card';
  scoreCard.innerHTML = `
    <div class="score-badge-circle ${result.passed ? 'pass' : 'fail'}">
      <span class="score-pct">${result.percentage}%</span>
      <small>${result.passed ? 'PASSED' : 'NEEDS PRACTICE'}</small>
    </div>
    <h2>${result.passed ? '🎉 Excellent Job!' : 'Keep Practicing!'}</h2>
    <p>You scored <strong>${result.score}</strong> out of <strong>${result.total_questions}</strong> questions correctly.</p>
    <div style="margin-top: 15px;">
      <button class="btn-sm btn-primary" onclick="document.getElementById('startQuizBtn').click()">🔄 Try Another Quiz</button>
    </div>
  `;
  elements.quizStageContainer.prepend(scoreCard);

  // Mark options as correct/incorrect and show explanation
  result.breakdown.forEach((item, idx) => {
    const card = elements.quizStageContainer.querySelector(`.quiz-card[data-q-index="${idx}"]`);
    if (!card) return;

    const optButtons = card.querySelectorAll('.quiz-option-btn');
    optButtons.forEach(btn => {
      btn.disabled = true;
      const text = btn.dataset.opt.trim().toLowerCase();
      const isCorrect = text === item.correct_answer.trim().toLowerCase();
      const isSelected = text === item.selected_answer.trim().toLowerCase();

      if (isCorrect) {
        btn.classList.add('correct');
      } else if (isSelected && !isCorrect) {
        btn.classList.add('incorrect');
      }
    });

    const feedback = card.querySelector('.quiz-feedback');
    feedback.classList.remove('hidden');
    feedback.innerHTML = `
      <div class="quiz-explanation-box">
        <strong>${item.is_correct ? '✅ Correct!' : '❌ Incorrect.'}</strong>
        Correct Answer: <em>${escapeHTML(item.correct_answer)}</em><br>
        <span>${escapeHTML(item.explanation)}</span>
      </div>
    `;
  });
}

// Load Quiz Attempts History
async function loadQuizHistory() {
  try {
    const res = await fetch('/api/quiz/history');
    const data = await res.json();
    if (!res.ok) throw new Error();

    if (!data.attempts || data.attempts.length === 0) {
      elements.quizHistoryContainer.innerHTML = '<p class="loading-text">No quiz attempts recorded yet. Take your first quiz above!</p>';
      return;
    }

    elements.quizHistoryContainer.innerHTML = `
      <table class="data-table">
        <thead>
          <tr>
            <th>Date & Time</th>
            <th>Topic</th>
            <th>Score</th>
            <th>Percentage</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${data.attempts.map(a => `
            <tr>
              <td>${escapeHTML(a.created_at)}</td>
              <td><strong>${escapeHTML(a.topic)}</strong></td>
              <td>${a.score} / ${a.total_questions}</td>
              <td>${a.percentage}%</td>
              <td>
                <span class="task-tag" style="background: ${a.percentage >= 60 ? 'var(--success-bg)' : 'var(--warning-bg)'}; color: ${a.percentage >= 60 ? 'var(--success)' : 'var(--warning)'}">
                  ${a.percentage >= 60 ? 'Passed' : 'Reviewed'}
                </span>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } catch (err) {
    elements.quizHistoryContainer.innerHTML = '<p class="loading-text">Unable to load quiz history.</p>';
  }
}

elements.refreshQuizHistoryBtn.addEventListener('click', loadQuizHistory);

// --- TAB 3: Learning Paths ---
elements.buildPathBtn.addEventListener('click', async () => {
  const topic = elements.pathTopicInput.value.trim();
  if (topic.length < 2) {
    showToast('Enter a subject or skill to build a roadmap.', 'error');
    return;
  }

  const level = elements.pathLevelSelect.value;
  elements.buildPathBtn.disabled = true;
  elements.buildPathBtn.innerHTML = '<span>🚀 Building Roadmap...</span>';
  elements.pathResultContainer.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">🧭</div>
      <h3>Crafting personalized roadmap...</h3>
      <p>Structuring prerequisites, beginner milestones, intermediate projects, and mastery goals.</p>
    </div>
  `;

  try {
    const res = await fetch('/learn/recommendations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, level })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to generate roadmap');

    elements.pathResultContainer.innerHTML = renderMarkdown(data.result);
    showToast('🗺️ Roadmap generated!', 'success');
  } catch (err) {
    elements.pathResultContainer.innerHTML = `<p class="loading-text" style="color: var(--danger)">Error: ${escapeHTML(err.message)}</p>`;
    showToast(err.message, 'error');
  } finally {
    elements.buildPathBtn.disabled = false;
    elements.buildPathBtn.innerHTML = '<span>🚀 Create Learning Path</span>';
  }
});

// --- TAB 4: Notes & History ---
// Subview navigation
elements.subTabButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    elements.subTabButtons.forEach(b => b.classList.remove('active'));
    elements.subviews.forEach(v => v.classList.remove('active'));

    btn.classList.add('active');
    const target = document.getElementById(btn.dataset.subview);
    if (target) target.classList.add('active');

    if (btn.dataset.subview === 'sub-history') loadHistory();
    else if (btn.dataset.subview === 'sub-bookmarks') loadBookmarks();
    else if (btn.dataset.subview === 'sub-notes') loadNotes();
  });
});

let currentFilter = 'all';
elements.filterChips.forEach(chip => {
  chip.addEventListener('click', () => {
    elements.filterChips.forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    currentFilter = chip.dataset.filter;
    loadHistory();
  });
});

elements.historySearchInput.addEventListener('input', (e) => {
  loadHistory(e.target.value.trim());
});

async function loadHistory(searchQuery = '') {
  try {
    let url = `/api/history?task_type=${currentFilter}`;
    if (searchQuery) url += `&search=${encodeURIComponent(searchQuery)}`;

    const res = await fetch(url);
    const data = await res.json();

    if (!data.history || data.history.length === 0) {
      elements.historyListContainer.innerHTML = '<p class="loading-text">No activity history found matching your filters.</p>';
      return;
    }

    elements.historyListContainer.innerHTML = data.history.map(item => `
      <div class="history-card" data-id="${item.id}">
        <div class="history-card-header">
          <span class="task-tag">${item.task_type}</span>
          <span class="card-date">${escapeHTML(item.created_at)}</span>
        </div>
        <div class="history-card-query">${escapeHTML(item.input_text)}</div>
        <div class="history-card-snippet">${escapeHTML(item.output_result.slice(0, 180))}...</div>
        <div class="history-card-actions">
          <button class="btn-sm btn-outline copy-item-btn" data-text="${escapeHTML(item.output_result)}">📋 Copy</button>
          <button class="btn-sm ${item.is_bookmarked ? 'btn-primary-light' : 'btn-outline'} bookmark-item-btn" data-id="${item.id}">
            ${item.is_bookmarked ? '⭐ Saved' : '☆ Bookmark'}
          </button>
          <button class="btn-sm btn-danger delete-item-btn" data-id="${item.id}">🗑️</button>
        </div>
      </div>
    `).join('');

    attachHistoryCardListeners(elements.historyListContainer);
  } catch (err) {
    elements.historyListContainer.innerHTML = '<p class="loading-text">Failed to load history.</p>';
  }
}

async function loadBookmarks() {
  try {
    const res = await fetch('/api/bookmarks');
    const data = await res.json();

    if (!data.bookmarks || data.bookmarks.length === 0) {
      elements.bookmarksListContainer.innerHTML = '<p class="loading-text">No bookmarked items yet. Star any response to save it here!</p>';
      return;
    }

    elements.bookmarksListContainer.innerHTML = data.bookmarks.map(item => `
      <div class="history-card" data-id="${item.id}">
        <div class="history-card-header">
          <span class="task-tag">${item.task_type}</span>
          <span class="card-date">${escapeHTML(item.created_at)}</span>
        </div>
        <div class="history-card-query">${escapeHTML(item.input_text)}</div>
        <div class="history-card-snippet">${escapeHTML(item.output_result.slice(0, 180))}...</div>
        <div class="history-card-actions">
          <button class="btn-sm btn-outline copy-item-btn" data-text="${escapeHTML(item.output_result)}">📋 Copy</button>
          <button class="btn-sm btn-primary-light bookmark-item-btn" data-id="${item.id}">⭐ Remove Bookmark</button>
          <button class="btn-sm btn-danger delete-item-btn" data-id="${item.id}">🗑️</button>
        </div>
      </div>
    `).join('');

    attachHistoryCardListeners(elements.bookmarksListContainer);
  } catch (err) {
    elements.bookmarksListContainer.innerHTML = '<p class="loading-text">Failed to load bookmarks.</p>';
  }
}

async function loadNotes() {
  try {
    const res = await fetch('/api/notes');
    const data = await res.json();

    if (!data.notes || data.notes.length === 0) {
      elements.notesListContainer.innerHTML = '<p class="loading-text">No custom study notes created yet. Click "+ New Note" above!</p>';
      return;
    }

    elements.notesListContainer.innerHTML = data.notes.map(note => `
      <div class="note-card" data-note-id="${note.id}">
        <div class="note-card-header">
          <span class="task-tag" style="background: rgba(139, 92, 246, 0.15); color: #c4b5fd;">${escapeHTML(note.category)}</span>
          <span class="card-date">${escapeHTML(note.created_at)}</span>
        </div>
        <h3 class="history-card-query">${escapeHTML(note.title)}</h3>
        <div class="history-card-snippet" style="white-space: pre-wrap;">${escapeHTML(note.content)}</div>
        <div class="note-card-actions">
          <button class="btn-sm btn-outline copy-item-btn" data-text="${escapeHTML(note.content)}">📋 Copy</button>
          <button class="btn-sm btn-danger delete-note-btn" data-id="${note.id}">🗑️ Delete</button>
        </div>
      </div>
    `).join('');

    elements.notesListContainer.querySelectorAll('.copy-item-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        await navigator.clipboard.writeText(btn.dataset.text);
        showToast('📋 Copied note!', 'success');
      });
    });

    elements.notesListContainer.querySelectorAll('.delete-note-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        if (!confirm('Delete this study note?')) return;
        const res = await fetch(`/api/notes/${btn.dataset.id}`, { method: 'DELETE' });
        if (res.ok) {
          showToast('Note deleted.', 'info');
          loadNotes();
        }
      });
    });
  } catch (err) {
    elements.notesListContainer.innerHTML = '<p class="loading-text">Failed to load study notes.</p>';
  }
}

function attachHistoryCardListeners(container) {
  container.querySelectorAll('.copy-item-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      await navigator.clipboard.writeText(btn.dataset.text);
      showToast('📋 Copied!', 'success');
    });
  });

  container.querySelectorAll('.bookmark-item-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;
      const res = await fetch(`/api/history/${id}/bookmark`, { method: 'POST' });
      if (res.ok) {
        showToast('Bookmark updated.', 'success');
        if (document.getElementById('sub-bookmarks').classList.contains('active')) {
          loadBookmarks();
        } else {
          loadHistory();
        }
      }
    });
  });

  container.querySelectorAll('.delete-item-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      if (!confirm('Delete this history record?')) return;
      const id = btn.dataset.id;
      const res = await fetch(`/api/history/${id}`, { method: 'DELETE' });
      if (res.ok) {
        showToast('History item deleted.', 'info');
        loadHistory();
      }
    });
  });
}

elements.clearHistoryBtn.addEventListener('click', async () => {
  if (!confirm('Are you sure you want to clear your entire activity history?')) return;
  try {
    const res = await fetch('/api/history', { method: 'DELETE' });
    const data = await res.json();
    if (res.ok) {
      showToast(`Cleared ${data.deleted_count} items from history.`, 'success');
      loadHistory();
    }
  } catch (err) {
    showToast('Failed to clear history.', 'error');
  }
});

// --- TAB 5: Analytics Dashboard ---
async function loadAnalytics() {
  try {
    const res = await fetch('/api/stats');
    const data = await res.json();
    if (!res.ok) throw new Error();

    elements.statQueries.textContent = data.total_queries;
    elements.statQuizzes.textContent = data.total_quizzes_taken;
    elements.statScore.textContent = `${data.average_quiz_score}%`;
    elements.statNotes.textContent = (data.total_bookmarks + data.total_notes);

    // Breakdown bars
    const maxVal = Math.max(...Object.values(data.task_breakdown), 1);
    const tasks = [
      { key: 'qa', label: 'Questions & Answers' },
      { key: 'explain', label: 'Concept Explanations' },
      { key: 'quiz', label: 'Quizzes Generated' },
      { key: 'summarize', label: 'Summaries' },
      { key: 'learn', label: 'Learning Paths' }
    ];

    elements.taskBreakdownBars.innerHTML = tasks.map(t => {
      const count = data.task_breakdown[t.key] || 0;
      const pct = Math.round((count / maxVal) * 100);
      return `
        <div class="bar-row">
          <span class="bar-label">${t.label}</span>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${pct}%"></div>
          </div>
          <span class="bar-count">${count}</span>
        </div>
      `;
    }).join('');
  } catch (err) {
    showToast('Unable to refresh analytics dashboard.', 'error');
  }
}

elements.refreshStatsBtn.addEventListener('click', loadAnalytics);

// --- Initial Setup on Page Load ---
window.addEventListener('DOMContentLoaded', () => {
  updateTaskView('qa');
  updateCharCount();

  // Check health and display active configuration
  fetch('/health')
    .then(r => r.json())
    .then(data => {
      if (data.ai_live) {
        elements.aiStatusBadge.className = 'ai-badge badge-live';
        elements.aiStatusText.textContent = `Gemini Live (${data.model})`;
      } else {
        elements.aiStatusBadge.className = 'ai-badge badge-demo';
        elements.aiStatusText.textContent = 'Demo / Offline Mode';
      }
    })
    .catch(() => {});
});
