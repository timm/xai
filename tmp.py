#!/usr/bin/env python3 -B
"""
six.py: stochastic incremental multi-objective expalanation
(c) 2025 Tim Menzies, MIT license

Options:
   -b bins=7   Number of bins
   -s seed=1   Random number seed
"""
import re,ast,sys,random
from math import log,exp,sqrt
BIG=1e32

#------------------------------------------------------------------------------
# create
def NUM():       return obj(it=NUM,  n=0, mu=0, m2=0, sd=0)
def ROW(lst):    return obj(it=ROW,  raw=lst, bins=lst, y=0)
def DATA(src): 
  src  = iter(src)
  data = obj(it=DATA, rows=[], cols=COLS(next(src)), nums={}, tally={})
  return Data(data,src)

def COLS(names):
  x,y,nums= set(),{},{}
  for c,s in enumerate(names):
    if s[-1] not in "+-X": x.add(c)
    if s[-1]     in "-+" : y[c] = s[-1] != "-"
    if s[0].isupper()    : nums[c] = NUM()
  return obj(it=COLS, names=names, x=x, y=y, nums=nums)

#------------------------------------------------------------------------------
# update
def Data(data, lsts):
  for lst in lsts:
    for c,num in data.cols.nums.items(): Num(num, lst[c])
    data.rows += [ROW(lst)]
  data.n = {}
  for row in data.rows: Row(data, row)
  return data

def Num(num,v):
  if v != "?":
    num.n   += 1
    d       = v - num.mu
    num.mu += d / num.n
    num.m2 += d * (v - num.mu)
    num.sd  = 0 if num.n < 2 else sqrt(max(0, num.m2) / (num.n - 1))

def Row(data, row):
  for c,num in data.cols.nums.items():
    if (v := row.raw[c]) != "?":
      row.bins[c] = v2b(v, num.mu, num.sd)
  row.y = disty(data,row)
  for c in data.cols.x:
    if (v := row.raw[c]) != "?":
      data.tally[(c,v)] = data.tally.get((c,v),0) + row.y

#------------------------------------------------------------------------------
def distx(data, row1, row2):
  def fn(a,b):
    if a==b=="?": return 1
    mid = (the.bins - 1) / 2
    if a=="?": a = (0 if b > mid else the.bins-1)
    if b=="?": b = (0 if a > mid else the.bins -1)
    return abs(a - b) / (the.bins - 1)
  xs = data.cols.x
  return sqrt(sum(fn(row1.bins[c], row2.bins[c])**2 for c in xs) / len(xs))

def disty(data, row):
  ys = data.cols.y.items()
  return sqrt(sum(abs(row.bins[c]/(the.bins-1) - goal) for c,goal in ys) / len(ys))

#-------------------------------------------------------------------------------
class obj(dict):
  __getattr__ = dict.__getitem__; __setattr__ = dict.__setitem__
  def __repr__(i):
    def say(k,v): 
      if isinstance(v,float): return round(v,2)
      return v.__name__ if type(v)==type(disty) else v
    return "{" + " ".join([f":{k} {say(k, i[k])}" for k in i]) + "}"

def era(src, size=20):
  cache = []
  for row in src:
    cache += [row]
    if len(cache) > size: yield shuffle(cache); cache=[]
  if cache: yield shuffle(cache)

def shuffle(lst): random.shuffle(lst); return lst

def v2b(v,mu,sd,eps=1/BIG):
  z = max(-3, min(3, (v-mu) / (sd+eps)))
  return int(the.bins / (1 + exp(-1.7 * z)))

def b2v(b,mu,sd,eps=1/BIG):
  p = min(1-eps, max(eps, b/the.bins))
  return mu + max(-3, min(3, log(p/(1-p))/1.7)) * (sd + 1/BIG)

#------------------------------------------------------------------------------
def config(s=__doc__):
  return obj(**{m[0]:coerce(m[1]) for m in re.findall(r"(\w+)=(\S+)", s)})

def coerce(s):
  try: return ast.literal_eval(s)
  except (ValueError, SyntaxError): return s.strip()

def csv(fileName):
  with open(fileName,encoding="utf-8") as f:
    for l in f:
      if l: yield [coerce(x) for x in l.split(",")]

def cli(funs,d,flags):
  for n, s in enumerate(flags):
    v = coerce(flags[n + 1]) if n < len(flags) - 1 else None
    if f := funs.get(f"go{s.replace('-', '_')}"):
      f(v) if v is not None else f()
    else:
      k = s.lstrip("-")[0]
      if k in d: d[k] = v

def go_h()     : print(__doc__)
def go__the()  : print(the)
def go_s(n)    : the.seed=n; random.seed(n)
def go__bins(_):
  for n in range(90,110):
     b=v2b(n,100,5)
     v=b2v(b,100,5)
     print(n,b,v)

def go__csv(f) : [print(row) for row in csv(f)]
def go__data(f): 
    tally= min(DATA(csv(f)).tally.items(), key=lambda x: x[1])
    print(tally)

#------------------------------------------------------------------------------
the=config()
random.seed(the.seed)
if __name__=="__main__": cli(vars(),the,sys.argv)
