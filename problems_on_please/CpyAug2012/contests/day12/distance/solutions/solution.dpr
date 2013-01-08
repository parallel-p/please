const
    max_n = 5000;
    max_m = 100000;
var
    n, m: longint;
    next, weight, vertex: array [1..2 * max_m] of longint;
    s: array [1..max_n] of longint;
    b, e, w: longint;
    d, p: array [0..max_n] of longint;
    u: array [0..max_n] of boolean;
    mini: longint;
    c, q: longint;
    vs, vt: longint;

procedure add(b, e, w: longint);
begin
    inc(c);
    next[c] := s[b];
    vertex[c] := e;
    weight[c] := w;
    s[b] := c;
end;

var
    i, j: longint;
begin
    reset(input, 'distance.in');
    rewrite(output, 'distance.out');

    read(n, m);
    read(vs, vt);
    for i := 1 to m do begin
        read(b, e, w);
        add(b, e, w);
        add(e, b, w);
    end;

    for i := 0 to n do begin
        d[i] := maxlongint;
    end;
    d[vs] := 0;

    for i := 1 to n do begin
        mini := 0;
        for j := 1 to n do begin
            if (not u[j]) and (d[mini] > d[j]) then begin
                mini := j;
            end;
        end;

        u[mini] := true;

        q := s[mini];
        while q <> 0 do begin
            if d[vertex[q]] > d[mini] + weight[q] then begin
                d[vertex[q]] := d[mini] + weight[q];
                p[vertex[q]] := mini;
            end;
            q := next[q];
        end;
    end;

    writeln(d[vt]);

//**************************** Added by IA ********************************
    q := vt;
    mini := 0;
    while q <> vs do begin
      inc(mini);
      s[mini] := q;
      q := p[q];
    end;
    write(vs, ' ');
    for i := mini downto 1 do
      write(s[i], ' ');   
//============================ Added by IA ================================

    close(input);
    close(output);
end.