
const raw = JSON.parse(document.getElementById('hero-data').textContent);
const heroes = raw.heroes;
const classColors = { '盾兵': '#E74C3C', '弓兵': '#3498DB', '槍兵': '#2ECC71' };
const rarityColors = raw.rarity_colors || { R: '#3498DB', SR: '#9B59B6', SSR: '#F1C40F' };
const tierColors = { 'S+': '#FF3B6E', 'S': '#F1C40F', 'A': '#4FC3F7', 'B': '#7FD37F', 'C': '#B0B8C1', 'D': '#7A8794' };

let selected = new Set();

function populateGenFilter() {
  const gens = [...new Set(heroes.map(h => h.generation))].sort((a,b)=>a-b);
  const sel = document.getElementById('genFilter');
  gens.forEach(g => {
    const opt = document.createElement('option');
    opt.value = g; opt.textContent = '第' + g + '世代';
    sel.appendChild(opt);
  });
}

function tierRank(t) {
  const order = ['S+','S','A','B','C','D'];
  return order.indexOf(t);
}

function getFiltered() {
  const q = document.getElementById('searchBox').value.trim().toLowerCase();
  const gen = document.getElementById('genFilter').value;
  const cls = document.getElementById('classFilter').value;
  const rar = document.getElementById('rarityFilter').value;
  const tier = document.getElementById('tierFilter').value;
  const sortBy = document.getElementById('sortBy').value;

  let list = heroes.filter(h => {
    if (q && !h.name.toLowerCase().includes(q)) return false;
    if (gen && String(h.generation) !== gen) return false;
    if (cls && h.hero_class !== cls) return false;
    if (rar && h.rarity !== rar) return false;
    if (tier && h.tier_overall !== tier) return false;
    return true;
  });

  if (sortBy === 'tier') list.sort((a,b) => tierRank(a.tier_overall) - tierRank(b.tier_overall) || a.name.localeCompare(b.name));
  else if (sortBy === 'name') list.sort((a,b) => a.name.localeCompare(b.name));
  else if (sortBy === 'gen') list.sort((a,b) => a.generation - b.generation || a.name.localeCompare(b.name));

  return list;
}

function render() {
  const list = getFiltered();
  const grid = document.getElementById('heroGrid');
  grid.innerHTML = '';
  document.getElementById('countLabel').textContent = list.length + ' 体表示中（全 ' + heroes.length + ' 体）';

  list.forEach(h => {
    const card = document.createElement('div');
    card.className = 'card' + (selected.has(h.name) ? ' selected' : '');
    card.innerHTML = `
      <div class="checkbox-indicator">${selected.has(h.name) ? '✓' : ''}</div>
      <div class="card-top">
        <span class="name">${h.name}</span>
        <span class="tier" style="background:${tierColors[h.tier_overall] || '#888'}">${h.tier_overall}</span>
      </div>
      <div class="meta">第${h.generation}世代 ・ ${h.rarity}</div>
      <div style="margin-bottom:6px;">
        <span class="class-tag" style="background:${classColors[h.hero_class] || '#888'}">${h.hero_class}</span>
      </div>
      <div class="notes">${h.notes || ''}</div>
    `;
    card.addEventListener('click', () => toggleSelect(h.name));
    grid.appendChild(card);
  });
}

function toggleSelect(name) {
  if (selected.has(name)) selected.delete(name);
  else {
    if (selected.size >= 4) { alert('比較は最大4体までです'); return; }
    selected.add(name);
  }
  renderTray();
  render();
}

function renderTray() {
  const tray = document.getElementById('compareTray');
  const chips = document.getElementById('trayChips');
  chips.innerHTML = '';
  if (selected.size === 0) { tray.classList.add('empty'); return; }
  tray.classList.remove('empty');
  selected.forEach(name => {
    const chip = document.createElement('div');
    chip.className = 'tray-chip';
    chip.innerHTML = `${name} <button data-name="${name}">✕</button>`;
    chip.querySelector('button').addEventListener('click', (e) => {
      e.stopPropagation();
      selected.delete(name);
      renderTray();
      render();
    });
    chips.appendChild(chip);
  });
}

