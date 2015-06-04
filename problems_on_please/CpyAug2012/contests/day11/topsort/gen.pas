{$I-}
Uses
  SysUtils;

Var
  I, N, M: LongInt;

Begin
  N := StrToInt(ParamStr(1));
  M := StrToInt(ParamStr(2));
  RandSeed := StrToInt(ParamStr(3));
  Writeln(N, ' ', M);
  For I := 1 to M do
    Writeln(Random(N) + 1, ' ', Random(N) + 1);
End.
