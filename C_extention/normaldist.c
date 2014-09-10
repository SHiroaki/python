#include "normaldist.h"
#include <math.h>

double normal_distribution(double myu, double sigma, double x){
 
  double d;
  double coefficient, in_exp;
  
  coefficient = sqrt(2 * M_PI * sigma); //係数
  in_exp = exp( -pow( x - myu, 2 ) / (2 * sigma ));  //expの肩にのるやつ

  d = in_exp / coefficient;

  return d;

}

