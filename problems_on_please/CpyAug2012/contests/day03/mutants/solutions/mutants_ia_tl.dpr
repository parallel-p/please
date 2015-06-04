Const
  maxn = 1000001;

Type
  integer = longint;

Var
  a: array [0..maxn] of integer;
  i, n, k, x: integer;

Function Search(x: integer) : integer;
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
  If a[right] <> x then Begin
    Search := 0;
    Exit;
  End;  
  m := 0;
  While a[right] = x do Begin
    inc(m);
    inc(right);
  End;
  Search := m;
End;


Begin
  For i := 1 to n do
    read(a[i]);
  For i := 1 to k do Begin
    read(x);
    writeln(Search(x));
  End;
End.