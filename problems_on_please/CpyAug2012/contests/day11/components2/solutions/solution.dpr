{$APPTYPE CONSOLE}

var
  a : array [1 .. 100, 1.. 100] of integer;
  color, b : array [1 .. 100] of integer;
  n, m, i, j, c : integer;
  v1, v2 : integer;
  
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
  assign (input, 'components2.in');
  assign (output, 'components2.out');
  reset(input);
  rewrite(output);
  fillchar(a, sizeof(a), 0);
  read (n, m);

  for i := 1 to m do begin
          read(v1, v2);
	  a[v1, v2] := 1;
	  a[v2, v1] := 1;
   end;

  fillchar (c, sizeof (c), 0);
  fillchar (b, sizeof (b), 0);
  c := 0;
  for i := 1 to n do
    if color [i] = 0 then begin
	  inc (c);
	  dfs (i, c);
	end;  

  writeln (c);
  for i := 1 to n do
    inc(b[color[i]]);
  for i := 1 to c do begin
    writeln(b[i]);
    for j := 1 to n do
      if color[j] = i then
        write(j, ' ');
  end;
   
  close (input); close (output)
end.
