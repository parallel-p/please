{$o-,r+}
const
	maxn = 300;

	dx: array [1..4] of longint = (-1, 0, 1, 0);
	dy: array [1..4] of longint = (0, 1, 0, -1);

var
	u, f, pair: array [0..maxn + 1, 0..maxn + 1] of longint;
	used: array [0..maxn + 1, 0..maxn + 1] of boolean;
	cur: longint;	
	q: array [1..maxn * maxn] of record
		i, j: longint;
	end;
	prev: array [1..maxn * maxn] of record
		q, k: longint;
	end;
	sum: longint;

function find(x, y: longint): boolean;
var
	i2, j2, h, t, i, j, k, l: longint;
begin
	h := 1;
	t := 2;
	q[h].i := x;
	q[h].j := y;
	u[x][y] := cur;

	while h < t do
	begin
		i := q[h].i;
		j := q[h].j;

     	for k := 1 to 4 do
     	begin
     		if f[i + dx[k]][j + dy[k]] = 1 then
     		begin
     			if not used[i + dx[k]][j + dy[k]] then
     			begin
     				find := true;
                    used[i + dx[k]][j + dy[k]] := true;

     				l := k;
     				while (i <> x) or (j <> y) do
     				begin
     					pair[i + dx[l]][j + dy[l]] := l;
     					l := prev[h].k;
     					h := prev[h].q;
     					i := q[h].i;
     					j := q[h].j;
     				end;
 					pair[i + dx[l]][j + dy[l]] := l;

 					sum := sum + t;

     				exit;
     			end else begin
     				i2 := i + dx[k] - dx[pair[i + dx[k]][j + dy[k]]];
     				j2 := j + dy[k] - dy[pair[i + dx[k]][j + dy[k]]];
     				if u[i2][j2] <> cur then
     				begin
     					q[t].i := i2;
     					q[t].j := j2;
     					u[i2][j2] := cur;
     					prev[t].q := h;
     					prev[t].k := k;
     					inc(t);
     				end;
     			end;
     		end;
     	end;
     	inc(h);
    end;
    sum := sum + t;
    find := false;
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
	for i := 1 to m do
		for j := 1 to n do
			if (f[i][j] = 1) and ((i + j) mod 2 = 0) then
    		begin
    			if find(i, j) then
    			begin
    				inc(k);
    			end;
				inc(cur);
    		end;

	writeln(a * k + b * (p - 2 * k));
{	writeln(sum / cur :0 :4);}

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