#include <Python.h>
#include "loop.h"

struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static char module_docstring[] =
    "The module provides quick calculations for loops in Python using C.";
static char clattices_loop_docstring[] =
    "Calculates coincidences between two given crystals using eq. 11.";

/* Loop for finding coincidence lattices module in C to be called from Python */
static PyObject* clattices_loop (PyObject* self, PyObject* args)
{
	double angle_start, angle_end, angle_step, tolerance, angle_tolerance;
	int Nmax;
	
	/* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "dddidd", &angle_start, &angle_end, &angle_step, &Nmax, &tolerance, &angle_tolerance))
        return NULL;
        
    loop (angle_start, angle_end, angle_step, Nmax, tolerance, angle_tolerance);	
	return Py_None;
}


/*
 * Bind Python function names to our C functions
 */
static PyMethodDef clattices_loop_methods[] = {
	{"clattices_loop", clattices_loop, METH_VARARGS, clattices_loop_docstring},
	{NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "clattices_loop",
        module_docstring,
        5*sizeof(double) + 1*sizeof(int),
        clattices_loop_methods,
        NULL,
        NULL,
        NULL,
        NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_clattices_loop(void)

#else
#define INITERROR return

void
initclattices_loop(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("clattices_loop", clattices_loop_methods);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("clattices_loop.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
