/* CASINO LEDGER -- the one-way meter every casino game reports to.
 *
 * Identical copy in each game's deploy folder (Wyrmhoard Keno, Safari Time). Elo's Hoard
 * has its own older ledger at machine/global with the same idea; this module is the
 * generalisation of it for games that had no Firebase of their own. All three feed the
 * casino console at merwinwebdesignz.com/work/games/casinoadmin.
 *
 * WHAT IT RECORDS. One document per game, ledgers/{game}: plays, wagered, paid and
 * feature triggers, split by calendar day and by "cell" (the game's own name for a
 * bet configuration -- denomination/tier/spots for keno, bet level for the slot). The
 * console compares the observed return per cell with the return the game's own maths
 * says that cell should produce. Nothing here ever reads the ledger back: the game does
 * not know its own history and cannot act on it. Every play stays independent.
 *
 * WHO WRITES. The session signs in anonymously to the elos-hoard Firebase project --
 * no name, no account, nothing about the player. That sign-in exists purely so the
 * security rules can insist a writer is a session at all, and cap what one write may do
 * (one play, at most $2 wagered, counters only ever go up). If anonymous sign-in is
 * off, or the SDK fails to load, or the network is down, report() is a no-op and the
 * game plays exactly as before. A play is never delayed or blocked by this file.
 *
 * Load it as a module: <script type="module" src="casino-ledger.js"></script>
 * Then from game code, at the moment a round settles:
 *     window.CasinoLedger && CasinoLedger.report('keno', { bet, paid, bonus, cell })
 * bet and paid in DOLLARS (not cents), bonus 0 or 1, cell a short token with no dots.
 */
const SDK = 'https://www.gstatic.com/firebasejs/10.12.2';
const CFG = {
  apiKey: 'AIzaSyBsF95vNPpWbgYHHMEhYKxdJaMzceO-rz8',   // public client id, not a secret
  authDomain: 'elos-hoard.firebaseapp.com',
  projectId: 'elos-hoard',
  appId: '1:555085175615:web:c485b0d13b18c05cbad18a'
};
const GAMES = ['keno', 'safari'];

let fb = null, ready = null, uid = null;
const pending = [];

function day() { return new Date().toISOString().slice(0, 10); }

async function boot() {
  const [app, auth, fs] = await Promise.all([
    import(SDK + '/firebase-app.js'),
    import(SDK + '/firebase-auth.js'),
    import(SDK + '/firebase-firestore.js')
  ]);
  const a = app.initializeApp(CFG, 'casino-ledger');
  fb = { auth: auth.getAuth(a), db: fs.getFirestore(a), ...auth, ...fs };
  await fb.setPersistence(fb.auth, fb.browserLocalPersistence).catch(() => {});
  await new Promise(res => {
    const off = fb.onAuthStateChanged(fb.auth, async u => {
      if (u) { uid = u.uid; off(); res(); return; }
      try { await fb.signInAnonymously(fb.auth); }
      catch (e) { off(); res(); }
    });
  });
}

async function write(game, o) {
  if (!fb || !uid) return;
  const inc = fb.increment, ref = fb.doc(fb.db, 'ledgers', game), d = day();
  const bet = Math.max(0, Math.min(2, Number(o.bet) || 0));
  const paid = Math.max(0, Number(o.paid) || 0);
  const bonus = o.bonus ? 1 : 0;
  const cell = String(o.cell || 'x').replace(/[^A-Za-z0-9_-]/g, '_');
  const patch = {
    plays: inc(1), wagered: inc(bet), paid: inc(paid), bonuses: inc(bonus),
    updatedAt: fb.serverTimestamp()
  };
  patch['days.' + d + '.n'] = inc(1);
  patch['days.' + d + '.w'] = inc(bet);
  patch['days.' + d + '.p'] = inc(paid);
  patch['days.' + d + '.b'] = inc(bonus);
  patch['cells.' + cell + '.n'] = inc(1);
  patch['cells.' + cell + '.w'] = inc(bet);
  patch['cells.' + cell + '.p'] = inc(paid);
  patch['cells.' + cell + '.b'] = inc(bonus);
  try {
    await fb.updateDoc(ref, patch);
  } catch (e) {
    // First play ever for this game: the document does not exist yet. Create it empty
    // (the rules only allow a zeroed create) and apply the same patch again.
    try {
      await fb.setDoc(ref, { plays: 0, wagered: 0, paid: 0, bonuses: 0, days: {}, cells: {},
                             createdAt: fb.serverTimestamp(), updatedAt: fb.serverTimestamp() });
      await fb.updateDoc(ref, patch);
    } catch (e2) { /* unrecorded; the game is unaffected */ }
  }
}

function report(game, o) {
  if (!GAMES.includes(game) || !o) return;
  if (!ready) ready = boot().catch(() => {});
  pending.push([game, o]);
  ready.then(async () => {
    while (pending.length) { const [g, p] = pending.shift(); await write(g, p); }
  });
}

window.CasinoLedger = { report };
