{$APPTYPE CONSOLE}

var
  a : array [1 .. 100, 1.. 100] of integer;
  color : array [1 .. 100] of integer;
  n, i, j, c : integer;
  
procedure no;
begin
  writeln ('NO');
  close (input); close (output);
  halt (0)  
end;  
  
procedure dfs (x : integer);
var
  i : integer;
begin
  color [x] := 1;
  for i := 1 to n do begin
    if (a[x, i] = 1) and (color [i] = 1) then no;
    if a[x, i] = 1 then begin
	  a [i, x] := 0;
	  a [x, i] := 0;
	  dfs (i)
	end;  
  end;  
end;	  
  
begin
  reset (input, 'baobab.in');
  rewrite (output, 'baobab.out');
  read (n);
  for i := 1 to n do
    for j := 1 to n do
	  read (a [i, j]);
  fillchar (c, sizeof (c), 0);
  dfs (1);  
  for i := 1 to n do 
    if color [i] = 0 then no;
  writeln ('YES'); 
  close (input); close (output)
end.
