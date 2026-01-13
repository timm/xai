#!/usr/bin/env python3 -B
"""
six.py: stochastic incremental multi-objective expalanation   
(c) 2025 Tim Menzies, MIT license   

Options:
 -s seed=1 Random number seed
"""
import re,ast,sys,random

class obj(dict):
  __getattr__ = dict.__getitem__; __setattr__ = dict.__setitem__
  def __repr__(i): 
    say = lambda k,v: f":{k} {round(v,2) if isinstance(v,float) else v}"
    return "{" + " ".join([say(k, i[k]) for k in i]) + "}"

#------------------------------------------------------------------------------
def norm(n,mu,sd): 
  return 1 / (1 + exp(-1.7 * max(-3, min(3, (n-mu)/(sd+1/BIG)))))

def Num(): return obj(it=Num, n=0,mu=0,md=0,sd=0)

def Data(names): 
  return obj(it=Data, rows=[], names=names, ys={}, 
             nums={c:Num() for c,s in enumerate(names) if s[0].isupper()})

def Row(data, row): 
  bins = row[:]
  for c,num in data.nums.items():
    if (v:= row[c]) != "?": 
     bins[c] = int(BINS * norm(v,num.mu, num.sd))
  return obj(it=Row, cells=row, bins=bins, y=0)

def updateStats(num,v):
  if v != "?":
    num.n++
    d       = v - num.mu
    num.mu += d / num.n
    num.m2 += d * (v - num.mu)
    num.sd  = 0 if n<2 else sqrt(max(0,m2)/(n-1))

def updateYs(data,row):
  row.y = disty(data,row)
  for c,v in enumerate(row.bins):
    if v != "?" and data.names[c][-1] not in "+-X":
     data.ys[(c,v)] = data.ys.get((c,v),0) + row.y
  return row

def era(src, size=20):
  cache = []
  for row in src:
    cache += [row]
    if len(cache) > size: yield shuffle(cache); cache=[]
  if cache: yield shuffle(cache)

def rows(data, era): 
  for row in era: 
    for c,num in data.nums.items():
      updateStats(num, row[c])
  for row in era: 
    data.rows += [updateYs(data, Row(data,row))]

def distx(data,row1,row2):
  xs = data.cols.x
  return sqrt(sum((row1[c] - row2[c])**2 
                  for c,s in enumerate(data.names) if s[0] not in "+-
#------------------------------------------------------------------------------
def coerce(s):
  try: return ast.literal_eval(s)
  except (ValueError, SyntaxError): return s.strip()

the = obj( **{m[0]:coerce(m[1]) for m in re.findall(r"(\w+)=(\S+)", __doc__)})

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
random.seed(the.seed)
if __name__=="__main__": cli(vars(),the,sys.argv)
