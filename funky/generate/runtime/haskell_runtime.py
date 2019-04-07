from funky.generate.runtime import Runtime, add_to_runtime

class HaskellRuntime(Runtime):

    def __init__(self):
        super().__init__()

        self.builtins = {
            "=="          :  self.runtime_eq,
            "!="          :  self.runtime_neq,
            "<"           :  self.runtime_less,
            "<="          :  self.runtime_leq,
            ">"           :  self.runtime_greater,
            ">="          :  self.runtime_geq,
            "**"          :  self.runtime_pow,
            "+"           :  self.runtime_add,
            "++"          :  self.runtime_concat,
            "-"           :  self.runtime_sub,
            "negate"      :  self.runtime_negate,
            "*"           :  self.runtime_mul,
            "/"           :  self.runtime_div,
            "%"           :  self.runtime_mod,
            "and"         :  self.runtime_logical_and,
            "or"          :  self.runtime_logical_or,
            "to_str"      :  self.runtime_to_str,
            "to_int"      :  self.runtime_to_int,
            "to_float"    :  self.runtime_to_float,
            "slice_from"  :  self.runtime_slice_from,
            "slice_to"    :  self.runtime_slice_to,

            "fail"        :  self.runtime_fail,
            "undefined"   :  self.runtime_undefined,
        }
    
    def runtime_eq(self):
        return "=="

    def runtime_neq(self):
        return "/="

    def runtime_less(self):
        return "<"

    def runtime_leq(self):
        return "<="

    def runtime_greater(self):
        return ">"

    def runtime_geq(self):
        return ">="

    def runtime_pow(self):
        return "^"

    def runtime_add(self):
        return "+"

    def runtime_concat(self):
        return "++"

    def runtime_sub(self):
        return "-"

    def runtime_negate(self):
        return "negate"

    def runtime_mul(self):
        return "*"

    def runtime_div(self):
        return "/"

    def runtime_mod(self):
        return "mod"

    def runtime_logical_and(self):
        return "&&"

    def runtime_logical_or(self):
        return "||"

    def runtime_to_str(self):
        return "show"

    IMPORT_TEXT = "import Text.Read"

    @add_to_runtime
    def runtime_to_int(self):
        self.used_runtime_methods.add(self.IMPORT_TEXT)
        fname = "to_int"
        return """{} :: Show a => a -> Integer
{} x = case readMaybe (show x) :: Maybe Float of
               Just x  -> round x
               Nothing -> case readMaybe (show x) :: Maybe Bool of
                            Just x -> if x then 1 else 0
                            Nothing -> read (read (show x)) :: Integer""".format(fname, fname), fname

    @add_to_runtime
    def runtime_to_float(self):
        self.used_runtime_methods.add(self.IMPORT_TEXT)
        fname = "to_float"
        return """{} :: Show a => a -> Float
{} x = case readMaybe (show x) :: Maybe Integer of
               Just x -> fromIntegral x :: Float
               Nothing -> read (read (show x)) :: Float""".format(fname, fname), fname

    # NOTE: runtime_slice_from and runtime_slice_to have to wrangle around the
    #       Haskell type system a bit. The drop function accepts Int, but we
    #       use Integer every else, so we have to convert if we want the
    #       Haskell code to type check.

    @add_to_runtime
    def runtime_slice_from(self):
        fname = "runtime_slice_from"
        return """{} :: Integer -> String -> String
{} n xs = drop ((fromIntegral n) :: Int) xs""".format(fname, fname), fname

    @add_to_runtime
    def runtime_slice_to(self):
        fname = "runtime_slice_to"
        return """{} :: Integer -> String -> String
{} n xs = take ((fromIntegral n) :: Int) xs""".format(fname, fname), fname

    def runtime_fail(self):
        return "error"

    def runtime_undefined(self):
        return "undefined"
