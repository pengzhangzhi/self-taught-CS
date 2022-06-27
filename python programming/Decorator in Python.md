## Decorator In python

Decorator is one of the most powerful techniques that let you to add  new functionalities to exsisting codes without gingantic modifications.  In addition, decorator can easily implement functions that requires writing a great many lines of code with conventional OOP. Less code means less bugs. This significantly save your life during  not only the devlopment but also maintaining process. However, many people have a hard time understand and master decorator due to its complex concepts. To this end, I am writing this tutorial to shed some lights on the following aspects of decorator.

- In which case you should use decorator (I will show them in couple of examples) ?
- How to use decorator?.

This tutorial is basically problem-guided and example-guided. You will master those complicated concepts when you trying so hard to figure out or solving a problem. Happy hacking.

## An glimpse of decorator

In python, we have the common sense: every thing is a object. This also includes function. If you have a function named f1, you can do the assignment: `f2 = f1`, which enables `f2` to have to the same functionalities as `f1`.  You can also pass a function as an argument to another function. Both works because it is a regular object.

Congraturations! You have mastered decorater. I will show you the simpler example.

There are function f1 and decorating function deco. 

```python
def f1():
    print("running f1")
```

```python
def deco(func):
    # deco takes a func and run it.
    print("decorating function")
    func()
```

The decoration is simple here. It addtionally print something before invoking a function. For real-world purpose, you can do more.

You can run the `deco`. 

```python
deco(f1)
```

Output:

```
decorating function
running f1
```

Everything is good. But the decorating is a little ugly. Althought f1 supports new features with the help of deco, I have to call `deco(f1)` to perfrom the functionalities instead of `f1()`, which forces me to replace all the code `f1()`  with `deco(f1)`. This is unacceptable amount of works. How to save our life in this case? More precisely, current problem is: invoking `f1`, which perfroms the same as `deco(f1)`.

Python support the feature with a syntax:  `@deco`. the usage is:

```python
@deco
def f1():
    print("running f1")
```

`@deco` is the same as `deco(f1)`.

As soon as decoring `f1` (executing these code), the above code outputs:

```
decorating function
running f1
```

The output shows an important information: **the decorating function `deco` is executed instantly as it decorates `@deco`.**

> A key feature of decorators is that they run right after the decorated function is defined. That is usually at import time, i.e. when a module is loaded by Python. 

If the `deco` do not invoke the funcion and intead return it. The output will be different: The func will not be executed for the reason we just explained.

```python
def deco(func):
    # deco takes a func and run it.
    print("decorating function")
    return func
```

output:

```python
decorating function
```

## Variable Scope

I am sure that most of you are familar with global variable and local variable. As a recap, global variable is defined in a python file that can be accessed anywhere in the file.  Local variable is only defined and accessiable in a function.

A exmaple,

```python
b = 1
def f3():
    print(b)
f3()
```

output: 1

But if you assign value to a global variable `b` in a function, this cause a error.

```python
b = 1
def f3():
    b += 1 # addition
    print(b)
f3()
```

output:

```python
UnboundLocalError: local variable 'b' referenced before assignment
```

This suggest: the global variable can only be read in a function.

> This is not a bug, but a design choice: Python does not require you to declare variables, but assumes that a variable assigned in the body of a function is local. This is much better than the behavior of JavaScript, which does not require variable declarations either, but if you do forget to declare that a variable is local (with var), you may clobber a global variable without knowing



If you really want to write a global variable, which I strongly do not recommend, here is what you do:

```python
b = 1
def f3():
    global b
    b += 1
    print(b)
f3()
```

You can declare that the variable is a global variable with syntax `global b`.

Here we want to introduce a new type of variable: free variable, shown in the following example.

```python
def f4():
    a = 2
    def f5():
        print(a)
    return f5
```

invoking f4 this way: `f4()()` , which actually does this: `f5()`. 

outputs:

`2`

But if you assign value to a:

 ```python
 def f4():
     a = 2
     def f5():
         a += 1
         print(a)
     return f5
 ```

this outputs the same error as before.

Because a is a free variable that can only be read but not write in a nested function.

If you really want to do this, add a declaration: `nonlocal a`.

```python
def f4():
    a = 2
    def f5():
        nonlocal a
        a += 1
        print(a)
    return f5
```

A exception is: if a variable is mutable, it can be mdofied without any declaration.

## An simple decorator

The following example is a decorator that clocks every invocation of the decorated function and prints the elapsed time, the arguments passed and the result of the call.

Here is the backbone of a decorator:

```python
def clock(func):
    def clocked(*args):
        # do whatever you want before the func is invoked.
        res = func()
        # do something after it is invoked.
        return res
    return clocked
```

What you going to do is to fill out these comments.

```python
import time
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        # do whatever you want before the func is invoked.
        res = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, res))

        # do something after it is invoked.
        return res
    return clocked

```

A test function:

```python
@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

```

```
factorial(10)
```

Outputs:

```python
[0.00000040s] factorial(1) -> 1
[0.00012430s] factorial(2) -> 2
[0.00014720s] factorial(3) -> 6
[0.00016500s] factorial(4) -> 24
[0.00018270s] factorial(5) -> 120
[0.00019920s] factorial(6) -> 720
[0.00021590s] factorial(7) -> 5040
[0.00023160s] factorial(8) -> 40320
[0.00025480s] factorial(9) -> 362880
[0.00027940s] factorial(10) -> 3628800

```

