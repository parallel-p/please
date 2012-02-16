%27/01/97 Вялый: определения констант размерности длины
ahlength:=4.5pt;
ahangle:=30;
gap:=4pt;

marksize:=4pt;
angle_radius:=8pt;
numeric pen_size;
hair:=0.4pt;
light:=0.8pt;
semibold:=1.2pt;
bold:=1.6pt;
extrabold:=3.2pt;
mv:=1cm;

%24.07.98 Вялый: Пометки на рисунках

%05.06.98 Вялый: dotlabel adjusted by shift
numeric labelcorrectionx,labelcorrectiony;
labelcorrectionx:=0;
labelcorrectiony:=0;
vardef laboff.adjusted@#=
if labeloffset>0.5pt :
(1/labeloffset)*(labelcorrectionx,labelcorrectiony) + fi laboff@#
enddef;
vardef labxf.adjusted@#=labelcorrectionx:=0; labxf@# enddef;
vardef labyf.adjusted@#=labelcorrectiony:=0; labyf@# enddef;

primarydef p adjust a= hide(labelcorrectionx:=xpart(a);
labelcorrectiony:=ypart(a)) p
enddef;

%27/01/97 Вялый: определения пометок на линиях и углах
%27/01/97 Вялый: based on MP manual
%25.07.98 Вялый: примитивная конструкция
def draw_mark(expr p,a) =
    begingroup
        save t,dm; pair dm;
pickup pencircle scaled hair;
        pen_size:=hair;
        t = arctime a of p;
        dm = marksize*unitvector direction t of p rotated 90;
        draw (-.5dm.. .5dm) shifted point t of p;
    endgroup
enddef;

%25.07.98 Вялый: культурная возможность ставить кратные метки
numeric __mult[];
__mult1:=1; __mult2:=2; __mult3:=3;
vardef dashmark@# (expr p) =
        begingroup
         save amid,n;
pickup pencircle scaled hair;
         amid=.5*arclength p;
         if known __mult@#: n:=__mult@# else: n:=1 fi;
         for i=-(n-1)/2 upto (n-1)/2:
          draw_mark(p, amid+.6marksize*i);
         endfor
         draw p;
        endgroup
enddef;

%25.07.98 Вялый: разметка углов недоделана
%25.07.98 Вялый: при разметке углов нужно указывать
%точки так: на первом луче, вершина, на втором луче;
%счет против часовой стрелки

%25.07.98 Вялый: пока хорош для малых углов
%25.07.98 Вялый: помечает черточками
vardef mark_angle@#(expr a,b,c) =
 begingroup
  save p,s; path p;
pickup pencircle scaled hair;
  p = unitvector(a-b){(a-b)rotated 90}..unitvector(c-b);
  s = .9marksize/length(point 1 of p - point 0 of p);
  if s < angle_radius: s:=angle_radius; fi
  dashmark@#(p scaled s shifted b);
 endgroup
enddef;

def mark_perp(expr a,b,c) =
 begingroup
pickup pencircle scaled hair;
 draw ((1,0)--(1,1)--(0,1)) zscaled
 (angle_radius*unitvector(a-b)) shifted b
 endgroup
enddef;

%27/01/97 Вялый: new macro
% отмечает угол несколькими дугами
%25.07.98 Вялый: также хорош только для малых углов
vardef arcs@#(expr a,b,c) =
 begingroup
  save p,s,n; path p;
pickup pencircle scaled hair;
if known __mult@#: n:=__mult@# else: n:=1 fi;
  p = unitvector(a-b){(a-b)rotated 90}..unitvector(c-b);
  s = .9marksize/length(point 1 of p - point 0 of p);
  if s < angle_radius: s:=angle_radius; fi
         for i=-(n-1)/2 upto (n-1)/2:
          draw p scaled (s+.5marksize*i) shifted b;
         endfor
 endgroup
enddef;


%30/01/97 Вялый: new macro
% определяет точку для метки угла
def text_point(expr a,b,c) (expr n) =
 begingroup
  save p,s,pp; path p; pair pp;
  p = unitvector(a-b){(a-b)rotated 90}..unitvector(c-b);
  s = .9marksize/length(point 1 of p - point 0 of p);
  if s < angle_radius: s:=angle_radius; fi
