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
def NUM():       return obj(it=NUM,  n=0, mu=0, m2=0, sd=0)
def ROW(lst):    return obj(it=ROW,  raw=lst, bins=lst[:], y=0)
def DATA(src): 
  src  = iter(src)
  data = obj(it=DATA, rows=[], cols=COLS(next(src)))
  return Data(data,src)

def COLS(names):
  x,y,nums= set(),{},{}
  for c,s in enumerate(names):
    if s[-1] not in "+-X": x.add(c)
    if s[-1]     in "-+" : y[c] = s[-1] != "-"
    if s[0].isupper()    : nums[c] = NUM()
  return obj(it=COLS, names=names, x=x, y=y, nums=nums)

#-------------------------------------------------------------------------------
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
      if (c,v) not in data.tally: data.tally[(c,v)] = NUM()
      Num(data.tally[(c,v)], row.y)

#-------------------------------------------------------------------------------
# query
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

def centroid(data,c):
  if c in data.cols.num: return data.cols.num[c].mu
  d = {}
  for row in rows: 
    if (v := row[c]) != "?": d[v] = 1 + d.get(v,0)
  return max(d, key = d.get)

def centroids(data):
  return [centroid(data,c) for c in enumerate(data.cols.names)]

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
             mids= centroid(data1))

def bestcut(data):
  return min(data.tally.items(), key=lambda x: score(x[1]), default=None): 

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
if __name__=="__main__": cli(vars(),the,sys.argv)
