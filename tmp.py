#!/usr/bin/env python3 -B
"""
six.py: stochastic incremental multi-objective expalanation
(c) 2025 Tim Menzies, MIT license

Options:
   -b bins=7   Number of bins
   -l leaf=2   Min examples in leaf of tree
   -s seed=1   Random number seed
"""
import re,sys,random
from math import log,exp,sqrt
BIG=1e32

#-------------------------------------------------------------------------------
# UPPER CASE functions are constructors
def COL(at=0, txt=" "): return dict(txt=txt, at=at, n=0, goal=txt[-1]!="-")
def NUM(**d):           return obj(**COL(**d), mu=0, m2=0, symp=True)
def SYM(**d):           return obj(**COL(**d), has={}, symp=False)
def ROW(lst):           return obj(raw=lst, bins=lst[:], y=0)
def DATA(src):
  src = iter(src)
  return Data(obj(rows=[], cols=COLS(next(src)), tally={}), src)

def COLS(names):
  cols= [(NUM if s[0].isupper() else SYM)(at=n,txt=s) for n,s in enumerate(names)]
  return obj(names=names, all=cols,
             x= [c for c in cols if c.txt[-1] not in "-+X"],
             y= [c for c in cols if c.txt[-1]     in "-+" ])

#-------------------------------------------------------------------------------
# update
# BUG discureize using outer
def Data(data, lsts=None):
  for lst in lsts or []:
    lst = [add(col,v) for col,v in zip(data.cols.all,lst)]
    data.rows += [ ROW(lst) ]
  for row in data.rows:
    row.y = disty(data,row)
    row.bins = [discretize(col,v) for col,v in zip(data.cols.all, row.raw)]
  data.tally = tally(data)
  return data

def add(col,v):
  if v != "?": return v
  col.n += 1
  if col.symp:
    col.has[v] = 1 + col.has.get(v,0)
  else:
    d = v-col.mu; col.mu += d/col.n; col.m2 += d*(v - col.mu)
  return v

def discretize(col,v):
  return v=="?" and v or v if col.symp else int(the.bins * norm(col,v))

def tally(data):
  d={}
  for row in data.rows:
    for b,col in zip(row.bins, data.cols.x):
      k = (col.at, b)
      if k not in d: d[k] = NUM()
      add(d[k], row.y)
  return d

#-------------------------------------------------------------------------------
# query
def centroids(data): return [centroid(col) for col in data.cols.all]
def centroid(col):   return max(col.has, key=col.has.get) if col.symp else col.mu

def spread(col): return ent(col) if col.symp else sd(col)

def sd(num):  return 0 if num.n < 2 else sqrt(num.m2 / (num.n - 1))
def ent(sym): return -sum(p*log(p,2) for n in sym.has.values() if (p:=n/sym.n)>0)

def score(num):
  return BIG if num.n < the.leaf else num.mu + num.sd /(sqrt(num.n) + 1/BIG)

def disty(data, row):
  ys = data.cols.y
  return sqrt(sum(abs(norm(y,row.raw[y.at]) - y.goal) for y in ys) / len(ys))

def norm(num,v):
  z = max(-3, min(3, (v - num.mu) / (num.sd + 1/BIG)))
  return 1 / (1 + exp(-1.7 * z))

def b2v(num,b): # inverse normalization
  eps = 1/BIG
  p = min(1 - eps, max(eps, b/the.bins))
  return num.mu + max(-3, min(3, log(p / (1 - p)) / 1.7)) * (num.sd + eps)

#-------------------------------------------------------------------------------
# tree
def Tree(data, rows=None, uses=set()):
  kids, rows = {}, rows or data.rows
  col, b, data1 = None, None, Data([data.cols.names]+rows)
  if len(rows) > the.leaf*2:
    if cut := bestcut(data1):
      (col,b), _ = cut
      ok,no = [],[]
      for r in rows: (ok if r.bins[col]==b else no).append(r)
      if ok and no:
        uses.add(col)
        kids[True]  = Tree(data, ok, uses)
        kids[False] = Tree(data, no, uses)
  return obj(data=data1, kids=kids, col=col, bin=b,
             mu= sum(row.y for row in rows) / len(rows),
             mids= centroids(data1))

def bestcut(data):
  return min(data.tally.items(), key=lambda x: score(x[1]), default=None)

def treeLeaf(tree, row):
  if tree.kids:
    return treeLeaf(tree.kids[row.bins[tree.col]==tree.bin], row)
  return tree

def treeShow(t, lvl=0, cut=".", w=60):
  if lvl==0:
    print(f"{'':{w}}  score    N    Goals\n{'':{w}}  -----  ----   -----")
  print(f"{('| '*(lvl-1)+cut):{w}}: ",end="")
  print(f"{o(t.mu):6} : {len(t.data.rows):4} : {o(t.mids)}")
  if t.kids:
    col = t.data.cols.names[t.col]
    for k in sorted(t.kids, reverse=True):
      treeShow(t.kids[k], lvl+1, f"{col} {'==' if k else '!='} {t.bin}", w)

#------------------------------------------------------------------------------
# lib
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

def cast(s, FUN=(int, float), BOOL={"true": True, "false": False}):
  for fn in FUN:
    try: return fn(s)
    except ValueError: pass
  return BOOL.get(s, s)

def csv(fileName):
  with open(fileName, encoding="utf-8") as f:
    for l in f:
      l = re.sub(r'\s+', '', l.split("#")[0]) # no whitespace, skip comments
      if l:
        yield [cast(x) for x in l.split(",")]

#-------------------------------------------------------------------------------
# cli
def config(s=__doc__):
  return obj(**{m[0]:cast(m[1]) for m in re.findall(r"(\w+)=(\S+)", s)})

def cli(funs,d,flags):
  for n, s in enumerate(flags):
    v = cast(flags[n + 1]) if n < len(flags) - 1 else None
    if f := funs.get(f"go{s.replace('-', '_')}"): f(v)
    elif (k := s.lstrip("-")[0]) in d: d[k] = v

# need an sd and ent test
def go_h(_)    : print(__doc__)
def go__the(_) : print(the)
def go_s(n)    : the.seed=n; random.seed(n)
def go__csv(f) : [print(row) for row in list(csv(f))[::40]]
def go__ys(f):
    data = DATA(csv(f))
    print(*data.cols.names)
    [print(row) for row in sorted(data.rows, key=lambda r: disty(data,r))[::40]]

def go__tally(f):
  data = DATA(csv(f))
  for (c,b),num in sorted(data.tally.items(), key=lambda x: score(x[1])):
    print(obj(name=data.cols.names[c], bins=b, mu=num.mu, sd=num.sd, n=num.n))

#------------------------------------------------------------------------------
the = config()
random.seed(the.seed)
print(NUM(at=2, txt="Sss"))
if __name__=="__main__": cli(vars(),the,sys.argv)
