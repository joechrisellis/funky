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
    v.clo.env  =  NULL;
    return v;
}

static Value MakeEnv(void* env) {
    Value v;
    v.env.t    =   ENV;
    v.env.env  =   env;
    return     v;
}

extern Value __add;
extern Value __subtract;
extern Value __times;
extern Value __divide;
extern Value __print;
extern Value __numEqual;
