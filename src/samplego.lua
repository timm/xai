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
function go.ranked()
  for r=1,20 do
    local data=csv2data("../data/auto93.csv") 
    data:ranked()
    p = 0.05 * #data.rows
    local best,tmp
    for i=1,10 do
      tmp = any(data.rows) 
      if not best or tmp.rank > best.rank then best=tmp end end 
    print(best.rank,100-p, n(.95,.05)) end 
  return true end

function go.half()
  for r=1,20 do
    local data=csv2data("../data/auto93.csv") 
    data:ranked()
    half.splits(data.rows) 
    print(last(data:evaled())) end
  return true end

---- ---- ---- ---- Start-up
main(help,the,go)
