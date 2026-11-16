"""Offline ten-year ordinary-account scenario. Requires Python 3.11 + numpy.
Tax assumptions approximate withholding; this is not actual tax-NAV accounting.
"""
from pathlib import Path
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parent
RAW=ROOT/'monthly_inputs.json'
J=json.loads(RAW.read_text(encoding='utf-8'))
NAMES=['SPY','QQQ','SCHD','GLD']; N=120; MONTHLY=2_000_000; PRINCIPAL=N*MONTHLY
DATES=[f'{y}-{m:02}' for y in range(2016,2027) for m in range(1,len(J['fx_close'][str(y)])+1)][10:]
FX_LEVELS=np.array([x for y in range(2016,2027) for x in J['fx_close'][str(y)]])
ALL_USD=np.array([[x for y in range(2016,2027) for x in J['returns_percent'][a][str(y)]] for a in NAMES]).T/100
USD=ALL_USD[10:]; FX=FX_LEVELS[10:]/FX_LEVELS[9:-1]-1
KRW=(1+USD)*(1+FX[:,None])-1
assert KRW.shape==(N,4) and DATES[0]=='2016-11' and DATES[-1]=='2026-10'
assert np.allclose(np.prod(1+KRW,axis=0),np.prod(1+USD,axis=0)*FX_LEVELS[-1]/FX_LEVELS[9])
CASH_GROSS=.02; RET=np.c_[KRW,np.full(N,(1+CASH_GROSS)**(1/12)-1)]
WEIGHTS={'A_안정우선':[.30,0,.05,.10,.55],'B_균형적립':[.45,.05,.05,.10,.35],
 'C_성장강화':[.55,.15,.05,.10,.15],'D_단순2종':[.65,0,0,0,.35],'E_주식집중비교':[.5,.5,0,0,0]}
YIELDS=np.array([.013,.006,.033,0,0])/12
TRADE_FEES=np.array([.00015,.00015,.00015,.0033,0])
EXTRA_DRAG=.001
def metrics(r):
 r=np.array(r);v=np.r_[1,np.cumprod(1+r)]
 return dict(cumulative=float(v[-1]-1),cagr=float(v[-1]**(12/len(r))-1),annual_vol=float(np.std(r,ddof=1)*np.sqrt(12)),
  mdd=float(np.min(v/np.maximum.accumulate(v)-1)),worst_month=float(r.min()))
def irr(ending):
 lo,hi=-.99,10.
 for _ in range(150):
  mid=(lo+hi)/2
  if sum(MONTHLY*(1+mid)**((N-t)/12) for t in range(N))>ending:hi=mid
  else:lo=mid
 return (lo+hi)/2
def purchases(h,budget,w):
 deficit=np.maximum((h.sum()+budget)*w-h,0)
 return budget*deficit/deficit.sum() if budget else np.zeros(5)
def model(w,withholding=.154,fees=True,extra_drag=EXTRA_DRAG,annual_rebalance=False,return_matrix=RET,glide=False):
 h=np.zeros(5);basis=np.zeros(5);values=[];income={};taxes=0.;trades=0.;rtax=0.;rs=[]
 def book(t,amount):
  year=DATES[t][:4];income[year]=income.get(year,0.)+float(amount)
 rates=TRADE_FEES if fees else np.zeros(5)
 for t,rr in enumerate(return_matrix):
  target=np.array(w,dtype=float)
  if glide and t>=84:
   target[:4]*=.75 if t<108 else .5;target[4]=1-target[:4].sum()
  buy=purchases(h,MONTHLY,target);fee=buy*rates;h+=buy-fee;basis+=buy-fee;trades+=float(fee.sum());before=h.sum()
  div=h*YIELDS;interest=h[4]*max(rr[4],0);book(t,div[:3].sum()+interest)
  dt=div*withholding;it=interest*withholding
  h=h*(1+rr)-div;h[:3]*=(1-extra_drag)**(1/12)
  h+=div-dt;basis+=div-dt;h[4]-=it;basis[4]=h[4];taxes+=float(dt.sum()+it)
  rs.append(float(h.sum()/before-1))
  if annual_rebalance and (t+1)%12==0 and t<N-1:
   sell=np.maximum(h-h.sum()*target,0);frac=np.divide(sell,h,out=np.zeros(5),where=h>0)
   gain=np.maximum(h[:3]-basis[:3],0)*frac[:3];tax=float(gain.sum()*withholding);book(t,gain.sum())
   sf=sell*rates;basis*=1-frac;h-=sell;pool=float((sell-sf).sum()-tax)
   trades+=float(sf.sum());taxes+=tax;rtax+=tax
   buy=purchases(h,pool,target);fee=buy*rates;h+=buy-fee;basis+=buy-fee;trades+=float(fee.sum())
  values.append(float(h.sum()))
 gain=np.maximum(h[:3]-basis[:3],0);tt=float(gain.sum()*withholding);tf=float((h*rates).sum())
 terminal_income=dict(income);terminal_income[DATES[-1][:4]]+=float(gain.sum())
 return dict(mark_to_market=float(h.sum()),after_withholding=float(h.sum()-tt-tf),terminal_tax=tt,terminal_fees=tf,
  paid_tax=taxes,paid_fees=trades,realized_rebalance_tax=rtax,unrealized_taxable_gain=float(gain.sum()),
  income_by_calendar_year=income,liquidation_income_by_year=terminal_income,max_regular_annual_income=max(income.values()),
  max_liquidation_annual_income=max(terminal_income.values()),terminal_weights=(h/h.sum()).tolist(),wealth=values,metrics=metrics(rs))
