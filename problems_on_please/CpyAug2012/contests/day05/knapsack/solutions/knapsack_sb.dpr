{$APPTYPE CONSOLE}
{$C+,Q+,R+}

uses SysUtils;

type integer = longint;

const MAXS = 10000;
  MAXN = 300;
  MAXW = 100000;

var s, n, i, j, res: integer;
  w: array[ 1 .. MAXN ] of integer;
  r: array[ 0 .. MAXS ] of boolean;

begin
  assign( input, 'knapsack.in' ); reset( input );
  assign( output, 'knapsack.out' ); rewrite( output );
  read( s, n );
  assert( ( s >= 1 ) and ( s <= MAXS ), 'Bad s' );
  assert( ( n >= 1 ) and ( n <= MAXN ), 'Bad n' );
  for i := 1 to n do begin
    read( w[i] );
    assert( ( w[i] >= 0 ) and ( w[i] <= MAXW ), 'Bad w[' + intToStr( i ) + ']' );
  end;
  r[0] := true;
  for i := 1 to n do for j := s downto 0 do
    if ( j >= w[i] ) then
      r[j] := r[j] or r[j - w[i]];
  res := 0;
  for j := 1 to s do if ( r[j] ) then res := j;
  writeln( res );
end.
