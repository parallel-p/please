{$APPTYPE CONSOLE}
{$C+,Q+,R+}

uses SysUtils;

type integer = longint;

const MAXN = 100;

var n, m, a, i, j, k: integer;
  e: array[ 1 .. MAXN, 1 .. MAXN ] of boolean;
  g: array[ 1 .. MAXN ] of boolean;
  ok: boolean;

begin
  assign( input, 'baobab.in' ); reset( input );
  assign( output, 'baobab.out' ); rewrite( output );
  read( n );
  assert( ( 1 <= n ) and ( n <= MAXN ), 'Bad n' );
  for i := 1 to n do for j := 1 to n do begin
    read( a );
    inc( m, a );
    assert( ( a = 0 ) or ( a = 1 ),
        'Bad a[' + intToStr( i ) + '][' + intToStr( j ) + ']' );
    e[i][j] := a = 1;
  end;
  for i := 1 to n do for j := 1 to n do
    assert( e[i][j] = e[j][i], 'Not symmetrical matrix' );
  g[1] := true;
  for i := 1 to n do for j := 1 to n do for k := 1 to n do
    g[k] := g[k] or ( g[j] and e[j][k] );
  ok := m = 2 * ( n - 1 );
  for i := 1 to n do ok := ok and g[i];
  if ( ok ) then writeln( 'YES' )
  else writeln( 'NO' );
  close(input);
  close(output);
end.
