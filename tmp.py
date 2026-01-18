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

#-------------------------------------------------------------------------------
# create
def COL(at=0, txt=" "): return dict(txt=txt, at=0, n=0, goal=txt[-1]!="-")
def NUM(**d):           return obj(**COL(**d), mu=0, m2=0, symp=True)
def SYM(**d):           return obj(**COL(**d), has={}, symp=False)
def ROW(lst):           return obj(raw=lst, bins=lst[:], y=0)
def DATA(src): 
  src = iter(src)
  return Data(obj(rows=[], cols=COLS(next(src)), tally={}), src)

def COLS(names):
  cols= [(NUM if s[0].isupper() else SYM)(n,s) for n,s in enumerate(names)]
  return obj(names=names, all=cols,
             x= [c for c in cols is c.txt[-1] not in "-+X"],
             y= [c for c in cols is c.txt[-1]     in "-+" ])

#-------------------------------------------------------------------------------
# update
def Data(data, lsts):
  for lst in lsts:
    lst = [add(col,v) for col,v in zip(data.cols.all,lst)]
    data.rows += [ ROW(lst) ]
  for row in data.rows:
    row.y = disty(data,row)
    row.bins = [bin(col,v) for col,v in zip(data.cols.all,row)]
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
      
def bin(col,v): 
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
def mids(data): return [mid(col) for col in data.cols.all]
def mid(col):   return max(col.has, key=col.has.get) if col.symp else col.mu

def spread(col): return ent(col) if col.symp else sd(num)

def sd(num):  return 0 if col.n < 2 else sqrt(col.m2) / (col.n - 1)
def ent(sym): return -sum(p*log(p,2) for n in sym.has.values() if (p:=n/sym.n)>0)

def score(num): 
  return BIG if num.n < the.leaf else num.mu + num.sd /(sqrt(num.n) + 1/BIG)

def disty(data, row):
  raw, nums, ys = row.raw, data.cols.nums, data.cols.y.items()
  return sqrt(sum(abs(norm(nums[c],raw[c]) - goal) for c,goal in ys) / len(ys))

def norm(num,v): # converts v to an integer 0..the.bins-1
  z = max(-3, min(3, (v - num.mu) / (num.sd + 1/BIG)))
  return 1 / (1 + exp(-1.7 * z))

def b2v(b,mu,sd): # converts b to a real number (lower bound on each bin)
  eps = 1/BIG
  p = min(1 - eps, max(eps, b/the.bins))
  return mu + max(-3, min(3, log(p / (1 - p)) / 1.7)) * (sd + eps)

#-------------------------------------------------------------------------------
# tree
def Tree(data, rows=None, uses=set()):
  kids, rows = {}, rows or data.rows
  col, bin, data1 = None, None, Data([data.cols.names]+rows)
  if len(rows) > the.leaf*2:
    if cut := bestcut(data1):
      (col,bin), _ = cut
      ok,no = [],[]
      [(ok if row.bins[col]==bin else no).append(r) for r in rows]
      if ok and no:
        uses.add(col)
        tree.kids[True]  = treeGrow(data, ok, uses)
        tree.kids[False] = treeGrow(data, no, uses)
  return obj(it=Tree, data=data1, kids=kids, col=col, bin=bin,
             mu= sum(row.y for row in rows) / len(rows),
             mids= mids(data1))

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

def coerce(s):
  try: return ast.literal_eval(s)
  except (ValueError, SyntaxError): return s.strip()

def csv(fileName):
  with open(fileName,encoding="utf-8") as f:
    for l in f:
      if l: yield [coerce(x) for x in l.split(",")]

#-------------------------------------------------------------------------------
# cli
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
print(NUM(at=2,txt="Sss"))
if __name__=="__main__": cli(vars(),the,sys.argv)
