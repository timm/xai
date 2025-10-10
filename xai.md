---
title: "A quick primer on XAI scripting"
author: |
  Tim Menzies\
  timm@ieee.org

  Shane McIntosh\
  shanemcintosh@acm.org
date: Oct 2025

toc: true
toc-depth: 2
highlight-style: pygments

header-includes:
  - |
    <style>
      /* --- Layout and body text --- */
      body {
        max-width: 600px;
        margin: auto;
        font-family: Georgia, serif;
        line-height: 1.5;
      }

      /* --- Floating Table of Contents --- */
      #TOC {
        position: fixed;
        top: 1em;
        left: 1em;
        width: 200px;
        max-height: 90%;
        overflow-y: auto;
        background: #f9f9f9;
        border: 1px solid #ddd;
        padding: 0.5em;
        z-index: 1000;
      }

      /* Make sure ToC text is visible and styled */
      #TOC, #TOC * {
        color: inherit !important;
        visibility: visible !important;
        display: block !important;
      }
      #TOC a {
        text-decoration: none;
        color: #333;
      }
      #TOC a:hover {
        text-decoration: underline;
        color: #000;
      }
      #TOC ul {
        list-style: none;
        padding-left: 0;
        margin-left: 0;
      }
      #TOC li {
        margin: 0.2em 0;
      }

      /* Shift main body to make room for TOC */
      body { margin-left: 220px; }

      /* --- Code block styling --- */
      pre code {
        font-size: 75%;
        xbackground: #f7f7f7;
        xborder: 1px solid blue; 
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
        xpadding: 0.5em;
        xborder-radius: 4px;
        xdisplay: block;
        xoverflow-x: auto;
      }

      /* --- Dark mode --- */
      body.dark { background:#111; color:#eee; }
      body.dark a { color: #6cf; }

      /* Optional: collapse TOC on narrow screens */
      @media (max-width: 800px) {
        #TOC { display: none; }
        body { margin-left: auto; }
      }
    </style>
    <script>
      function toggleDark() {
        document.body.classList.toggle('dark');
      }
    </script>

include-before-body: |
  <button onclick="toggleDark()" 
          style="position:fixed;top:1em;right:1em;
                 z-index:999;font-size:1.2em;">🌙</button>
---


<img src="https://media.licdn.com/dms/image/v2/C5112AQF2uhimL9_E7Q/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1536912136344?e=1762992000&v=beta&t=ELpC8PM9rcYgFEtlSdS2KWbrhGOTyMovKe3DV5-z1BI"
width=400 align=right>

Artificial intelligence comes in many forms. Some of it dazzles but
remains a mystery—black-box systems that are hard to interpret, let
alone maintain. Yet not all AI is like this. A growing family of
explainable AI (XAI) techniques aim to deliver insights in ways
that people can actually follow and trust.

This short document shows the XAI techniques we have beeen using, for decades, for software analytic,
Our job is to dig through sprawling, messy data and pull out
clear, defensible nuggets of knowledge. Over the years, we gave
developed a toolkit of approaches that make complex patterns simple,
and simple stories powerful.

In this paper we want to share those approaches. They are lighter
than today’s heavyweight LLMs and easier to use and  explain and
critique. Most importantly, the results can be understood,
debated, and acted upon by teams of people seeking actionable
insights into their own domains.

## Our Structure

 lts of egs'

This document is structure around a study of real world data miners, working at Mcirosoft [^amershi19].
That work showed that actually "modeling training " (i.e. running the data mining algorithms) was only
around 10% of a larger process. In the bigger process, much time needs to be spent determining the goals
of the learning, checking the data up front, then monitoring the deployed AI since:

> Data mining can be very error prone; so we need to check for
those errors at every step of our process.




[^amershi19]: S. Amershi et al., 
[Software Engineering for Machine Learning: A Case Study](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/03/amershi-icse-2019_Software_Engineering_for_Machine_Learning.pdf), 
2019 IEEE/ACM 41st International Conference
on Software Engineering: Software Engineering in Practice (ICSE-SEIP),
Montreal, QC, Canada, 2019, pp. 291-300, doi: 10.1109/ICSE-SEIP.2019.00042.

When we get to the data mining,
for those of you  that like "rolling your own", we present a tiny
home brew data mining tool kit that does clustering, rule learning, tree learning,
optimization in just 200 lines of code. The lesson of this first part 
is that:

> Many of these AI tools are very simple and can be created and combined
using very little coding.

After that, we repeat all the presentation using a standard machine learning
library (scikit-learn). The lesson of this second part is that:

> There are many tools
can can help you with your data mining.

## Installation

Call up a  terminal, make sure you have **git** and  gawk 3.1 dn,mdcdddddddddddddddddddddddddddddddddddd**python3.13** (or later) installed, then

    mkdir xai                               # or any other name you line
    cd xai
    git clone http://github.com/timm/moot   # example data
    git clone http://github.com/timm/ezr    # code
    cd erz
    python3 -m ezr -h
    python3 -m ezr -f ../../moot/optimize/config/SS-A.csv

If that works, you should see something like

    ezr.py (v0.5): lightweight XAI for multi-objective optimization
    (c) 2025, Tim Menzies <timm@ieee.org>, MIT license
    [code](https://github.com/timm/ezr) ::
    [data](https://github.com/timm/moot)
    
    Options:
    
        -a  acq=near          label with (near|xploit|xplor|bore|adapt)
        -A  Any=4             on init, how many initial guesses?
        -B  Budget=30         when growing theory, how many labels?
        -C  Check=5           budget for checking learned model
        -D  Delta=smed        effect size test for cliff's delta
        -F  Few=128           sample size of data random sampling
        -K  Ks=0.95           confidence for Kolmogorovâ€"Smirnov test
        -l  leaf=3            min items in tree leaves
        -m  m=1               Bayes low frequency param
        -p  p=2               distance co-efficient
        -s  seed=1234567891   random number seed
        -f  file=../moot/optimize/misc/auto93.csv    data file
        -h                     show help
    
     File:    ../../moot/optimize/config/SS-A.csv
     Rows:    1343
     X:       3
     Y:       2 Throughput+ Latency-
     
     n:  26   win:   53     if Counters > 7
     n:  15   win:   60     |  if Counters > 14
     n:   3   win:   90     |  |  if Spout_wait > 9;
     n:  12   win:   52     |  |  if Spout_wait <= 9
     n:   7   win:   63     |  |  |  if Spliters > 4
     n:   4   win:   66     |  |  |  |  if Spout_wait <= 4;
     n:   3   win:   59     |  |  |  |  if Spout_wait > 4;
     n:   5   win:   37     |  |  |  if Spliters <= 4;
     n:  11   win:   44     |  if Counters <= 14
     n:   7   win:   48     |  |  if Spout_wait > 4
     n:   3   win:   52     |  |  |  if Spliters > 4;
     n:   4   win:   45     |  |  |  if Spliters <= 4;
     n:   4   win:   37     |  |  if Spout_wait <= 4;
     n:   4   win:  -84     if Counters <= 7;
     
     Used:  Spout_wait Spliters Counters
     Best train: 100 hold-out: 63




## Symbols and Numbers

To begin at the beginning, in this world, there are $Sym$bols and $Num$bers.

- $Sym$bols are discrete things that can be compared (with equal or
not equals);
- $Num$bers  can be combined together (using addition,
multiplication, etc).
- The difference between $Sym$bols and $Num$bers is that there is nothing
  in between each symbol, but numbers can be interpolated to fill in that gap
  (e.g. some new number is the average of two existing numbers).

```py
from types import simplenamespace as o

def Sym(at=0,s=" "): 
  return o(it=Sym, 
           at=at,   # column number
           txt=s,   # text of column name
           n=0,     # items seen
           has={})  # symbol counts of items seen

def Num(at=0,s=" "): 
  return o(it=Num, 
           at=at,   # column number
           txt=s,   # text of column name
           n=0,     # items seen
           mu=0,    # mean
           sd=0,    # standard deviation
           m2=0,    # low-level detail (used to calculate sd)
           hi=-big, lo=big,  # smallest and largest value seen
           best = 0 if s[-1] == "-" else 1) # 0,1 = minimize,maximize
```
$Num$s and $Sym$s have a central tendency which is called the mean
($mu$) or median for numerics and symbolics.
Given a dictionary of symbol counts, the median is the
key with maximum value: 

```py
def mid(col: o) -> Atom:
  "Get central tendency of one column"
  return max(col.has, key=col.has.get) if col.it is Sym else col.mu
```

$Num$s and $Sym$s also know how much their values tend
to diverge from from the central tendency. For $Num$s, this
is called the standard deviation which normally extends
$\pm 3$ standard deviations around the mean.


```py
def div(col:o) -> float:
  "Return the central tendency for one column."
  if col.it is Num: return col.sd
  vs = col.has.values()
  N  = sum(vs)
  return -sum(p*math.log(p,2) for n in vs if (p:=n/N) > 0)
```

$Sym$s and $Num$s can be stored in rows and rows can be stored in
a $Data$ table.  The columns of these tables are of $x$ $independent$
inputs and $y$ dependent goal $labels$.  If $|y| > 0$, this is a
_supervised_ task that reasons about the goal labels;

- If $|y|==1$, we can either do classification (for $Sym$bolic goals)
  or regression (for $Num$eric goals).
- If $|y| > 1$, then this could be a multi-objective problem.
  - Each $y_i$  is a $Num$eric goal to be minimized or maximized;
  - Each such goal has a "best" value (0 for minimization and
    1 for maximization);
  - Rows has a "heaven" point which is the best value for their
    goals. 
    For example, if we are minimizing cost and maximizing benefit,
    then the best vector is (0,1).
  - Each row has a "distance to heaven" which is the distance of
    of the $y_i$ values to the best vector.
    
If $|y| == 0$, this is a called an _unsupervised_ task that must work 
  without labels:

- E.g. cluster together  similar rows, then report what distinguished
  each cluster;
- E.g. Iteratively label rows that seem most informative for
  distinguishing better and worst things (this is called "active learning").

    

XXX nums, x and ys 

```py
def Data(src) -> o:
  "Create data structure from source rows"
  src = iter(src)
  return adds(src, o(it=Data, n=0, mid=None, rows=[], kids=[], 
                     ys=None, cols=Cols(next(src)))) 

def clone(data:Data, rows=None) -> o:
  "Create new Data with same columns but different rows"
  return adds(rows or [], Data([data.cols.names]))
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit
in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
officia deserunt mollit anim id est laborum.



