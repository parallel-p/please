{$O-}
{$APPTYPE CONSOLE}

uses SysUtils, Math;
{$R+}
Const
  maxn = 1010;
  filename = 'lcs';
Var
  a, b: array [1..maxn] of longint;
  v: array [0..maxn, 0..maxn] of longint;
  i, n, m, j : longint;
Begin
  assign(input, filename + '.in');
  reset(input);
  assign(output, filename + '.out');
  rewrite(output);
  fillchar(v, sizeof(v), 0);
  read(n);
  for i := 1 to n do
    read(a[i]);
  read(m);
  for i := 1 to m do
    read(b[i]);
  for i := 1 to n do
    for j := 1 to m do
      if a[i] = b[j] then
        v[i, j] := v[i - 1, j - 1] + 1 else
        v[i, j] := max(v[i - 1, j], v[i, j - 1]);
  write(v[n, m]);      
  close(input);
  close(output);
End.