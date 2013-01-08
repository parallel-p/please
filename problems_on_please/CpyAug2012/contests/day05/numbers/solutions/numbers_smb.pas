
Const MaxN = 20;

Var I, J, N: Integer;
    A: array[1..MaxN, 0..9] of Extended;

Begin
  Assign(Input, 'numbers.in');
  Assign(Output, 'numbers.out');
  Reset(Input);
  Rewrite(Output);
  Read(N);
  For I := 1 to 9 do
    A[1, I] := 1;
  For I := 2 to N do 
    For J := 0 to 9 do Begin
      If J > 0 Then A[I, J] := A[I, J] + A[I - 1, J - 1];
      A[I, J] := A[I, J] + A[I - 1, J];
      If J < 9 Then A[I, J] := A[I, J] + A[I - 1, J + 1];
    End;
  For J := 1 to 9 do 
    A[N, 0] := A[N, 0] + A[N, J];
  Writeln(A[N, 0]:0:0);
  Close(Input);
  Close(Output);
End.