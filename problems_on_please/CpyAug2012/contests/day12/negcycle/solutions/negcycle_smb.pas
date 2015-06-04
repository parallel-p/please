const
	MAXN = 110;
	INF = 100000;

type
	int = longint;

var
	n, pathn : int;
	d, m: array[1..MAXN, 1..MAXN] of int;
	neg : boolean;
	path : array[1..MAXN] of int;

procedure readData;
var
	i, j : int;
begin
	read(n);
	for i := 1 to n do
		for j := 1 to n do
			read(d[i][j]);
end;

procedure getpath(i, j : int);
begin
	if 0 = m[i, j] then begin
		inc(pathn);
		path[pathn] := i;
	end	else begin
		getpath(i, m[i, j]);
		getpath(m[i, j], j);
	end;
end;

procedure floyd;
var k, i, j : int;
begin
	neg := false;

	for i := 1 to n do
		m[i, i] := 0;

	for k := 1 to n do begin
		for i := 1 to n do
			if d[i, i] < 0 then begin
				pathn := 0;
				getpath(i, i);
				neg := true;
				exit;
			end;
		for i := 1 to n do
			for j := 1 to n do
				if (INF <> d[i, k]) and (INF <> d[k, j]) and (d[i, j] > d[i, k] + d[k, j]) then begin
					d[i, j] := d[i, k] + d[k, j];
					m[i, j] := k;
				end;
	end;
end;

procedure print;
var i : int;
begin
	if not neg then writeln('NO') else begin
    	writeln('YES');
    	writeln(pathn);
    	for i := 1 to pathn do
    		write(path[i], ' ');
    end;
end;

begin
    assign(input, 'negcycle.in'); reset(input);
    assign(output, 'negcycle.out'); rewrite(output);

    readData;
    floyd;
    print;

    close(input);
    close(output);
end.
