#include <stdio.h>
#include <stdlib.h>

#define LOWER_BOUND    0
#define UPPER_BOUND    1000
#define MAX_BIT_LENGTH 10

unsigned int binaryToGray(unsigned int);
unsigned int grayToBinary(unsigned int);

int main(){
  //pythonで呼び出す方法をここに書く
  int b[MAX_BIT_LENGTH], gray[MAX_BIT_LENGTH];
  int m,n,i;
  int min = 200;
  int max = 200;
  int len;
  unsigned int random_int;
  unsigned int gray_int;

  if (min < LOWER_BOUND){
    exit(0);
  }
  else if (max > UPPER_BOUND){
    exit(0);
  }
  //ランダムに整数を発生させる
  random_int = min + (int)(rand()*(max-min+1.0)/(1.0+RAND_MAX));
  gray_int = (random_int >> 1) ^ random_int; //gray codeに変換

  n = gray_int;
  //2進数に変換
  for (i=0; n>0; i++){
    m=n%2;   //2で割ったあまり
    n=n/2;  //2で割る
    b[i] = m;
  }

  len = i; //整数の2進数変換した時の長さ

  //10bitになるようにけつに0を追加する
  for (i=len; i<MAX_BIT_LENGTH; i++ ){
    b[i] = 0;
  }

  //逆順だったビット列を2進数の順にコピーする
  for (i=MAX_BIT_LENGTH-1; i>=0; i--){
    gray[i] = b[i];
  }


  return 0;
}



unsigned int binaryToGray(unsigned int num)
{
        return (num >> 1) ^ num;
}
 

unsigned int grayToBinary(unsigned int num)
{
    unsigned int mask;
    for (mask = num >> 1; mask != 0; mask = mask >> 1)
    {
        num = num ^ mask;
    }
    return num;
}
