uses
	sysutils;

const
	maxn = 100;

var
	p, k, i, j: longint;
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
	n := 99;
	m := 70;
	writeln(n, ' ', m, ' 3 2');
	fillchar(a, sizeof(a), '.');

	genline(1, 1, 2, 100, 1);

	for i := 1 to n do
	begin
		for j := 1 to m do
			write(a[i][j]);
		writeln;
	end;
end.              