local _ = require"lib"
local any,big,cat,chat,cli,coerce    = _.any,_.big,_.cat,_.chat,_.cli,_.coerce
local csv,fmt,get,gt                 = _.csv,_.fmt,_.get,_.gt
local klass,last,lines,lt,main,many,map= _.klass,_.last,_.lines,_.lt,_.main,_.many,_.map
local obj,per,push,rand,rev,rnd      = _.obj,_.per,_.push,_.rand,_.rev,_.rnd
local rogues,same,shuffle,slice,sort = _.rogues,_.same,_.shuffle,_.slice,_.sort
local values,words                   = _.values,_.words

local _ = require"xai"
local the, help,csv2data =  _.the, _.help, _.csv2data
local ABOUT,DATA,NOM     = _.ABOUT, _.DATA,_.NOM
local RATIO,ROW,XY       = _.RATIO,_.ROW,_.XY
local bins,half,how      = _.bins, _.half, _.how

---- ---- ---- ---- Tests
-- Tests fail if they do not return `true`.
local go={}

local function c(n,p) return 1-(1-p)^n end
local function n(c,p) return math.log(1-c)/math.log(1-p) end

function go.pass() return true end
function go.sort(   data)
  local data=csv2data("../data/auto93.csv") 
  data:ranked()
  sort(data.rows)
  --for _,row in pairs(data.rows) do print(row.rank) end 
  chat(data:clone(slice(data.rows,1,30)):mid())
  chat(data:clone(slice(data.rows,350)):mid())
  for _,row in pairs(slice(data.rows,1,30)) do print(row.rank) end
  end

function simpleRandom(   out)
  out=RATIO("Srand")
  for r=1,20 do
    local data=csv2data("../data/auto93.csv") 
    data:ranked()
    for i=1,10 do out:add(any(data.rows).rank) end end 
  return out end 

function quota(   halving,guess)
  halving = RATIO("halving")
  guess   = RATIO("guess")
  evals   = RATIO("evals")
  for r=1,20 do
    local data=csv2data("../data/auto93.csv") 
    data:ranked()
    local best,_,top = half.splits(data.rows) 
    for _,row in pairs(best) do guess:add(row.rank) end 
    for _,n in pairs(data:evaled()) do halving:add(n) end 
    evals:add(how._nevaled(data.rows))  end
  return halving,guess,evals end

function stratified(   data)
  local guess = RATIO("strafied")
  for r=1,20 do
    local data = csv2data("../data/auto93.csv") 
    data:ranked()
    for n,rows in pairs(shuffle(half._tree(data.rows))) do 
      if n<21 then guess:add(any(rows).rank) end end  end
  return guess end

function quota(   halving,guess)
  halving = RATIO("halving")
  guess   = RATIO("guess")
  evals   = RATIO("evals")
  for r=1,20 do
    local data=csv2data("../data/auto93.csv") 
    data:ranked()
    local best = half.splits(data.rows) 
    for _,row in pairs(best) do guess:add(row.rank) end 
    for _,n in pairs(data:evaled()) do halving:add(n) end 
    evals:add(how._nevaled(data.rows))  end
  return halving,guess,evals end

function rule()
  local data=csv2data("../data/auto93.csv") 
  data:ranked()
  local xys,data1 = how.rules(data)
  print(#data1.rows, cat(xys))
  end

---- ---- ---- ---- Start-up
math.randomseed(the.seed)
the.p=2
bases=simpleRandom()
halfs,guesses,evals=quota()
trees=stratified()
RATIO.tiles({bases,trees,halfs,guesses}, 
                {width=32,pers={.1,.3, .5, .7,.9}})

print""; print("evals",evals:mid(), rnd(evals:div()))

rule()
