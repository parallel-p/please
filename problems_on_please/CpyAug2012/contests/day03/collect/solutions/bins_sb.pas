{$C+}
uses SysUtils;

type integer = longint;

const MAXN = 100001;

var a: array[ 1 .. MAXN ] of integer;

procedure qsort( l, r: integer );
  var i, j, t, x: integer;

  begin
    if ( l >= r ) then exit;
    i := l; j := r; x := a[( l + r ) shr 1];
    repeat
      while ( a[i] < x ) do inc( i );
      while ( a[j] > x ) do dec( j );
      if ( i <= j ) then begin
        t := a[i]; a[i] := a[j]; a[j] := t;
        inc( i ); dec( j );
      end;
    until i > j;
    qsort( l, j ); qsort( i, r );
  end;

var n, k, i, b, l, r, m: integer;

begin
  read( n );
  for i := 1 to n do begin
    read( a[i] );
  end;
  read( k );
  for i := 1 to k do begin
    read( b );
    l := 1; r := n;
    while ( l < r ) do begin
      m := ( l + r ) shr 1;
      if ( a[m] < b ) then l := m + 1
      else r := m;
    end;
    if ( a[l] = b ) then writeln( 'YES' )
    else writeln( 'NO' );
  end;
end.
