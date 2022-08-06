-- t={lo=x,hi=x,width=x,ps=x,rank=x}
TILE=obj("TILE")
function TILE:new() return {lo=0, hi=1, width=32, ps={.25,.5,.75}} end
function TILE:draws(ratios) 
  for _,ratio in pairs(ratios) do 
    local t = ratio:holds()
    self.lo = math.min(self.lo, t[1])
    self.hi = math.max(self.hi, t[#t]) end
  return map(ratios, function(t) self:draw(ratio) end) end

function TILE:draw(ratio)
  local s,t   = {}, ratio:holds()
  local where = function(n) return math.floor(self.width*ratio:norm(n)) end
  local pos   = function(p) return t[1] + p*(t[#t] - t[1]) end
  for i =  1, self.width do s[i]=" " end
  for p = .1,.3,.01      do s[where(pos(p))] ="-" end 
  for p = .7,.9,.01      do s[where(pos(p))] ="-" end 
  s[where(per(t,.5))] = "|"
  return {rank = ratio.rank or 1,
          str  = table.concat(s), 
          mid  = per(t,.5),
          per  = map(self.ps, function (p) return per(t,p) end)} end
