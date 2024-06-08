#include <Python.h>

static PyObject*
spam_strlen(PyObject* self, PyObject* args)
{
	char* str;
	int len;
	if (!PyArg_ParseTuple(args, "s", &str))
		return NULL;
	len = strlen(str);
	return Py_BuildValue("i", len);
}
static PyObject* bar_len(PyObject* self, PyObject* args)
{
	int cnt;
	int total;
	int max_height = 250;
	if (!PyArg_ParseTuple(args, "ii", &cnt,&total))
		return NULL;
	int len = max_height * cnt / total;
	return Py_BuildValue("i", len);

}

static PyMethodDef SpamMethods[] = {
	{"strlen", spam_strlen, METH_VARARGS, "count a string length."},
	{"barlen", bar_len, METH_VARARGS, "return a bar length."},
	{NULL, NULL, 0, NULL} 
};
static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",
	"It is test module.",
	-1, SpamMethods
};
PyMODINIT_FUNC

PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}