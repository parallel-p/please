uses
	sysutils;

const
	maxn = 100;

var
	dx1, dx2, p, k, i, j: longint;
	n, m: longint;
	a: array [1..maxn, 1..maxn] of char;

procedure put(i, j: longint);
begin
	if (i < 1) or (i > n) or (j < 1) or (j > m) then
		exit;
	a[i][j] := '*';
end;

procedure genline(x, y, w, h, dx: longint);
var
	i, j: longint;
begin
	for i := 1 to h do
	begin
		for j := 1 to w do
			put(x + i - 1, y + (i - 1) * dx + j - 1);
	end;
end;

begin
	n := 81;
	m := 93;
	p := 67;
	randseed := 5896;
	writeln(n, ' ', m, ' 7 6');
	fillchar(a, sizeof(a), '.');

	dx1 := 10;
	dx2 := 13;

    for k := 1 to p do
    begin
    	genline(random(n) + 1, random(m) + 1, random(30) + 2, random(n) + 2, 1 - 2 * random(2));
    end;

	for i := 1 to n do
	begin
		for j := 1 to m do
			write(a[i][j]);
		writeln;
	end;
end.              