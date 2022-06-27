# Interrupts

中断的场景很简单，就是硬件想要得到操作系统的关注。 比如说网卡收到了一个packet，网卡会生成一个中断；键盘按下了一个按键，键盘会产生一个中断。 和trap类似，当中断产生生，操作系统需要保存当前的工作，处理中断，恢复之前的工作。 如你所知道的那样，trap，page fault， and interrupts 有相同的机制。

但是中断有它特殊的地方：

1. asynchronous（异步）。当硬件产生中断时，interrupt handler与当前正在进行的进程在CPU上没有关联。而如果是系统调用，则发生在进程的context之下。
2. concurrency。  CPU和生成中断的设备是并行的。也就是说，网卡在独立处理接受packet并产生中断，同时，CPU也在运行处理它的任务。
3. program device。 外部设备需要被编程，而外部设备的代码被称为驱动。

在这个tutorial，我们会讨论两件事：

1. console中**“$”**符号是如何显示的。
2. 当你在键盘上按下ls，这些字符是怎样在console显示的。

------

## 硬件中断

中断是哪里产生的？我们今天主要关注于外部设备的中断，而不是定时器中断或软件中断。 外设中断来自于主板上的设备，如图是一个SiFive主板。

![img](Lec%2009%20Interrupts.assets/image.png)

你可以看到有很多的设备连接在上面。主板可以连接以太网卡，MicroUSB，MicroSD等，主板上的各种线路将外设和CPU连接在一起。

今天的重点是当设备产生中断时,CPU会发生什么，以及如何从设备中读写数据 

如下图是SiFive处理的文档，右侧是各种设备。 比如UART0。UART0会映射到内存地址的某处，而所有设备的物理地址都映射在0x800000之下。 类似于读写内存，通过对设备的地址进行load store，我们就能对设备进行编程。

![img](Lec%2009%20Interrupts.assets/image.png)

所有的设备都连接到处理器上，处理器通过platform level interrupt control (PLIC)来处理设备中断。

以下是PLIC的的结构图。

![img](Lec%2009%20Interrupts.assets/image.png)

图左上角告诉我们一共有53三个设备。他们的中断信号进入到PLIC后会被PLIC路由到右边其中之一的CPU。

如果所有CPU都在处理中断，那么PLIC会保留当前中断信号，直到有一个CPU可以处理中断。所以PLIC需要有一些内部数据来保存中断状态。

这里的流程是：

1. PLIC会通知CPU当前有一个待处理的中断。
2. 其中一个CPU会claim接受该中断，这样PLIC就会把中断路由到对应CPU上。
3. CPU处理完该中断后会通知PLIC。
4. PLIC不再保存该中断的状态信息。

## 设备驱动概述

管理设备的代码被称为驱动。 这篇tutorial我们主要介绍UART设备的驱动，代码在uart.c中。 

大部分驱动代码都分成bottom top两部分。

bottom部分通常是interrupt handler。当一个中断送到CPU，并且CPU设置接受这个中断，CPU就会调用相应的interrupt handler，它并不运行在特定进程的context中，仅仅处理中断。

top部分是用户进程或其他部分调用的接口。 对于UART来说，这里有read write接口，这些接口可以被更高级的代码调用，从而操控UART的驱动代码。

![img](Lec%2009%20Interrupts.assets/image.png)

驱动中有一些队列（或者称buffer），top部分的代码会从队列中读写数据，而interrupt handler （bottom部分）也会向队列中读写数据。 这里的队列可以将运行的设备和CPU解耦开。

接下来介绍如何对设备进行编程。 编程是通过memory mapped I/O 完成。 之前说过，每个设备都有自己对应的物理地址，我们只需要对这个物理地址进行读写操作就能对设备编程。

load store 指令实际上就是读写设备的控制寄存器。比如对网卡执行一个store指令，CPU会修改网卡的某个控制寄存器，进而导致网卡发送一个packet。 所以这里的读写操作不会控制内存，而是会操作设备。

## 在XV6中设置中断

接下来介绍$是如何在窗口上显示的。

对于$来说，设备会将字符传给UART的寄存器（TOP），UART在发送完字符后会产生一个中断(bottom interrupt handler)。在QEMU中，模拟的线路的另一端会有另外一个UART芯片，连接到虚拟的Console上，会进一步将$显示在console上.

