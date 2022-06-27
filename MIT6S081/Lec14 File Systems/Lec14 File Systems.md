# File Systems

文件系统有以下特性：

1. User-friendly， 层级的路径名帮助用户组织目录中的文件。
2. 方便在用户之间和进程之间共享。
3. 持久化（persistence, durability)。文件内容不会在关机后丢失。

文件系统很有趣因为，

文件系统是对于硬件disk的抽象。

crash safety。 在文件操作过程中计算机崩溃了，文件数据依然存在。

文件系统需要决定如何在硬件磁盘上排布。 例如目录和文件，他们都需要以某种方式在磁盘中存在。当你重启计算机时，他们仍然存在。

因此，磁盘上有一些数据结构表示了文件系统的结构和内容。这是今天的重点内容。

性能优化。 在磁盘上读取数据需要话很长的时间，在这个时间内CPU能做数百万条指令。因此我们希望能够尽量避免读写磁盘。这里有一些提升性能的办法，

其中一些你还很熟悉。比如buffer，或者叫block cache。 同时这里有很多的并发，比如说你在查找文件路径名，这是一个多次交互的操作。你需要先找到文件结构，然后查找一个路径的文件名，之后查找下一个目录。这个过程中，我们希望另一个进程可以并行运行着。

除此之外，你会对文件系统感兴趣是因为这是接下来两个lab的内容。下一个lab完全关注在文件系统，下下个lab结合了虚拟内存和文件系统。即使是这周的lab，也会尝试让buffer cache可以支持更多的并发。所以这就是为什么文件系统是有趣的。

## File System Implementation

为了了解文件系统必须提供什么样的功能，我们先看看与文件系统有关的基础sys call。从这些sys call中，我们就能发现一些与文件系统有关的细节。

让我来假设一个场景，假设我们创建了文件 x/y，或者说在目录x中创建了文件y。我们会调用`open(“x/y”)`,而进程会对file discriptor调用write。

这里我们希望向文件写入 “abc” 三个字符。

![img](Lec14%20File%20Systems.assets/image.png)

这里我们可以发现一些信息：

- 路径名是可读的字符串
- write sys call没有使用offset作为参数，所以写入到文件的哪个位置是隐含在文件系统中的。文件系统必然保存了文件的offset。 因此你如果你再调用write sys call，新写入的数据会从第四个字节开始。

除此之外，还有一些其他的sys call。 比如说，创建链接，给同一个文件指定多个名字。你可以通过调用link，为文件“x/y”创建另一个名字 ”x/z“

![img](Lec14%20File%20Systems.assets/image.png)

所以文件系统中需要以某种方式唯一表明一个文件内容，追踪同一个文件的多个文件名。

我们还可能在文件打开时，删除或者更新文件的命名空间，例如用户可以通过unlink 系统调用来删除特定的文件名。如果此时相应的文件描述符还是打开的状态，那我们还可以向文件写数据，并且这也能正常工作。

所以，在文件内部，文件描述符必然与某个对象关联，而这个对象不依赖文件名。这样，即使文件名变化了，文件描述符仍然能够指向或者引用相同的文件对象。 所以操作系统内部对于文件有自己的描述形式，且这种描述形式于文件名无关。

除此之外，我还想提一点。文件系统的目的是实现上面描述的API，也即是典型的文件系统API。但是，这并不是唯一构建一个存储系统的方式。如果只是在磁盘上存储数据，你可以想出一个完全不同的API。举个例子，数据库也能持久化的存储数据，但是数据库就提供了一个与文件系统完全不一样的API。所以记住这一点很重要：还存在其他的方式能组织存储系统。我们这节课关注在文件系统，文件系统通常由操作系统提供，而数据库如果没有直接访问磁盘的权限的话，通常是在文件系统之上实现的（注，早期数据库通常直接基于磁盘构建自己的文件系统，因为早期操作系统自带的文件系统在性能上较差，且写入不是同步的，进而导致数据库的ACID不能保证。不过现代操作系统自带的文件系统已经足够好，所以现代的数据库大部分构建在操作系统自带的文件系统之上）。

