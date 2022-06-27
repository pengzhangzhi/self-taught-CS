# Page Fault

page fault就是物理地址报的错误（比如访问了不该访问的地址）。

事实上我们可以利用好page fault 来实现一系列虚拟内存功能，从而优化操作系统的性能和效率。

- lazy allocation
- copy-on-write fork
- demand paging
- memory mapped files

![img](Page%20Fault.assets/image.png)

为了提高效率，几乎所有操作系统都实现了上述功能。 而在xv6中，为了简便，没有这些功能。 在xv6中一旦触发page fault，会导致进程会被杀死。这是最直接的解决方案。

值得强调的是，在操作系统的实现上，我们有很多大手大脚的行为，比如直接分配一大块的内存地址。而现实情况是，用户进程可能只能使用一小部分内存，这会导致很大的浪费。 如果这样的现象在操作系统中经常出现，就很容易导致OOM（out of memory）。 而page fault提供了很多灵活的功能让我们优化这类问题。

在具体进入到page fault之前，我们先来回忆一下virtual memory。virtual memory 有两个主要优点：

1. 隔离性： 每个应用程序都有属于它们自己的空间，并且它们无法知道其他程序的内存地址。

2. 抽象：处理器和所有的指令都可以使用虚拟地址，而内核会完成虚拟地址和物理地址的转换。

   当然其中有几个特殊的地方： trampoline page，它使得内核将一个物理page映射到多个虚拟地址（多个用户空间中）。 即多个用户共享一个trampoline page。

目前为止，我们介绍的虚拟地址都还是静态的。一旦 page table 被设置好就不会改变。而今天结束的page fault就能实现一些动态的变动提高内核的灵活性。

在这之前，我们需要思考，当出现page fault，内核需要知道什么信息才能响应page fault？

1. 出错的虚拟地址： 触发 page fault的源。当一个地址出错，xv6 kernel会打印出错的地址，并且这个地址会被保存到STVAL Register。当出错发生，trap机制会被触发，同时STVAL会存储出错的地址。
2. 出错的原因：对于不同的原因（load/ read 触发的page fault），应该有不同的解决方案。在RISC-V中，SCAUSE （Supervisior Cause）register保存了trap机制中进入到supervisor mode的原因。比如，13表示是因为load引起的page fault；15表示是因为store引起的page fault；12表示是因为指令执行引起的page fault。所以第二个信息存在SCAUSE寄存器中，其中总共有3个类型的原因与page fault相关，分别是读、写和指令。ECALL进入到supervisor mode对应的是8，这是我们在上节课中应该看到的SCAUSE值。基本上来说，page fault和其他的异常使用与系统调用相同的trap机制（注，详见lec06）来从用户空间切换到内核空间。如果是因为page fault触发的trap机制并且进入到内核空间，STVAL寄存器和SCAUSE寄存器都会有相应的值。

![img](Page%20Fault.assets/image.png)

3. 引发出错的指令：知道出错的指令，就能在修复后继续执行。作为trap的一部分，这个地址存在SEPC（Supervisor Exception Program Counter），并同时会被储存到trapframe->epc.(注，详见lec06中。)

## 8.2 Lazy page allocation

sbrk是内存allocation的方法。 它使得用户程序能够扩大自己的heap。当一个应用程序启动时，sbrk指向heap最底端，即stack最顶端。这个位置通过p->sz表示。

![img](Page%20Fault.assets/image.png)

sbrk它接受一个参数，代表申请page的数量，按照这个大小扩展heap的上边界。

![img](Page%20Fault.assets/image.png)

这意味着，当sbrk被调用时，kernel会分配一些物理地址，并把他们映射到对应的虚拟地址上，最后把他们的内容初始化为0. 同样你也能传入一个负数给sbrk，从而减少heap的地址空间。

在xv6中，allocation的默认方式是eager allocation。这意味着，你申请了多少的地址就会直接分配对应大小的物理地址。这不好吗？

通常来说，用户地址会申请多于自己需要的内存。这意味着，申请的地址大部分不会被使用到。从而造成很严重的浪费。

为了节约这点空间，我们可以利用lazy allocation。 lazy allocation的核心思想非常简单。当sbrk被调用申请地址时，它仅仅提升p->sz，增加n（申请的地址大小），而不分配任何物理地址。 之后在某个时间点，用户程序使用到新申请的地址，这时候会触发 page fault，因为我们还没有分配真正的物理地址，也没有映射上去。 因此，当我们在使用一个大于旧的p->sz且小于新的p->sz的地址，我们希望内核能够分配一块物理地址给他，因为这块地址真的在被使用。 分配完成后，我们就能重新执行指令了。

## Zero Fill On Demand

上面介绍的lazy allocation的基本思想是：用时再分配。 这个简单的思想基本上贯穿了这一章的内容。接下来介绍的 zero fill on demand也是如此。

在用户程序的地址空间中，有三个区域，Text，data，and BSS. 其中BSS包含了未初始化或初始化为0的全局或静态变量。 如果BSS中有一个很大的矩阵，初始化为0，全部储存它们是一笔很大的花费，而且矩阵中不是所有内容都会被用到。

因此，我们可以使用一个物理地址，让它的值为0，并且让BSS区域内所有的虚拟地址都映射到这个物理地址。这样使得我们只花了一个物理地址就储存了BSS中所有的内容。 当BSS中有变量被修改时，就要引发page fault，从而为它分配一块物理地址，将映射关系设置为新的物理地址。

![img](Page%20Fault.assets/image.png)

其中有很多细节需要注意。

首先，我们不能允许对这个物理地址执行写操作，因为所有的虚拟地址page都得是0. 因此这里对应的PTE是只读的。

