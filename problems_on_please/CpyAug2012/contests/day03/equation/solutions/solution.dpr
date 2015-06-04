{$APPTYPE CONSOLE}
{$R+,S+,Q+,I+,O-}
{R-,S-,Q-,I-,O+}

uses
        SysUtils, Math;

var
        i : longint;
        a, b, c, d, x, l, r : extended;

begin
{$IFDEF AguL}
        reset(input, 'input.txt');
        rewrite(output, 'output.txt');
{$ENDIF}
        read(a, b, c, d);
        l := -1e18;
        r := 1e18;
        for i := 1 to 200000 do begin
                x := (l + r) / 2;
                if a * x * x * x + b * x * x + c * x + d > 0 then begin
                        if a < 0 then l := x else r := x;
                end else begin
                        if a < 0 then r := x else l := x;
                end;
        end;
        write(l:0:16);
end.
