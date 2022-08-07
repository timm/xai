local l = require"lib"
local the = {bins=8, ratios=256}

local _is={
  nom   = "^[a-z]",  -- ratio cols start with uppercase
  goal  = "[!+-]$",  -- !=klass, [+,-]=maximize,minimize
  klass = "!$",      -- klass if "!"
  skip  = ":$",      -- skip if ":"
  less  = "-$"}      -- minimize if "-"

local function COL(txt,at)
  txt = txt or ""
  return {n    = 0,                -- how many items seen?
          at   = at or 0,         -- position ot column
          txt  = txt,            -- column header
          isNom= txt:find(_is.nom),
          w    = txt:find(_is.less) and -1 or 1,
          ok   = true,             -- false if some update needed
          has  = {}} end           -- place to keep (some) column values.

function ABOUT(sNames)
  local about = {names=sNames, all={}, x={}, y={}, klass=nil}
  for at,name in pairs(sNames) do
    local one = l.push(about.all, COL(name,at))
    if not name:find(_is.skip) then
      l.push(name:find(_is.goal) and about.y or about.x, one)
      if name:find(_is.klass) then about.klass=one end end end
  return about end

function ROW(t) return {cells=t, cooked=l.map(t,l.same)} end
function DATA() return {rows={}, about=nil } end

function has(col)
  if col.isNom then return col.has end
  if not col.ok then table.sort(col.has) end
  col.ok=true
  return col.has end
 
function addCol(col,x)
  if x ~= "?" then 
    col.n = col.n + 1
    if col.isNom 
    then col.has[x] = 1 + (col.has[x] or 0)
    else local pos
         if     #col.has < the.ratios       then pos = 1 + (#col.has) 
         elseif l.rand() < the.ratios/col.n then pos = l.rand(#col.has) end
         if pos then
           col.ok=false -- the `kept` list is no longer in sorted order
           col.has[pos]=x end end end end

function addCols(data,row)
  row = row.cells and row or ROW(row)
  for _,cols in pairs{data.about.x,data.about.y} do
    for _,col in pairs(cols) do
      addCol(col, row.cells[col.at]) end end 
  return row end

function addRow(data,t)
  if   data.about 
  then l.push(data.rows, addCols(data, t))
  else data.about = ABOUT(t) end end

function where(col,x,     a,b,lo,hi)
  if col.nom then return x else
    a = has(col)
    lo,hi = a[1], a[#a]
    b = (hi - lo)/the.bins
    return hi==lo and 1 or math.floor(x/b+.5)*b  end end

function norm(col,num)
  local a= has(col) -- "a" contains all our numbers,  sorted.
  return a[#a] - a[1] < 1E-9 and 0 or (num-a[1])/(a[#a]-a[1]) end

function bins(data)
  for _,col in pairs(data.about.x) do
    for _,row in pairs(data.rows) do
      local x = row.cells[col.at]
      if x~= "?" then
        row.cooked[col.at] = where(col,x) end end end end 

function better(data,row1,row2)
  row1.evaled,row2.evaled= true,true
  local s1,s2,d,n,x,y=0,0,0,0
  local ys,e = data.about.y,math.exp(1)
  for _,col in pairs(ys) do
    x,y= row1.cells[col.at], row2.cells[col.at]
    x,y= norm(col,x), norm(col,y)
    s1 = s1 - e^(col.w * (x-y)/#ys)
    s2 = s2 - e^(col.w * (y-x)/#ys) end
  return s2/#ys < s1/#ys end

d=DATA()
l.csv("../data/auto93.csv",function(row) addRow(d,row) end)
--map(d.about.x, chat)
-- chat(d.about.x)
bins(d)
for _,row in pairs(d.rows) do l.chat(row.cooked) end
for i=1,20 do
  r1=l.any(d.rows)
  r2=l.any(d.rows)
end