> This is the typical behavior of a decorator: it replaces the decorated function with a new function that accepts the same arguments and (usually) returns whatever the decorated function was supposed to return, while also doing some extra processing

There a few shortcomings of the decorator. 1) It does not support keyword arguments. 2) It masks the function name.

The first problem can be solved by passing a keyword arugments: `**kwargs`. For the second problem, let’s first figure out what does it mean?

if you print the function `factorial`, it outputs: 

```
<function __main__.clock.<locals>.clocked(*args)>
```

This suggest that the function is clocked instead of factorial. Because the decorator have masked its name when `@clock` is executed.

To tackle this, python standrad library provides an off-the-shelf decorator: `@functools.wraps()`.

 An improved version:

```python
import time
def clock(func):
    @functools.wraps(func) 
    def clocked(*args):
        t0 = time.perf_counter()
        # do whatever you want before the func is invoked.
        res = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, res))

        # do something after it is invoked.
        return res
    return clocked

```

now, printing fac torial, it output the correct assignments

```
<function __main__.factorial(n)>
```

## Decorators in the standard library

In this chapter, I will introduce two useful decorators.

###  `functools.lru_cache`

When your recursive function does repeatitive computations, which is a big waste. A solution is to memoirize previous calculated results and use them in the future interation.

For example, `fibonacci(n)` is a classical function that repeatitively calculate previous results.

```python
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

```

```
fibonacci(5)
```

outputs:

```
[0.00000030s] fibonacci(1) -> 1 #
[0.00000040s] fibonacci(0) -> 0
[0.00000030s] fibonacci(1) -> 1 # 
[0.00003680s] fibonacci(2) -> 1
[0.00011660s] fibonacci(3) -> 2
[0.00000020s] fibonacci(0) -> 0
[0.00000030s] fibonacci(1) -> 1 # 
[0.00002490s] fibonacci(2) -> 1
[0.00000020s] fibonacci(1) -> 1 #
[0.00000030s] fibonacci(0) -> 0
[0.00000020s] fibonacci(1) -> 1 #
[0.00002390s] fibonacci(2) -> 1
[0.00004790s] fibonacci(3) -> 2
[0.00009660s] fibonacci(4) -> 3
[0.00023760s] fibonacci(5) -> 5

```

It can be observed that the `fibonacci(1)` is calculated five times.

 To implment memoirization, you can use `@functools.lru_cache() `, which would automatically save previous results for futher computation.

```python
@functools.lru_cache() # 
@clock # 
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
```

This time,

`fibonacci(5)`

outputs,

```
[0.00000030s] fibonacci(1) -> 1
[0.00000030s] fibonacci(0) -> 0
[0.00001410s] fibonacci(2) -> 1
[0.00009380s] fibonacci(3) -> 2
[0.00000060s] fibonacci(4) -> 3
[0.00013050s] fibonacci(5) -> 5
```

Each interation is only calculated once.

Note that lru_cache can be tuned by two arguments

`functools.lru_cache(maxsize=128, typed=False)`

the `maxsize` specify the maximum records that can be memoirized.

if `typed` is ture,  the same value but with different type will be saved seperately. For example, 1 and 1.0 is different for the former is integer the later is floating number, they will be save for different value.

### `functools.singledispatch`

If you are familar with other programming languague like C++ and Java, there is a key feature you must know:  function overloading. 

It allows you wo write the same function (same name) to deal with different arguments. For example:

```cpp
void hello(int num){
	sout>>"int">>endl;
}
void hello(string str){
	sout>>"string">>endl;
}
```

The function `hello` can deal with two types of arugments and processes them respectively. This allows us to do different works for different types of input. However, when it comes to python, where data type do not exist, how to implement overloading?

A natural idea is using a chain of  if-else, which is not extensible for future devlopment. 

> The new functools.singledispatch decorator in Python 3.4 allows each module to contribute to the overall solution, and lets you easily provide a specialized function even for classes that you can’t edit. If you decorate a plain function with @singledispatch it becomes a generic function: a group of functions to perform the same operation in different ways, depending on the type of the first argument (This is what is meant by the term single-dispatch. If more arguments were used to select the specific functions, we’d have multiple-dispatch).

The following example shows the usage.  Decorating a function with @singledispatch. 



```python
from functools import singledispatch
@singledispatch
def hello(obj):
    print(repr(obj))

```

Then, register a sub-function that deals with a specific type. 

```python
@hello.register(str)
def _(string):
    print("string")

```

Test:

`hello(1)`

Output:

```
1
```

Because the argument is a integer, it is processed by the base function `hello`.

Test:

`hello('1')`

Output:

```
string

```

Indicating the argument ‘1’ is processed by the sub function `_(string)`.

## Parameterized Decorators

Have you notice that the decorator `functools.singledispatch` takes two arugments? A more professional term is parameterized decorator, that can customize the decorator to perform as you want.

To implement parameterized decorator, you have to write a nested three-layer function.

```python
def deco(activate=True):
    def warpper(func):
        def inner(*args,**kwargs):
            if activate:
                print("activated!")
            return func(*args,**kwargs)
        return inner
    return warpper
```

Notice that the `@deco()`, instead of `@deco`.

```python
@deco()
def f1():
    print("f1")
```

Test:

```python
f1()
```

output:

```
activated!
f1
```

## Conclusion

That it! That is pretty much all of this tutorial. I hope you have learned some. The takeaway is: decorator provides a method that enchance your existing code to do more works by decorating them instead of modifing them. BTW, make sure you are clear about the variable scope before using global variable or free variable. Misuse would introduce tranmendous disasters.

