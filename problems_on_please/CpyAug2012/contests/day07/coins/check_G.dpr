uses testlib,SysUtils;

const MAX_M = 16;

var
	a,b: array [1..MAX_M] of longint;
	N,M,nn: longint;
	i,j: longint;
	ja,ca: longint;
	x: longint;
	y: boolean;
begin
	N:=inf.ReadLongint;
	M:=inf.ReadLongint;
	nn:=N;
	for i:=1 to M do begin
		a[i]:=inf.ReadLongint;
		b[i]:=2;
	end;
	ja:=ans.ReadLongint;
	ca:=ouf.ReadLongint;
	if ca=-1 then begin
		if ja=ca then begin
			quit(_ok,'Not enough money');
		end else begin
			quit(_wa,'-1 when we have enough money');
		end;
	end;
	if ca=0 then begin
		if ja=ca then begin
			quit(_ok,'Change is needed');
		end else begin
			if ja=-1 then begin
				quit(_wa,'We have not enough money, but contest thinks we have');
			end else begin
				quit(_wa,'0 when solution exists');
			end;
		end;
	end;
	for i:=1 to ca do begin
		x:=ouf.ReadLongint;
		y:=true;
		for j:=1 to M do begin
			if a[j]=x then begin
				N:=N-x;
				if N<0 then Quit(_wa,'The sum does not match');
				dec(b[j]);
				y:=false;
				break;
			end;
		end;
		if y then begin
			quit(_wa,'No coin with value '+inttostr(x));
		end;
	end;
	for i:=1 to M do begin
		if b[i]<0 then begin
			quit(_wa,'Too many coins with value '+ inttostr(a[i])+' used');
		end;
	end;
	if N<>0 then begin
		quit(_wa,'The sum does not mathes');
	end;
	if ja<=0 then begin
		quit(_fail,'Contestant''s solution is better');
	end;
	if ca>ja then begin
		quit(_wa,'Not optimal');
	end;
	N:=nn;
	quit(_ok,'N = '+ inttostr(N)+', M = '+inttostr(M));
end.
