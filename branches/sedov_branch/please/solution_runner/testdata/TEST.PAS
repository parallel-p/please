var
   a, b : integer;
begin
     assign(input, 'test.in');
     assign(output, 'test.out');
     reset(input);
     rewrite(output);
     readln(a, b);
     writeln(b);
     close(input);
     close(output);

end.