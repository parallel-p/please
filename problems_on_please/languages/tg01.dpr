program tg01;

{$APPTYPE CONSOLE}

uses
  SysUtils;

const
 len = 10;
 num_of_words = 6;
 num_of_pep = 5;
 num_in_pep = 5;

var
 i,j,k,num:integer;
 mas : array [1..num_of_words] of string;
 used : array [0..num_of_words]  of boolean;
 ch : char;

begin
 randomize;
 writeln(num_of_pep);
 for i:=1 to num_of_words do
  begin
   mas[i]:='';
   for j:=1 to random(len)+1 do
    begin
     ch:= chr(random(25)+97);
     mas[i]:=mas[i]+ch;
    end;
  end;
 for i:=1 to num_of_pep do
  begin
   num := random(num_in_pep-1)+1;
   writeln(num);
   for j:=1 to num_of_words do used[j]:=true;
   used[0]:=false;
   for j:=1 to num do
    begin
     k:=0;
     while not(used[k]) do k := random(num_of_words-1)+1;
     used[k]:=false;
     writeln(mas[k]);
    end;
  end;

end.
