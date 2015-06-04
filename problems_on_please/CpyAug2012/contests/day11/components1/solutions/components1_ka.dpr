{$APPTYPE CONSOLE}

var
  a : array [1 .. 100, 1.. 100] of integer;
  color : array [1 .. 100] of integer;
  n, i, j, c : integer;
  
procedure dfs (x, c : integer);
var
  i : integer;
begin
  color [x] := c;
  for i := 1 to n do
    if (a[x, i] = 1) and (color [i] = 0) then
	  dfs (i, c)
end;	  
  
begin
  assign (input, 'components1.in');
  assign (output, 'components1.out');
  reset(input);
  rewrite(output);
  read (n);
  for i := 1 to n do
    for j := 1 to n do
	  read (a [i, j]);
  fillchar (c, sizeof (c), 0);
  c := 0;
  for i := 1 to n do
    if color [i] = 0 then begin
	  inc (c);
	  dfs (i, c);
	end;  
  writeln (c); 
  close (input); close (output)
end.
