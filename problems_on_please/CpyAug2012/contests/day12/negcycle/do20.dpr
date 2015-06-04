const name='20';
      n=80;
var i,j:longint;

begin
  writeln(n);
  for i:=1 to n do
    begin
      for j:=1 to n do begin
if (j <> 1) then write(' ');
        write('-1');
end;
      writeln;
    end;    
end.