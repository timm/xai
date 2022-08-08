package.path = '../?.lua;' .. package.path 
local l = require"lib"
local r = require"rl"
local About= r.About
local Data = r.Data
local Row  = r.Row
local Col  = r.Col
local the  = r.the

local go={}
function go.pass()  return true end

-- local d=r.Data.load("../data/auto93.csv")
-- l.chat(r.Data.mid(d))
-- l.chat(d.about.x[1])
--
function go.the() l.chat(the); return true end
function go.per() return 6==(l.per{1,2,3,4,5,6,7,8,9,10,11}) end

function go.nom(   nom)
  nom=Col.nom()
  for _,x in pairs{"a","a","a","a","b","b","c"} do Col.add(nom,x) end 
  return "a"==Col.mid(nom) and 1.38==l.rnd(Col.div(nom),2) end

function go.ratio(    r)
  r=Col.ratio()
  the.keep = 64
  for i=1,100 do Col.add(r,i) end
  return 52==Col.mid(r) and 32.56==l.rnd(Col.div(r),2)  end

function go.about()
  local t= {"Clndrs","Volume","Hp:","Lbs-","Acc+","Model","origin","Mpg+"}
  l.map( About.new(t).y , l.chat)
  l.map( About.new(t).x , l.chat)
  return true end

function go.data(     data1,data2)
  data1=Data.load("../../data/auto93.csv")
  print("mid1", l.cat(Data.mid(data1,2)))
  print("div1", l.cat(l.rnds(Data.div(data1,2))))
  data2=  Data.clone(data1, data1.rows)
  print("mid2", l.cat(Data.mid(data2,2)))
  print("div2", l.cat(l.rnds(Data.div(data2,2))))
  return true
  end

function go.dist()
  local data1=Data.load("../../data/auto93.csv")
  print(#data1.rows)
  for j = 1,20 do
    local row1=l.any(data1.rows)
    local row2=l.any(data1.rows)
    print(Row.dist(row1,row2)) end
  for j,rowd in pairs(Row.around(l.any(data1.rows), data1.rows)) do
    if j< 5 or j>393 then l.chat(rowd.row.cells) end end 
  return true 
  end

function go.half()
  local data1=Data.load("../../data/auto93.csv")
  local A,B,As,Bs,c = Data.half(data1, data1.rows) 
  print(c, #As, #Bs, l.cat(A.cells), l.cat(B.cells))
  local data2=Data.clone(data1,As)
  local data3=Data.clone(data1,Bs)
  print("As", l.cat(Data.mid(data2,2)))
  print("Bs", l.cat(Data.mid(data3,2)))
  return true end

function go.trends()
  local data1=Data.load("../../data/auto93.csv")
  Data.cheat(data1)
  local rows= Data.trends(data1)
  print("rows:",#rows)
  print("As", l.cat(Data.mid(Data.clone(data1,l.slice(rows,1,50)),2)))
  print("As", l.cat(Data.mid(Data.clone(data1,l.slice(rows,100,150)),2)))
  print("As", l.cat(Data.mid(Data.clone(data1,l.slice(rows,200,250)),2)))
  print("As", l.cat(Data.mid(Data.clone(data1,l.slice(rows,300,350)),2)))
  print("Bs", l.cat(Data.mid(Data.clone(data1,l.slice(rows,351)),2))) 
  print(#l.map(data1.rows,l.grab"evaled"))
  for j,row in pairs(rows) do print(j,row.rank) end
  return true end

function go.quota()
  local evals = {} 
  local guess = {}
  local tops  = {}
  for r=1,20 do
    local data1=Data.load("../../data/auto93.csv")
    Data.cheat(data1)
    local best = Data.best(data1)
    local evaled = l.sort(l.map(data1.rows, l.grab"evaled"),l.lt"rank")
    l.push(tops, evaled[1].rank)
    l.push(evals,#evaled)
    for _,row in pairs(best) do l.push(guess, row.rank) end end
  print("guess",l.cat(l.pers(guess, {.1,.3,.5,.7,.9})))
  print("evals",l.cat(l.pers(evals, {.1,.3,.5,.7,.9})))
  print("tops",l.cat(l.pers(tops,  {.1,.3,.5,.7,.9})))
  return true
  end

l.main(the._help, the,go)
