package.path = '../?.lua;' .. package.path 
local l = require"lib"
local r = require"rl"
local go={}

function go.pass()  return true end
function go.the() l.chat(r.the);  return true end

-- local d=r.Data.load("../data/auto93.csv")
-- l.chat(r.Data.mid(d))
-- l.chat(d.about.x[1])
--
l.main(r.the.sHelp, r.the,go)
