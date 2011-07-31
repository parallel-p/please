var
  a, b: integer;

begin
  reset(input, 'aplusb.in');
  rewrite(output, 'aplusb.out');
  read(a, b);
  writeln(a + b);
  close(input);
  close(output);
end.