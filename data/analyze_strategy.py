"""Reproduce five-year proxy analysis. Python 3.11 and numpy only; no network.

Input values are rounded observations transcribed from identified webpages.
Outputs are proxy calculations, NOT actual domestic ETF or investor returns.
"""
from pathlib import Path
import json
import hashlib
import itertools
import calendar
import numpy as np

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'monthly_inputs.json'
J = json.loads(RAW.read_text(encoding='utf-8'))
NAMES = list(J['returns_percent'])
assert NAMES == ['SPY', 'QQQ', 'SCHD', 'GLD']
ALL_MONTHS = [f'{y}-{m:02d}' for y in range(2021, 2027)
              for m in range(1, len(J['fx_close'][str(y)]) + 1)]
ALL_USD = np.array([sum(J['returns_percent'][a].values(), []) for a in NAMES]).T / 100
FX_LEVELS = np.array(sum(J['fx_close'].values(), []))
DATES = ALL_MONTHS[10:]
USD = ALL_USD[10:]
FX = FX_LEVELS[10:] / FX_LEVELS[9:-1] - 1
KRW = (1 + USD) * (1 + FX[:, None]) - 1
assert KRW.shape == (60, 4) and len(DATES) == 60
assert DATES[0] == '2021-11' and DATES[-1] == '2026-10'
assert np.all(np.isfinite(KRW)) and np.min(KRW) > -1
assert np.allclose(np.prod(1 + KRW, axis=0),
                   np.prod(1 + USD, axis=0) * FX_LEVELS[-1] / FX_LEVELS[9])


def metrics(r):
    r = np.asarray(r)
    wealth = np.r_[1, np.cumprod(1 + r)]
    dd = wealth / np.maximum.accumulate(wealth) - 1
    t = int(np.argmin(dd))
    peak = int(np.argmax(wealth[:t + 1]))
    recovered = np.where(wealth[t + 1:] >= wealth[peak])[0]
    return dict(cumulative=float(wealth[-1] - 1),
                cagr=float(wealth[-1] ** (12 / len(r)) - 1),
                annual_vol=float(np.std(r, ddof=1) * np.sqrt(12)),
                mdd=float(np.min(dd)), worst_month=float(np.min(r)),
                positive_months=int(np.sum(r > 0)),
                peak_index=peak, trough_index=t,
                recovery_index=int(t + 1 + recovered[0]) if len(recovered) else None)


WEIGHTS = {
    'A_안정우선': [.25, 0, .15, .10, .50],
    'B_균형적립': [.30, .05, .15, .10, .40],
    'C_성장강화': [.40, .15, .15, .10, .20],
    'D_단순2종': [.60, 0, 0, 0, .40],
    'E_주식집중비교': [.50, .50, 0, 0, 0],
}


def simulate(risky, weights, cash_annual=0., drag_annual=0., contribution=0., rebalance=True):
    """Start-of-month contributions; end-of-every-12-month rebalance.

    Return series belongs to unit portfolio before external contributions.
    Initial holdings zero for DCA, one unit for lump sum.
    Drag is additional annualized stress on risky assets, not actual tax.
    """
    w = np.array(weights, dtype=float)
    assert np.isclose(w.sum(), 1) and np.all(w >= 0)
    cash_r = (1 + cash_annual) ** (1/12) - 1
    r = np.c_[risky, np.full(len(risky), cash_r)]
    r[:, :4] = (1 + r[:, :4]) * (1 - drag_annual) ** (1/12) - 1
    holdings = np.zeros(5) if contribution else w.copy()
    portfolio_returns, turnover, values = [], [], []
    contributions = []
    for t, rr in enumerate(r):
        if contribution:
            holdings += contribution * w
            contributions.append(contribution)
        before = holdings.sum()
        holdings *= 1 + rr
        total = holdings.sum()
        portfolio_returns.append(total / before - 1)
        if rebalance and (t + 1) % 12 == 0 and t < len(r) - 1:
            # One-way sell volume, as fraction of portfolio, not sum of buys+sells.
            turnover.append(float(np.abs(holdings - total*w).sum() / (2*total)))
            holdings = total*w
        values.append(float(total))
    return np.array(portfolio_returns), values, turnover


