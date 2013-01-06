{$APPTYPE CONSOLE}

type
  edge = record
    dest, next : integer;
  end;	

var
  a : array [1 .. 100010] of edge;
  way, beg: array [1 .. 100010] of integer;
  color : array [1 .. 100010] of integer;
  n, m, i, c, x, y : integer;
  
procedure writeway;
begin
  writeln ('-1');
  close (input); close (output);
  halt (0)  
end;  
  
procedure dfs (x : integer);
var
  i, t, e : integer;
begin
  color[x] := 1;
  e := beg[x];
  while e <> 0 do begin
    if color[a[e].dest] = 1 then writeway;
	if color[a[e].dest] = 0 then dfs (a[e].dest);
	e := a[e].next
  end;  
  color[x] := 2;
  inc (c);
  way[c] := x;
end;	  
  
procedure addEdge(m, x, y : integer);
begin
  a[m].dest := y;
  a[m].next := 0;
  if beg[x] = 0 then begin
    beg[x] := m;
	color[x] := m
  end else begin
    a[color [x]].next := m;
    color[x] := m
  end	
end;  
  
begin
  reset (input, 'topsort.in');
  rewrite (output, 'topsort.out');
  fillchar (color, sizeof (color), 0);
  fillchar (beg, sizeof (beg), 0);
  read (n, m);
  for i := 1 to m do begin
    read (x, y);
	addEdge(i, x, y)
  end;
  c := 0;
  fillchar (color, sizeof (color), 0);
  for i := 1 to n do
    if color [i] = 0 then dfs (i);  
  for i := c downto 1 do
    write (way [i],' ');
  close (input); close (output)
end.