而当你在键盘上按下ls,键盘连接到UART的输入线路,将按键字符通过串口线发送到另一端的UART芯片 将数据bit合并成byte,之后再产生一个中断,并告诉处理器这里有一个来自键盘的字符. 之后interrupt handler会处理来自UART的字符.

RISC-V有很多与中断相关的寄存器：

SIE （supervisor interrupt Enable）。 这个register有一个bit（E）专门针对UART的外部设备的中断，一个bit (S) 针对软件中断，一个bit （T） 针对定时器中断。

SSTATUS（supervisor status）。 这个Register有一个bit来打开和关闭中断，每一个CPU都有独立的SIE和SSTATUS。

SIP（supervisor Interrupt Pending）告诉CPU这是什么类型的中断。

SCAUSE 说明当前状态的原因是中断

STVEC 保存中断发生时现场的数据以便稍后恢复程序运行。



接下来我们看看xv6是怎么对这些寄存器编程，使得CPU能够接受中断。

首先是位于start.c的start函数。

![img](Lec%2009%20Interrupts.assets/image.png)

这里所有的中断都设置在supervisor mode，然后设置SIE寄存器来接受External，软件和定时器中断。

接下来看main函数是如何处理external中断的。

接下来我们看一下main函数中是如何处理External中断。

![img](Lec%2009%20Interrupts.assets/image.png)

第一个外设是console，最开始就被初始化了。

![img](Lec%2009%20Interrupts.assets/image.png)

这里首先初始化锁，然后调用uartinit，uartinit位于uart.c。 这个函数配置好UART。

![img](Lec%2009%20Interrupts.assets/image.png)

这里的流程是先关中断，设置波特率等，再开中断。

以上是uartint，运行完原则上uart就可以产生中断了。但我们还没有设置PLIC，因此中断不会被捕获到。

因此在最后，main函数会调用plicinit

![img](Lec%2009%20Interrupts.assets/image.png)

第一行代码，enable了UART的中断，实际上就是设置PLIC会接受哪些中断，进而将中断路由到CPU。第二行设置PLIC接受来自IO磁盘的中断。

plicinit由0号CPU运行，之后每个CPU都会调用plicinitthart来表明自己对哪种中断感兴趣。

![img](Lec%2009%20Interrupts.assets/image.png)

所以在plicinithart函数中，每个CPU的核都表明自己对来自于UART和VIRTIO的中断感兴趣。因为我们忽略中断的优先级，所以我们将优先级设置为0。

到目前为止，我们有了生成中断的外部设备，我们有了PLIC来传递中断到CPU，但CPU自己还没有设置好来处理中断。因为我们还没有设置到SSTATUS，

在main函数最后，程序调用了scheduler函数，

![img](Lec%2009%20Interrupts.assets/image.png)

scheduler主要是运行进程，但每次运行前都会执行intr_on函数打开中断。

intr_on只做一件事，设置寄存器SSTATUS，打开中断标志位。

![img](Lec%2009%20Interrupts.assets/image.png)

## UART驱动的top部分

接下来介绍的内容是，如何从Shell输出提示符$到console。

我们先看init.c的main函数。

这是系统启动后运行的第一个进程。

![img](Lec%2009%20Interrupts.assets/image.png)

首先main函数创建了一个代表console的设备。这里通过mknod操作创建了console设备。这是第一个打开的文件，文件描述符为0.

之后通过dup创建stdout和stderr，实际上就是通过复制文件描述符0得到了另外两个文件描述符1,2.最终文件描述符0,1,2都用来表示console。

shell程序首先打开文件描述符0,1,2，之后向文件描述符2打印提示符$.

![img](Lec%2009%20Interrupts.assets/image.png)

在printf.c中，代码调用了write sys call，在我们的例子中，fd对应的就是文件描述符2，c是字符$.

shell每输出一个字符，都会触发一个write sys call。这个write调用会调用sysfile.c里的sys_write函数，而sys_write又调用了filewrite，在filewrite函数中首先会判断文件描述符的类型。mknod生成的文件描述符属于设备（FD_DEVICE），而对于设备类型的文件描述符，我们会为这个特定的设备执行设备相应的write函数。因为我们现在的设备是Console，所以我们知道这里会调用console.c中的consolewrite函数。

![img](Lec%2009%20Interrupts.assets/image.png)

