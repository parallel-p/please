program valid;

{$APPTYPE CONSOLE}

uses
  SysUtils,TestLib;

var
 n,i,j:integer;
 m : array [1..10000] of integer;
 s : string;

begin
  n := inf.readinteger;
  for i:=1 to n do
   begin
    m[i] := inf.readinteger;
    for j:=1 to m[i] do
     s := inf.readstring;
   end;
  Quit(_ok,'OK');
end.
