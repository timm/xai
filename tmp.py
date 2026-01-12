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
def norm(n,mu,sd): return 1 / (1 + exp(-1.7 * max(-3, min(3, (n-mu)/sd))))

def bins(src):
  nums,n,mu,m2 = {},[],[],[]
  for row in src:
    if nums:

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
