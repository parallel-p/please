program grig;

{Andrew Gein, correct solution}

var n, k, i, j : longint;
    a : array [-100..100000] of longint;

begin
  for i := -100 to 100000 do a[i] := 0;
  read(n, k);
  if (n > 30) or (k > 10) then halt(1);
  a[1] := 1;
  for i := 2 to n do 
     for j := 1 to k do
        a[i] := a[i] + a[i - j];
  write(a[n]);
end.