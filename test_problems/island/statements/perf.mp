input 2d

def cosplot(expr k,t)= (t*h, h*cosd(k*180*t/pi))
enddef;

pi:=3.141596;

linewidth:=light;
phaseshift:=0pt;

vardef clipcyc(expr c,a)=
save tmp_; picture tmp_;
tmp_:=nullpicture;
addto tmp_ doublepath a withpen (pencircle scaled linewidth);
clip tmp_ to c; draw tmp_;
enddef;

hashwidth:=1.5mm;

vardef hash(expr c)=
save tmp,xl,xr,yl,yr; picture tmp;
tmp:=nullpicture;
addto tmp doublepath c withpen (pencircle scaled linewidth);
xl=xpart(llcorner tmp); xr=xpart(lrcorner tmp);
yl=ypart(llcorner tmp); yr=ypart(urcorner tmp);
%show xl,yl,xr,yr;
for u:=xl-(yr-yl) step hashwidth until xr:
clipcyc(c, ((u,yl)--(u+(yr-yl),yr)));
endfor;
enddef;

vardef xhash(expr c)(expr ray, lnwd,hswd)=
save tmp,xl,xr,yl,yr,linewidth,hashwidth, L,M, rp; picture tmp;
pair rp;
linewidth:=lnwd;
hashwidth:=hswd;

tmp:=nullpicture;
addto tmp doublepath c withpen (pencircle scaled linewidth);
xl=xpart(llcorner tmp); xr=xpart(lrcorner tmp);
yl=ypart(llcorner tmp); yr=ypart(urcorner tmp);

L:=abs(unitvector(ray) dotprod (urcorner tmp - llcorner tmp));
rp:=unitvector(ray) rotated 90;
M:=abs(rp dotprod (urcorner tmp - llcorner tmp));
for u:=-M-hashwidth-phaseshift step hashwidth until M+hashwidth+phaseshift:
clipcyc(c, (((xl,yl)+(u*rp)-(L*unitvector(ray)))--
            ((xl,yl)+(u*rp)+(L*unitvector(ray)))
));
endfor;
enddef;

picture X, Y;

X:=thelabel(btex $x$ etex,(0,0));
Y:=thelabel(btex $y$ etex,(0,0));

hcorr:=0; wcorr:=0;
def coord=   drawarrow(0,-h/2)--(0,h/2+hcorr);drawarrow(-w/2,0)--(w/2+wcorr,0);
enddef;

def Rcoord=   drawarrow(0,0)--(0,h+hcorr);drawarrow(0,0)--(w+wcorr,0);
enddef;

def xymark=  label.lrt(X,(w/2+wcorr,0)); label.lft(Y,(0,h/2+hcorr));
enddef;

def Rxymark=  label.lrt(X,(w+wcorr,0)); label.lft(Y,(0,h+hcorr));
enddef;


def style = pickup pencircle scaled hair;
enddef;
def Style = pickup pencircle scaled light;
enddef;
def STYLE = pickup pencircle scaled semibold;
enddef;

def pr(expr x,y,z)= (x*ex+y*ey+z*ez) enddef;