> 学生提问：link增加了了对于文件的一个引用，unlink减少了一个引用？
>
> Frans教授：是的。我们稍后会介绍更多相关的内容。
>
> 学生提问：能介绍一下soft link和hard link吗？
>
> Frans教授：我今天不会讨论这些内容。但是你们将会在下一个File system lab中实现soft link。所以XV6本身实现了hard link，需要你们来实现soft link。
>
> 学生提问：link是对inode做操作，而不是对文件描述符做操作，对吧？
>
> Frans教授：是的，link是对inode做操作，我们接下来介绍这部分内容。

接下来介绍一下文件系统的结构。 文件系统究竟维护了什么样的结构来实现前面的API呢？

首先，最重要的是inode。这是代表一个文件的对象，不依赖文件名。实际上inode通过自身的编号来区分，编号是一个整数。所以文件系统内部通过一个数字而不是文件名来引用inode。同时，基于前面的介绍，inode对象需要有一个link count，统计有多少文件名link到这个文件，其次还有一个openfd count，打开了当前文件的file discriptor的数量。 一个文件只能在这两个count == 0的时候被删除。

基于之前的讨论，我们知道write，read 没有针对文件offset的参数，所以file discriptor必然悄悄维护了对于文件offset。

文件系统中核心的数据结构就是inode和file discriptor，前者在系统中使用，后者与用户进程交互。

文件系统十分复杂，以层次化的角度划分的话，可以这样理解：

最底层的是磁盘，也就是保存了实际数据的存储设备。正是这些设备提供了持久化存储。

在这之上的buffer cache。这些cache可以避免频繁读取磁盘，提高性能，这里我们将buffer cache存储在内存中。

为了保证持久性，我们还有一个logging层。

在logging层智商还有inode cache。主要是为了同步，synchronization。inode通常小于一个disk block，所以一般多个inode会打包保存在一个disk block中，为了向单个inode提供同步操作，xv6维护了inode cache。

- 再往上，就是文件名，和文件描述符操作。

![img](Lec14%20File%20Systems.assets/image.png)

不同的文件系统组织方式和每一层可能都略有不同，有的时候分层也没有那么严格，即使在XV6中分层也不是很严格，但是从概念上来说这里的结构对于理解文件系统还是有帮助的。实际上所有的文件系统都有组件对应这里不同的分层，例如buffer cache，logging，inode和路径名。

## HOW FILE SYSTEM USES DISK

接下来会介绍最底层的仓储设备。 实际上有很多种不同的储存设备，比如SSD和HDD。 这里有两个存储单元：

sectors: 磁盘驱动可以读写的最小单元，一般是512byte。

block：从操作系统，文件系统的角度定义的数据单元，一般来说是1024byte。所以在xv6中一个block对应两个sector

有的时候，人们也将磁盘上的sector称为block。所以这里的术语也不是很精确。

这些设备连接到电脑总线上，总线上也连接了CPU和内存。 一个文件系统运行在CPU中，内部的数据存储在内存上，同时也会以读写block的形式存储在SSD或HDD中。这里的接口还比较简单，包括read write。以block作为单位。

![img](Lec14%20File%20Systems.assets/image.png)

在内部，SSD和HDD工作方式完全不一样，但是对于硬件的抽象屏蔽了这些差异。磁盘驱动通常会使用一些标准的协议，例如PCIE，与磁盘交互。从上向下看磁盘驱动的接口，大部分的磁盘看起来都一样，你可以提供block编号，在驱动中通过写设备的控制寄存器，然后设备就会完成相应的工作。这是从一个文件系统的角度的描述。尽管不同的存储设备有着非常不一样的属性，从驱动的角度来看，你可以以大致相同的方式对它们进行编程。

