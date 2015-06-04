{$APPTYPE CONSOLE}
{  N (k<=N<=l) M (x<=M<=y)
   a1 ,,, aN (p<=ai<=q)
   b1 ,,, bN (pb<=ai<=qb)}

uses SysUtils;

const
  x=1;
  y=1000;
  k=1; 
  l=100;
  p=1;
  q=100;
  pb=1;
  qb=100;

var
  i, j, numtests, maxqb, N, M, maxq : integer;
  filename : string;
  f : Text;
begin
  RandSeed := 5011979;
  write(ParamStr(1));
  numtests := strtoint(ParamStr(1));
  for i:=1 to numtests do begin
    filename:=inttostr(i);
    if i<10 then
      filename:='0'+filename;
    rewrite(f,filename);
    if i<6 then 
      N:=i
    else 
      N:=k+random(l-k+1);
    M := x+random(y-x+1);
    writeln(f,M);
    maxq:=p+3+random(q-p-2);
    for j:=1 to N do begin
      write(f,p+random(maxq-p+1));
      if j=n then
        writeln(f)
      else
         write(f,' ');
    end;
    maxqb:=pb+3+random(qb-pb-2);
    for j:=1 to N do begin
      write(f,pb+random(maxqb-pb+1));
      if j=n then
        writeln(f)
      else
         write(f,' ');
    end;
    close(f);
  end;
end.