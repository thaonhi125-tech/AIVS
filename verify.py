import math

A = dict(v_trial=13.0, c_trial=22.0, k_foul=0.004, s_foul=0.0015,
         m_weather=0.09, s_weather=0.035, margin_desk=0.05, W_expected=1.2,
         bunker_price=650, target_margin=0.25, comp_spread=0.12, seed=20260835)

ROUTES = [
    dict(name='Santos -> Qingdao',      nm=11800, port_days=5.0, port_costs=185000, coastal=False),
    dict(name='US Gulf -> Rotterdam',   nm=4900,  port_days=4.0, port_costs=140000, coastal=False),
    dict(name='Richards Bay -> Mundra', nm=4100,  port_days=3.5, port_costs=120000, coastal=False),
    dict(name='Vancouver -> Japan',     nm=4300,  port_days=4.0, port_costs=130000, coastal=False),
    dict(name='Newcastle -> Zhoushan',  nm=4400,  port_days=3.5, port_costs=125000, coastal=False),
    dict(name='Tubarao -> Rotterdam',   nm=4600,  port_days=4.0, port_costs=135000, coastal=False),
    dict(name='Paradip -> Kandla',      nm=1900,  port_days=3.0, port_costs=95000,  coastal=True),
    dict(name='New Orleans -> Kobe',    nm=9200,  port_days=5.0, port_costs=175000, coastal=False),
]

MASK = 0xFFFFFFFF
def imul(a, b):
    return ((a & MASK) * (b & MASK)) & MASK

def mulberry32(a):
    state = {'a': a & MASK}
    def rnd():
        state['a'] = (state['a'] + 0x6D2B79F5) & MASK
        t = state['a']
        t = imul(t ^ (t >> 15), 1 | t)
        t = (t + imul(t ^ (t >> 7), 61 | t)) & MASK ^ t
        t &= MASK
        return ((t ^ (t >> 14)) & MASK) / 4294967296
    return rnd

def cost_actual(D, port, h, W):
    v = A['v_trial'] * (1 - A['s_foul']*h - A['s_weather']*W)
    c = A['c_trial'] * (1 + A['k_foul']*h) * (1 + A['m_weather']*W)
    days = D / (24*v); fuel = days*c
    return dict(days=days, fuel=fuel, cost=fuel*A['bunker_price']+port)

def cost_seatrial(D, port):
    days = (D/(24*A['v_trial']))*(1+A['margin_desk'])
    fuel = days*A['c_trial']*(1+A['margin_desk'])
    return dict(days=days, fuel=fuel, cost=fuel*A['bunker_price']+port)

def cost_model(D, port, h):
    v = A['v_trial'] * (1 - A['s_foul']*h - A['s_weather']*A['W_expected'])
    c = A['c_trial'] * (1 + A['k_foul']*h) * (1 + A['m_weather']*A['W_expected'])
    days = D/(24*v); fuel = days*c
    return dict(days=days, fuel=fuel, cost=fuel*A['bunker_price']+port)

def jsround(x):            # match JS Math.round (half-up), not Python banker's rounding
    return math.floor(x + 0.5)

def generate():
    rnd = mulberry32(A['seed'])
    vs = []
    for i in range(10):
        r = ROUTES[int(rnd()*len(ROUTES))]     # int() == Math.floor for positive
        cargo = 30000 + jsround(rnd()*8000)
        h = jsround(8 + rnd()*46)
        W = 0.5 + rnd()*1.5
        noise = -A['comp_spread'] + rnd()*2*A['comp_spread']
        act = cost_actual(r['nm'], r['port_costs'], h, W)
        st = cost_seatrial(r['nm'], r['port_costs'])
        md = cost_model(r['nm'], r['port_costs'], h)
        fair = (act['cost']/cargo)*(1+A['target_margin'])
        competitor = fair*(1+noise)
        st_quote = (st['cost']/cargo)*(1+A['target_margin'])
        md_quote = (md['cost']/cargo)*(1+A['target_margin'])
        def outcome(quote, estcost, estdays):
            revenue = quote*cargo
            return dict(win=quote<=competitor, quote=quote,
                        estTCE=(revenue-estcost)/(estdays+r['port_days']),
                        realTCE=(revenue-act['cost'])/(act['days']+r['port_days']),
                        realProfit=revenue-act['cost'])
        vs.append(dict(route=r['name'], nm=r['nm'], cargo=cargo, h=h, W=round(W,2),
                       competitor=competitor,
                       seaTrial=outcome(st_quote, st['cost'], st['days']),
                       model=outcome(md_quote, md['cost'], md['days'])))
    return vs

def summarize(vs, key):
    won=profit=gap=0; n=0
    for v in vs:
        if v[key]['win']:
            won+=1; profit+=v[key]['realProfit']
            gap+=v[key]['estTCE']-v[key]['realTCE']; n+=1
    return dict(won=won, profit=profit, avgGap=gap/n if n else 0)

vs = generate()
print('VOYAGES (seed %d)' % A['seed'])
for i,v in enumerate(vs):
    ok = (not v['seaTrial']['win']) or v['seaTrial']['realTCE'] < v['seaTrial']['estTCE']
    print('%2d. %-22s h=%2d W=%.2f | ST win=%s estTCE=%6d realTCE=%7d %s | MD win=%s' % (
        i+1, v['route'], v['h'], v['W'],
        'Y' if v['seaTrial']['win'] else 'n',
        round(v['seaTrial']['estTCE']), round(v['seaTrial']['realTCE']),
        'OK' if ok else '*** FAIL ***',
        'Y' if v['model']['win'] else 'n'))

st=summarize(vs,'seaTrial'); md=summarize(vs,'model')
print('\nSEA TRIAL : won %d/10  profit $%s  avgGap $%d/day' % (st['won'], format(round(st['profit']),','), round(st['avgGap'])))
print('MODEL     : won %d/10  profit $%s  avgGap $%d/day' % (md['won'], format(round(md['profit']),','), round(md['avgGap'])))
allok = all((not v['seaTrial']['win']) or v['seaTrial']['realTCE']<v['seaTrial']['estTCE'] for v in vs)
print('\nCHECK invariant realised<estimated (ST won): %s' % ('PASS' if allok else 'FAIL'))
print('CHECK model wins fewer: %s' % ('PASS' if md['won']<st['won'] else 'FAIL'))
print('CHECK model earns more: %s' % ('PASS' if md['profit']>st['profit'] else 'FAIL'))
