{$A8,B-,C+,D+,E-,F-,G+,H+,I+,J-,K-,L+,M-,N+,O-,P+,Q-,R+,S-,T-,U-,V+,W-,X+,Y+,Z1}
program collect_rg;

{$APPTYPE CONSOLE}

uses
  SysUtils;

const maxn = 10000000;

procedure init;
begin
end;

procedure print;
begin
  halt(0);
end;

var a : array [1..maxn] of longint;
    m, n, x : longint;
    i, j, left, right, mid : Longint;
begin
  init;
  read(n);
  for i := 1 to n do
    read(a[i]);
  read(m);
  for i := 1 to m do begin
    read(x);
    left := 1;
    right := n;
    mid := (left + right + 1) div 2;
    while (left < right) do
      begin
        if x >= a[mid] then
          left := mid else
          right := mid - 1;
        mid := (left + right + 1) div 2;
      end;
    if a[left] = x then writeln('YES') else
                        writeln('NO');  
  end;
  print;
end.
