#include <Python.h>

#ifdef _MSC_VER
typedef unsigned __int32 uint32_t;
#else
#include <stdint.h>
#endif

#include <vector>
#include <math.h>

static const int SMALL_BLOCK_SIZE = 32;
static const int LARGE_BLOCK_SIZE = 256; 
static const int BLOCK_RATE       = 8;

struct BitVectorCore {
    std::vector<uint32_t> v;
    std::vector<uint32_t> r;
    uint64_t size;
    uint64_t size1;
};

uint32_t rank32(uint32_t x, int i) {
    x <<= (SMALL_BLOCK_SIZE - i);
    x = ((x & 0xaaaaaaaa) >>  1) + (x & 0x55555555);
    x = ((x & 0xcccccccc) >>  2) + (x & 0x33333333);
    x = ((x & 0xf0f0f0f0) >>  4) + (x & 0x0f0f0f0f);
    x = ((x & 0xff00ff00) >>  8) + (x & 0x00ff00ff);
    x = ((x & 0xffff0000) >> 16) + (x & 0x0000ffff);
    return x;
}

int select32(uint32_t x, int i, bool b) {
    if (!b) {
        x = ~x;
    }
    uint32_t x1 = ((x  & 0xaaaaaaaa) >>  1) + (x  & 0x55555555);
    uint32_t x2 = ((x1 & 0xcccccccc) >>  2) + (x1 & 0x33333333);
    uint32_t x3 = ((x2 & 0xf0f0f0f0) >>  4) + (x2 & 0x0f0f0f0f);
    uint32_t x4 = ((x3 & 0xff00ff00) >>  8) + (x3 & 0x00ff00ff);
    uint32_t x5 = ((x4 & 0xffff0000) >> 16) + (x4 & 0x0000ffff);
    ++i;
    int pos = 0;
    uint32_t v5 = x5 & 0xffffffff;
    if (i > v5) {
        i -= v5;
        pos += 32;
    }
    uint32_t v4 = (x4 >> pos) & 0x0000ffff;
    if (i > v4) {
        i -= v4;
        pos += 16;
    }
    uint32_t v3 = (x3 >> pos) & 0x000000ff;
    if (i > v3) {
        i -= v3;
        pos += 8;
    }
    uint32_t v2 = (x2 >> pos) & 0x0000000f;
    if (i > v2) {
        i -= v2;
        pos += 4;
    }
    uint32_t v1 = (x1 >> pos) & 0x00000003;
    if (i > v1) {
        i -= v1;
        pos += 2;
    }
    uint32_t v0 = (x >> pos) & 0x00000001;
    if (i > v0) {
        i -= v0;
        pos++;
    }
    return pos;
}

extern "C" {

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    BitVectorCore* bitvector;
} BitVector;

static void
BitVector_dealloc(BitVector* self)
{
    delete self->bitvector;
    self->bitvector = 0;
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject *
BitVector_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    BitVector *self;

    self = (BitVector *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->bitvector = new BitVectorCore();
    }

    return (PyObject *)self;
}

static int
BitVector_init(BitVector* self, PyObject *args, PyObject *kwds) {
    return 0;
}

