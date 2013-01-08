{$APPTYPE CONSOLE}

type
  edge = record
    dest, next : integer;
  end;	

var
  a : array [1 .. 100000] of edge;
  way, beg: array [1 .. 100000] of integer;
  color, path : array [1 .. 100000] of integer;
  n, m, i, c, x, y : integer;
  
procedure writepath(x, y: integer);
var i : integer;
begin
  writeln ('YES');
  {repeat
    write(x,' ');
    x := path[x]
  until x = y;
  writeln(y);}
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

    if color[a[e].dest] = 1 then 
      writepath(a[e].dest, x);

    path[x] := a[e].dest; 	  
    dfs (a[e].dest);
  end;
  color[x] := 2;  
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
  assign (input, 'cycle.in');
  assign (output, 'cycle.out');
  reset(input);
  rewrite(output);
  fillchar (color, sizeof (color), 0);
  fillchar (beg, sizeof (beg), 0);
  read (n, m);
  for i := 1 to m do begin
    read (x, y);
	addEdge(i, x, y)
  end;
  fillchar (color, sizeof (color), 0);
  for i := 1 to n do
    if color [i] = 0 then dfs (i);  
  writeln ('NO'); 
  close (input); close (output)
end.
