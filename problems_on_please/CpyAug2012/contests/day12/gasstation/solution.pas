const nmax=100;
      inf=maxint div 4;

var a:array[1..nmax,1..nmax] of byte;
    b:array[0..nmax,0..1] of integer;
    c:array[1..nmax,0..1] of byte;
    n,m:integer;
    z:array[1..nmax] of integer;

procedure readdata;
  var i,j:integer; q,w:integer;
  begin
  assign(input,'filling.in');
  reset(input);
  assign(output,'filling.out');
  rewrite(output);
  read(n);
  for i:=1 to n do read(z[i]);
  fillchar(a,sizeof(a),0);
  read(m);
  for i:=1 to m do begin
    read(q,w);
    a[q,w]:=1;
    a[w,q]:=1;
    end;
  end;

procedure deykstr;
  var i,j,q,qq,ww,w:integer;
      st:integer;
  begin
  for i:=0 to n do
    for j:=0 to 1 do begin
      c[i,j]:=0;
      b[i,j]:=inf;
      end;
  b[1,0]:=0;
  for i:=1 to 2*n do begin
    {Poisk}
    qq:=0;
    ww:=0;
    for q:=1 to n do
      for w:=0 to 1 do
        if (c[q,w]=0) and (b[q,w]<=b[qq,ww]) then begin
          qq:=q;
          ww:=w;
          end;
    {Hod}
    for q:=1 to n do
      if a[qq,q]=1 then begin
        for w:=0 to 1 do begin
          st:=w-ww+1;
          st:=st*z[qq]+b[qq,ww];
          if st<b[q,w] then b[q,w]:=st;
          end;
        end;
    c[qq,ww]:=1;
    end;
  end;

procedure done;
  begin
  if b[n,0]<b[n,1] then writeln(b[n,0])
  else if b[n,1]=inf then writeln(-1) else
      writeln(b[n,1]);
  close(input);
  close(output);
  end;

begin
readdata;
deykstr;
done;
end.





