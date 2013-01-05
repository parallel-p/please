uses
    SysUtils;

var
    i, n: longint;

begin
    n := StrToInt(ParamStr(1));
    writeln(n);
    for i := 1 to n do begin
        write(i);
        if (i < n) then begin
            write(' ');
        end;
    end;
    writeln;
end.
