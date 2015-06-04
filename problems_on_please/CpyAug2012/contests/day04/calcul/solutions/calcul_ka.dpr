{$APPTYPE CONSOLE}

var
  a : array [1 .. 1000000, 1 .. 2] of integer;
  way : array [1 .. 100000] of integer;
  n, i, k : integer;

begin
  reset (input, 'calcul.in');
  rewrite (output, 'calcul.out');
  read (n);
  a [1, 1] := 0;
  a [1, 2] := 0;
  for i := 2 to n do begin
    a[i, 1] := a[i - 1, 1] + 1;
	a[i, 2] := i - 1;
	if i mod 2 = 0 then
	  if a[i div 2, 1] + 1 < a[i, 1] then begin
	    a[i, 1] := a[i div 2, 1] + 1;
		a[i, 2] := i div 2;
	  end;	
	if i mod 3 = 0 then
	  if a[i div 3, 1] + 1 < a[i, 1] then begin
	    a[i, 1] :=  a[i div 3, 1] + 1;
		a[i, 2] := i div 3;
      end
  end;
  writeln (a[n, 1]); 
  i := n;
  k := 0;
  while i <> 0 do begin
	inc (k);
	way [k] := i;
	i := a[i, 2]
  end;
  for i := k downto 1 do
    write (way [i], ' ');
  close (input); close (output)
end.


