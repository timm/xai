----------------------
-- Showing off Colon mode.
-- If you hate @ tags, you can use colons. However, you need to specify colon
-- mode explicitly -C or --colon, or `colon=true` in the config.ld. Be careful
-- not to use a colon followed by a space for any other purpose!
--
-- So the incantation in this case is `ldoc -C colon.lua`.

-- classmod: colon


--- first useless function.
-- Optional type specifiers are allowed in this format.
-- As an extension, '?T' is short for '?nil|T'.
-- Note how these types are rendered!
function one (name,age,options)
end

--- implicit table can always use colon notation.
person2 = {
    id=true, -- string: official ID number
     sex=true, -- string: one of 'M', 'F' or 'N'
     spouse=true, -- ?person3: wife or husband
}


-- classmod: colon2

--- second useless function.
-- Optional type specifiers are allowed in this format.
-- As an extension, '?T' is short for '?nil|T'.
-- Note how these types are rendered!
function two22 (name,age,options)
end



