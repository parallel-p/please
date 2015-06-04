const inf=1000000000;
      maxn=100;

var k,n,i,j:longint;
    middle,w:array[1..maxn,1..maxn]of longint;
    yes:boolean;
    path:array[1..maxn]of longint;
    where,count:longint;

procedure rec(i,j:longint);
begin
  if middle[i,j]=0 then
    begin
      inc(count);
      path[count]:=i;
    end
  else
    begin
      rec(i,middle[i,j]);
      rec(middle[i,j],j);
    end;  
end;

begin
  assign(input,'negcycle.in');
  reset(input);
  assign(output,'negcycle.out');
  rewrite(output);

  read(n);
  for i:=1 to n do
    for j:=1 to n do
      begin
        read(w[i,j]);
        if w[i,j]=100000 then
          w[i,j]:=inf;
      end;

  fillchar(middle,sizeof(middle),0);

  yes:=false;
  for k:=1 to n do
    begin
      for i:=1 to n do
        if w[i,i]<0 then
          begin
            yes:=true;
            where:=i;
          end;
      if yes then
        break;
      for i:=1 to n do
        for j:=1 to n do
          if w[i,j]>w[i,k]+w[k,j] then
            begin
              w[i,j]:=w[i,k]+w[k,j];
              middle[i,j]:=k;
            end;
    end;

  if yes then
    writeln('YES')
  else
    writeln('NO');

   if yes then
     begin
       count:=0;
       rec(where,where);
       writeln(count);
       for i:=1 to count do
         write(path[i],' ');
//       write(where); 
     end;

  close(input);
  close(output);
end.