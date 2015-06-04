program solution;

{$APPTYPE CONSOLE}
{$R+,Q+,S+,H+,O-}

uses
  SysUtils;
  

type integer = longint;

type rec = record
  s : string;
  n : integer;
end;

type
pnode = ^node;
node = record
  prior, cnt : longint;
  rev : boolean;
  add : longint;
  val : string;
  valn: integer;
  sval : longint;
  l,r : pnode;
end;


var root : pnode;

var all : array [1..100000] of rec;
    alln : integer;


Procedure Swap(var a, b; size: integer);
var p: pointer;
begin
  getmem(p, size);
  move(a, p^, size);
  move(b, a, size);
  move(p^, b, size);
  freemem(p, size);
end;
procedure split(root : pnode; key : string; var l,r : pnode);
var cur_key : string;
begin
  if root = nil then
    begin
      l := nil;
      r := nil;
      exit;
    end;
  cur_key := root.val;
  if key <= cur_key then
    begin
      split(root.l, key, l, root.l);  r := root;
    end else
    begin
      split(root.r, key, root.r, r); l := root;
    end;
end;

function merge(l,r : pnode) : pnode;
begin
  if (l = nil) then merge := r else
  if (r = nil) then merge := l else
  if l.prior > r.prior then
    begin
      l.r := merge(l.r, r); merge := l;
    end else
    begin
      r.l := merge(l, r.l); merge := r;
    end;
end;

function new_node(val : string) : pnode;
var t : pnode;
begin
  new(t);
  t.prior := random(1000000);
  t.cnt := 1;
  t.rev := false;
  t.val := val;
  t.valn := 1;
  t.sval := 0;
  t.l := nil; t.r := nil;
  new_node := t;
end;

function search(var root : pnode; s : string) : pnode;
begin
  if root = nil then search := nil else
    if s = root.val then search := root else
      if s < root.val then search := search(root.l, s) else
        search := search(root.r, s);
end;

procedure insert(var root : pnode; it : pnode);
var t1,t2 : pnode;
begin
  split(root, it.val, t1, t2);
  root := merge(merge(t1, it), t2);
end;

procedure add(s : string);
var p : pnode;
begin
  p := search(root, s);
  if p <> nil then inc(p^.valn) else insert(root, new_node(s));
end;

procedure sort(l,r: integer);
  function less(x,y : rec) : boolean;
  begin
    less := (x.n > y.n) or ((x.n = y.n) and (x.s < y.s));
  end;
var i,j : integer;
x,y: rec;
begin
  i := l;
  j := r;
  x := All[ (l + r) div 2 ];
  repeat
    while less(All[i], x) do inc(i);
    while less(x, All[j]) do dec(j);
    if not (i>j) then
      begin
        y    := All[i];
        All[i] := All[j];
        All[j] := y;
        inc(i);
        dec(j);
      end;
  until i>j;
  if l < j then sort(l,j);
  if i < r then sort(i,r);
end;

procedure run(root : pnode);
begin
  if root = nil then exit;
  inc(alln);
  all[alln].s := root.val;
  all[alln].n := root.valn;
  run(root.l);
  run(root.r);
end;


var s : string;
    i,k,k1 : integer;
    wc : integer;


begin
  wc := 0;
  randomize();
  root := nil;
  alln := 0;
  while not eof do
    begin
      readln(s);
	  for k := 1 to 100000000 do
	    k1 := (k1+k1-k1 div 2) mod (k1 div 3 + 1);
      s := s + ' ';
      while s <> '' do
        begin
          add(copy(s,1,pos(' ',s)-1));
          delete(s,1,pos(' ',s));
        end;
    end;
  run(root);
  sort(1,alln);
  for i := 1 to alln do writeln(all[i].s);
end.