def periodic_irr(ending, monthly=1_000_000, n=60):
    # Contributions are at t=0,1,...,n-1 and ending value at t=n.
    low, high = -.95, 10.
    for _ in range(150):
        mid = (low+high)/2
        implied = sum(monthly * (1+mid)**((n-t)/12) for t in range(n))
        if implied > ending:
            high = mid
        else:
            low = mid
    return (low+high)/2


def goal_glide(contribution=0.):
    """B weights for years 1-3; risky budget 45%, 30% for years 4,5."""
    base=np.array(WEIGHTS['B_균형적립'])
    h=np.zeros(5) if contribution else base.copy()
    ret=[];values=[]
    for t, rr in enumerate(np.c_[KRW,np.zeros(60)]):
        factor=1. if t<36 else (.75 if t<48 else .5)
        w=base.copy();w[:4]*=factor;w[4]=1-w[:4].sum()
        if t>0 and t%12==0:h=h.sum()*w
        if contribution:h+=contribution*w
        before=h.sum();h*=1+rr
        ret.append(h.sum()/before-1);values.append(float(h.sum()))
    return np.array(ret),values


COV = np.cov(KRW, rowvar=False, ddof=1)
CORR = np.corrcoef(KRW, rowvar=False)
assert np.allclose(CORR, CORR.T) and np.allclose(np.diag(CORR), 1)
assert np.min(np.linalg.eigvalsh(COV)) > -1e-12
assets = {a: dict(krw=metrics(KRW[:, i]), usd=metrics(USD[:, i])) for i,a in enumerate(NAMES)}
portfolios = {}
for name, w in WEIGHTS.items():
    r, values, turnover = simulate(KRW, w)
    dr, dv, _ = simulate(KRW, w, contribution=1_000_000)
    risk_w = np.array(w[:4])
    variance = risk_w @ COV @ risk_w
    risk_share = risk_w * (COV @ risk_w) / variance
    corr1 = np.corrcoef(KRW[:36], rowvar=False)
    portfolios[name] = dict(weights=w, metrics=metrics(r),
        dca_final=dv[-1], dca_profit_ratio=dv[-1]/60_000_000-1,
        dca_annual_irr=periodic_irr(dv[-1]),
        static_annual_vol=float(np.sqrt(variance*12)),
        risk_share=risk_share.tolist(), annual_turnover=turnover,
        early36=metrics(simulate(KRW[:36],w)[0]),
        later24=metrics(simulate(KRW[36:],w)[0]),
        no_rebalance=metrics(simulate(KRW,w,rebalance=False)[0]),
        cash2=metrics(simulate(KRW,w,cash_annual=.02)[0]),
        drag05=metrics(simulate(KRW,w,drag_annual=.005)[0]),
        monthly_returns=r.tolist(), wealth=[1.]+values)

# Risk-only diversification comparisons at the same risky budget.
comparisons={
    'SPY100': [1,0,0,0,0],
    'SPY50_QQQ50': [.5,.5,0,0,0],
    'SPY50_SCHD50': [.5,0,.5,0,0],
    'SPY80_GLD20': [.8,0,0,.2,0],
    'SPY60_SCHD20_GLD20': [.6,0,.2,.2,0]
}
comparison_results={k:metrics(simulate(KRW,w)[0]) for k,w in comparisons.items()}

# 6-month circular moving-block bootstrap: diagnostic interval, not a forecast.
rng = np.random.default_rng(20261108)
boots=[]
for _ in range(2000):
    starts=rng.integers(0,60,size=10)
    ix=np.concatenate([(s+np.arange(6))%60 for s in starts])
    boots.append(np.corrcoef(KRW[ix],rowvar=False))
ci=np.quantile(np.array(boots),[.025,.975],axis=0)
pairs=[]
for i in range(4):
    for k in range(i+1,4):
        rolling=[np.corrcoef(KRW[t-12:t,i],KRW[t-12:t,k])[0,1] for t in range(12,61)]
        pairs.append(dict(pair=[NAMES[i],NAMES[k]],corr=float(CORR[i,k]),
            bootstrap_low=float(ci[0,i,k]),bootstrap_high=float(ci[1,i,k]),
            rolling12_min=float(min(rolling)),rolling12_max=float(max(rolling)),
            early36=float(np.corrcoef(KRW[:36],rowvar=False)[i,k]),
            later24=float(np.corrcoef(KRW[36:],rowvar=False)[i,k])))

