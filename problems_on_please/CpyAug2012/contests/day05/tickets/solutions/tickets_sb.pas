{$C+,Q+,R+}

uses SysUtils, Math;

type integer = longint;

const MAXN = 5000;
  MAXC = 3600;

var n, i, j, a: integer;
  r: array[ -2 .. MAXN + 1 ] of integer;

begin
  assign( input, 'tickets.in' ); reset( input );
  assign( output, 'tickets.out' ); rewrite( output );

  read( n );
  assert( ( n >= 1 ) and ( n <= MAXN ), 'Bad n' );
  for i := 2 to n + 1 do r[i] := 2 * MAXN * MAXC;
  for i := 1 to n do begin
    for j := 1 to 3 do begin
      read( a );
      assert( ( a >= 1 ) and ( a <= MAXC ), 'Bad a[' + intToStr( i ) + '][' + intToStr( j ) + ']' );
      if ( i + j <= n + 1 ) then
        r[i + j] := min( r[i + j], r[i] + a );
    end;
  end;
  writeln( r[n + 1] );
  close(input);
  close(output);
end.
