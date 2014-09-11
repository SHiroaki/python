#include <Python.h>

#define LOWER_BOUND    0
#define UPPER_BOUND    1000
#define MAX_BIT_LENGTH 10

int binaryToValue(int *);

static PyObject *
make_individual(PyObject *self, PyObject *args)
{

  int b[MAX_BIT_LENGTH];
  int m,n,i,len;
  unsigned int min, max;
  unsigned int random_int;
  unsigned int gray_int;

  PyListObject *gray; //pythonのlistオブジェクトを表現
  gray = (PyListObject *) PyList_New(MAX_BIT_LENGTH); //サイズがMAX~のリストを作る

  if (!PyArg_ParseTuple(args, "ii", &min, &max)) //引数が複数の時はiiみたいに並べて書く
        return NULL;

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
  n = 0;
  for (i=MAX_BIT_LENGTH-1; i>=0; i--){
  //gray に1bitずつint型の値を入れていく
 
  PyList_SET_ITEM(gray, n++, Py_BuildValue("i", b[i]));
  }

  return Py_BuildValue("O", gray);

}

static PyObject *
grayToBinary(PyObject *self, PyObject *args)
{

  unsigned int num;
  unsigned int mask;
  int m,n,i,len;
  int b[MAX_BIT_LENGTH], inputed_binary[MAX_BIT_LENGTH];
  PyListObject *binary; //pythonのlistオブジェクトを表現
  PyObject *get_list;
  binary = (PyListObject *) PyList_New(MAX_BIT_LENGTH); 

  if (!PyArg_ParseTuple(args, "O", &get_list )) 
    return NULL;

  if PyList_Check(get_list) {
  for (i=0; i<PyList_Size(get_list); i++){
  //リストオブジェクトの中身をCで見れるように変換しながら取り出す?(自信なし)
      inputed_binary[i] = PyInt_AsSsize_t(PyList_GetItem(get_list, (Py_ssize_t)i)); //ok
    }
  }

  num = binaryToValue(inputed_binary);
  
  for (mask = num >> 1; mask != 0; mask = mask >> 1){
  //gray codeから元に戻す
  num = num ^ mask;
  }
  
  n = num;
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
  n = 0;
  for (i=MAX_BIT_LENGTH-1; i>=0; i--){
  //binary に1bitずつint型の値を入れていく
 
  PyList_SET_ITEM(binary, n++, Py_BuildValue("i", b[i]));
  }

  return Py_BuildValue("O", binary);
}


int binaryToValue(int *b){
  //2進数を整数に変換する
  int i,n;
  i=0; n=0;

  while(i < MAX_BIT_LENGTH){
  if (b[i] == 1) n+=1;
  i+=1;
  if (i == MAX_BIT_LENGTH) break;
  n=n*2;
  //printf("%d\n", n);
  }
  return n;
}

static PyObject *
binaryToPtype(PyObject *self, PyObject *args)
{

  int i,n;
  int inputed_binary[MAX_BIT_LENGTH];
  PyListObject *binary; //pythonのlistオブジェクトを表現
  PyObject *get_list;

  if (!PyArg_ParseTuple(args, "O", &get_list )) //pythonオブジェクトをそのまま渡す
    return NULL;

  if PyList_Check(get_list) {
  for (i=0; i<PyList_Size(get_list); i++){
      inputed_binary[i] = PyInt_AsSsize_t(PyList_GetItem(get_list, (Py_ssize_t)i)); //ok
    }
  }

  i=0; n=0;

  while(i < MAX_BIT_LENGTH){
  if (inputed_binary[i] == 1) n+=1;
  i+=1;
  if (i == MAX_BIT_LENGTH) break;
  n=n*2;
  //printf("%d\n", n);
  }
  return Py_BuildValue("i", n);
}


static PyObject *
hello(PyObject *self)
{
    printf("Hello World!!\n");
    Py_RETURN_NONE;
}

static char ext_doc[] = "C extention module example\n";

static PyMethodDef methods[] = {
  {"hello", (PyCFunction)hello, METH_NOARGS, "print hello world.\n"},
    {"make_individual", make_individual, METH_VARARGS, "return gray code.\n"},
      {"gray_to_binary", grayToBinary, METH_VARARGS, "return binary code.\n"},
	{"binary_to_ptype", binaryToPtype, METH_VARARGS, "return ptype value.\n"},
	{NULL, NULL, 0, NULL}
};

void initcbinarymethods(void)
{
    Py_InitModule3("cbinarymethods", methods, ext_doc);
}
