# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !! IMPORTANT: I only tested this with Pylance in VSCode !!
# !!            (Pyright version 1.1.351).                !!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from NList import NList, num

# NOTE:
# * `NList[L0, L6, L5, L1]` is the type of an nlist of length 651
#    * `L{x}` is an alias for `Literal[x]`, for x = 0, 1, ..., 9.
# * `NList(num(293))` is equivalent to `NList((0,2,9,3))`
#   * both create an nlist of type `NList[L0, L2, L9, L3]`

nlist1 = NList(num(293))
nlist2 = NList(num(358))
nlist3 = nlist1.concat(nlist2)  # NList[L0, L6, L5, L1]

r1 = nlist3.get(num(125)) + 6   # OK: int + int
r2 = nlist3.get(num(650)) + 7   # OK: int + int
r3 = nlist3.get(num(651)) + 1   # Error: None + int  (Cause: Out Of Bounds)
r4 = nlist3.get(num(2241)) - 8  # Error: None - int  (Cause: Out Of Bounds)

empty_nl = NList(num(0))

ie1 = nlist3.is_empty()         # Literal[False]
ie3 = empty_nl.is_empty()       # Literal[True]

_ = nlist3.last_val             # OK: non-empty
_ = empty_nl.last_val           # ERROR: empty :)

nlist4 = NList(num(651))
nlist5 = nlist3 + nlist4        # OK: same length
nlist6 = nlist3 + nlist2        # ERROR: wrong length :)
