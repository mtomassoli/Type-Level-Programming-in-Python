from pathlib import Path
from itertools import product

NUM_OPS = 4
DEST_DIR_FP = Path('.')
OVERWRITE_FILES = False


def write_op(op_num: int, *, overwrite = False):
    """Creates a file `f"ops{op_num}.py"` in `DEST_DIR_FP` with the operations
    `f"adc{op_num}"` and `"sbb{op_num}"`, which perform addition with carry and
    subtraction with borrow, respectively.
    """
    lines: list[str] = [
        "from typing import overload",
        "from misc import L0, L1, L2, L3, L4, L5, L6, L7, L8, L9, Digit\n",
    ]

    ##### ADC #####    
    for x, y, c in product(range(10), range(10), range(2)):
        val = x + y + c
        new_digit = val % 10
        new_carry = val // 10
        lines.extend([
            "@overload",
            (
                f"def adc{op_num}(x: L{x}, y: L{y}, c: L{c}) "
                f"-> tuple[L{new_digit}, L{new_carry}]: ..."
            )
        ])
    lines.append(f"def adc{op_num}(x: Digit, y: Digit, c: L0 | L1) "
                 "-> tuple[Digit, L0 | L1]: ...")

    lines.append("\n# ----------------------\n")

    ##### SBB #####
    for x, y, b in product(range(10), range(10), range(2)):
        val = 10 + x - y - b
        new_digit = val % 10
        new_borrow = 1 - val // 10
        lines.extend([
            "@overload",
            (
                f"def sbb{op_num}(x: L{x}, y: L{y}, b: L{b}) "
                f"-> tuple[L{new_digit}, L{new_borrow}]: ..."
            )
        ])
    lines.append(f"def sbb{op_num}(x: Digit, y: Digit, b: L0 | L1) "
                 "-> tuple[Digit, L0 | L1]: ...")

    mode = 'wt' if overwrite else 'xt'
    try:
        with open(DEST_DIR_FP / f"ops{op_num}.py", mode, encoding='utf-8') as f:
            f.writelines(line + '\n' for line in lines)
    except FileExistsError:
        pass

for i in range(1, NUM_OPS + 1):
    write_op(i, overwrite=OVERWRITE_FILES)