在consolewrite函数中，先通过either_copyin将字符拷入，之后调用uartputc函数，将字符写入uart设备。consolewrite是一个UART驱动的top部分。uart.c文件中的uartputc函数会实际的打印字符。

![img](Lec%2009%20Interrupts.assets/image.png)

uartputc内有一个buffer用来发送数据，大小为32个字符。同时有一个为consumer提供的读指针和为producer提供的写指针，来构造一个环形的buffer。

![img](Lec%2009%20Interrupts.assets/image.png)

![img](Lec%2009%20Interrupts.assets/image.png)

在这个例子中，shell是producer，所以需要调用uartpuc函数。 第一件事是判断是否buffer已经满了（read = write+1），如果满了，无法写入数据，就sleep当前进程，让出cpu资源。而我们这种情况下，肯定是不满的，字符会被送到buffer中，更新写指针，再调用uartart。

![img](Lec%2009%20Interrupts.assets/image.png)

uartstart会通知设备执行操作，首先检查设备是否空闲，如果空闲，我们会从buffer中读出数据，写入到THR（transmission holding register）发送寄存器，这里相当于告诉设备我有一个字节需要你来发送。一旦设备接受到数据，系统调用就会返回，用户的shell程序可以继续执行。

与此同时，uart会将数据送出，在某个时间点，我们会接受到中断，接下来就是bottom部分（interrupt handler） 的工作了。

## UART驱动的bottom部分

在我们向console输出字符时，如果发生中断，RISC-V会做什么？ 如果一切顺利（SSTATUS打开了中断，PLIC将中断路由给了一个available CPU，并且这个CPU设置了SIE register的E bit），那么会发生以下事情：

1. 首先会清除SIE寄存器的E bit，防止CPU被其他中断打扰
2. 设置SEPC 为当前PC
3. 保存当前的mode
4. 将mode设置为supervisor mode
5. 将PC设置为STVEC。（注，STVEC用来保存trap处理程序的地址，详见lec06）在XV6中，STVEC保存的要么是uservec或者kernelvec函数的地址，具体取决于发生中断时程序运行是在用户空间还是内核空间。在我们的例子中，Shell运行在用户空间，所以STVEC保存的是uservec函数的地址。而从之前的课程我们可以知道uservec函数会调用usertrap函数。所以最终，我们在usertrap函数中。我们这节课不会介绍trap过程中的拷贝，恢复过程，因为在之前的课程中已经详细的介绍过了。

在trap.c 中的usertrap函数，我们会处理 系统调用，page fault（像之前介绍的一样），也会处理中断。

![img](Lec%2009%20Interrupts.assets/image.png)

其中的devintr函数首先通过SSCAUSE判断中断是否来自外设，如果是再调用plic_claim来获取中断。

![img](Lec%2009%20Interrupts.assets/image.png)

plic_claim中，CPU会告知PLIC自己要处理中断， PLIC_SCLAIM会将中断信号返回，对于UART来说，返回的是10.

![img](Lec%2009%20Interrupts.assets/image.png)

获取到中断发生设备后，判断如果是UART中断就会调用uartintr函数。

![img](Lec%2009%20Interrupts.assets/image.png)

所以代码会直接运行到uartstart函数，这个函数会将Shell存储在buffer中的任意字符送出。实际上在提示符“$”之后，Shell还会输出一个空格字符，write系统调用可以在UART发送提示符“$”的同时，并发的将空格字符写入到buffer中。所以UART的发送中断触发时，可以发现在buffer中还有一个空格字符，之后会将这个空格字符送出。

通过buffer的方式，驱动的top和bottom部分就解耦开了。

驱动的top部分和用户进程交互，获取数据，产生中断。而bottom部分进行中断处理。

## Interrupt相关的并发

这一节将讨论与中断相关的并发，并发大大增加了中断编程的难度。这里的并发包括以下几个方面：