有关存储设备我们就说这么多。

> 学生提问：对于read/write的接口，是不是提供了同步/异步的选项？
>
> Frans教授：你可以认为一个磁盘的驱动与console的驱动是基本一样的。驱动向设备发送一个命令表明开始读或者写，过了一会当设备完成了操作，会产生一个中断表明完成了相应的命令。但是因为磁盘本身比console复杂的多，所以磁盘的驱动也会比我们之前看过的console的驱动复杂的多。不过驱动中的代码结构还是类似的，也有bottom部分和top部分，中断和读写控制寄存器（注，详见lec09）。

从文件系统的角度看磁盘十分直观。因为对于磁盘就是一个block数据。

![img](Lec14%20File%20Systems.assets/image.png)

而文件系统的工作就是将所有数据结构以一种能够重启之后重新构建文件系统的方式，存放在磁盘上。虽然有不同方式，但xv6的实现特别简单，



通常来说，

block0要么，没有要么用作boot sector来启动操作系统。

block1成为super block。描述了文件系统的信息，包括多少个block。

log从block2到block32结束。一共三十个。

在block32到block45之间，xv6存储了inode。多个inode会被打包在一个block中，一个inode是64字节。

之后是bitmap block。记录数据block是否空闲。

之后就全是数据block，存储了文件的内容和目录的内容。

通常来说，bitmap blcok，inode blocks和log blocks被称为meta data，他们不包含实际数据，但是存储了帮助文件系统完成工作的原数据。

> 学生提问：boot block是不是包含了操作系统启动的代码？
>
> Frans教授：完全正确，它里面通常包含了足够启动操作系统的代码。之后再从文件系统中加载操作系统的更多内容。
>
> 学生提问：所以XV6是存储在虚拟磁盘上？
>
> Frans教授：在QEMU中，我们实际上走了捷径。QEMU中有个标志位-kernel，它指向了内核的镜像文件，QEMU会将这个镜像的内容加载到了物理内存的0x80000000。所以当我们使用QEMU时，我们不需要考虑boot sector。
>
> 学生提问：所以当你运行QEMU时，你就是将程序通过命令行传入，然后直接就运行传入的程序，然后就不需要从虚拟磁盘上读取数据了？
>
> Frans教授：完全正确。

假设inode是64字节，如果你想要读取inode10，那么你应该按照下面的公式去对应的block读取inode。

![img](Lec14%20File%20Systems.assets/image.png)

e17会在block33。只要有inode的编号，我们总是可以找到inode在磁盘上存储的位置。

> 学生回答：会是268*1024字节

是的，最大文件尺寸对应的是下面的公式。

