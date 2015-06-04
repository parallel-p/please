uses
	sysutils;
var
	i, j: longint;
	n, m: longint;
begin
	n := strtoint(paramstr(1));
	m := strtoint(paramstr(2));
	writeln(n, ' ', m, ' 230 190');
	for i := 1 to n do
	begin
		for j := 1 to m do
			if (i mod 2 = 1) and (j mod 2 = 1) then
				write('.')
			else
			    write('*');
		writeln;
	end;
end.