Const
  maxn = 1000001;

type
  integer = longint;

Var
  a: array [0..maxn] of integer;
  i, n, k, x: integer;

Function SearchL(x: integer) : integer;
Var
  right, left, m: integer;
Begin
  left := 0;
  right := n;
  While right - left > 1 do Begin
    m := (right + left) div 2;
    If a[m] >= x then
      right := m
    Else
      left := m;
  End;
  If a[right] <> x then
    right := 1;  
  SearchL := right;
End;

Function SearchR(x: integer) : integer;
Var
  right, left, m: integer;
Begin
  left := 1;
  right := n + 1;
  While right - left > 1 do begin
    m := (right + left) div 2;
    If a[m] > x then
      right := m
    Else
      left := m;
  End;                
  if a[left] <> x then
    left := 0;
  SearchR := left;
End;


Begin
  For i := 1 to n do
    read(a[i]);
  For i := 1 to k do Begin
    read(x);
    writeln(SearchR(x) - SearchL(x) + 1);
  End;
End.