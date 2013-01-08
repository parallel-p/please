const name='16';
      n=17;
var i,j:longint;

begin
  randseed:=8275982;
  writeln(n);
  for i:=1 to n do
    begin
      for j:=1 to n do begin
if (j <> 1) then write(' ');
        if random(5)<>0 then
          write(random(20000)-10000)
        else
          write('100000');
end;
      writeln;
    end;    
end.