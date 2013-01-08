{$R+,Q+}

uses
    SysUtils;

const
    INFTY = 1000000000;
    MAXN = 5000;

function min(a, b : longint): longint;
begin
    if (a < b) then
        result := a
    else
        result := b;
end;

var
    n: longint;
    a, b, c: longint;
    ans: array [-2..MAXN+3] of longint;

    i, j: longint;

begin
    assign(input, 'tickets.in');
    reset(input);
    assign(output, 'tickets.out');
    rewrite(output);

    read(n);
    
    for i := 2 to n+3 do begin
        ans[i] := INFTY;
    end;
    
    ans[1] := 0;

    for i := 1 to n do begin
        for j := 1 to 3 do begin
            read(a);
            ans[i + j] := min(ans[i + j], ans[i] + a);
        end;
    end;

    writeln(ans[n + 1]);

    close(input);
    close(output);

end.
