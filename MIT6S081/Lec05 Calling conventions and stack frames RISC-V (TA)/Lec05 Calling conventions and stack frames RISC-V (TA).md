# Calling Convention

讨论C语言转换到汇编语言的过程，以及处理器相关的内容。

## RISC-V寄存器

![img](Lec05%20Calling%20conventions%20and%20stack%20frames%20RISC-V%20(TA).assets/image.png)

汇编指令直接在寄存器上执行。

表单中的第4列，Saver列，当我们在讨论寄存器的时候也非常重要。它有两个可能的值Caller，Callee。我经常混淆这两个值，因为它们只差一个字母。我发现最简单的记住它们的方法是：

- 

- Caller Saved寄存器在函数调用的时候不会保存

- Callee Saved寄存器在函数调用的时候会保存

这里的意思是，一个Caller Saved寄存器可能被其他函数重写。假设我们在函数a中调用函数b，任何被函数a使用的并且是Caller Saved寄存器，调用函数b可能重写这些寄存器。我认为一个比较好的例子就是Return address寄存器（注，保存的是函数返回的地址），你可以看到ra寄存器是Caller Saved，这一点很重要，它导致了当函数a调用函数b的时侯，b会重写Return address。所以基本上来说，任何一个Caller Saved寄存器，作为调用方的函数要小心可能的数据可能的变化；任何一个Callee Saved寄存器，作为被调用方的函数要小心寄存器的值不会相应的变化。我经常会弄混这两者的区别，然后会到这张表来回顾它们。

## Stack

Stack 是函数执行的区域。函数的局部变量，寄存器等等都存储在栈中。

每次调用一个函数，函数都会生成一个 stack frame为自己使用。

![img](https://files.gitbook.com/v0/b/gitbook-28427.appspot.com/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MM3Hk7Gv6ibvM2lxjCc%2F-MM4D2J3t3ajqkngxRPC%2Fimage.png?alt=media&token=1f78ffd1-9322-4666-85f2-8aa831ced49e)

stack的空间从上往下，从高地址往低地址扩展。因此每当分配空间时，都通过`stack pointer --`完成。

一个stack frame 通常包括：函数参数，保存的寄存器，本地变量。 其中不同函数这些内容的数量和大小不同。但对于一个stack frame有一些事是确定的：return address永远在stack frame顶部。 指向前一个stack frame 的位置也是固定的。

在stack frame中有两个重要的指针。 stack pointer(SP) 指向栈的底部，代表当前stack frame的位置。第二个是frame pointer（FP），指向栈的顶部。因为return address 和 指向前一个stack frame的指针 在stack frame中的位置都是确定的，因此可以直接通过FP获取他们的内容。

我们保存前一个Stack Frame的指针的原因是为了让我们能跳转回去。所以当前函数返回时，我们可以将前一个Frame Pointer存储到FP寄存器中。所以我们使用Frame Pointer来操纵我们的Stack Frames，并确保我们总是指向正确的函数。

当我们调用函数时，编译器首先生成汇编代码，然后由汇编代码生成stack frame。

一个汇编函数通常有三部分组成：

prologue

body

epllogue

如图黄色部分为prologue，它首先初始化stack 16字节的空间，然后把sp的位置储存到return address上。

![img](Lec05%20Calling%20conventions%20and%20stack%20frames%20RISC-V%20(TA).assets/image.png)

如下图黄色是epllogue，首先将stack pointer里的return address加载到return address Register上，然后删除16字节的stack frame 空间，最后退出。

![img](Lec05%20Calling%20conventions%20and%20stack%20frames%20RISC-V%20(TA).assets/image.png)

