uses testlib;

var j, i, n : longint;
    w : array [1..100, 1..100] of longint;
    ja, ca : string; 
    pl, st : longint;
    c, p : longint;
    ww : longint;

begin
  n := inf.readlongint;
  for i := 1 to n do
    for j := 1 to n do
      w[i, j] := inf.readlongint;
  ja := ans.readword(blanks, blanks);
  ca := ouf.readword(blanks, blanks);

  if ((ca <> 'YES') and (ca <> 'NO')) then 
    quit(_pe, 'YES or NO expected');
  if (ca = 'NO') then begin
    if (ja <> 'NO') then 
      quit(_wa, 'Expected YES, find NO')
    else
      quit(_ok, 'Answer NO');
  end else begin
    pl := ouf.readlongint;
    ww := 0;
    if (pl < 1) then
      quit(_pe, 'Illegel path length');
    st := ouf.readlongint;
    p := st;
    for i := 2 to pl do begin
      c := ouf.readlongint;
      if (w[p, c] >= 100000) then
        quit(_wa, 'No edge');
      ww := ww + w[p,c];
      p := c;
    end;
    ww := ww + w[p, st];
    if w[p, st] >= 100000 then
       quit(_wa, 'No edge');
    if(ww >= 0) then
      quit(_wa, 'Path length is not negative')
    else begin
      if(ja = 'NO') then
        quit(_fail, 'Students solution is better');
      quit(_ok, 'Ok');
    end;
  end;
end.