static PyObject*
BitVector_build(BitVector* self) {
    self->bitvector->size1 = 0;
    int count = self->bitvector->v.size();
    for (int i = 0; i < count; i++) {
        uint32_t value = self->bitvector->v[i];
        if (i % BLOCK_RATE == 0) {
            self->bitvector->r.push_back(self->bitvector->size1);
        }
        self->bitvector->size1 += rank32(value, SMALL_BLOCK_SIZE);
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject*
BitVector_clear(BitVector* self) {
    self->bitvector->r.clear();
    self->bitvector->v.clear();
    self->bitvector->size = 0;
    self->bitvector->size1 = 0;

    Py_INCREF(Py_None);
    return Py_None;
}


static PyObject*
BitVector_size(BitVector* self) {
    return PyLong_FromLong(self->bitvector->size);
}

static PyObject*
BitVector_size0(BitVector* self) {
    return PyLong_FromLong(self->bitvector->size - self->bitvector->size1);
}

static PyObject*
BitVector_size1(BitVector* self) {
    return PyLong_FromLong(self->bitvector->size1);
}

static PyObject*
BitVector_set(BitVector* self, PyObject *args, PyObject *keywds) {
    int value;
    int flag = 1;
    static char *kwlist[] = {"value", "flag", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "i|b", kwlist, &value, &flag))
        return NULL;

    if (value >= self->bitvector->size) {
        self->bitvector->size = value + 1;
    }
    int q = value / SMALL_BLOCK_SIZE;
    int r = value % SMALL_BLOCK_SIZE;
    while (q >= self->bitvector->v.size()) {
        self->bitvector->v.push_back(0);
    }
    int m = 0x1 << r;
    if (flag) {
        self->bitvector->v[q] |=  m;
    } else {
        self->bitvector->v[q] &= ~m;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject*
BitVector_get(BitVector* self, PyObject* args) {
    int value;
    if (!PyArg_ParseTuple(args, "i", &value))
        return NULL;

    if (value >= self->bitvector->size) {
        PyErr_SetString(PyExc_RuntimeError, "bitvector->get() : range error");
        return NULL;
    }

    int q = value / SMALL_BLOCK_SIZE;
    int r = value % SMALL_BLOCK_SIZE;
    int m  = 0x1 << r;
    return PyBool_FromLong(self->bitvector->v[q] & m);
}


static PyObject*
BitVector_rank(BitVector* self, PyObject *args, PyObject *keywds) {
    int i;
    int b = 1;
    static char *kwlist[] = {"i", "b", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "i|b", kwlist, &i, &b))
        return NULL;

    if (i > self->bitvector->size) {
        PyErr_SetString(PyExc_RuntimeError, "bitvector->rank() : range error");
        return NULL;
    }
    if (i == 0) {
        return  PyLong_FromLong(0);
    }
    i -= 1;
    int q_large = (int)floor(i / LARGE_BLOCK_SIZE);
    int q_small = (int)floor(i / SMALL_BLOCK_SIZE);
    int r       = (int)floor(i % SMALL_BLOCK_SIZE);
    int rank = self->bitvector->r[q_large];
    if (!b) {
        rank = q_large * LARGE_BLOCK_SIZE - rank;
    }
    int begin = q_large * BLOCK_RATE;
    int value;
    for (int j = begin; j < q_small; j++) {
        if (b) {
            value = self->bitvector->v[j];
        } else {
            value = ~self->bitvector->v[j];
        }
        rank += rank32(value, SMALL_BLOCK_SIZE);
    }
    value = (b) ? self->bitvector->v[q_small] : ~self->bitvector->v[q_small];
    return PyLong_FromLong(rank + rank32(value, r + 1));
}


static PyObject*
BitVector_select(BitVector* self, PyObject *args, PyObject *keywds) {
    int i;
    int b = 1;
    static char *kwlist[] = {"i", "b", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "i|b", kwlist, &i, &b))
        return NULL;
    if (b) {
        if (i >= self->bitvector->size1) {
            PyErr_SetString(PyExc_RuntimeError, "bitvector->select() : range error");
            return NULL;
        }
    } else if (i >= (self->bitvector->size - self->bitvector->size1)) {
        PyErr_SetString(PyExc_RuntimeError, "bitvector->select() : range error");
        return NULL;
    }
    int left = 0;
    int right = self->bitvector->r.size();
    while (left < right) {
        int pivot = (int)floor((left + right) / 2);
        int rank  = self->bitvector->r[pivot];
        if (!b) {
            rank = pivot * LARGE_BLOCK_SIZE - rank;
        }
        if (i < rank) {
            right = pivot;
        } else {
            left = pivot + 1;
        }
    }
    right -= 1;
    if (b) {
        i -= self->bitvector->r[right];
    } else {
        i -= right * LARGE_BLOCK_SIZE - self->bitvector->r[right];
    }
    int j = right * BLOCK_RATE;
    while (1) {
        int value;
        if (b) {
            value = self->bitvector->v[j];
        } else {
            value = ~self->bitvector->v[j];
        }
        int rank = rank32(value, SMALL_BLOCK_SIZE);
        if (i < rank) {
            break;
        }
        ++j;
        i -= rank;
    }
    return PyLong_FromLong(j * SMALL_BLOCK_SIZE + select32(self->bitvector->v[j], i, b));
}

static PyObject*
BitVector_int32vector(BitVector* self) {
    int count = self->bitvector->v.size();
    PyObject* result = PyList_New(count);
    for (int i = 0; i < count; i++) {
        PyList_SetItem(result, i, PyLong_FromLong(self->bitvector->v[i]));
    }
    return result; 
}

static PyMethodDef BitVector_methods[] = {
    {"build", (PyCFunction)BitVector_build, METH_NOARGS,
     "Precalculates rank() number. It should be called before using select() and rank()."
    },
    {"clear", (PyCFunction)BitVector_clear, METH_NOARGS,
     "Clears bit-vector."
    },
    {"size", (PyCFunction)BitVector_size, METH_NOARGS,
     "It returns bit-vector length"
    },
    {"size0", (PyCFunction)BitVector_size0, METH_NOARGS,
     "It returns number of 0 bit in bit-vector."
    },
    {"size1", (PyCFunction)BitVector_size1, METH_NOARGS,
     "It returns number of 0 bit in bit-vector."
    },
    {"set", (PyCFunction)BitVector_set, METH_VARARGS | METH_KEYWORDS,
     "set bit"
    },
    {"get", (PyCFunction)BitVector_get, METH_VARARGS,
     "get bit"
    },
    {"rank", (PyCFunction)BitVector_rank, METH_VARARGS | METH_KEYWORDS,
     "rank"
    },
    {"select", (PyCFunction)BitVector_select, METH_VARARGS | METH_KEYWORDS,
     "select"
    },
    {"int32vector", (PyCFunction)BitVector_int32vector, METH_NOARGS,
     "dump content"
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject BitVectorType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_bitvector.BitVector",             /* tp_name */
    sizeof(BitVector),                  /* tp_basicsize */
    0,                                  /* tp_itemsize */
    (destructor)BitVector_dealloc,      /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_reserved */
    0,                                  /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash  */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    0,                                  /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "BitVector speedup objects",        /* tp_doc */
    0,		                            /* tp_traverse */
    0,		                            /* tp_clear */
    0,		                            /* tp_richcompare */
    0,		                            /* tp_weaklistoffset */
    0,		                            /* tp_iter */
    0,		                            /* tp_iternext */
    BitVector_methods,                  /* tp_methods */
    0,                                  /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    (initproc)BitVector_init,           /* tp_init */
    0,                                  /* tp_alloc */
    BitVector_new,                      /* tp_new */
};


static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
init_bitvector(void) 
{
    PyObject* m;

    if (PyType_Ready(&BitVectorType) < 0)
        return;

    m = Py_InitModule3("_bitvector", module_methods,
                       "Example module that creates an extension type.");

    if (m == NULL)
      return;

    Py_INCREF(&BitVectorType);
    PyModule_AddObject(m, "BitVector", (PyObject *)&BitVectorType);
}

} // extern "C"
