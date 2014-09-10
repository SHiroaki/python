#include "normaldist.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define  A
//#define B

#ifdef A
#define NUM_OF_GENERATION       20
#endif
#ifdef B
#define NUM_OF_GENERATION     40000
#endif

int main(){
  //myum sigma, divが動的に決まるようにしたいね
  double *r;
  int i;
  
  r = get_base_bias(500, 40000, 40);

  /*for (i=0; i<(sizeof(biases)/sizeof(double)); i++){
    printf("%f\n", biases[i]);
    }*/
  get_bias_gen(20, 50, 0);
  return 0;
}

double normal_distribution(double myu, double sigma, double x){
 
  double d;
  double coefficient, in_exp;
  
  coefficient = sqrt(2 * M_PI * sigma); //係数
  in_exp = exp( -pow( x - myu, 2 ) / (2 * sigma ));  //expの肩にのるやつ
  d = in_exp / coefficient;

  return d;

}

double *get_base_bias( double myu, double sigma, int div){
  //基本となるバイアスを返す.divは何世代バイアスをかけるか.genは外圧のかかる世代

  double d;
  double coefficient, in_exp;
  double base_bias[1001];
  int i, j, div_gen;
  double *real_bias;

  real_bias = (double *)malloc(sizeof( double ) * div);

  for (i=0; i<=1000; i++){
    coefficient = sqrt(2 * M_PI * sigma); //係数
    in_exp = exp( -pow( i - myu, 2 ) / (2 * sigma ));  //expの肩にのるやつ
    d = in_exp / coefficient;    
    base_bias[i] = d*100000.0;
    //printf("%f\n", base_bias[i]);
  }
  
  //1000をdiv区切りにする
  div_gen = 1000 / div;
  j = 0;
  for (i=0; i<=1000; i+=div_gen ){
    real_bias[j] = base_bias[i];
    j+=1;
    //printf("%d, %f\n", i, real_bias[j-1]);
  }

  /*for (i=0; i<div; i++){
    printf("%f\n", *(real_bias+i));
    }*/

  printf("real bias %x\n",&real_bias);
  free(real_bias);

  return 0;
}

double get_bias_gen(int div, int gen, double power){

  int i;
  double bias_gen[div]; //biasがかかる世代[50,51,52,53...]

  for (i=0; i<div; i++){
    bias_gen[i] = gen + i;
    //printf("%f\n", bias_gen[i]);
  }

}
