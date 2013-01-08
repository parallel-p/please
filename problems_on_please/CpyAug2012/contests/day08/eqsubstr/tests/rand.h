
static int seed=0;
static unsigned int zeed=0;

static inline int rand8() {
  unsigned int x=zeed;
  for(int i=0;i<8;++i) {
    unsigned int z=x&0x02D;
    unsigned int s;
    for(s=0;z;s^=1,z&=(z-1));
    x=(x>>1)|(s<<31);
  }
  zeed=x;
  return x&0xFF;
}

static inline int rand31() {
  return (seed=(1664525*seed+1013904223)&0x7FFFFFFF);
}

static int tablex[256];
static int initialized=0;

void z_srand(int seed) {
  ::seed=seed;
  zeed=3562951413U;
  for(int i=0;i<256;++i) {
    tablex[i]=rand31();
  }
  initialized=1;
}

int z_rand16() {
  if(!initialized) {
    z_srand(3141592653U);
  }
  int ind=rand8();
  int res=tablex[ind];
  tablex[ind]=rand31();
  return res&0xFFFF;
}

int z_rand31(){
  return ((z_rand16() << 16) | z_rand16())&0x7FFFFFFF;
}

int z_rand(){
  return z_rand31();
}

int z_rand(int mod){
  return z_rand() % mod;
}

int z_rand(int l, int r){
  return z_rand() % (r - l + 1) + l;
}

template <class T> void z_swap(T * el1, T * el2){
	T val = *el1;
	*el1 = *el2;
	*el2 = val;
}

template <class T> void z_random_shuffle(T * first, T * last){
	int n = last - first;
	for (int i = 0; i < n - 1; i++){
		int pos = z_rand() % (n - i);
		z_swap(first + i, first + i + pos);
	}
}

template <class T> void z_swap(T & el1, T & el2){
	T val = el1;
	el1 = el2;
	el2 = val;
}

template <class iterator> void z_random_shuffle(iterator first, iterator last){
	int n = (int)(last - first);
	for (int i = 0; i < n - 1; i++){
		int pos = z_rand() % (n - i);
		z_swap(*(first + i), *(first + i + pos));
	}
}
