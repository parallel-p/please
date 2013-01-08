program lcs;

{Andrew Gein, correct solution}

uses Math;

var n, m, i, j : longint;
    a, b : array [1..1000] of longint;
    dp : array [0..1000, 0..1000] of longint;

begin
  assign(input, 'lcs.in');
  assign(output, 'lcs.out');
  reset(input);
  rewrite(output);

  read(n);
  for i := 1 to n do read(a[i]);
  read(m);
  for i := 1 to m do read(b[i]);

  fillchar(dp, sizeof(dp), 0);

  for i := 1 to n do
    for j := 1 to m do
      if a[i] = b[j] then
         dp[i, j] := dp[i - 1, j - 1] + 1
      else
         dp[i, j] := max(dp[i - 1, j], dp[i, j - 1]);

  write(dp[n, m]);

  close(output);
end.