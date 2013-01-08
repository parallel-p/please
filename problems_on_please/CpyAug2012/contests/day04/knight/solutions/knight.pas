type
	int = longint;

const
	taskid = 'knight';
	infile = taskid + '.in';
	outfile = taskid + '.out';
	MAXN = 200;

var
	dp: array [-2..MAXN, -2..MAXN] of int64;
	n, m: int;

procedure solve;
var
	i, j: int;
begin
	readln(n, m);
	fillchar(dp, 0, sizeof(dp));
	dp[1][1] := 1;
	for i := 1 to n do
		for j := 1 to m do if (i <> 1) or (j <> 1) then begin
			dp[i][j] := dp[i - 1][j - 2] + dp[i - 2][j - 1];
		end;
	writeln(dp[n][m]);
end;

begin
	solve;
  close(output);
end.
