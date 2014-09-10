#include <stdio.h>
#include <math.h>

double normal_distribution(double, double, double);

int main(void){
  
  double m = 0.0;
  double s = 0.2;
  double i;


  for(i = -3.0; i <= 3.0; i+=0.01){
    printf("");
    normal_distribution(m, s, i);
  }

  return 0;

}

double normal_distribution(double myu, double sigma, double x){
  //normal_dist_bias = (1.0/math.sqrt(2**sigma))
 
  double d;
  double coefficient, in_exp;
  
  coefficient = sqrt(2 * M_PI * sigma); //係数
  in_exp = exp( -pow( x - myu, 2 ) / (2 * sigma ));  //expの肩にのるやつ

  d = in_exp / coefficient;
  printf("%f, %2.5f\n", x, d);
}
