#!/usr/bin/perl -w

use strict;

#######################################################################
# Стандартные определения и проверки входных аргументов
my $OK=0;
my $PE=4;
my $WA=5;
my $CF=6;

if ( $#ARGV < 2)
{
    print "Слишком мало параметров получено\n";
    exit $CF;
}

if ( ! (-r $ARGV[0]) )
{
    print "Входной файл $ARGV[0] недоступен для чтения\n";
    exit $CF;
}

if ( ! (-r $ARGV[1]) )
{
    print "Выходной файл $ARGV[1] недоступен для чтения\n";
    exit $CF;
}

if ( ! (-r $ARGV[2]) )
{
    print "Файл с ответом $ARGV[2] недоступен для чтения\n";
    exit $CF;
}

# Конец стандартной проверки
########################################################################

my ($N, $W, @weight, @price, $i, $ans, @ans, $out, @out, $tw1, $ts1, $tw2, $ts2, $prev);

undef $/;

open IN, $ARGV[0];
$_=<IN>;
if ( ! m<^\s*(\d+)\s*\n\s*(.*\d)\s*\n\s*(.*\d)\s*$>s)
{
	print "Не удалось разобрать файл с тестом";
	exit $CF;
}
$W=$1;
@weight=split(/\s+/,$2);
$N=$#weight + 1;
@weight=(0, @weight);
@price=split(/\s+/,$3);
@price=(0,@price);

# print "N=$N\n";
# print "W=$W\n";
# print "2=:", join(':', @weight), ":\n";
# print "3=:", join(':', @price), ":\n";


open ANSWER, $ARGV[2];
$_=<ANSWER>;
s/^\s*//;
s/\s*$//;
@ans=sort(split(/\s+/,$_));

$tw1=0;
$ts1=0;
$prev=0;
foreach $i(@ans)
{
	if($i !~ /^\d+$/)
	{
		print "Номер предмета $i не является числом";
		exit $CF;
	}
	if($i<1 or $i>$N)
	{
		print "Недопустимый номер предмета $i";
		exit $CF;
	}
	if($i == $prev)
	{
		print "Предмет номер $prev встречается дважды";
		exit $CF;
	}
	$tw1+=$weight[$i];
	$ts1+=$price[$i];
	$prev=$i;
}

if($tw1>$W)
{
	print "Перебор по массе";
	exit $CF;
}

open OUT, $ARGV[1];
$_=<OUT>;
s/^\s*//;
s/\s*$//;
@out=sort(split(/\s+/,$_));

$tw2=0;
$ts2=0;
$prev=0;
foreach $i(@out)
{
	if($i !~ /^\d+$/)
	{
		print "Номер предмета $i не является числом";
		exit $PE;
	}
	if($i<1 or $i>$N)
	{
		print "Недопустимый номер предмета $i";
		exit $WA;
	}
	if($i == $prev)
	{
		print "Предмет номер $prev встречается дважды\n";
		exit $WA;
	}
	$tw2+=$weight[$i];
	$ts2+=$price[$i];
	$prev=$i;
}

if($tw2>$W)
{
	print "Перебор по массе\n";
	exit $WA;
}


exit $OK if $ts1 == $ts2;
exit $WA if $ts1 > $ts2;
if ($ts1 < $ts2)
{
    print "Сумма авторского решения $ts1\n";
    print "Сумма  решения участника $ts2\n";
    exit $CF;
}

