#!/usr/bin/env python3 -B
"""
six.py: stochastic incremental multi-objective expalanation
(c) 2025 Tim Menzies, MIT license

Options:
   -b bins=7   Number of bins
   -l leaf=2   Min examples in leaf of tree
   -s seed=1   Random number seed

"""
import re,ast,sys,random
from math import log,exp,sqrt
BIG=1e32

#------------------------------------------------------------------------------
# create
def NUM():       return obj(it=NUM,  n=0, mu=0, m2=0, sd=0)
def ROW(lst):    return obj(it=ROW,  raw=lst, bins=lst[:], y=0)
def DATA(src): 
  src  = iter(src)
  data = obj(it=DATA, rows=[], cols=COLS(next(src)), tally={})
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
  data.tally = {}
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
      row.bins[c] = int(the.bins * norm(num,v))
  row.y = disty(data, row)
  for c in data.cols.x:
    if (v := row.bins[c]) != "?":
      k = (c,v)
      if k not in data.tally: data.tally[k] = NUM()
      Num(data.tally[k], row.y)

def score(num): 
  return BIG if num.n < the.leaf else num.mu + num.sd /(sqrt(num.n) + 1/BIG)

def disty(data, row):
  raw, nums, ys = row.raw, data.cols.nums, data.cols.y.items()
  return sqrt(sum(abs(norm(nums[c],raw[c]) - goal) for c,goal in ys) / len(ys))

def norm(num,v): # converts v to an integer 0..the.bins-1
  z = max(-3, min(3, (v-num.mu) / (num.sd+1/BIG)))
  return 1 + exp(-1.7 * z)

def b2v(b,mu,sd): # converts b to a real number (lower bound on each bin)
  eps = 1/BIG
  p = min(1-eps, max(eps, b/the.bins))
  return mu + max(-3, min(3, log(p/(1-p))/1.7)) * (sd + eps)

#-------------------------------------------------------------------------------
def o(v):
  if isinstance(v, float): return round(v, 2)
  if isinstance(v, (list, tuple, set)): return [o(x) for x in v]
  if isinstance(v, dict):
    return "[" + " ".join([f":{k} {o(val)}" for k, val in v.items()]) + "]"
  if hasattr(v, '__name__'): return v.__name__
  if hasattr(v, '__dict__'): return f"{type(v).__name__}{o(vars(v))}"
  return v

class obj(dict):
  __getattr__, __setattr__, __repr__ = dict.__getitem__, dict.__setitem__, o

def era(src, size=20):
  cache = []
  for row in src:
    cache += [row]
    if len(cache) > size: yield shuffle(cache); cache=[]
  if cache: yield shuffle(cache)

def shuffle(lst): random.shuffle(lst); return lst

def coerce(s):
  try: return ast.literal_eval(s)
  except (ValueError, SyntaxError): return s.strip()

def csv(fileName):
  with open(fileName,encoding="utf-8") as f:
    for l in f:
      if l: yield [coerce(x) for x in l.split(",")]

def config(s=__doc__):
  return obj(**{m[0]:coerce(m[1]) for m in re.findall(r"(\w+)=(\S+)", s)})

def cli(funs,d,flags):
  for n, s in enumerate(flags):
    v = coerce(flags[n + 1]) if n < len(flags) - 1 else None
    if f := funs.get(f"go{s.replace('-', '_')}"): f(v)
    elif (k := s.lstrip("-")[0]) in d: d[k] = v

def go_h(_)    : print(__doc__)
def go__the(_) : print(the)
def go_s(n)    : the.seed=n; random.seed(n)
def go__csv(f) : [print(row) for row in csv(f)]
def go__ys(f): 
    data = DATA(csv(f))
    print(*data.cols.names)
    [print(row) for row in sorted(data.rows, key=lambda r: disty(data,r))[::40]]

def go__tally(f): 
    print(o(min(DATA(csv(f)).tally.items(), key=lambda x: score(x[1]))))

#------------------------------------------------------------------------------
the = config()
random.seed(the.seed)
if __name__=="__main__": cli(vars(),the,sys.argv)
