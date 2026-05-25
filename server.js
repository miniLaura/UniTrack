const express = require('express');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_DIR = path.join(__dirname, 'data');
const DB_FILE = path.join(DATA_DIR, 'db.json');

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

function loadDB() {
  try {
    if (!fs.existsSync(DB_FILE)) return { users: {}, sessions: {} };
    return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
  } catch {
    return { users: {}, sessions: {} };
  }
}

function saveDB(db) {
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2), 'utf8');
}

function hashPassword(password) {
  return crypto.createHash('sha256').update(password + 'unitrack-salt-2026').digest('hex');
}

function generateToken() {
  return crypto.randomBytes(32).toString('hex');
}

function cleanSessions(db) {
  const now = Date.now();
  const SEVEN_DAYS = 7 * 24 * 60 * 60 * 1000;
  for (const token of Object.keys(db.sessions)) {
    if (now - db.sessions[token].createdAt > SEVEN_DAYS) {
      delete db.sessions[token];
    }
  }
}

app.use(express.json({ limit: '2mb' }));
app.use(express.static(path.join(__dirname, 'public')));

function requireAuth(req, res, next) {
  const token = req.headers['x-session-token'];
  if (!token) return res.status(401).json({ error: 'Não autenticado' });
  const db = loadDB();
  const session = db.sessions[token];
  if (!session) return res.status(401).json({ error: 'Sessão inválida ou expirada' });
  req.username = session.username;
  next();
}

app.post('/api/register', (req, res) => {
  const { username, password, displayName } = req.body;
  if (!username || !password) return res.status(400).json({ error: 'Usuário e senha são obrigatórios' });
  if (username.length < 3) return res.status(400).json({ error: 'Usuário deve ter ao menos 3 caracteres' });
  if (password.length < 6) return res.status(400).json({ error: 'Senha deve ter ao menos 6 caracteres' });

  const db = loadDB();
  const key = username.toLowerCase().trim();
  if (db.users[key]) return res.status(409).json({ error: 'Usuário já existe' });

  db.users[key] = {
    username: key,
    displayName: displayName || username,
    passwordHash: hashPassword(password),
    createdAt: Date.now(),
    data: { aluno: displayName || username, curso: '', semestre: '', disciplinas: [] },
  };
  saveDB(db);
  res.json({ ok: true });
});

app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.status(400).json({ error: 'Preencha usuário e senha' });

  const db = loadDB();
  const key = username.toLowerCase().trim();
  const user = db.users[key];
  if (!user || user.passwordHash !== hashPassword(password)) {
    return res.status(401).json({ error: 'Usuário ou senha incorretos' });
  }

  cleanSessions(db);
  const token = generateToken();
  db.sessions[token] = { username: key, createdAt: Date.now() };
  saveDB(db);
  res.json({ ok: true, token, displayName: user.displayName });
});

app.post('/api/logout', requireAuth, (req, res) => {
  const token = req.headers['x-session-token'];
  const db = loadDB();
  delete db.sessions[token];
  saveDB(db);
  res.json({ ok: true });
});

app.get('/api/data', requireAuth, (req, res) => {
  const db = loadDB();
  const user = db.users[req.username];
  res.json(user.data || { aluno: '', curso: '', semestre: '', disciplinas: [] });
});

app.post('/api/data', requireAuth, (req, res) => {
  const db = loadDB();
  const user = db.users[req.username];
  if (!user) return res.status(404).json({ error: 'Usuário não encontrado' });

  const { aluno, curso, semestre, disciplinas } = req.body;
  user.data = {
    aluno: aluno || '',
    curso: curso || '',
    semestre: semestre || '',
    disciplinas: Array.isArray(disciplinas) ? disciplinas : [],
  };
  saveDB(db);
  res.json({ ok: true });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`\n🎓 UniTrack rodando em http://localhost:${PORT}\n`);
});
