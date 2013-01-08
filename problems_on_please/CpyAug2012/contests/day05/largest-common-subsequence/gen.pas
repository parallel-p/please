uses
    SysUtils;

const
    MaxN = 1000;
    MaxRange = 10000;

var
    a, b: array [1..1000] of integer;
    n, m, i, j: integer;

begin
    n := strtoint(ParamStr(1));
    m := strtoint(ParamStr(2));
    randseed := strtoint(ParamStr(3));

    if n = 0 then begin
        n := random(MaxN) + 1;
    end;

    if m = 0 then begin
        m := random(MaxN) + 1;
    end;

    for i := 1 to n do begin
        a[i] := random(MaxRange * 2) - MaxRange;
    end;

    for i := 1 to m do begin
        b[i] := random(MaxRange * 2) - MaxRange;
    end;

    for i := 1 to n do begin
        write(a[i]);

        if (i < n) then begin
            write(' ');
        end else begin
            writeln;
        end;
    end;

    for i := 1 to m do begin
        write(b[i]);

        if (i < m) then begin
            write(' ');
        end else begin
            writeln;
        end;
    end;

end.
