Const MaxN = 2000;
      Big = 1000000000;

type 
  integer = longint;

Var I, J, N, S1, S2, M: Integer;
    A: array[1..MaxN, 1..MaxN] of Integer;
    D: array[0..MaxN] of Integer;
    Use: array[0..MaxN] of Boolean;

Begin
  Assign(Input, 'dijkstra.in');
  Assign(Output, 'dijkstra.out');
  Reset(Input);
  Rewrite(Output);
  Read(N, S1, S2);
  For I := 1 to N do Begin
    For J := 1 to N do Begin
      Read(A[I, J]);
      If A[I, J] < 0 Then A[I, J] := Big;
    End;
    D[I] := Big;
  End;
  D[0] := Big + 1;
  D[S1] := 0;
  For I := 1 to N do Begin
    M := 0;
    For J := 1 to N do
      If (D[J] < D[M]) and not Use[J] Then M := J;
    Use[M] := True;
    For J := 1 to N do
      If D[J] > A[M, J] + D[M] Then D[J] := A[M, J] + D[M];
  End;
  If D[S2] = Big Then Write('-1')
                 Else Write(D[S2]);
  Close(Input);
  Close(Output);
End.
