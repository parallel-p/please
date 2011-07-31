{$APPTYPE CONSOLE}
uses
  SysUtils;
type PEdge = ^TEdge;
     TEdge = record
               t, x: integer;
               next: PEdge;
             end;
var n, m, i, x, y, l, r, qq: integer;
    a: array [1..100000] of integer;
    q, b, pr, ans: array [0..200000] of integer;
    list: array [1..200000] of PEdge;
    f: array [1..200000] of boolean;
    p: PEdge;
const inf = high(integer) div 3;
procedure Add(x, y, t: integer);
var p: PEdge;
begin
  new(p);
  p^.next := list[x];
  list[x] := p;
  p^.t := y;
  p^.x := t
end;
begin
  assign(input, 'island2.in');
  assign(output, 'island2.out');
  reset(input);
  rewrite(output);
  read(n, m);
  for i := 1 to n do read(a[i]);
  for i := 1 to n do
    add(i+n, i, 1);
  for i := 1 to m do
  begin
    read(x, y);
    if a[x] = a[y] then
    begin
      add(x, y, 0);
      add(y, x, 0);
    end else
    begin
      add(x, y + ((x+1) mod 2) * n, 1);
      add(y, x + ((y+1) mod 2) * n, 1)
    end
  end;
  b[1] := 0;
  for i := 2 to 2*n do
    b[i] := inf;
  q[n] := 1;
  l := n;
  r := n+1;
  while l < r do
  begin
    x := q[l];
    p := list[x];
    inc(l);
    if not f[x] then
      while p <> nil do
      begin
        if (b[x] + p^.x < b[p^.t]) and not f[p^.t] then
        begin
          b[p^.t] := b[x] + p^.x;
          pr[p^.t] := x;
          case p^.x of
          0: begin
               dec(l);
               q[l] := p^.t
             end;
          1: begin
               q[r] := p^.t;
               inc(r)
             end;
          end
        end;
        p := p^.next
      end;
    f[x] := TRUE
  end;
  if b[n] = inf then
  begin
    writeln('impossible');
    close(input);
    close(output);
    halt(0)
  end;
  write(b[n], ' ');
  x := n;
  qq := 0;
  while x <> 0 do
  begin
    if x <= n then
    begin
      inc(qq);
      ans[qq] := x;
    end;
    x := pr[x]
  end;
  writeln(qq);
  for i := qq downto 1 do
    write(ans[i], ' ');
  close(input);
  close(output)
end.
