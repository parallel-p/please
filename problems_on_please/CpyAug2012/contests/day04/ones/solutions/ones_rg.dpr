{$APPTYPE CONSOLE}

uses SysUtils;

Const
  maxn = 40;

Var
  a: array [1..maxn] of longint;
  i, n : longint;
Begin
  read(n);
  a[1] := 2;
  a[2] := 4;
  a[3] := 7;
  for i := 4 to n do
    a[i] := a[i - 1] + a[i - 2] + a[i - 3];
  write(a[n]);   
End.
