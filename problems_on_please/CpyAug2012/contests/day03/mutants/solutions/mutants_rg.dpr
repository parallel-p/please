{$O-}
{$APPTYPE CONSOLE}

uses SysUtils;

Const
  maxn = 1000000;

Var
  a: array [1..maxn] of longint;
  i, n, k, x: integer;
  t1, t2 : Longint;

function lower(x : longint): longint;
var left, right, mid: longint;
begin
  left := 0;
  right := n;
  while right - left > 1 do begin
    mid := (left + right) div 2;
    if a[mid] < x then left := mid else
                       right := mid;
  end;
  result := right;
end;

function upper(x : longint): longint;
var left, right, mid: longint;
begin
  left := 1;
  right := n+1;
  while right - left > 1 do begin
    mid := (left + right) div 2;
    if a[mid] <= x then left := mid else
                       right := mid;
  end;
  if a[left] = x then result := left else result := n+1;
end;

Begin
  for i := 1 to n do
    read(a[i]);
  for i := 1 to k do begin
      read(x);
      t2 := upper(x);
      if t2 <= n then begin
        t1 := lower(x);
        writeln(t2 - t1 + 1);
      end else writeln(0);  
  end;
End.