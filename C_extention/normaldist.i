%module normaldist

%{
#define SWIG_FILE_WITH_INIT
#include "normaldist.h"
#include <math.h>
  %}

double normal_distribution(double myu, double sigma, double x);

