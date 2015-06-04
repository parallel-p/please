{$APPTYPE CONSOLE}
{$R+; Q+; S+}
{$MAXSTACKSIZE $11000000}
type pnode = ^tnode;
     tnode = record
       b : longint;
       next : pnode; 
     end;
var
  a : array [1 .. 100001] of pnode;
  from : array [1..100001] of longint;
  used : array [1..100001] of longint;
  n, m, i, x, y : integer;

procedure addvertex(x, y : longint);
var p: pnode;
begin
  new(p);
  p^.b := y;
  p^.next := a[x];
  a[x] := p;
end;

procedure print;
begin
  close(input);
  close(output);
  halt(0);
end;

procedure writepath(t, start : longint);
begin
  if t = start then begin
    write(start,' ');
    exit;
  end;
  writepath(from[t], start);
  write(t, ' ');
end;

procedure dfs(t : longint);
var 
p: pnode;
    y: longint;
begin
  p := a[t];
  if used[t] = 1 then
    begin
      writeln('YES');
      {writepath(from[t], t);}
      print;
    end;
  used[t] := 1;
  while p <> nil do begin
    y := p^.b;
    from[y] := t;
    dfs(y);
    p := p^.next;
  end;
  used[t] := 2;
end;
begin
  assign (input, 'cycle.in');
  reset(input);
  assign (output, 'cycle.out');
  rewrite(output);
  fillchar(a,sizeof(a),0);
  read(n, m);
  fillchar(from, sizeof(from), 0);
  for i := 1 to m do
    begin
      read(x, y);
      addvertex(x, y);
    end;
  for i := 1 to n do
    if used[i] = 0 then
      dfs(i); 
  write('NO');
  close (input);
  close (output)
end.
