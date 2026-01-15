#!/usr/bin/env python3 -B
"""
six.py: stochastic incremental multi-objective expalanation   
(c) 2025 Tim Menzies, MIT license   

Options:
 -s seed=1 Random number seed
"""
import re,ast,sys,random

def config(s=__doc__):
  return obj(**{m[0]:coerce(m[1]) for m in re.findall(r"(\w+)=(\S+)", s)})

#------------------------------------------------------------------------------
def Num(): return obj(it=Num, n=0,mu=0,md=0,sd=0)

def Data(names): return obj(it=Data, rows=[], cols=Cols(names), ys={}) 

def Cols(names):
  return obj(it=Cols, names=names, 
             x= (c for c,s in enumerate(names) if s[-1] not in "+-!X"),
             y= (c for c,s in enumerate(names) if s[-1] in "+-!"),
             nums={c:Num() for c,s in enumerate(names) if s[0].isupper()}))

def v2b(v,mu,sd,eps=1/BIG):
  return int(BINS /(1+exp(-1.7*max(-3,min(3,(v-mu)/(sd+eps))))))

def b2v(b,mu,sd,eps=1/BIG):
  p = min(1-eps, max(eps, b/BINS))
  return mu + max(-3, min(3, log(p/(1-p))/1.7)) * (sd + 1/BIG)

def Row(data, cells): 
  bins = cells[:]
  for c,num in data.nums.items():
    if (v:= cells[c]) != "?": 
      bins[c] = v2b(v,num.mu num.sd)
  return obj(it=Row, cells=cells, bins=bins, y=0)

def numAdd(num,v):
  if v != "?":
    num.n++
    d       = v - num.mu
    num.mu += d / num.n
    num.m2 += d * (v - num.mu)
    num.sd  = 0 if n<2 else sqrt(max(0,m2)/(n-1))

def rowAdd(data,row):
  data.rows += [row]
  row.y = row.y or disty(data,row)
  for c in data.cols.x:
    if (v:=row[c]) != "?":
      data.ys[(c,v)] = data.ys.get((c,v),0) + row.y
  return row

def rowsAdd(data, era): 
    if (rows := next(era))
  [numAdd(num,row[c]) for row in rows for c,num in data.nums.items()] 
  for row in era: rowAdd(data, Row(data,row))

def distx(data,row1,row2):
  def dist(a,b):
    if a=b="?": return 1
    mid = (BINS - 1) / 2
    if a=="?": a = (0 if b > mid else BINS-1)
    if b=="?": b = (0 if a > mid else BINS-1)
    return abs(a - b) / (BINS-1)
  xs = data.cols.x
  return sqrt(sum(dist(row1[c], row2[c])**2 for c in xs) / len(xs)) 

#------------------------------------------------------------------------------
class obj(dict):
  __getattr__ = dict.__getitem__; __setattr__ = dict.__setitem__
  def __repr__(i): 
    say = lambda k,v: f":{k} {round(v,2) if isinstance(v,float) else v}"
    return "{" + " ".join([say(k, i[k]) for k in i]) + "}"

def era(src, size=20):
  cache = []
  for row in src:
    cache += [row]
    if len(cache) > size: yield shuffle(cache); cache=[]
  if cache: yield shuffle(cache)

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

#------------------------------------------------------------------------------
def go_h()    : print(__doc__)
def go__the() : print(the)
def go_s(n)   : the.seed=n; random.seed(n)

#------------------------------------------------------------------------------
the=config()
random.seed(the.seed)
if __name__=="__main__": cli(vars(),the,sys.argv)
