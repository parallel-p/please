const name='18';
      n=80;
      c=7;
var i,j:longint;

begin
  randseed:=1;
  writeln(n);
  for i:=1 to n do
    begin
      for j:=1 to n do  begin
if (j <> 1) then write(' ');
        if (random(c)=0)and(i<>j) then
          write(random(20000)-10000)
        else
          if i=j then
            write('0')
          else
            write('100000');
end;
      writeln;
    end;    
end.