function openCompareModal() {
  if (selected.size < 1) { alert('比較・詳細表示するヒーローを選んでください'); return; }
  const list = heroes.filter(h => selected.has(h.name));
  const rows = [
    ['兵種', h => h.hero_class],
    ['レアリティ', h => h.rarity],
    ['世代', h => '第' + h.generation + '世代'],
    ['総合ティア', h => h.tier_overall],
    ['遠征ティア', h => h.tier_expedition],
    ['探検ティア', h => h.tier_exploration],
    ['入手方法', h => h.how_to_obtain || '-'],
    ['解説', h => h.notes || '-'],
    ['推奨用途', h => h.best_use || '-'],
  ];

  let html = '<div class="table-scroll"><table><thead><tr><th>項目</th>';
  list.forEach(h => html += `<td class="hero-col-name">${h.name}</td>`);
  html += '</tr></thead><tbody>';
  rows.forEach(([label, fn]) => {
    html += `<tr><th>${label}</th>`;
    list.forEach(h => html += `<td>${fn(h)}</td>`);
    html += '</tr>';
  });
  html += '</tbody></table></div>';

  // Mobile-friendly stacked card view (one card per hero, no horizontal scrolling needed)
  let cardsHtml = '<div class="compare-cards-view">';
  list.forEach(h => {
    cardsHtml += `
      <div class="compare-hero-card">
        <div class="ch-head">
          <h3>${h.name}</h3>
          <span class="tier" style="background:${tierColors[h.tier_overall] || '#888'}">${h.tier_overall}</span>
        </div>
        <div class="ch-meta">
          <span class="class-tag" style="background:${classColors[h.hero_class] || '#888'}">${h.hero_class}</span>
          ${h.rarity} ・ 第${h.generation}世代
        </div>
        <div class="ch-field">
          <div class="ch-label">遠征ティア / 探検ティア</div>
          <div class="ch-tiers">
            <span class="tier-chip" style="background:${tierColors[h.tier_expedition] || '#888'}">遠征 ${h.tier_expedition}</span>
            <span class="tier-chip" style="background:${tierColors[h.tier_exploration] || '#888'}">探検 ${h.tier_exploration}</span>
          </div>
        </div>
        <div class="ch-field">
          <div class="ch-label">入手方法</div>
          <div class="ch-value">${h.how_to_obtain || '-'}</div>
        </div>
        <div class="ch-field">
          <div class="ch-label">解説</div>
          <div class="ch-value">${h.notes || '-'}</div>
        </div>
        <div class="ch-field">
          <div class="ch-label">推奨用途</div>
          <div class="ch-value">${h.best_use || '-'}</div>
        </div>
      </div>
    `;
  });
  cardsHtml += '</div>';

  document.getElementById('compareTableWrap').innerHTML = html + cardsHtml;
  document.getElementById('compareModalTitle').textContent = list.length === 1 ? '英雄詳細' : '英雄比較';
  document.getElementById('modalOverlay').classList.add('open');
}

document.getElementById('searchBox').addEventListener('input', render);
document.getElementById('genFilter').addEventListener('change', render);
document.getElementById('classFilter').addEventListener('change', render);
document.getElementById('rarityFilter').addEventListener('change', render);
document.getElementById('tierFilter').addEventListener('change', render);
document.getElementById('sortBy').addEventListener('change', render);
document.getElementById('clearTray').addEventListener('click', () => { selected.clear(); renderTray(); render(); });
document.getElementById('openCompare').addEventListener('click', openCompareModal);
document.getElementById('closeModal').addEventListener('click', () => document.getElementById('modalOverlay').classList.remove('open'));
document.getElementById('modalOverlay').addEventListener('click', (e) => { if (e.target.id === 'modalOverlay') e.currentTarget.classList.remove('open'); });

populateGenFilter();
render();
