uses
    SysUtils;

var
    n, i, j : longint;

begin
    n := strtoint(ParamStr(1));

    writeln(n);

    for i := 1 to n do begin
        for j := 1 to n do begin
            write('0');

            if (j < n) then begin
                write(' ');
            end;
        end;

        writeln;
    end;
end.