uses
	sysutils;

const
	maxn = 300;

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

begin
	n := strtoint(paramstr(1));
	m := strtoint(paramstr(2));
	p := strtoint(paramstr(3));
	writeln(n, ' ', m, ' 600 590');
	fillchar(a, sizeof(a), '.');
	for i := 1 to p do
	begin
		j := random(n) + 1;
		k := random(m) + 1;
		put(j, k);
		put(j + 1, k);
		put(j, k + 1);
	end;
	for i := 1 to n do
	begin
		for j := 1 to m do
			write(a[i][j]);
		writeln;
	end;
end.              