![img](https://mit-public-courses-cn-translatio.gitbook.io/~/files/v0/b/gitbook-28427.appspot.com/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MRiqHd8klcdJiYeRvr7%2F-MRj6v153sUes_fzLr6w%2Fimage.png?alt=media&token=2ac667a8-c0bd-4c3c-a1c1-15f27ab33b5c)

可以算出这里就是268KB，这么点大小能存个什么呢？所以这是个很小的文件长度，实际的文件系统，文件最大的长度会大的多得多。那可以做一些什么来让文件系统支持大得多的文件呢？

e17会在block33。只要有inode的编号，我们总是可以找到inode在磁盘上存储的位置。

## INODE

接下来介绍INODE的数据结构。

- type字段，表明inode是文件还是目录。
- nlink，link count
- size，文件数据有多少个字节
- 12个block的编号，direct block number，指向构成文件的前12个block。如果文件只有2个字节，那么只会有一个block编号0，它包含的数字是磁盘上文件前2个字节的block的位置。

- 256个block编号，indirect block number，对应磁盘上的一个blcok，这256个block number包含了文件的数据。所以inode中block number 0到block number 11都是direct block number，而block number 12保存的indirect block number指向了另一个block。

![img](Lec14%20File%20Systems.assets/image.png)

基于上面的内容，XV6中文件最大的长度是多少呢？

> 学生回答：会是268*1024字节

是的，最大文件尺寸对应的是下面的公式。

![img](Lec14%20File%20Systems.assets/image.png)

可以算出这里就是268KB，这么点大小能存个什么呢？所以这是个很小的文件长度，实际的文件系统，文件最大的长度会大的多得多。那可以做一些什么来让文件系统支持大得多的文件呢？

> 学生回答：可以扩展inode中indirect部分吗？

是的，可以用类似page table的方式，构建一个双重indirect block number指向一个block，这个block中再包含了256个indirect block number，每一个又指向了包含256个block number的block。这样的话，最大的文件长度会大得多（注，是256*256*1K）。这里修改了inode的数据结构，你可以使用类似page table的树状结构，也可以按照B树或者其他更复杂的树结构实现。XV6这里极其简单，基本是按照最早的Uinx实现方式来的，不过你可以实现更复杂的结构。实际上，在接下来的File system lab中，你将会实现双重indirect block number来支持更大的文件。

> 学生提问：为什么每个block存储256个block编号？
>
> Frans教授：因为每个编号是4个字节。1024/4 = 256。这又带出了一个问题，如果block编号只是4个字节，磁盘最大能有多大？是的，2的32次方（注，4TB）。有些磁盘比这个数字要大，所以通常人们会使用比32bit更长的数字来表示block编号。

在下一个File system lab，你们需要将inode中的一个block number变成双重indirect block number，这个双重indirect block number将会指向一个包含了256个indirect block number的block，其中的每一个indirect block number再指向一个包含了256个block number的block，这样文件就可以大得多。

![img](Lec14%20File%20Systems.assets/image.png)

接下来，我们想要实现read系统调用。假设我们需要读取文件的第8000个字节，那么你该读取哪个block呢？从inode的数据结构中该如何计算呢？

> 学生回答：首先应该减去12个direct block的大小，然后再看在indirect block中的偏移量是多少。

对于8000，我们首先除以1024，也就是block的大小，得到大概是7。这意味着第7个block就包含了第8000个字节。所以直接在inode的direct block number中，就包含了第8000个字节的block。为了找到这个字节在第7个block的哪个位置，我们需要用8000对1024求余数，我猜结果是是832。所以为了读取文件的第8000个字节，文件系统查看inode，先用8000除以1024得到block number，然后再用8000对1024求余读取block中对应的字节。

总结一下，inode中的信息完全足够用来实现read/write系统调用，至少可以找到哪个disk block需要用来执行read/write系统调用。

接下来介绍目录。目录使得文件以一种层次化的方式展现，对用户十分友好。每一个目录都有一条entry，格式为：

1. 前2个字节包含目录中文件或者子目录的inode编号。
2. 接下来14个字节包含了子目录或者文件名。

所以每个entry总共是16个字节。

![img](Lec14%20File%20Systems.assets/image.png)

对于实现路径名查找，这里的信息就足够了。假设我们要查找路径名“/y/x”，我们该怎么做呢？

我们知道root inode是根目录，编号是inode 1，然后扫描inode 1的所有block，读取所有的direct block number和indirect block number，根据名字y找到y目录，假设编号为inode122，再在y中扫描找到x。

> 学生提问：有没有一些元数据表明当前的inode是目录而不是一个文件？
>
> Frans教授：有的，实际上是在inode中。inode中的type字段表明这是一个目录还是一个文件。如果你对一个类型是文件的inode进行查找，文件系统会返回错误。

很明现，这里的结构不是很有效。为了找到一个目录名，你需要线性扫描。实际的文件系统会使用更复杂的数据结构来使得查找更快，当然这又是设计数据结构的问题，而不是设计操作系统的问题。你可以使用你喜欢的数据结构并提升性能。出于简单和更容易解释的目的，XV6使用了这里这种非常简单的数据结构。

## File System 工作示例

xv6启动时，会通过makefs创建一个全新的镜像，包含了我们在指令系统传入的一些文件。 xv6总是会打印文件系统的一些信息。包括了：

- boot block
- super block
- 30个log block
- 13个inode block
- 1个bitmap block
- 之后是954个data block

这是一个袖珍的文件系统，非常非常小。只有一千个block。总容量为1000*1024=1000B =1KB 

在LAB中，我们会去支持更大的文件系统。

我还稍微修改了一下XV6，使得任何时候写入block都会打印出block的编号。我们从console的输出可以看出，在XV6启动过程中，会有一些对于文件系统的调用，并写入了block 33，45，32。

我们以echo “hi”>x为例，看看哪些block被写入了。

![img](Lec14%20File%20Systems.assets/image.png)

如图，这里可以分为三个阶段。让我们一个阶段一个阶段的看echo的执行过程，并理解对于文件系统发生了什么。相比看代码，这里直接看磁盘的分布图更方便：

![img](https://gblobscdn.gitbook.com/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MRhzbAZwhuzp63wWdRE%2F-MRielGcbrHOzPCrxHcO%2Fimage.png?alt=media&token=f685aafe-7c22-4965-9936-d811b090023d)

**第一阶段是创建文件。**

写入33，这是inode block，因为这里创建了一个新的文件，势必要创建inode block。

block 46指的是第一个data block代表根目录，这里我们向根目录创建了一个新的entry，文件名为x，inode在block33.

之后write32，是更新根目录的inode，因为这里我们在根目录中创建了新文件。

最后又有一次write 33，我在稍后会介绍这次写入的内容，这里我们再次更新了文件x的inode， 尽管我们又还没有写入任何数据。

**第二阶段是写入hi。**

这里首先修改blcok 45，这是bitmap。意味着扫描整个bitmap找到一个还没有使用过的data block，更新它的flag = 1，表示已经被使用了。

可以猜到，这个block应该是595.

之后写了两次block 595，应该是character by character，先写h，再写i。

最后的write 33是更新文件x对应的inode中的size字段，因为现在文件x中有了两个字符。

**第三阶段是写入“\n”**。

与之前相同。

> 学生提问：block 595看起来在磁盘中很靠后了，是因为前面的block已经被系统内核占用了吗？
>
> Frans教授：我们可以看前面makefs指令，makefs存了很多文件在磁盘镜像中，这些都发生在创建文件x之前，所以磁盘中很大一部分已经被这些文件填满了。
>
> 学生提问：第二阶段最后的write 33是否会将block 595与文件x的inode关联起来？
>
> Frans教授：会的。这里的write 33会发生几件事情：首先inode的size字段会更新；第一个direct block number会更新。这两个信息都会通过write 33一次更新到磁盘上的inode中。

以上就是磁盘中文件系统的组织结构的核心，希望你们都能理解背后的原理。

## XV6创建inode代码展示

接下来我们通过查看xv6中的代码，更进一步的了解文件系统。先来看看如何分配inode。在sysfile.c中，分配inode发生在sys_open中。

这个函数负责创建文件。

![img](Lec14%20File%20Systems.assets/image.png)

在sys_open中会调用create函数，其中传入path，和type。

create会解析路径名，找到最后一个目录，查看文件是否存在，如果存在会返回错误。

之后create函数会调用ialloc函数，分配inode。

![img](Lec14%20File%20Systems.assets/image.png)

这里就是简单的变量找到free inode，标记后再分配。

以上就是ialloc函数，与XV6中的大部分函数一样，它很简单，但是又不是很高效。它会遍历所有可能的inode编号，找到inode所在的block，再看位于block中的inode数据的type字段。如果这是一个空闲的inode，那么将其type字段设置为文件，这会将inode标记为已被分配。函数中的log_write就是我们之前看到在console中有关写block的输出。这里的log_write是我们看到的整个输出的第一个。

以上就是第一次写磁盘涉及到的函数调用。如果多个进程同时调用create函数会发生什么？对于一个多核计算机，两个进程可能同时调用ialloc，进而调用bread（bufferread）函数，所以需要有些机制确保两个进程不会相互影响。

先看看bread代码

![img](Lec14%20File%20Systems.assets/image.png)

bread调用了bget从buffer cache中找到blcok的缓存。来看看bget函数。

![img](Lec14%20File%20Systems.assets/image.png)

这里遍历了一个链表，找cache。 如果找到，则refcnt++,并且把所有cache部分的锁去掉，对找到的cache block单独加上sleep lock。

如果有多个进程同时调用bget，这里用锁来保证了并发的正确性。因为当一个进程获取到了cache lock，其他进程就无法扫描进程了。

当第一个进程获取到了sleep lock后函数返回，而另一个进程成功获取cache lock走到acquiresleep，会在acquiresleep中等待第一个进程释放锁。

> 学生提问：当一个block cache的refcnt不为0时，可以更新block cache吗？因为释放锁之后，可能会修改block cache。
>
> Frans教授：这里我想说几点；首先XV6中对bcache做任何修改的话，都必须持有bcache的锁；其次对block 33的cache做任何修改你需要持有block 33的sleep lock。所以在任何时候，release(&bcache.lock)之后，b->refcnt都大于0。block的cache只会在refcnt为0的时候才会被驱逐，任何时候refcnt大于0都不会驱逐block cache。所以当b->refcnt大于0的时候，block cache本身不会被buffer cache修改。这里的第二个锁，也就是block cache的sleep lock，是用来保护block cache的内容的。它确保了任何时候只有一个进程可以读写block cache。

当一个进程结束了对cache block的使用，会调用brelse函数，释放锁，并且把它加入到一个LIST中，为了LRU算法，更新cache。

![img](Lec14%20File%20Systems.assets/image.png)

## Sleep Lock

sleeplock 与之前的spinlock 有所不同，具体来说sleep lock为了适应文件系统，做了一些更加精细化的改进。

我们先来看看acquiresleep函数，

![img](Lec14%20File%20Systems.assets/image.png)

它首先获取一个spin lock，如果spin lock获取成功，它就sleep。把CPU资源释放掉。

这样做有一些好处：

1. 获取到lock的同时，我们能够出让CPU资源，因为文件操作通常来说耗时很长，我们不希望白白浪费这些资源。
2. 其次是，spinlock限制很多，比如说加锁时必须要关中断，而在文件系统中，可能同时有另一个CPU发出中断信号希望读取文件数据。

因此这里我们使用sleep lock，这使得我们可以在加锁时使用中断，并且sleep线程，提高了CPU的利用率。

接下来看看brelse函数，

![img](Lec14%20File%20Systems.assets/image.png)

brelse首先释放sleep lock，之后获取bcache的锁，减少block cache的引用计数，表明一个进程不再对cache block感兴趣。最后如果refcnt == 0， 则它会修改buffer cache的linked-list,将block cache移到linked-list头部。这是为了支持LRU算法。

当我们在cache 中找不到想要的block，我们会从disk中找，并同时移除掉linked-list头部的cache block，将空间腾出来给想要的block。

这就是block cache的介绍。这里有几点需要注意：

1. block cache只能有一份。
2. sleep lock可以在IO操作中使用。
3. LRU作为cache替换的策略
4. buffer中有两层锁，一层buffer锁（保护buffer中内部数据），一层cache block锁（保护单个cache block）。

总结一下：

今天介绍了文件系统这样一个基于磁盘抽象出来的数据结构。

block cache的实现，为了提高读写磁盘的效率。

下节课我将会介绍crash safety，这是文件系统设计中非常棒的一部分。我们将会在crash safety讲两节课。下节课我们会看到基于log实现的crash safety机制，下下节课我们会看到Linux的ext3是如何实现的logging，这种方式要快得多。