b+(s+n*angle_radius)*unitvector((unitvector(a-b)+unitvector(c-b)))
 endgroup
enddef;

%%%%%%%%%%%%%%%%%%% Основная часть %%%%%%%%%%%%%%%%%
def using(text t)= save t enddef;

%25.07.98 Вялый: регистрация объектов
def object(suffix o)=
 if pair o: 0    % point
 elseif length(o)=4: 1  %circle
 elseif distance(0.5[start.o,final.o], point 0.5 of o)<0.05pt:
                     2  %segment
 elseif path o:      3  %parabola
 else:              -1  %unregistered
 fi
enddef;

def isparabola(suffix c)=
  if object(c)=3 : true else: false fi
enddef;

def iscircle(suffix c)=
  if object(c)=1 : true else: false fi
enddef;

def isline(suffix c)=
  if object(c)=2 : true else: false fi
enddef;

def ispoint(suffix c)=
  if object(c)=0 : true else: false fi
enddef;

def distance(expr a,b)=  (arclength(a--b)) enddef;

%25.07.98 Вялый: концы отрезка
vardef start@# =point 0 of @# enddef;
vardef final@# =point length(@#) of @# enddef;

%08.05.98 Вялый: пересечение двух прямых, заданных точками
def  meetpoint(expr m)(expr a,b)(expr c,d) =
begingroup
 m=whatever[a,b]; m=whatever[c,d];
endgroup
enddef;

%27.04.98 Вялый: биссектриса
def bisector(expr a,c,b)(suffix bs) =
 begingroup
   save sa,sb,sc;
   pair sa,sb,sc;
   sa=unitvector(a-c);
   sb=unitvector(b-c);
   bs=whatever[a,b];
   bs=whatever[c,c+ (sa+sb)];
 endgroup
enddef;


%25.07.98 Вялый: подходящие константы
def vertical primary x= (x,0)--(x,-1cm)
enddef;
def horizontal primary x= (0,x)--(-1cm,x)
enddef;



%25.07.98 Вялый: параболы задаются подходящими
%контрольными точками. Точнее, задаются две точки на параболе
%и точка пересечения касательной в первой точке и параллельной оси,
%делящей отрезок  между точками в отношении 1:2 (считая от первой)
def parabolas text t=
 path t;    clearparp;
enddef;

pair __parp[];
def clearparp=save __parp; pair __parp[]; enddef;

%25.07.98 Вялый: процедуры для определения параболы
vardef forth_point(expr zl,zr,zp)=
clearparp;
save am,ap; pair am,ap;
     ap=0.333333[zl,zr]; am=0.333333[zr,zl];
     meetpoint(__parp0)(zp,zp+(zr-zl))(am,am+(zp-ap));
 expandafter __parp0
enddef;

vardef defpara(expr zl,zr)(expr zp) =
  clearparp;
zl..controls zp and forth_point(zl,zr,zp)..zr;
enddef;

def primarypara =
__parp1..controls __parp2 and __parp3..__parp4;
enddef;


%25.07.98 Вялый: аттрибуты параболы

