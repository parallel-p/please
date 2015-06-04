program generator;

var s: string;
    len, i: integer;
    c: char;

begin
    randomize();

    for c := 'a' to 'z' do
      writeln(random(1000) + 1);

    len := random(1000) + 1;
    s := '';
    for i := 1 to len do
      s := s + chr(ord('a') + random(26));

    writeln(s);
end.
