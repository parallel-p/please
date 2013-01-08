program floyd;

{Correct solution}
{Ющенко Павел, pau@pau.ru}

var
  n, i, j, k :integer;
  a : array [1..100, 1..100] of integer;

function min(a, b : integer) : integer;
begin
  if a < b then min := a else min := b;
end;

begin
  assign(input, 'floyd.in');
  assign(output, 'floyd.out');
  reset(input);
  rewrite(output);

  read(N);

  for i := 1 to n do
    for j := 1 to n do
      read(a[i,j]);

  for k := 1 to n do
    for i := 1 to n do
      for j := 1 to n do
        a[i, j] := min(a[i, j], a[i, k] + a[k, j]);

  for i := 1 to n do begin
    for j := 1 to n do
      write(a[i, j], ' ');
    writeln;
  end;

  close(input);
  close(output);
end.
