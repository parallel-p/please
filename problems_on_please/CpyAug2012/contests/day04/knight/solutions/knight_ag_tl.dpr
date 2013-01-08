program knight;

{Andrew Gein, TL solution}

function solve(x, y : longint) : longint;
begin
  if (x <= 0) or (y <= 0) then begin
     result := 0;
     exit;
  end;
  if (x = 1) and (y = 1) then begin
     result := 1;
     exit;
  end;
  result := solve(x - 1, y - 2) + solve(x - 2, y - 1);
end;

var n, m : longint;

begin
  read(n, m);
  write(solve(n, m));
end.