program Project2;
{$O-}
{$APPTYPE CONSOLE}

uses
  SysUtils;
  
const
    n = 100000;

type
  mas = array[1..n] of string;

function is_in (names : mas; Len : Integer; name : string) : Integer;
var
   i, tmp : Integer;
begin
  tmp := - 1;
  for i := 1 to Len do begin
    if names[i] = name then begin
      tmp := i;
      Break;
    end;
  end;
  is_in  := tmp;

end;

var
    names_array : mas;
    payments_array : array [1..n] of Integer;
    i, j, tmp, payment : Integer;
    name, tmpstring : string;

begin
  Assign(Input, 'payments.in');
  Assign(output, 'payments.out');
  Reset(input);
  Rewrite(output);

  FillChar(payments_array, SizeOf(payments_array), 0);

  i := 1;
  while not Eof(input) do begin
    readln(tmpstring);
    if tmpstring <> '' then begin
      name := copy(tmpstring, 1, pos(' ', tmpstring) - 1);
      tmpstring := Copy(tmpstring, Pos(' ', tmpstring) + 1, Length(tmpstring));
      payment := strtoint(tmpstring);
      tmp := is_in(names_array, i, name);
      if tmp > 0 then
        inc(payments_array[tmp], payment)
      else
        begin
          names_array[i] := name;
          payments_array[i] := payment;
          inc(i);
        end;
      end;
  end;

  for j := 1 to i - 1 do
    Writeln(names_array[j],' ', payments_array[j]);
  close(Input);
  Close(output);
end.