当程序尝试写BSS中的一个page，page fault会触发，内核会申请一块新的物理地址，将其内容设置为0，并且更新mapping的关系，PTE要设置为可读可写。

之后重新执行指令。

> 学生提问：但是因为每次都会触发一个page fault，update和write会变得更慢吧？
>
> Frans教授：是的，这是个很好的观点，所以这里是实际上我们将一些操作推迟到了page fault再去执行。并且我们期望并不是所有的page都被使用了。如果一个page是4096字节，我们只需要对每4096个字节消耗一次page fault即可。但是这里是个好的观点，我们的确增加了一些由page fault带来的代价。
>
> page fault的代价是多少呢？我们该如何看待它？这是一个与store指令相当的代价，还是说代价要高的多？
>
> > 学生回答：代价要高的多。store指令可能需要消耗一些时间来访问RAM，但是page fault需要走到内核。

## Copy On Write Fork

copy-on-write fork，有时也称为COW fork。和之前的思想一样，当写的时候再复制。

当你在shell中运行一个指令时，它会创建一个新的子进程来执行这个指令。 问题在于，这个子进程会完全拷贝父进程中的内容，而子进程调用exec执行指令时就会丢弃这些内容。这看起来有些浪费。 拷贝了了又释放，干脆就不要拷贝。

copy on write fork的方法是，共享父进程中的物理内存page。在创建子进程中，直接设置子进程的PTE指向父进程对应的物理地址。

![img](Page%20Fault.assets/image.png)

 在这里需要特别小心，为了保证进程之间的隔离性，PTE 标志位都设置为已读。

当修改共享内存的内容时，会触发page fault。 因为我们对一个只读的page进程写操作。 得到page fault后，我们首先申请物理page，然后将出错的物理page的内容复制到新的物理地址，并且将建立对新分配物理page的映射。这时，新分配的物理地址只对当前进程可见，因此我们可以把这条PTE设置为可读写。重新执行之前的指令。 实际上，由于当前进程已经有了一块新的物理地址，之前的PTE也只对一个进程可见了，因此也可以设置对应的PTE为可读写。

在这种情况下，引发page fault的原因是对一个只读的地址进行写操作。内核如何分辨这是 copy-on-write fork？这很重要，因为在其他情况下，应用程序也会执行这样的操作。我们需要识别出这是copy-on-write fork，从而对它进行一些特定的操作。

在PTE中，有两位RSW，就会标示这一点。

当内核在管理这些page table时，对于copy-on-write相关的page，内核可以设置相应的bit位，这样当发生page fault时，我们可以发现如果copy-on-write bit位设置了，我们就可以执行相应的操作了。否则的话，比如说lazy allocation，我们就做一些其他的处理操作。

在copy-on-write lab中，你们会使用RSW在PTE中设置一个copy-on-write标志位。

还有一个细节，当用户程序退出时，我们能否立即清空其对应的内存？不可以，因为它的子进程很有可能在共享它的物理page。

因此，我们需要对每一个物理page进行计数，当我们释放虚拟page时，我们将物理page的引用数减一，如果物理page的引用数为0，说明此时没有虚拟地址和它映射，可以直接清空。所以在copy-on-write lab中，你们需要引入一些额外的数据结构或者元数据信息来完成引用计数。

## Demand Paging

在加载程序内存（text，data）时，使用lazy allocation的方式，当用到的时候再真正分配物理地址。 因此对于exec来说，我们只需要在虚拟地址中为text，data分配好地址段，但是相应的PTE不对应任何物理地址，valid bit位设置为0.

当用户使用到程序里的内容时，就会发生page fault。此时我们将程序文件读取到内存的物理地址中，之后再建立对应的映射，重新执行指令。

如果程序的大小大于物理地址的容量，此时内存会发生OOM,此时你需要evict page，撤回page。 比如说将部分写入到内存的page写会到文件系统中。释放一些空间。再重新执行指令。

那么，什么样的page可以被撤回？用什么样的策略撤回page？

按照LRU（Least Recently Used). 此外，page会被分成dirty page 和 non-dirty page。 dirty page是曾经被写过的page，而non-dirty page只被读过。

现实中会选择non-dirty page。如果non-dirty page出现在page table1中，你可以将内存page中的内容写到文件中，之后将相应的PTE标记为non-valid，这就完成了所有的工作。之后你可以在另一个page table重复使用这个page。所以通常来说这里优先会选择non-dirty page来撤回。

在PTE中，bit 7标示着dirty bit。类似的，还有一个Access bit，任何时候一个page被读或者被写了，这个Access bit会被设置，用来实现LRU。

## Memory Mapped Files

我们希望加载文件到内存中，从而通过load，store等指令操控文件。为了实现这个功能，操作系统提供一个sys call mmap，它接受virtual address（VA），length（len），protection，flags，file discriptor，offset。它的工作是从file discriptor对应的文件的偏移量开始，映射len长度的数据到虚拟地址VA，同时加上一些保护，只读或读写。当然，我们不希望是以eager 的方式，而是先保存mmap映射的文件信息，这些信息（file discriptor，offset）保存在VMA（virtual memory area）结构体中，告诉我们文件在哪。当访问到这些文件内容时，系统会因为在内存中无法找到而报page fault。这时只需要从磁盘把这些文件内容读入到内存中即可。



## 总结

我们首先详细看了一下page table是如何工作的，之后我们详细看了一下trap是如何工作的。而page fault结合了这两部分的内容，可以用来实现非常强大且优雅的虚拟内存功能。我们这节课介绍的内容，只是操作系统里面基于page fault功能的子集。一个典型的操作系统实现了今天讨论的所有内容，如果你查看Linux，它包含了所有的内容，以及许多其他有趣的功能。今天的内容希望能给让你们理解，一旦你可以在page fault handler中动态的更新page table，虚拟内存将会变得有多强大。