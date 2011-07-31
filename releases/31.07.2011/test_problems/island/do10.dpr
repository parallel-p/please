program do06;

{$apptype console}
const maxn=2000;
      maxm=100000;
      Seed=65478913;
      max_Hash=1 shl 20-1;
type Edge=
      record
        u,v:longint;
      end;

var town:array[1..maxn]of byte;
    ed:array[1..maxm]of Edge;
    h_table:array[0..1 shl 9]of int64;
    hash:array[0..max_Hash]of int64;  
procedure Init();
var i:longint;
begin
  RandSeed:=Seed;
  for i:=0 to 1 shl 9 do
    h_table[i]:=int64(random(1 shl 30)) shl 30 or random(1 shl 30);
  fillchar(hash,sizeof(hash),0);
end;
procedure Solve();
var x,i,u,v:longint;
    h:int64;
begin
  for i:=1 to maxn do
    town[i]:=random(2)+1;
  for i:=1 to maxm do
    while true do
    begin
      u:=random(maxn-1)+1;
      v:=random(maxn-u)+u+1;
      h:=h_table[u shr 9] xor h_table[u and (1 shl 9-1)] xor h_table[v shr 9] xor h_table[v and (1 shl 9-1)];
      x:=h and Max_hash;
      while (hash[x]<>0) and (hash[x]<>h) do
        x:=(x+1) and Max_hash;
      if hash[x]=0 then
      begin
        ed[i].u:=u;
        ed[i].v:=v;
        hash[x]:=h;
        break;
      end;
    end;
end;
procedure Print();
var i:longint;
begin
  writeln(maxn,' ',maxm);
  for i:=1 to maxn do begin
    if i <> maxn then
      write(town[i],' ')
    else 
      write(town[i]);
  end;
  writeln;
  for i:=1 to maxm do
    if random(2)=0 then
      writeln(ed[i].u,' ',ed[i].v)
    else
      writeln(ed[i].v,' ',ed[i].u);    
end;
begin
  Init();
  Solve();
  Print();
end.