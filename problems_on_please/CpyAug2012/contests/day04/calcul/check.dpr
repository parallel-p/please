uses testlib;
var
    yourans, n, i, j, last : integer;
begin
    yourans := ouf.readlongint;
    if yourans = ans.readlongint then begin
        n := inf.readlongint;
        last := ouf.readlongint;
        for i := 2 to yourans+1 do begin
            j := ouf.readlongint;
            if i > 1 then
              if (j = last*2) or (j = last*3) or (j = last+1) then begin
              end
               else Quit (_WA, 'Wrong number');
            last := j;
        end;
        if last = N then Quit (_OK, 'Accepted')
          else Quit (_WA, 'Wrong last number');
    end
      else Quit (_WA, 'Wrong answer');

end.