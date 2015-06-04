type integer = longint;

Const 
  MaxN = 1000;

Var 
  I, J, N, Max: Longint;
  A: array[1..MaxN] of Longint;
  P: array[1..MaxN] of Integer;

Begin
  Assign(Input, 'sequence.in');
  Assign(Output, 'sequence.out');
  Reset(Input);
  Rewrite(Output);
  Read(N);
  For I := 1 to N do Begin
    Read(A[I]);
    P[I] := 1;
  End;
  Max := 1;
  For I := 1 to N do 
    For J := 1 to I - 1 do
      If (A[J] <> 0) and (A[I] mod A[J] = 0) and (P[I] < P[J] + 1) Then Begin
        P[I] := P[J] + 1;
        If P[I] > Max Then Max := P[I];
      End;
  Write(Max);
  Close(Input);
  Close(Output);
End.
