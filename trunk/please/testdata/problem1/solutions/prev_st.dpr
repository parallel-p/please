{$APPTYPE CONSOLE}

const
    MAXN = 100010;

var
    a: array[0..MAXN] of longint;
    n: longint;

procedure init();
begin
    assign(input, 'prev.in');
    reset(input);
    assign(output, 'prev.out');
    rewrite(output);
end;

procedure swap(var x, y: longint);
var
    t: longint;
begin
    t := x;
    x := y;
    y := t;
end;

procedure reverse(left, right: longint);
var
    i, j: longint;
begin
    i := left;
    j := right;
    while (i <= j) do begin
        swap(a[i], a[j]);
        inc(i);
        dec(j);
    end;
end;

procedure solve();
var
    i, j, midx: longint;
begin
    read(n);
    for i := 1 to n do begin
        read(a[i]);
    end;

    i := n - 1;

    while ((a[i] < a[i + 1]) and (i > 0)) do begin
        dec(i);
    end;

    if (i = 0) then begin
        for j := 1 to n do begin
            a[j] := n - j + 1;
        end;
    end else begin
        midx := i + 1;
        for j := i + 1 to n do begin
            if ((a[j] < a[i]) and (a[midx] < a[j])) then begin
                midx := j;
            end;
        end;

        swap(a[i], a[midx]);
        reverse(i + 1, n);
    end;

    for i := 1 to n do begin
        write(a[i], ' ');
    end;
end;

begin
    init();
    solve();
end.