assets={a:dict(krw=metrics(KRW[:,i]),usd=metrics(USD[:,i]),trailing={str(y):dict(krw=metrics(KRW[-12*y:,i]),usd=metrics(USD[-12*y:,i])) for y in [1,5,10]}) for i,a in enumerate(NAMES)}
COV=np.cov(KRW,rowvar=False,ddof=1);CORR=np.corrcoef(KRW,rowvar=False);portfolios={}
for name,w in WEIGHTS.items():
 w=np.array(w);h=w.copy();rs=[];wealth=[1.]
 for t,rr in enumerate(RET):
  before=h.sum();h*=1+rr;rs.append(float(h.sum()/before-1));wealth.append(float(h.sum()))
  if (t+1)%12==0 and t<N-1:h=h.sum()*w
 est=model(w);ref=model(w,0,False,0);annual=model(w,annual_rebalance=True);rw=w[:4];var=float(rw@COV@rw)
 portfolios[name]=dict(weights=w.tolist(),metrics=metrics(rs),wealth=wealth,dca_final=est['after_withholding'],dca_annual_irr=irr(est['after_withholding']),
  reference=ref,tax_estimate=est,annual_rebalance=annual,cost_drag0=model(w,extra_drag=0)['after_withholding'],cost_drag05=model(w,extra_drag=.005)['after_withholding'],
  risk_share=(rw*(COV@rw)/var).tolist(),early60=metrics(rs[:60]),later60=metrics(rs[60:]),
  stress_loss=float(rw@np.array([-.4,-.5,-.35,-.2])),
  additional_tax_sensitivity={str(rate):float(max(est['max_liquidation_annual_income']-20_000_000,0)*rate) for rate in [.11,.231]},
  cash0_final=model(w,return_matrix=np.c_[KRW,np.zeros(N)])['after_withholding'])
rng=np.random.default_rng(20261116);boots=[]
for _ in range(2000):
 ix=np.concatenate([(s+np.arange(6))%N for s in rng.integers(0,N,size=20)])
 boots.append(np.corrcoef(KRW[ix],rowvar=False))
ci=np.quantile(boots,[.025,.975],axis=0);pairs=[]
for i in range(4):
 for k in range(i+1,4):
  rolling=[np.corrcoef(KRW[t-24:t,i],KRW[t-24:t,k])[0,1] for t in range(24,N+1)]
  pairs.append(dict(pair=[NAMES[i],NAMES[k]],corr=float(CORR[i,k]),bootstrap_low=float(ci[0,i,k]),bootstrap_high=float(ci[1,i,k]),rolling24_min=float(min(rolling)),rolling24_max=float(max(rolling)),early60=float(np.corrcoef(KRW[:60],rowvar=False)[i,k]),later60=float(np.corrcoef(KRW[60:],rowvar=False)[i,k])))
checks={}
for a,official in {'QQQ':.1633,'SCHD':.0948,'GLD':.1862}.items():
 calc=float(np.prod(1+ALL_USD[-61:-1,NAMES.index(a)])**.2-1)
 checks[a]=dict(start='2021-10',end='2026-09',computed=calc,official_nav=official,difference_pp=(calc-official)*100)
 assert abs(calc-official)<.005
forward={str(r):sum(MONTHLY*(1+r)**((N-t)/12) for t in range(N)) for r in [-.02,0,.03,.05,.07]}
assert abs(forward['0']-PRINCIPAL)<.01
for w in WEIGHTS.values():
 h=np.zeros(5)
 for rr in RET:h=(h+purchases(h,MONTHLY,np.array(w)))*(1+rr)
 assert np.isclose(model(w,0,False,0)['mark_to_market'],h.sum())
 assert model(w)['after_withholding']<=model(w,0,False,0)['after_withholding']
assert np.allclose(CORR,CORR.T) and np.allclose(np.diag(CORR),1) and min(np.linalg.eigvalsh(COV))>-1e-12
glide=model(WEIGHTS['B_균형적립'],glide=True)
result=dict(period=dict(start='2016-10-31',end='2026-10-31',monthly_count=N,first_return=DATES[0],last_return=DATES[-1]),account='ordinary taxable brokerage',
 monthly_contribution=MONTHLY,principal=PRINCIPAL,input_sha256=hashlib.sha256(RAW.read_bytes()).hexdigest(),cash_gross_assumption=CASH_GROSS,
 assets=assets,correlation_krw=CORR.tolist(),correlation_usd=np.corrcoef(USD,rowvar=False).tolist(),covariance_annual=(COV*12).tolist(),pairs=pairs,portfolios=portfolios,official_checks=checks,
 forward_net_scenarios=forward,goal_glide=dict(metrics=glide['metrics'],dca_final=glide['after_withholding'],final_weights=glide['terminal_weights']),fx_cumulative=float(FX_LEVELS[-1]/FX_LEVELS[9]-1))
(ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'monthly_krw_returns.json').write_text(json.dumps(dict(months=DATES,assets=NAMES,returns_krw=KRW.tolist(),returns_usd=USD.tolist(),fx_returns=FX.tolist()),indent=2),encoding='utf-8')
print(json.dumps(dict(correlation=CORR.tolist(),plans={k:dict(gross=v['reference']['mark_to_market'],net=v['dca_final'],metrics=v['metrics'],income=v['tax_estimate']['max_liquidation_annual_income']) for k,v in portfolios.items()},forward=forward),ensure_ascii=True,indent=2))
