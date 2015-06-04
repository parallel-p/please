uses
    SysUtils;

const
    MAX_RANGE = 10000;
    MAX_N = 1000;

var
    n, i, j: longint;
    a: array [1..MAX_N] of longint;

begin
    n := strtoint(ParamStr(1));
    randseed := strtoint(ParamStr(2));

    for i := 1 to n do begin
        a[i] := random(MAX_RANGE * 2) - MAX_RANGE;        
    end; 

    for j := 1 to 2 do begin

        for i := 1 to n do begin
            write(a[i]);

            if (i < n) then begin
                write(' ');
            end else begin
                writeln;
            end;
        end;
    end;
end.