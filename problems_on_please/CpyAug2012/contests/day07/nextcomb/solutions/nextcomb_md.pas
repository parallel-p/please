const
  MAX = 50;

type
  int = longint;

var
  n, k, i: int;
  a: array[1..MAX] of int;
  used: array[1..MAX] of boolean;

begin
  assign(input, 'nextcomb.in');
  assign(output, 'nextcomb.out');
  reset(input);
  rewrite(output);
  read(n, k);
  for i := 1 to k do
  begin
    read(a[i]);
  end;
  i := k;
  while (i > 0) and (a[i] = i - k + n) do
    dec(i);
  if (i = 0) then
  begin
    writeln(0);
    close(output);
    halt(0);
  end;
  inc(a[i]);
  inc(i);
  while (i <= k) do
  begin
    a[i] := a[i - 1] + 1;
    inc(i);
  end;
  for i := 1 to k do
    write(a[i], ' ');
  close(output);
end.