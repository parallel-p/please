{$apptype console}
{$O-}
uses testlib,SysUtils;

type integer = longint;

const
  maxm = 100000;
var a,b,vert:array [1..maxm] of integer;
  n,m:integer;
  i:integer;
  ca,ja:integer;
                                               
begin
  n:=inf.Readlongint;
  m:=inf.readlongint;
  for i:=1 to m do begin
    a[i]:=inf.readLongint;
    b[i]:=inf.readLongint;
  end;

  ca:=ouf.readLongint;
  ja := ans.readLongint;

  if ( ca = -1 ) then begin
    if ( ja = -1 ) then quit( _ok, '' )
    else quit( _wa, 'There is a solution' );
  end;

  fillChar( vert, sizeOf( vert ), 0 );
  if ( ca < 0 ) or ( ca > n ) then
    quit( _wa, 'Invalid vertex number ' + intToStr( ca ) );
  vert[ca]:=1;
  for i:=2 to n do begin
    ca := ouf.readLongint;
    if ( ca < 0 ) or ( ca > n ) then
      quit( _wa, 'Invalid vertex number ' + intToStr( ca ) + ' at ' + intToStr( i ) );
    if ( vert[ca] <> 0 ) then
      quit( _wa, 'Duplicate vertex ' + intToStr( ca ) );
    vert[ca]:=i;
  end;

  for i:=1 to m do begin
    if vert[a[i]]>vert[b[i]] then quit(_wa,'');
  end;

  if ( ja = -1 ) then quit( _Fail, 'Contestant has a solution!!' );

  quit(_ok,'');
end.
