program sec_sol;

{$APPTYPE CONSOLE}

uses
  SysUtils;

const
  Len = 90000;

type
  rec = record
   s:string;
   c:Integer;
  end;

var
  hh:int64;
  mas : array [1..len] of rec;
  n,m,t,i,j:Integer;
  s:string;

function g (s:string;i:integer):int64;
 const
   p = 31;
 begin
  if i>Length(s) then Exit;
  g:= (Ord(s[i]) + p*g(s,i+1)) mod len+1;
 end;

function h (s:string):Int64;
 const
   p = 31;
 begin
   h := g(s,1);
 end;



begin
  Readln(n);
  for i:=1 to n do
   begin
     Readln(m);
     for j:=1 to m do
      begin
        Readln(s);
        hh := h(s);
        Inc(mas[hh].c);
        mas[hh].s:=s;
      end;
   end;
  n:=0;
  m:=0;
  t:=0;
  for i:=1 to len do
   begin
     if mas[i].c=n then
        Inc(m);
     if mas[i].c>0 then
        Inc(t);     
   end;

  Writeln(m);
  for i:=1 to len do
     if mas[i].c=n then
        writeln(mas[i].s);

  m:=t;
  Writeln(m);
  for i:=1 to len do
     if mas[i].c>0 then
        writeln(mas[i].s)
end.
 