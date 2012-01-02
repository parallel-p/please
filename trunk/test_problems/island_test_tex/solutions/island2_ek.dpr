program island_ek;
//{$mode delphi}
{$apptype console}
const kk=2;
      maxn=100000;
      maxm=100000;
      inf=1 shl 30;
type Edge=
      record
        u,v:longint;
        w:byte;
      end;
var n,m,i,cur,kol,p:longint;
    town:array[1..maxn]of byte;
    use:array[1..maxn]of Boolean;
    ed:array[1..maxm shl 1]of Edge;
    list:array[0..kk,0..maxn]of longint;
    pr,d:array[1..maxn]of longint;
    first:array[1..maxn]of longint;
    next:array[1..maxm shl 1]of longint;
    path:array[1..maxn]of longint;
begin
  assign(input,'island2.in'); reset(input);
  assign(output,'island2.out'); rewrite(output);

  read(n,m);
  for i:=1 to n do
    read(town[i]);
  for i:=1 to m do
  begin
    read(ed[i].u,ed[i].v);
    ed[i].w:=abs(town[ed[i].u]-town[ed[i].v]);
    ed[i+m].w:=abs(town[ed[i].u]-town[ed[i].v]);    
    ed[i+m].u:=ed[i].v;
    ed[i+m].v:=ed[i].u;
    if ed[i].u and 1=0 then
      ed[i].w:=ed[i].w*kk;
    if ed[i+m].u and 1=0 then
      ed[i+m].w:=ed[i+m].w*kk;
  end;

  fillchar(first,sizeof(first),0);
  for i:=1 to m shl 1 do
  begin
    next[i]:=first[ed[i].u];
    first[ed[i].u]:=i;
  end;

  cur:=0;
  kol:=1;
  fillchar(list,sizeof(list),0);
  list[0,0]:=1;
  list[0,1]:=1;
  d[1]:=0;
  for i:=2 to n do
    d[i]:=inf;
  fillchar(use,sizeof(use),false);

  while kol<>0 do
  begin
    while list[cur,0]=0 do
      cur:=(cur+1) mod (kk+1);
    p:=list[cur,list[cur,0]];
    dec(list[cur,0]);
    dec(kol);
    if not use[p] then
    begin
      use[p]:=true;
      i:=first[p];
      while i<>0 do
      begin
        if (not use[ed[i].v]) and (d[ed[i].v]>d[ed[i].u]+ed[i].w) then
        begin
          d[ed[i].v]:=d[ed[i].u]+ed[i].w;
          pr[ed[i].v]:=ed[i].u;
          inc(list[(cur+ed[i].w) mod (kk+1),0]);
          list[(cur+ed[i].w) mod (kk+1),list[(cur+ed[i].w) mod (kk+1),0]]:=ed[i].v;
          inc(kol);
        end;
        i:=next[i];
      end;
    end;
  end;
  if d[n]=inf then
    writeln('impossile')
  else
  begin
    write(d[n]);
    kol:=1;
    path[1]:=n;
    while n<>1 do
    begin
      inc(kol);
      n:=pr[n];
      path[kol]:=n;
    end;
    writeln(' ',kol);
    for i:=kol downto 1 do
      write(path[i]+1,' ');
  end;  

  close(input);
  close(output);
end.