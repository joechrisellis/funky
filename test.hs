-- code generated by funky's haskell generator
-- timestamp: 2019-02-20 at 12:17:44

-- section: create_adts
data List = Cons Integer List
          | Nil 
          deriving (Show, Eq)

data Tree = Branch Tree Integer Tree
          | Empty 
          deriving (Show, Eq)

v0 = \v0_0 -> \v0_1 -> case v0_0 of { Cons cons_v0_0_0 cons_v0_0_1 -> ((Cons)(cons_v0_0_0))(((v0)(cons_v0_0_1))(v0_1)); _ -> case v0_1 of { Nil  -> v0_0; _ -> case v0_0 of { Nil  -> v0_1; _ -> undefined } } }
v1 = \v1_0 -> \v1_1 -> \v1_2 -> case v1_2 of { Nil  -> v1_1; _ -> case v1_2 of { Cons cons_v1_2_0 cons_v1_2_1 -> ((v1_0)(cons_v1_2_0))((((v1)(v1_0))(v1_1))(cons_v1_2_1)); _ -> undefined } }
v2 = \v2_0 -> \v2_1 -> case v2_1 of { Empty  -> (((Branch)(Empty))(v2_0))(Empty); _ -> case v2_1 of { Branch branch_v2_1_0 branch_v2_1_1 branch_v2_1_2 -> case ((<=)(v2_0))(branch_v2_1_1) of { True -> (((Branch)(((v2)(v2_0))(branch_v2_1_0)))(branch_v2_1_1))(branch_v2_1_2); False -> case ((>)(v2_0))(branch_v2_1_1) of { True -> (((Branch)(branch_v2_1_0))(branch_v2_1_1))(((v2)(v2_0))(branch_v2_1_2)); False -> undefined } }; _ -> undefined } }
v3 = \v3_0 -> case v3_0 of { Empty  -> Nil; _ -> case v3_0 of { Branch branch_v3_0_0 branch_v3_0_1 branch_v3_0_2 -> ((v0)(((v0)((v3)(branch_v3_0_0)))(((Cons)(branch_v3_0_1))(Nil))))((v3)(branch_v3_0_2)); _ -> undefined } }
v4 = \v4_0 -> (v3)((((v1)(v2))(Empty))(v4_0))

-- section: emit_main
main = do
       print (let { v5 = ((Cons)(5))(((Cons)(1))(((Cons)(7))(((Cons)(7))(((Cons)(3))(Nil))))) } in (v4)(v5))