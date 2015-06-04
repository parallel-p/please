{$APPTYPE CONSOLE}
{$C+,Q+,R+}
{$M 10000000 50000000}

uses SysUtils;

type integer = longint;

const MAXN = 100000;
  MAXM = 100000;

var g, vert, head: array[ 1 .. MAXN ] of integer;
  edge, next: array[ 1 .. MAXM ] of integer;
  time: integer;

function topsort( v: integer ): boolean;

  var cur: integer;

  begin
    topsort := false;
    if ( g[v] = 2 ) then topsort := true;
    if ( g[v] > 0 ) then exit;
    g[v] := 1;
    cur := head[v];
    while ( cur <> 0 ) do begin
      if ( not topsort( edge[cur] ) ) then exit;
      cur := next[cur];
    end;
    topsort := true;
    g[v] := 2;
    vert[time] := v;
    dec( time );
  end;

var n, m, empty, i, a, b, cur: integer;
  ok: boolean;

begin
  assign( input, 'topsort.in' ); reset( input );
  assign( output, 'topsort.out' ); rewrite( output );
  read( n, m );
  assert( ( n >= 1 ) and ( n <= MAXN ) and ( m >= 1 ) and ( m <= MAXM ),
      'Bad n or m' );
  empty := 1;
  for i := 1 to m do begin
    read( a, b );
    assert( ( a >= 1 ) and ( a <= n ) and ( b >= 1 ) and ( b <= n ),
        'Bad edge number ' + intToStr( i ) );
    edge[empty] := b;
    next[empty] := head[a];
    head[a] := empty;
    inc( empty );
  end;
  ok := true;
  time := n;
  for i := 1 to n do ok := ok and topsort( i );
  if ( ok ) then begin
    {for i := 1 to n do begin
      cur := head[i];
      while ( cur <> 0 ) do begin
        assert( vert[i] < vert[edge[cur]], 'Edge from ' + intToStr( i ) + ' to ' +
            intToStr( edge[cur] ) + ' goes in a wrong direction' );
        cur := next[cur];
      end;
    end;}
    write( vert[1] );
    for i := 2 to n do write( ' ', vert[i] );
    writeln;
  end else writeln( '-1' );
end.
