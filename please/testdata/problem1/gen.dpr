uses
    SysUtils;

const
    MaxN = 100000;
    C = 10;

var
    i, j, n, t, k: longint;
    A: array[1..MaxN] of longint;

begin
    RandSeed := StrToInt(ParamStr(2));
    n := StrToInt(ParamStr(1));
    writeln(n);
    for i := 1 to n do
        A[i] := i;
    for k := 1 to C * n do begin
        i := Random(n) + 1;
        j := Random(n) + 1;
        t := A[i];
        A[i] := A[j];
        A[j] := t;
    end;
    for i := 1 to n do begin
        write(A[i]);
        if (i < n) then begin
            write(' ');
        end;
    end;
    writeln;
end.
