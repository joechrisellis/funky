// section: includes
#include <stdlib.h>
#include <stdio.h>

// section: runtime
struct Integer;
struct Boolean;
struct Closure;
union  Value;

enum Tag { VOID, INTEGER, BOOLEAN, CLOSURE, ENV };

typedef union Value (*Lambda)() ;

struct Integer { enum Tag t; int value;               };
struct Boolean { enum Tag t; unsigned int value;      };
struct Closure { enum Tag t; Lambda lam; void* env;   };
struct Env     { enum Tag t; void* env;               };

union Value {
    enum   Tag     t;
    struct Integer z;
    struct Boolean b;
    struct Closure clo;
    struct Env     env;
};

typedef union Value Value;

static Value MakeClosure(Lambda lam, Value env) {
    Value v;
    v.clo.t    =  CLOSURE;
    v.clo.lam  =  lam;
    v.clo.env  =  env.env.env;
    return v;
}

static Value MakeInteger(int n) {
    Value v;
    v.z.t      =  INTEGER;
    v.z.value  =  n;
    return v;
}

static Value MakeBoolean(unsigned int b) {
    Value v;
    v.b.t      =  BOOLEAN;
    v.b.value  =  b;
    return v;
}

static Value MakePrimitive(Lambda prim) {
    Value v;
    v.clo.t    =  CLOSURE;
    v.clo.lam  =  prim;

Value __prim_add(Value e, Value a, Value b) {
    return MakeInt(a.z.value + a.z.value);
}

Value __prim_subtract(Value e, Value a, Value b) {
    return MakeInt(a.z.value - b.z.value);
}

Value __prim_times(Value e, Value a, Value b) {
    return MakeInt(a.z.value * b.z.value);
}

Value __prim_divide(Value e, Value a, Value b) {
    return MakeInt(a.z.value / b.z.value);
}

Value __prim_print(Value e, Value v) {
    printf("%i\n", v.z.value);
    return v;
}

Value __prim_numEqual(Value e, Value a, Value b) {
    return MakeBoolean(a.z.value == b.z.value);
}

// section: default_storage
Value __add;
Value __subtract;
Value __times;
Value __divide;
Value __print;
Value __numEqual;

// section: create_adts
