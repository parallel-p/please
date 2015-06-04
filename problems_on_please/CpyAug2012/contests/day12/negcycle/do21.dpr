const name='21';
      n=80;
var i,j:longint;

begin
  writeln(n);
  for i:=1 to n do
    begin
      for j:=1 to n do begin
if (j <> 1) then write(' ');
        if (j=i+1) then
          write('-10000')
        else 
          write('100000');
end;
      writeln;
    end;    
end.