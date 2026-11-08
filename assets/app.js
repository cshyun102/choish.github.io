(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('analysis-data').textContent);
  const tabs = [...document.querySelectorAll('[data-plan]')];
  const labels = ['S&P500', '나스닥100', '미국 배당성장', '금', '원화 안전자금'];
  const colors = ['#28584a', '#7f9dba', '#a9bea5', '#c9aa61', '#d7dccb'];
  const descriptions = {
    A: ['안전자금부터 든든하게 확보하는 선택', '5년 뒤 사용할 가능성이 높고 손실 부담이 큰 경우의 검토안입니다. 주식과 금도 포함되어 있어 원금이 보장되지는 않습니다.', '안전자금 절반을 확보하고 성장주 추가 집중을 줄입니다.', '상승장 수익 참여가 작고 주식·금의 손실 가능성이 남습니다.'],
    B: ['성장과 안정 사이, 균형을 찾는 선택', '계속 적립할 수 있는 자금의 검토 출발점입니다. 5년 뒤 반드시 사용할 돈은 후반부에 위험을 줄이는 계획을 함께 세웁니다.', '성장·배당·금·원화자금에 나눠 투자합니다.', '자산이 여러 개여서 점검이 필요하고 환율 영향이 남습니다.'],
    C: ['조금 더 오래 기다릴 여유가 있을 때', '5년 후에도 필요하다면 인출을 미룰 수 있고, 큰 하락을 견딜 수 있을 때 검토합니다. 필수 생활자금과 분리해 주세요.', '주식 상승에 더 많이 참여할 수 있습니다.', '주식 비중 70%로 하락 폭이 커질 수 있고 노후 필수자금에는 부담입니다.'],
    D: ['두 종류로 가볍게 시작하는 선택', '여러 상품을 관리하기 어렵다면 S&P500과 원화 안전자금으로 단순하게 운용할 수 있습니다.', '매월 배분과 잔액 관리가 단순합니다.', '위험자산이 미국 주식 한 종류에 집중되며 금·배당 스타일 분산은 없습니다.']
  };
  const input = document.getElementById('monthly-amount');
  let selected = data.plans.find(p => p.id === 'B');
  const number = (value, digits = 0) => new Intl.NumberFormat('ko-KR', { maximumFractionDigits: digits }).format(value);
  const pct = value => (value * 100).toFixed(1);
  const setText = (id, text) => { document.getElementById(id).textContent = text; };
  function chart(plan) {
    const values = plan.wealth.map(v => v * 100);
    const width = 560, height = 175, left = 32, right = 10, top = 13, bottom = 27;
    // Fixed axes across all plans make risk and growth comparisons meaningful.
    const min = 80, max = 240;
    const x = i => left + i / (values.length - 1) * (width - left - right);
    const y = v => top + (max - v) / (max - min) * (height - top - bottom);
    const points = values.map((v, i) => `${x(i).toFixed(2)},${y(v).toFixed(2)}`).join(' ');
    const ticks = [100, 150, 200].map(v => `<line x1="${left}" y1="${y(v)}" x2="${width - right}" y2="${y(v)}" stroke="#e2e5d9" stroke-dasharray="3 4"/><text x="${left - 8}" y="${y(v) + 4}" text-anchor="end">${v}</text>`).join('');
    const area = `${x(0)},${y(min)} ${points} ${x(60)},${y(min)}`;
    document.getElementById('wealth-chart').innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">${plan.name} 목돈 투자 가치 추이</title><desc id="chart-desc">2021년 10월 말 100에서 2026년 10월 말 ${number(values[60], 1)}. 과거 원화 환산 대리분석이며 미래 예상 성과가 아닙니다.</desc><defs><linearGradient id="chart-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#a9bea5" stop-opacity=".4"/><stop offset="100%" stop-color="#a9bea5" stop-opacity="0"/></linearGradient></defs>${ticks}<polygon points="${area}" fill="url(#chart-fill)"/><polyline points="${points}" fill="none" stroke="#28584a" stroke-width="2.3" stroke-linejoin="round"/><circle cx="${x(60)}" cy="${y(values[60])}" r="3" fill="#28584a"/><text x="${left}" y="${height - 6}">2021.10</text><text x="${width - right}" y="${height - 6}" text-anchor="end">2026.10</text></svg>`;
  }
  function updateAmount() {
    const amount = Number(input.value);
    const valid = input.value.trim() !== '' && Number.isFinite(amount) && amount >= 1 && amount <= 10000;
    document.getElementById('amount-error').hidden = valid;
    input.setAttribute('aria-invalid', String(!valid));
    if (!valid) {
      document.querySelectorAll('[data-budget]').forEach(el => { el.textContent = '—'; });
      setText('dca-value', '—');
      setText('dca-principal', '매달 모을 금액을 확인해 주세요');
      return;
    }
    document.querySelectorAll('[data-budget]').forEach(el => {
      el.textContent = `${number(amount * selected.weights[Number(el.dataset.budget)], 1)}만원`;
    });
    setText('dca-value', `${number(selected.dcaFinal / 10000 * amount / 100)}만원`);
    setText('dca-principal', `총납입액 ${number(amount * 60)}만원`);
  }
  function select(id) {
    selected = data.plans.find(p => p.id === id);
    tabs.forEach(tab => {
      const active = tab.dataset.plan === id;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
    });
    document.getElementById('plan-panel').setAttribute('aria-labelledby', `tab-${id}`);
    setText('plan-label', `${id} · ${selected.name}`);
    ['plan-headline', 'plan-description', 'plan-pro', 'plan-con'].forEach((name, i) => setText(name, descriptions[id][i]));
    document.getElementById('allocation-bar').innerHTML = selected.weights.map((w, i) => `<span style="width:${w * 100}%;background:${colors[i]}"></span>`).join('');
    document.getElementById('allocation-list').innerHTML = labels.map((label, i) => `<div class="allocation-row"><span class="name"><span class="swatch" style="background:${colors[i]}" aria-hidden="true"></span>${label}</span><span><b>${number(selected.weights[i] * 100)}%</b><span class="money" data-budget="${i}"></span></span></div>`).join('');
    const stats = [['과거 연복리 수익', selected.metrics.cagr, ''], ['연환산 변동성', selected.metrics.annual_vol, ''], ['월말 최대낙폭', selected.metrics.mdd, 'loss']];
    document.getElementById('stats').innerHTML = stats.map(([label, value, cls]) => `<div class="${cls}"><span class="stat-label">${label}</span><strong class="stat-value">${pct(value)}<small>%</small></strong></div>`).join('');
    chart(selected);
    updateAmount();
  }
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab.dataset.plan));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (i + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (i - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault(); select(tabs[next].dataset.plan); tabs[next].focus();
    });
  });
  input.addEventListener('input', updateAmount);
  select('B');
})();
