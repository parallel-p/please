{$C+,I+,O-,Q+,R+}
Var I, J, N, M, V: Longint;
    Err: Integer;

Begin
  Val(ParamStr(4), RandSeed, Err);
  Val(ParamStr(1), N, Err);
  Val(ParamStr(2), M, Err);
  Val(ParamStr(3), V, Err);
  Writeln(N, ' ', Random(N) + 1, ' ', Random(N) + 1);
  For I := 1 to N do Begin
    For J := 1 to N do begin
      If I = J Then 
        Write('0')
      Else If Random(5000) < V Then 
        Write(Random(M - 1) + 2)
      Else
        Write('-1');

      if (J < N) then begin
        Write(' ');
      end;
    end;
    Writeln;  
  End;
End.