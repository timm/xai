---
title:  A quick primer on XAI scripting
author: |
  <img src=img/xai.png width=350 align=right>
  Tim Menzies\
  timm@ieee.org\
  \
  Shane McIntosh\
  timm@ieee.org
css: style.css
---

-------

Artificial intelligence comes in many forms. Some of it dazzles but
remains a mystery—black-box systems that are hard to interpret, let
alone maintain. Yet not all AI is like this. A growing family of
explainable AI (XAI) techniques aim to deliver insights in ways
that people can actually follow and trust.

We write from the perspective of decades in software analytics,
where the job is to dig through sprawling, messy data and pull out
clear, defensible nuggets of knowledge. Over the years, we’ve
developed a toolkit of approaches that make complex patterns simple,
and simple stories powerful.

In this paper we want to share those approaches. They are lighter
than today’s heavyweight LLMs and easier to use and  explain and
critique. Most importantly, the results can be understood,
debated, and acted upon by teams of people seeking actionable
insights into their own domains.

## In the Beginning, were $Sym$bols and $Num$bers

To start at the very beginning, there are $Sym$bols and $Num$bers.
$Sym$bols are discrete things that can be compared (with equal or
not equals) while $Num$bers  can be combined together (using addition,
multiplication, etc).

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
    For example, if we are minimizing cost and maximizming benefit,
    then the best vector is (0,1).
  - Each row has a "distance to heaven" which is the distance of
    of the $y_i$ values to the best vector.
    
If $|y| == 0$, this is a called an _unsupervised_ task that must work 
  without labels:

- E.g. cluster together  similar rows, then report what distinguished
  each cluster;
- E.g. iteratively label rows that seem most informative for
  distinguishing best from rest (this is called "active learning").

    

 

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



