var f:text;
begin
assign(f,'test_2');rewrite(f);
writeln(f,'1 2');
close(f);
assign(f,'test');rewrite(f);
writeln(f,'3 4');
close(f);
end.