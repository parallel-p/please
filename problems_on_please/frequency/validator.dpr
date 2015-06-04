{$APPTYPE CONSOLE}
{$R+,Q+,S+,O-,H+}

procedure bad;
begin
  halt(1);
end;

type integer = longint;

var w : integer;

procedure readline();
var s : string; i,l : integer;
begin
  readln(s);
  if s = '' then
    if not eof then
      bad
    else
      exit;
  if s[1] = ' ' then bad;
  if s[length(s)] = ' ' then bad;
  s := s + ' ';
  i := 1;
  while (i < length(s)) do
    begin
      if not (s[i] in ['a'..'z']) then bad;
      l := 0;
      while s[i] in ['a'..'z'] do
        begin
          inc(l);
          inc(i);
        end;
      if l > 20 then bad;
      inc(w);
      inc(i);
    end;
end;

begin
  w := 0;
  while not eof do readline();
  if (w > 100000) then bad;
end.