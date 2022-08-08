package.path = '../?.lua;' .. package.path 
local l = require"lib"
local r = require"rl"
local go={}
local About= r.About
local Data = r.Data
local Row  = r.Row
local Col  = r.Col
local the  = r.the

function go.pass()  return true end

-- local d=r.Data.load("../data/auto93.csv")
-- l.chat(r.Data.mid(d))
-- l.chat(d.about.x[1])
--
function go.the() l.chat(the); return true end
function go.per() return 6==(l.per{1,2,3,4,5,6,7,8,9,10,11}) end

function go.nom(   nom)
  nom=Col.new("n")
  for _,x in pairs{"a","a","a","a","b","b","c"} do Col.add(nom,x) end 
  return "a"==Col.mid(nom) and 1.38==l.rnd(Col.div(nom),2) end

function go.ratio(    r)
  r=Col.new()
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

function go.dist(    data1,row1,row2)
  data1=Data.load("../../data/auto93.csv")
  print(#data1.rows)
  for i = 1,20 do
    row1=l.any(data1.rows)
    row2=l.any(data1.rows)
    print(Row.dist(row1,row2)) end
  for j,rowd in pairs(Row.around(l.any(data1.rows), data1.rows)) do
    if j< 5 or j>393 then l.chat(rowd.row.cells) end end 
  return true end

function go.half(    data1,row1,row2)
  data1=Data.load("../../data/auto93.csv")
  local A,B,As,Bs,c = Data.half(data1, data1.rows) 
  print(c, #As, #Bs, l.cat(A.cells), l.cat(B.cells))
  return true end
  
l.main(the._help, the,go)
