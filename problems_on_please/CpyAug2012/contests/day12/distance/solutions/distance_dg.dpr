{$apptype console}

const maxn=5000;
      maxm=100000;
      inf=1000000000;
 
var s,t,m,n:longint;
    next,v,w:array[1..2*maxm]of longint;
    d,col,first:array[1..maxn]of longint;

procedure add(i:longint);
var j:longint;
begin
  col[i]:=1;
  j:=first[i];
  while j>0 do
    begin
      if w[j]+d[i]<d[v[j]] then
        d[v[j]]:=w[j]+d[i];
      j:=next[j];
    end;
end;

var r,i,j,a,b,c:longint;
    
begin
  assign(input,'distance.in');
  reset(input);
  assign(output,'distance.out');
  rewrite(output);

  read(n,m);
  read(s,t);
  fillchar(first,sizeof(first),0);
  r:=0;
  for i:=1 to m do begin
    read(a,b,c);
    inc(r);
    next[r]:=first[a];
    first[a]:=r;
    v[r]:=b;
    w[r]:=c;
    inc(r);
    next[r]:=first[b];
    first[b]:=r;
    v[r]:=a;
    w[r]:=c;
  end;

  fillchar(col,sizeof(col),0);
  for i:=1 to n do
    d[i]:=inf;
  d[s]:=0;
  add(s);
  while col[t]<>1 do
    begin
      i:=-1;
      for j:=1 to n do
        if col[j]=0 then
          if (i=-1)or(d[j]<d[i]) then
            i:=j;
      if i=-1 then
        break;
      if d[i]=inf then
        runerror(1);
      add(i);
    end;
  if col[t]<>1 then
    runerror(1);
  write(d[t]);

  close(input);
  close(output);
end.