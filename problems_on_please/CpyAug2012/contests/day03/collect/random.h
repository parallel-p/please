/*
   Generator idea by Donald E. Knuth.
   Using constants suggested in "Numerical Recipes in C" book version 2
    (link: http://www.nr.com).
   Initial implementation by Ivan Kazmenko (gassa[at]mail[dot]ru).
   Modified by various authors at Russian School Summer Training Camps.
   (c) Ivan Kazmenko, 2009.
   License: Lesser General Public License version 3+
    (links: http://www.gnu.org/licenses/lgpl.html,
            http://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License)
*/
#ifndef __random_h__
#define __random_h__

#include <cmath>
#include <cstdio>
#include <cstdlib>

const int MBIG = 1000000000, MSEED = 161803398;
const double FAC = 1.0 / MBIG;

int inext, inextp;
int ra [56];

/**
  Internal function to generate next pseudo-random number.
  It is uniformly distributed in the range [0 .. MBIG-1].
  Please do not use this function directly.
  */
int nextrand (void)
{
  int j;
  if (++inext == 56) inext = 1;
  if (++inextp == 56) inextp = 1;
  j = ra[inext] - ra[inextp];
  if (j < 0) j += MBIG;
  ra[inext] = j;
  return j;
}

/**
  Initialize pseudo-random number generator.
  Call this before any calls to other functions.
  */
bool initrand (int seed)
{
  int i, j, k, l;
  l = MSEED - seed;
  if (l < 0) l = -l;
  l %= MBIG;
  ra[55] = l;
  k = 1;
  for (i = 1, j = 0; i <= 54; i++)
  {
   j += 21;
   if (j > 55) j -= 55;
   ra[j] = k;
   k = l - k;
   if (k < 0) k += MBIG;
   l = ra[j];
  }
  for (k = 1; k <= 4; k++)
   for (i = 1, j = 31; i <= 55; i++, j >= 55 ? j = 1 : j++)
   {
    ra[i] -= ra[j];
    if (ra[i] < 0) ra[i] += MBIG;
   }
  inext = 0;
  inextp = 31;
  return true;
}

/**
  Generate next pseudo-random number as a double in range [0 .. 1).
  */
double rndvalue (void)
{
  return nextrand () * FAC;
}

/**
  Generate next pseudo-random number as an integer in range [0 .. k-1).
  */
int rndvalue (int k)
{
  return (int) floor (rndvalue () * k);
}

/**
  Read current time stamp counter
  (number of processor ticks passed since system start).
  */
long long Time (void)
{
#ifdef __GNUC__
  long long res;
  asm volatile ("rdtsc" : "=A" (res));
  return res;
#else
  unsigned lo, hi;
  __asm {
    rdtsc
    mov lo, eax
    mov hi, edx
  }
  return lo | ((unsigned long long) hi << 32ull);
#endif
}

/**
  Macro to generate a pseudo-random integer in range [A .. B].
  */
#define R(A, B) ((A) + rndvalue((B) - (A) + 1))

#endif // __random_h__