beginfig(2);
u:=1cm;
pair h,a,aa,ab,c;
z0=(0,0);
ph:= 35;
a:=(u,0) ;
c=(u,-2u);
h=a-c;
r:=abs(h);
path cr[];
cr4=defcirc(z0,r);
cr0=defcirc(c,r);
cr2=cr4 yscaled 0.3;
cr3=(cr2 ) shifted a;
Style;
drawarrow z0--a; drawarrow z0--c;
draw cr0;
z1=(0.9h rotated -22) shifted c;
0.3z2+0.7a=z1;
draw a--z1 dashed evenly; draw z1--z2;
style;
drawarrow z0--h;
draw cr3 dashed evenly;
dotlabel.lft(btex 0 etex,z0);
dotlabel("", z1); dotlabel.rt(btex $a'$ etex, z2);
label.urt(btex $a$ etex, a);
label.rt(btex $c$ etex, c);
label.rt(btex $h$ etex, h);
endfig;

beginfig(1);
z0=(0,0); z1=(1cm,0);
for i=2 upto 5 : z[i]=z1 rotated (360*(i-1)/5); endfor
%meetpoint(z6)(z2,z3)(z4,z5);
z6=whatever[z2,z3];
z6=whatever[z4,z5];
Style;


draw  z1--z2--z3--z4--z5--cycle; draw z4--z6--z3;
for i=1 upto 6: dotlabel("", z[i]);
endfor
endfig;

beginfig(3);
  for i = 0 upto 5: z[i]=(1.4cm,0) rotated (i*60); endfor
  Style;
  draw z0 for i=1 upto 5: --z[i] endfor -- cycle;
  draw z3{dir15}..{dir -15}z0;
  draw z2{dir -45}..{dir -75}z5;
  draw z1{dir -105}..{dir -135}z4;
  for i=0 upto 5: dotlabel("", z[i]); endfor
  for i = 6 upto 11: z[i]=z[i-6] shifted (4z0); endfor
  z12= 0.3z1+z9;  z13= 0.3z3+z9;  z14= 0.3z5+z9;
  draw z10--z11--z6--z7--z8;
  draw z8{dir -45}..{dir -75}z11;
  draw z7{dir -105}..{dir -135}z10;
  for i=6 upto 8: dotlabel("", z[i]); endfor
  for i=10 upto 14: dotlabel("", z[i]); endfor
  for i=12 upto 14:
    draw z6--z[i]; draw z8--z[i]; draw z10--z[i];
  endfor;
  draw z12--z13--z14--cycle;
  style;
  drawarrow 1.25z0--2.5z0;
  for i=15 upto 17: z[i]=z[i-3] shifted (-1.1z0+(0,0.6cm));
  endfor;
  draw z15--z16--z17--cycle;
  for i=15 upto 17: dotlabel("", z[i]); endfor  
endfig;

end

beginfig(2);
pair v[][];

for i=0 upto 4:
 for j=0 upto 4: v[i][j]=(i*4mm,j*4mm);
 endfor
endfor


pickup pencircle scaled 0.4pt;
for i=0 upto 4:
      draw (i*4mm,0)--(i*4mm,16mm);
      draw (0,i*4mm)--(16mm,i*4mm);
endfor
for i=0 upto 4:
 for j=0 upto 4: dotlabel("",v[i][j]);
 endfor
endfor


pickup pencircle scaled 2pt;
draw v[1][2]--v[4][2]--v[4][4]--v[3][4]--v[3][3]--v[0][3];
endfig;


beginfig(3);
pair v[][];

for i=0 upto 4:
 for j=0 upto 4: v[i][j]=(i*4mm,j*4mm);
 endfor
endfor


pickup pencircle scaled 0.4pt;
for i=0 upto 4:
      draw (i*4mm,0)--(i*4mm,16mm);
      draw (0,i*4mm)--(16mm,i*4mm);
endfor
for i=0 upto 4:
 for j=0 upto 4: dotlabel("",v[i][j]);
 endfor
endfor


pickup pencircle scaled 2pt;
draw v[1][2]--v[4][2]--v[4][4]--v[3][4]--v[3][3]--v[1][3]--cycle;
endfig;


def dred(expr d)=
pickup pencircle scaled 1pt;
 for i=1 upto N-d: draw z[i]--z[i+d];
 endfor
 for i=N-d+1 upto N: draw z[i]--z[i+d-N];
 endfor
enddef;


beginfig(4);
r:=1.5cm;
N:=7;
for i=1 upto N: z[i]= ((0,-r) rotated (180/N+(i-1)*360/N));
endfor
for i=1 upto N: dotlabel ("",z[i]) ;
endfor
dred(2);
endfig;


beginfig(5);
r:=1.5cm;
N:=7;
for i=1 upto N: z[i]= ((0,-r) rotated (180/N+(i-1)*360/N));
endfor
for i=1 upto N: dotlabel ("",z[i]);
endfor
dred(1);dred(3);
endfig;



beginfig(6);
r:=1.5cm;
N:=9;
for i=1 upto N: z[i]= ((0,-r) rotated (180/N+(i-1)*360/N));
endfor
for i=1 upto N: dotlabel ("",z[i]);
endfor
dred(3);
endfig;

beginfig(7);
r:=1.5cm;
N:=15;
for i=1 upto N: z[i]= ((0,-r) rotated (180/N+(i-1)*360/N));
endfor
for i=1 upto N: dotlabel ("",z[i]);
endfor
dred(3); dred(5);
endfig;

beginfig(8);
r:=1.5cm;
N:=17;
for i=1 upto N: z[i]= ((0,-r) rotated (180/N+(i-1)*360/N));
endfor
for i=1 upto N: dotlabel ("",z[i]);
endfor
%dred(1); dred(2);
%dred(4); dred(8);
dred(3); dred(5);
%dred(6); dred(7);
endfig;


beginfig(9);
r:=1.5cm;
N:=7;
pair v[];
for i=1 upto N: v[i]= ((0,-r) rotated (180/N+(i-1)*360/N));
endfor
z[1]=v[5];
z[2]=v[4];
z[3]=v[3];
z[4]=v[2];
z[5]=v[7];
z[6]=v[1];
z[7]=v[6];
dotlabels.rt(6,4,3);
dotlabels.lft(1,7,5);
dotlabels.top(2);
dred(1);dred(3);
endfig;


beginfig(10);
r:=1.5cm;
N:=7;
pair v[];
for i=1 upto N: v[i]= ((0,-r) rotated (180/N+(i-1)*360/N));
endfor
z[1]=v[6];
z[2]=v[3];
z[3]=v[7];
z[4]=v[4];
z[5]=v[1];
z[6]=v[2];
z[7]=v[5];
dotlabels.rt(6,5,2);
dotlabels.lft(1,3,7);
dotlabels.top(4);
dred(1);dred(3);
endfig;


end
