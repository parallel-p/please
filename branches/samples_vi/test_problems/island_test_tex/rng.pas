{$R+,Q+,O-}
unit rng;

interface

function random: extended; overload;
function random(n: longint): longint; overload;

function rand: longint;
procedure setseed(seed: longint);

implementation

(* Knuth RNG is used *)
(* Translated from C by Andrew Stankevich *)

(* Original disclaimer :

/*    This program by D E Knuth is in the public domain and freely copyable
 *    AS LONG AS YOU MAKE ABSOLUTELY NO CHANGES!
 *    It is explained in Seminumerical Algorithms, 3rd edition, Section 3.6
 *    (or in the errata to the 2nd edition --- see
 *        http://www-cs-faculty.stanford.edu/~knuth/taocp.html
 *    in the changes to Volume 2 on pages 171 and following).              */

/*    N.B. The MODIFICATIONS introduced in the 9th printing (2002) are
      included here; there's no backwards compatibility with the original. */

/*    This version also adopts Brendan McKay's suggestion to
      accommodate naive users who forget to call ran_start(seed).          */

/*    If you find any bugs, please report them immediately to
 *                 taocp@cs.stanford.edu
 *    (and you will be rewarded if the bug is genuine). Thanks!            */

/************ see the book for explanations and caveats! *******************/
/************ in particular, you need two's complement arithmetic **********/
*)

const           
    { The long lag }
    KK = 100;   
    { The short lag }
    LL = 37;        
    { The modulus }
    MM = (1 shl 30); 

function mod_diff(x, y: longint): longint;
begin
    mod_diff := (x - y) and (MM - 1);
end;

var
    ran_x: array [0..KK - 1] of longint;

{ put n new random numbers in aa }
procedure ran_array(var aa: array of longint; n: integer);
var
    i, j: integer;
begin
    for j := 0 to KK - 1 do 
        aa[j] := ran_x[j];
    for j := KK to n - 1 do 
        aa[j] := mod_diff(aa[j - KK], aa[j - LL]);
    j := n;
    for i := 0 to LL - 1 do begin
        ran_x[i] := mod_diff(aa[j - KK], aa[j - LL]);
        inc(j);
    end;
    for i := LL to KK - 1 do begin
        ran_x[i] := mod_diff(aa[j - KK], ran_x[i - LL]);
        inc(j);
    end;
end;

{ the following routines are from exercise 3.6--15 }
{ after calling ran_start, get new randoms by, e.g., "x:=ran_arr_next()" }
const
    { recommended quality level for high-res use }
    QUALITY = 1009;


var
    ran_arr_buf: array [0..QUALITY - 1] of longint;
    ran_arr_dummy: longint = -1;
    ran_arr_started: longint = -1;

    ran_arr_ptr: ^longint = @ran_arr_dummy;

{ guaranteed separation between streams }
const
    TT = 70;

procedure ran_start(seed: longint);
var
    t, j: longint;
    { the preparation buffer }
    x: array [0..KK + KK - 2] of longint;
    ss: longint;
begin
    ss := (seed + 2) and (MM - 2);
    for j := 0 to KK - 1 do begin
        { bootstrap the buffer }
        x[j] := ss;
        { cyclic shift 29 bits }
        ss := ss shl 1;
        if ss >= MM then
            ss := ss - (MM - 2);
    end;
    { make x[1] (and only x[1]) odd }
    inc(x[1]);
    t := TT - 1;
    ss := seed and (MM - 1);
    while t <> 0 do begin
        t := t;
        { "square" }
        for j := KK - 1 downto 1 do begin
            x[j + j] := x[j];
            x[j + j - 1] := 0;
        end;
        for j := KK + KK - 2 downto KK do begin
            x[j - (KK - LL)] := mod_diff(x[j - (KK - LL)], x[j]);
            x[j - KK] := mod_diff(x[j - KK], x[j]);
        end;
        if odd(ss) then begin
            { "multiply by z" }
            for j := KK downto 1 do
                x[j] := x[j - 1];
            { shift the buffer cyclically }
            x[0] := x[KK];
            X[LL] := mod_diff(x[LL], x[KK]);
        end;
        if ss <> 0 then
            ss := ss shr 1
        else
            dec(t);
    end;

    for j := 0 to LL - 1 do begin
        ran_x[j + KK - LL] := x[j];
    end;
    for j := LL to KK - 1 do begin
        ran_x[j - LL] := x[j];
    end;
    { warm things up }
    for j := 0 to 9 do 
        ran_array(x, KK + KK - 1);
    ran_arr_ptr := @ran_arr_started;
end;

function ran_arr_cycle: longint;
begin
    if ran_arr_ptr = @ran_arr_dummy then
        ran_start(randseed);
    ran_array(ran_arr_buf, QUALITY);
    ran_arr_buf[100] := -1;
    ran_arr_ptr := @ran_arr_buf[1];
    ran_arr_cycle := ran_arr_buf[0];
end;

function ran_arr_next: longint;
begin
    if ran_arr_ptr^ >= 0 then begin
        ran_arr_next := ran_arr_ptr^;
        inc(ran_arr_ptr);
    end else begin
        ran_arr_next := ran_arr_cycle;
    end;
end;

function random: extended;
begin
    random := rand() / (MM - 1);
end;

function random(n: longint): longint;
var
    k: int64;
begin
    if n = 0 then
        random := 0
    else if n <= 1048576 then
        random := rand() mod n
    else begin
        { Knuth modulo is too small, we will use two successive 
            numbers to generate a longer one first }
        k := int64(rand()) * MM + rand();
        random := k mod n
    end;
end;

function rand: longint;
begin
    rand := ran_arr_next;
end;

procedure setseed(seed: longint);
begin
    ran_start(seed);
end;

{ $define selftest}

{$ifdef selftest}
var
    a: array [0..2008] of longint;
    i: longint;
begin
    randseed(310952);
    for i := 0 to 2009 do ran_array(a, 1009);
    assert(a[0] = 995235265);
    randseed(310952);
    for i := 0 to 1009 do ran_array(a, 2009);
    assert(a[0] = 995235265);
{$endif}
end.