# Grid diagnostic, not a future-optimal portfolio: long-only risky assets.
def grid(cov, returns):
    candidates=[]
    for units in itertools.product(range(21),repeat=3):
        last=20-sum(units)
        if last<0:continue
        w=np.r_[units,last]/20
        if w[0]<.20 or w[1]>.20 or w[2]>.60 or w[3]>.20:continue
        vol=float(np.sqrt(w@cov@w*12))
        arith=float(np.mean(returns,axis=0)@w*12)
        candidates.append((vol,arith/vol,w))
    return min(candidates,key=lambda x:x[0]),max(candidates,key=lambda x:x[1]),len(candidates)
gmin,gmax,count=grid(COV,KRW)
gtrain,_,_=grid(np.cov(KRW[:36],rowvar=False),KRW[:36])
grid_results=dict(step=.05,count=count,
    min_variance=dict(weights=gmin[2].tolist(),vol=gmin[0],
        backtest=metrics(simulate(KRW,np.r_[gmin[2],0])[0])),
    max_mean_vol=dict(weights=gmax[2].tolist(),score=gmax[1]),
    first36_minvar=dict(weights=gtrain[2].tolist(),
        later24=metrics(simulate(KRW[36:],np.r_[gtrain[2],0])[0])))

# Rounding sensitivity: every observed monthly input can vary +/- 0.05pp.
sens=[]
for _ in range(1000):
    pert=(1+USD+rng.uniform(-.0005,.0005,size=USD.shape))*(1+FX[:,None])-1
    sens.append([np.corrcoef(pert,rowvar=False)[i,k] for i,k in [(0,1),(0,2),(0,3)]])
rounding=np.quantile(sens,[.025,.975],axis=0)

# Cross-check same 60 months to official quarterly USD NAV: 2021-10..2026-09.
official={'QQQ':.1633,'SCHD':.0948,'GLD':.1862}
checks={}
for a,v in official.items():
    rr=ALL_USD[9:-1,NAMES.index(a)]
    calc=float(np.prod(1+rr)**.2-1)
    checks[a]=dict(start='2021-10',end='2026-09',computed=calc,official_nav=v,
                   difference_pp=(calc-v)*100)
    # Large discrepancy stops publication; small difference is disclosed, not calibrated away.
    assert abs(calc-v)<.005, (a,calc,v)

result=dict(period=dict(start='2021-10-31',end='2026-10-31',monthly_count=60,
    first_return='2021-11',last_return='2026-10'),
    input_sha256=hashlib.sha256(RAW.read_bytes()).hexdigest(),
    assets=assets,correlation_krw=CORR.tolist(),correlation_usd=np.corrcoef(USD,rowvar=False).tolist(),
    covariance_annual=(COV*12).tolist(),pairs=pairs,portfolios=portfolios,
    comparisons=comparison_results,grid=grid_results,official_checks=checks,
    rounding_corr_interval=rounding.tolist(),
    fx_cumulative=float(FX_LEVELS[-1]/FX_LEVELS[9]-1),
    rounding_wealth_relative_bound=[float((1-.0005/(1+USD)).prod(axis=0).min()-1),
        float((1+.0005/(1+USD)).prod(axis=0).max()-1)])
glide_r,glide_values=goal_glide()
_,glide_dca=goal_glide(1_000_000)
result['goal_glide']=dict(metrics=metrics(glide_r),dca_final=glide_dca[-1],
    dca_annual_irr=periodic_irr(glide_dca[-1]),
    final_weights=[.15,.025,.075,.05,.70])
(ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'monthly_krw_returns.json').write_text(json.dumps(dict(months=DATES,assets=NAMES,
    returns_krw=KRW.tolist(),returns_usd=USD.tolist(),fx_returns=FX.tolist()),indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k in ['assets','correlation_krw','comparisons','grid','official_checks']},ensure_ascii=True,indent=2))
print('PORTFOLIOS')
for name,p in portfolios.items():
    print(name.encode('unicode_escape').decode(), json.dumps({k:p[k] for k in
        ['weights','metrics','dca_final','dca_annual_irr','risk_share','early36','later24','cash2','drag05']},ensure_ascii=True))
