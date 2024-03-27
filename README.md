# A statically typed list that knows its length

## In a nutshell

* `NList[L0, L6, L5, L1]` has length 651
* Instance creation:
  * `NList((0,6,5,1))`
  * `NList(num(651))`
* Concatenation is statically typed:
  * `nlist1 = NList(num(1111))`
  * `nlist2 = NList(num(2222))`
  * `nlist3 = nlist1.concat(nlist2)` is of type `NList[L3, L3, L3, L3]`
* Point-wise addition is statically checked:
  * *OK*: `nlist3 + NList(num(3333))`
  * *ERROR*: `nlist1 + nlist2`
* Indexing is statically bound-checked:
  * *OK*: `nlist1.get(num(46)) + 12`
  * *OK*: `nlist1.get(num(597)) + 12`
  * *ERROR*: `nlist1.get(num(1111)) + 12`
  * *ERROR*: `nlist1.get(num(2567)) + 12`
  * **NOTE:** `get` returns:
    * `int` for correct indexing
    * `None` for out-of-bounds indexing
* In particular, a list knows whether it's empty:
  * `empty_nl = NList(num(0))`
  * `nlist3.is_empty()` is of type `Literal[False]`
  * `empty_nl.is_empty()` is of type `Literal[True]`
  * *OK*: `nlist3.last_val`
  * *ERROR*: `empty_nl.last_val`

## Why?

I wanted to see if it was possible.

## A few words

I only tested this in *Visual Studio Code* (VSCode), which uses *Pyright* (v. 1.1.351).

Just open `main.py` in VSCode and play with it. You might need to close VSCode and reopen it (or relaunch Pylance) from time to time as we're pushing the envelope here.

Note that this is just a *POC* (Proof Of Concept), so I only implemented a few operations and I omitted the runtime part, meaning `NList` contains no data and the methods have no body. Feel free to complete `Nlist`, if you want.

I only support 4-digit numbers, but my method scales *linearly* with the number of digits. Unfortunately, Pyright slows down too much as we go up and we hit the limits of the memoization scheme used. I'm confident there's *huge* room for (ad hoc) optimization on Pyright's side.

## Code Organization

* **`main.py`:** It shows `NList` in action.
* **`NList.py`:** It contains `NList` with some comments about why I did things in a certain way, about possible bugs in Pyright, doubts, and technical obstacles in general (e.g. why are there 4 `opsX.py` files instead of just one?)
* **`write_ops.py`:** It generates the files `opsX.py`. You don't need to run this unless you want to add more digits...
* **`misc.py`** It contains a few definitions.