1. 设备与CPU并行。当UART向console发送字符时，CPU会返回执行shell，而shell可能会再执行一次系统调佣，向buffer写入其他字符，这些都在并行执行。这里的并行称为 producer-consumer 并行。
2. 中断会停止当前运行的程序。 在之前我们学过trap，用户代码可能会被随时打断。这问题不大，我们会在之后恢复。而中断可能会打断运行在kernel mode的代码。因此，这时要十分注意。kernel mode中可能会运行一些十分重要的代码，并且不能被打破。对于这类代码，运行时需要关闭中断，来保证这段代码的原子性。
3. 驱动的top和bottom是并行的。比如说shell在传输完”$“后，调用write sys call传输字符空格，代码会走到UART驱动的top部分把字符存进buffer里，同时在另一个CPU上会收到来自UART的中断，运行bottom部分的代码。而buffer对于所有CPU是共享的，所以这里我们需要加上锁保证buffer在一个时间内只被一个CPU操控。



今天只关注producer-consumder 并发。在驱动中的buffer有两个指针：read 和 write 指针。

如果read == write，说明buffer为空，

当字符被写入buffer中时，write指针++。buffer可以一直被写入。

但如果read = write +1说明buffer 满了。此时producer会停止运行，即sleep进程。

此时interrupt handler 也就是uartintr函数是consumer，每当有中断就会读取一个字符，再通过UART设备发送到外设上，并将读指针++。

直到 read == write时，不作任何操作。

## UART读取键盘输入

当处理键盘输入（来自键盘的中断），Shell 会调用read从键盘上读取字符。实际上是调用fileread函数，再调用console.c文件中的consoleread函数。

![img](Lec%2009%20Interrupts.assets/image.png)



shell变成consumer，keyboard是producer。当buffer为空时，shell会sleep。当你在键盘上按下l字符时，字符首先会被送到UART芯片上，存在buffer里，再产生中断，交给某个CPU来处理。之后歘devint函数，发现这是一个UART中断，通过 uartgetc获取相应的字符，再传给consoleintr函数。默认情况下，字符会通过consputc，输出到console上给用户查看。之后，字符被存放在buffer中。在遇到换行符的时候，唤醒之前sleep的进程，也就是Shell，再从buffer中将数据读出。+

![img](Lec%2009%20Interrupts.assets/image.png)

所以这里也是通过buffer将consumer和producer之间解耦，这样它们才能按照自己的速度，独立的并行运行。如果某一个运行的过快了，那么buffer要么是满的要么是空的，consumer和producer其中一个会sleep并等待另一个追上来。

## Interrupt的演进

1. 快设备，使用pooling（不停轮询设备）
2. 慢设备，使用中断

最后我想介绍一下Interrupt在最近几十年的演进。当Unix刚被开发出来的时候，Interrupt处理还是很快的。这使得硬件可以很简单，当外设有数据需要处理时，硬件可以中断CPU的执行，并让CPU处理硬件的数据。

而现在，中断相对处理器来说变慢了。从前面的介绍可以看出来这一点，需要很多步骤才能真正的处理中断数据。如果一个设备在高速的产生中断，处理器将会很难跟上。所以如果查看现在的设备，可以发现，现在的设备相比之前做了更多的工作。所以在产生中断之前，设备上会执行大量的操作，这样可以减轻CPU的处理负担。所以现在硬件变得更加复杂。

如果你有一个高性能的设备，例如你有一个千兆网卡，这个网卡收到了大量的小包，网卡每秒可以生成1.5Mpps，这意味着每一个微秒，CPU都需要处理一个中断，这就超过了CPU的处理能力。那么当网卡收到大量包，并且处理器不能处理这么多中断的时候该怎么办呢？

这里的解决方法就是使用polling。除了依赖Interrupt，CPU可以一直读取外设的控制寄存器，来检查是否有数据。对于UART来说，我们可以一直读取RHR寄存器，来检查是否有数据。现在，CPU不停的在轮询设备，直到设备有了数据。

这种方法浪费了CPU cycles，当我们在使用CPU不停的检查寄存器的内容时，我们并没有用CPU来运行任何程序。在我们之前的例子中，如果没有数据，内核会让Shell进程sleep，这样可以运行另一个进程。

所以，对于一个慢设备，你肯定不想一直轮询它来得到数据。我们想要在没有数据的时候切换出来运行一些其他程序。但是如果是一个快设备，那么Interrupt的overhead也会很高，那么我们在polling设备的时候，是经常能拿到数据的，这样可以节省进出中断的代价。

所以对于一个高性能的网卡，如果有大量的包要传入，那么应该用polling。对于一些精心设计的驱动，它们会在polling和Interrupt之间动态切换（注，也就是网卡的NAPI）。