vardef axisdir@# = unitvector
(0.5[point 0 of @#,point 1 of@#]-point 0.5 of @#) enddef;
vardef focus@# =
clearparc;
hide(
__parc2=unitvector(direction 0 of @#);
__parc1=-axisdir@# reflectedabout((0,0),__parc2);
__parc4=-unitvector(direction 1 of @#);
__parc3=-axisdir@# reflectedabout((0,0),__parc4);
__parc0=point 0 of @# +whatever*__parc1;
__parc0=point 1 of @# +whatever*__parc3
)
expandafter __parc0
enddef;
vardef directrix@# =
((point 0 of @#) -distance(point 0 of @#, focus@#)*axisdir@#)--
((point 1 of @#) -distance(point 1 of @#, focus@#)*axisdir@#)
enddef;



vardef quadratic_plot(expr a,b,c,xl,xr,scale)=
clearparp;
 save  xp,yp,yl,yr,aux;
 numeric xp,yp,yr,yl;
 path aux;
 xp=scale*(2xl+xr)/3;
 yl=scale*(a*(xl**2)+b*xl+c);
 yr=scale*(a*(xr**2)+b*xr+c);
 yp=yl+(xp-scale*xl)*(2*a*xl+b);
%30.07.98 Вялый: show yl,yr,xp,yp;
 __parp1=(scale*xl,yl); __parp4=(scale*xr,yr); __parp2=(xp,yp);
 __parp3=forth_point(__parp1,__parp4,__parp2);
%  aux= primarypara;
aux=__parp1..controls __parp2 and __parp3..__parp4;

  expandafter aux
enddef;

vardef circumpara(expr p,q,r,xl,xr)=
clearparp;
save aux,a,b,c,d; path aux; numeric a,b,c,d;
%  d1:=abs(xpart(p)-xpart(q));
%  d2:=abs(xpart(p)-xpart(r));
%  d3:=abs(xpart(r)-xpart(q));
%  d4:=d1*d2*d3;
  xpart(p)**2*a+xpart(p)*b+c=ypart(p);
  xpart(q)**2*a+xpart(q)*b+c=ypart(q);
  xpart(r)**2*a+xpart(r)*b+c=ypart(r);
  aux=quadratic_plot(a,b,c, xl, xr, 1);
  expandafter aux
enddef;

vardef scaledcircumpara(expr p,q,r,xl,xr,scale)=
clearparp;
save aux,a,b,c,d; path aux; numeric a,b,c,d;
  d1:=abs(xpart(p)-xpart(q));
  d2:=abs(xpart(p)-xpart(r));
  d3:=abs(xpart(r)-xpart(q));
  d4:=d1*d2*d3;
  d4*xpart(p)**2*a+xpart(p)*b+c=ypart(p);
  d4*xpart(q)**2*a+xpart(q)*b+c=ypart(q);
  d4*xpart(r)**2*a+xpart(r)*b+c=ypart(r);
  show a*d4;
  aux=quadratic_plot(a*d4,b,c, xl, xr, scale);
  expandafter aux
enddef;


%26.07.98 Вялый: касается прямых a b c
vardef inpara(suffix a,b,c)(expr ot,do,scale)=
clearparc;
clearparp;
save aux, va,vb,vc, A,B,C,ta,tb,tc,xa,xb,xc;
path va,vb,vc, aux;
pair A,B,C,ta,tb,tc;
numeric xa,xb,xc;
  C=cross(a,b); B=cross(a,c); A=cross(b,c);
  2xpart(C)=xa+xb;
  2xpart(B)=xa+xc;
  2xpart(A)=xc+xb;
  va=vertical xa; vb=vertical xb; vc=vertical xc;
  ta=cross(va,a); tb=cross(vb,b); tc=cross(vc,c);
  show ta; show tb; show tc;
  if ot>do:
  aux=circumpara(ta,tb,tc,min(xa)(xa,xb,xc),max(xa)(xa,xb,xc));
  else:
  aux=scaledcircumpara(ta,tb,tc,ot/scale,do/scale,scale);
  fi
  expandafter aux
enddef;



%28/01/97 Вялый: окружности
def circles text t=
 path t;    clearparc;
enddef;

pair __parc[];
numeric __parc_count;
def clearparc=save __parc; pair __parc[]; __parc_count:=3; enddef;


def defcirc(expr c,r) =%28/01/97 Вялый: путь, центр, радиус
  c+(r,0)..c+(0,r)..c+(-r,0)..c+(0,-r)..cycle;
enddef;

vardef circumcirc(expr a,b,c)=
clearparc;
save aux; path aux;
  (__parc0-.5[a,b])dotprod(b-a)=0;
  (__parc0-.5[a,c])dotprod(c-a)=0;
  aux=defcirc(__parc0,distance(__parc0,a));
  expandafter aux
enddef;

%26.07.98 Вялый: вписана в углы a,b,c и b,c,d
vardef incirc(expr a,b,c,d)=
clearparc;
save aux; path aux;
  bisector(a,b,c)(__parc1);
  bisector(b,c,d)(__parc2);
  __parc0=b+whatever*(__parc1-b);
  __parc0=c+whatever*(__parc2-c);
  (__parc3-__parc0) dotprod unitvector(b-c)=0;
  __parc3=whatever[b,c];
  aux=defcirc(__parc0,  distance(__parc0,__parc3));
  expandafter aux
enddef;



%25.07.98 Вялый: аттрибуты окружности
vardef radius@# =0.5distance(point 0 of @#, point 2 of @#) enddef;
vardef centre@# =0.5[point 0 of @#, point 2 of @#] enddef;

%25.07.98 Вялый: выбор из двух точек
%25.07.98 Вялый: константы для обработки по умолчанию
numeric default; default:=0;
vardef choose_point.first(suffix a) = a=__parc1;  enddef;
vardef choose_point.second(suffix a) = a=__parc2; enddef;
vardef choose_point.lft(suffix a) = a= if xpart(__parc1)<xpart(__parc2):
__parc1; else: __parc2; fi
enddef;
vardef choose_point.rt(suffix a) = a= if xpart(__parc1)>xpart(__parc2):
__parc1; else: __parc2; fi
enddef;
vardef choose_point.top(suffix a) = a=  if ypart(__parc1)>ypart(__parc2):
__parc1; else: __parc2; fi
enddef;
vardef choose_point.bot(suffix a) = a= if ypart(__parc1)<ypart(__parc2):
__parc1; else: __parc2; fi
enddef;

%25.07.98 Вялый: общий макрос для пересечений введенных кривых
vardef cross@#(suffix c,s) =
clearparc;
   save u, l,ll;
   pair u;
   numeric l,ll;
  if length(c)>3:
  %25.07.98 Вялый: окружность c и прямая s
   (center.c-u)dotprod(start.s-final.s)=0;
   u=whatever[start.s,final.s];
   l=distance(center.c,u);
   if l>radius.c:
   show l;
   show radius.c;
   stop "2D package: circle and line don't intersect"
   else:   ll=radius.c+-+l
   fi;
   __parc1=u+ll*unitvector(start.s-u);
   __parc2=u-ll*unitvector(start.s-u);
  elseif distance(0.5[start.c,final.c], point 0.5 of c)<0.05pt:
  %25.07.98 Вялый: прямая c и прямая s
  if abs(unitvector(start.c-final.c)-unitvector(start.s-final.s))<0.001:
   stop "2D package:  lines don't intersect"
  else:
  meetpoint(__parc1)(start.c,final.c)(start.s,final.s)
  fi;
  __parc2=__parc1;
  else:
  %25.07.98 Вялый: парабола c и прямая s
    u=c intersectiontimes s; l=xpart(u);
    if l=-1:
     stop "2D package:  line doesn't intersect parabola"
    fi;
    __parc1=point l of c;
    save u,lll; pair u; numeric lll;
    u=(subpath (l+0.001, length(c)) of c) intersectiontimes s; ll=ypart(u);
    if ll=-1:
      save u; pair u;
      u=(subpath (0,l-0.001) of c) intersectiontimes s; lll=ypart(u);
      if lll=-1: __parc2=__parc1 else:
      __parc2=point lll of s
      fi;
    else:
      __parc2=point ll of s;
    fi
  fi
   if known default@#: choose_point.first(__parc0)
   else: choose_point@#(__parc0)  fi;
   expandafter __parc0
enddef;

%27/01/97 Вялый: касательные в точке
vardef tangent@#(expr a) =
clearparc;
if isparabola(@#):
__parc0=unitvector(focus@# - a) - axisdir@#;
else: %circle
__parc0=(centre@# -a) rotated-90;
fi
expandafter __parc0
enddef;


%25.07.98 Вялый: расширения парабол и прямых



%25.07.98 Вялый: поляры


%27/01/97 Вялый: касательные из точки
vardef support@#(suffix c,p) =
clearparc;
  if iscircle(c):
  %25.07.98 Вялый: окружность c
   save sa,sb,sc;
   pair sa,sb,sc;
   if distance(centre.c,p)<radius.c:
   stop "2D package: no tangents through  a point in a circle"
   else:
   sa=(radius.c,distance(centre.c,p)+-+radius.c)
   fi;
   sb=unitvector(sa);
   sc=centre.c+radius.c*unitvector(p-centre.c);
   __parc1 = sc rotatedaround (centre.c,angle(sb));
   __parc2 = sc rotatedaround (centre.c,-angle(sb));
  else:
  %25.07.98 Вялый: парабола c
  save a, au; path a; pair au[];
  a=defcirc(p, distance(p, focus.c));
  au1=cross.first(a, directrix.c);
  au2=cross.second(a, directrix.c);
  (__parc1-p) dotprod (focus.c-au1)=0;
  (__parc1-au1)=whatever*axisdir.c;
  (__parc2-p) dotprod (focus.c-au2)=0;
  (__parc2-au2)=whatever*axisdir.c;
  fi
   if known default@#: choose_point.first(__parc0)
   else: choose_point@#(__parc0)  fi;
   expandafter __parc0
enddef;

def change(suffix x,y)= if x<y: x:=x+y; y:=x-y; x:=x-y; fi
enddef;

vardef middle(suffix b,c)(expr x,y,z,v)=
   save a,d; numeric a,d;
   a:=x; b:=y; c:=z; d:=v;
%show a,b,c,d;
   change(a,b); change(a,c); change(a,d);
   change(b,d); change(c,d);
%show b,c;
enddef;
%
vardef extend@#(expr xl,xr)(expr yl,yr)=
clearparc;
save aux, pl,pr,pu,pb,m,__p;
path aux;
numeric pl,pr,pu,pb,m[];
pair __p[];
if isline(@#):
xpart(pl*unitvector(final@#-start@#)*cm+start@#)=xl;
xpart(pr*unitvector(final@#-start@#)*cm+start@#)=xr;
ypart(pu*unitvector(final@#-start@#)*cm+start@#)=yr;
ypart(pb*unitvector(final@#-start@#)*cm+start@#)=yl;

middle(m1,m2)(pl,pr,pu,pb);
 __parc0=m1*unitvector(final@#-start@#)*cm+start@#;
 __parc1=m2*unitvector(final@#-start@#)*cm+start@#;
 aux=__parc0--__parc1;
elseif isparabola(@#):
__p0=point 0 of @#;
__p1=point 0.5 of @#;
__p2=point 1 of @#;
%aux=circumpara(__p0,__p1,__p2, xl,xr);
aux=@#;
else: aux=@#;
fi
expandafter aux
enddef;

%%%%%%%%%%%%%%% old
def tangents(expr p,c,r)(suffix tp,tn) =
 begingroup
   save sa,sb,sc;
   pair sa,sb,sc;
   sa=(r,distance(c,p)+-+r);
   sb=unitvector(sa);
   sc=c+r*unitvector(p-c);
   tp = sc rotatedaround (c,angle(sb));
   tn = sc rotatedaround (c,-angle(sb));
 endgroup
enddef;

def circumscribe(expr q,c,r,x,y,u) =
 begingroup
  (c-.5[x,y])dotprod(x-y)=0;
  (c-.5[x,u])dotprod(x-u)=0;
  r=distance(c,x);
  circum(q,c,r);
 endgroup
enddef;

%27/01/97 Вялый: касательные и вписанные окружности



%27.04.98 Вялый: отражение прямой относительно прямой (есть общая точка)
def reflect_line(expr c,cc)(suffix ln,rln) =
 begingroup
   (ln-rln) dotprod (cc-c)=0;
   0.5[ln,rln]=whatever[cc,c];
 endgroup
enddef;

%28.04.98 Вялый: окружность, вписанная в криволинейный треугольник

def InsCribe(expr p,l,r)(expr x,c,y)(expr a,R)(expr xx,yy,aa) =
   begingroup
      save mu,ld,zz,phi, u,cs,sn,dd,D;
      pair u[],zz;
      numeric mu,ld,phi,cs,sn,dd,D;

      bisector(c,x,y)(u0);
      zz=unitvector(u0-c);
      mu=zz dotprod(c-a);
      u1=whatever[c,x];
      (u1-zz) dotprod (c-x)=0;
      sn=distance(u1,zz);
      cs=1-sn*sn;
      dd=distance(a,c);
      D:=R*sqrt((sn+mu/R)**2-cs*((dd/R)**2-1));
      ld=(-(R*sn+mu)+D)/cs;
      l=ld*zz+c;
%      draw c--c+2mv*zz dashed evenly;
      r=ld*sn;
      circum(p,l,r);
      xx=c+ld*sqrt(cs)*unitvector(x-c);
      yy=c+ld*sqrt(cs)*unitvector(y-c);
      aa=R*unitvector(l-a)+a;
   endgroup
enddef;




%11.05.98 Вялый: отражение относительно прямой
def reflect (expr x)(expr a,b,p)(expr r)=
begingroup
r=x -2*(((b-a)dotprod(x-p))/((b-a)dotprod(b-a)))*(b-a);
endgroup
enddef;


