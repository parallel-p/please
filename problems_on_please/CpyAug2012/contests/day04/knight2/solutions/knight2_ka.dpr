{$MODE DELPHI}

var
  a : array [-1 .. 50, -1 .. 50] of integer;
  k, i, j, n, m : integer;

begin
  fillchar (a, sizeof(a), 0);
  read (n, m);
  a[1, 1] := 1;
  for k := 2 to n do begin
    i := k;
	j := 1;
	while (i >= 1) and (j <= m) do begin
      a[i, j] := a[i - 1, j - 2] + a[i - 2, j - 1] + a[i + 1, j - 2] + a[i - 2, j + 1];
	  dec (i);
	  inc (j)
	end
  end;
  for k := 2 to m do begin
    i := n;
	j := k;
	while (i >= 1) and (j <= m) do begin
      a[i, j] := a[i - 1, j - 2] + a[i - 2, j - 1] + a[i + 1, j - 2] + a[i - 2, j + 1];
	  dec (i);
	  inc (j)
	end
  end;
  writeln (a[n, m]);	  
end.

