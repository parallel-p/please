program grig;

{Andrew Gein, TL solution}

var n, k, i : longint;
    a : array [-100..100000] of longint;

function solve(n, k : longint) : longint;
var i : longint;
begin
  if n <= 0 then result := 0;
  if n = 1 then result := 1;
  if n <= 1 then exit;
  result := 0;
  for i :=  1 to k do result := result + solve(n - i, k);
end;

begin
  for i := -100 to 100000 do a[i] := 0;
  read(n, k);
  write(solve(n, k));
end.