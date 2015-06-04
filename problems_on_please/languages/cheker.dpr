program cheker;

{$APPTYPE CONSOLE}

uses
  SysUtils,
  Testlib;

type
 tmas = array [1..1000] of string;

var
 n1,n2,m1,m2,i,j:integer;
 nmas1,nmas2,mmas1,mmas2 : tmas;

procedure sort (var mas:tmas;n:integer);
 var
  j:integer;
  t:Boolean;
  temp:string;
 begin
  t:=True;
  while t do
   begin
    t:=False;
    for j:=1 to n-1 do
     if mas[j]>mas[j+1] then
      begin
       temp:=mas[j];
       mas[j]:=mas[j+1];
       mas[j+1]:=temp;
       t:=True;
      end;
   end;
 end;

function check (mas,mas2 : tmas;n:integer) : boolean;
 var
  i:integer;
 begin
  result:=true;
  for i:=1 to n do
   if mas[i]<>mas2[i] then result := false;
 end;

begin
  {while not(ouf.SeekEof) do
    nmas1[i]:=ouf.ReadString;
  Quit(_ok  ,'OK');  }
  n1 := ouf.ReadInteger;
  if n1>1000 then Quit(_pe,'4');
  ouf.NextLine;
  n2 := ans.ReadInteger;
  if n1>1000 then Quit(_pe,'4');
  ans.NextLine;
  for i:=1 to n1 do
   nmas1[i]:=ouf.ReadString;
  sort(nmas1,n1);
  for i:=1 to n2 do
   nmas2[i]:=ans.ReadString;
  sort(nmas2,n2);
  m1 := ouf.ReadInteger;
  if m1>1000 then Quit(_pe,'4');
  ouf.NextLine;
  m2 := ans.ReadInteger;
  if m2>1000 then Quit(_pe,'4');
  ans.NextLine;
  for i:=1 to m1 do
   mmas1[i]:=ouf.ReadString;
  sort(mmas1,m1);
  for i:=1 to m2 do
   mmas2[i]:=ans.ReadString;
  sort(mmas2,m2);
  if (n1<>n2)or(m1<>m2) then Quit(_wa,'1');
  if not(check(nmas1,nmas2,n1)) then Quit(_wa,'2');
  if not(check(mmas1,mmas2,m1)) then Quit(_wa,'3');
  Quit(_ok  ,'OK');
end.

