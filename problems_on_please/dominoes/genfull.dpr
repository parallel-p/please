uses
	sysutils;
var
	i, j: longint;
	n, m: longint;
begin
	n := strtoint(paramstr(1));
	m := strtoint(paramstr(2));
	writeln(n, ' ', m, ' 0 1');
	for i := 1 to n do
	begin
		for j := 1 to m do
			write('*');
		writeln;
	end;
end.