#include <Python.h>


static PyObject *
spam_system(PyObject *self, PyObject *args)
{
  const char *command;
  int sts;

  if (!PyArg_ParseTuple(args, "s", &command)) 
    /*Python の文字列または Unicode オブジェクトを、キャラクタ文字列を指す 
      C のポインタに変換. "s"の意味
    */
      return NULL;

  sts = system(command);
  return Py_BuildValue("i", sts);
  /*書式化文字列と任意の数の C の値を引数にとり、新たな Python オブジェクト
   を返す. "i"は整数オブジェクトという意味*/
}

static PyMethodDef SpamMethods[] = {
  {"system", spam_system, METH_VARARGS,
   "説明 Execute a shell command."},
  {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC
initspam(void)
{
  (void) Py_InitModule("spam", SpamMethods);
}

