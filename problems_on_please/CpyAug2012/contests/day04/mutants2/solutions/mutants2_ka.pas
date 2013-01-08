var
  a, sum : array [0 .. 1000, 0 .. 1000] of longint;
  i, j, n, m, k : integer;

procedure path(x, y: integer);
begin
  if (x > 1) or (y > 1) then
    if sum[x - 1, y] < sum[x, y - 1] then 
      path(x - 1, y) 
    else
      path(x, y - 1);
  writeln(x, ' ', y);
end;

begin
  fillchar (sum, sizeof(sum), 0);
  read (n, m);
  for i := 1 to n do 
    for j := 1 to m do
      read(a[i, j]);
  sum[1, 1] := a[1, 1];
  for i := 0 to n do 
    sum[i, 0] := maxlongint;
  for i := 0 to m do 
    sum[0, i] := maxlongint;
  for i := 2 to n do
    sum[i, 1] := sum[i - 1, 1] + a[i, 1];
  for i := 2 to m do
    sum[1, i] := sum[1, i - 1] + a[1, i];
  for i := 2 to n do
    for j := 2 to m do 
      if sum[i - 1, j] < sum[i, j - 1] then
        sum[i, j] := a[i, j] + sum[i - 1, j]
      else
        sum[i, j] := a[i, j] + sum[i, j - 1];
  writeln(sum[n, m]);
end.
