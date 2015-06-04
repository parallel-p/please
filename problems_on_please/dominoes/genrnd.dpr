uses
	sysutils;
var
	i, j: longint;
	n, m, p: longint;
begin
	n := strtoint(paramstr(1));
	m := strtoint(paramstr(2));
	p := strtoint(paramstr(3));
	writeln(n, ' ', m, ' 0 1');
	for i := 1 to n do
	begin
		for j := 1 to m do
			if random(100) < p then
				write('*')
			else
				write('.');
		writeln;
	end;
end.