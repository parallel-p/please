const
	maxn = 1000;

	dx: array [1..4] of longint = (-1, 0, 1, 0);
	dy: array [1..4] of longint = (0, 1, 0, -1);

var
	u, f, pair: array [0..maxn + 1, 0..maxn + 1] of longint;
	used: array [0..maxn + 1, 0..maxn + 1] of boolean;
	best, cur, sum, cases: longint;	

function rec(i, j, level: longint): boolean;
var
	k, i2, j2: longint;
begin
	u[i][j] := cur;
	if best < level then best := level;
	for k := 1 to 4 do
	begin
		if f[i + dx[k]][j + dy[k]] = 1 then
		begin
			if not used[i + dx[k]][j + dy[k]] then
			begin
				rec := true;
				pair[i + dx[k]][j + dy[k]] := k;
				used[i + dx[k]][j + dy[k]] := true;
				exit;
			end else begin
				i2 := i + dx[k] - dx[pair[i + dx[k]][j + dy[k]]];
				j2 := j + dy[k] - dy[pair[i + dx[k]][j + dy[k]]];
				if u[i2][j2] <> cur then
				begin
					if rec(i2, j2, level + 1) then
					begin
						pair[i + dx[k]][j + dy[k]] := k;
						rec := true;
						exit;
					end;
				end;
			end;
		end;
	end;
	rec := false;
end;

var
	i, j, a, b, p, k, m, n: longint;
	c: char;

begin
	assign(input, 'dominoes.in');
	reset(input);
	assign(output, 'dominoes.out');
	rewrite(output);

	readln(m, n, a, b);
	p := 0;
	cur := 1;
	for i := 1 to m do
	begin
		for j := 1 to n do
		begin
			read(c);
			if c = '.' then
				f[i][j] := 0
			else
				f[i][j] := 1;
			if f[i][j] = 1 then
				inc(p);
		end;
		readln;
	end;

	if a >= 2 * b then
	begin
		writeln(p * b);
		exit;
	end;

	k := 0;
	sum := 0;
	cases := 0;
	for i := 1 to m do
		for j := 1 to n do
			if (f[i][j] = 1) and ((i + j) mod 2 = 0) then
    		begin
    			best := 0;
    			inc(cases);
    			if rec(i, j, 1) then
    				inc(k);
    			sum := sum + best;
				inc(cur);
    		end;

	writeln(a * k + b * (p - 2 * k));
//	writeln(sum / cases :0 :4);

{	for i := 1 to m do
	begin
		for j := 1 to n do
		begin
			if pair[i][j] <> 0 then
				write(pair[i][j])
			else
				write(0);
			write(' ');
		end;
		writeln;
    end;}

	close(input);
	close(output);
end.