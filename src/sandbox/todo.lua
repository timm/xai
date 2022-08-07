l=require"lib"
per=l.per
map=l.map
fmt=l.fmt

function with(settings, updates) 
  for k,v in pairs(updates or {}) do settings[k]=v end
  return settings end

function tiles(t, args)
  args = with({lo=0, hi=1, width=32, ns={.25,.5,.75}, rank=1},args)
  local norm = function(n) return (n-args.lo) / (args.hi-args.lo) end
  local at   = function(n) return math.floor(args.width*norm(n)) end
  local pos  = function(p) return t[1] + p*(t[#t] - t[1]) end
  local s={}
  for i=1,args.width do s[i]=" " end
  for p = .1,.3,.01 do s[at(pos(p))] ="-" end 
  for p = .7,.9,.01 do s[at(pos(p))] ="-" end 
  s[at(per(t,.5))] = "|"
  return {rank = args.rank,
          str  = table.concat(s), 
          mid  = per(t,.5),
          per  = map(args.ns, function (p) return per(t,p) end)} end 

function tiles4ratios(ratios,  args)
  local lo,hi=0,1
  for _,ratio in pairs(ratios) do 
    local t = ratio:holds()
    lo = math.min(lo, t[1])
    ho = math.max(hi, t[#t]) end
  for _,ratio in pairs(ratios) do 
    local tile = tiles(ratio:holds(), with({lo=lo,hi=hi,rank=ratio.rank},args))
    print(tile.rank, tile.str, cat(map(tile.per, l.rnd))) end end

t={}
math.randomseed(10019)
for i=1,100 do t[1+#t]=math.random()^.5 end
out=tiles(l.sort(t))
print(fmt("|%s|",out.str),l.cat(map(out.per,l.rnd)))
