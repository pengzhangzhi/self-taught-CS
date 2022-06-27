# File System Crash

今天讨论的是file system crash，我们关注的重点是当crash或者power failure发生导致在磁盘上的文件系统处于不一致或不正确的状态的问题。比如说，一个data block 属于两个文件，或者一个inode被分配给两个不同的文件。这种数据不一致的问题十分严重，绝对不能允许在我们的操作系统中出现。

这个问题可能出现的场景可能是这样，当你在运行make指令时，make与文件系统会有频繁的交互，并读写文件，但是在make执行的过程中断电了，可能是你的笔记本电脑没电了，也可能就是停电了，之后电力恢复之后，你重启电脑并运行ls指令，你会期望你的文件系统仍然在一个好的可用的状态。

![img](Lec15%20File%20System%20Crash.assets/image.png)



这里我们关心两种crash

1. power failure
2. kernel panic，大部分内核会panic，可能由内核bug引起。

我们希望，即使是内核出现panic也能在恢复后，文件系统能重新使用。

这里指的不是crash后，数据丢失或文件系统损坏。crash主要带来的是数据不一致的问题。突然发生的crash会导致我们丢失了对文件的数据的最终。可能操作系统认为这是一块已经被读写过的block，而它其实还没有被使用。这会造成浪费。

我们今天介绍的解决方案是logging。这是一种在数据库中被广泛使用的方法。当OS对文件系统进行操作，我们把这些操作记录在loging block中，等待一定数量的操作完成后，我们统一commit到真正的block上。如果crash发生在commit之前，当我们恢复后，就能重新commit这些操作。而如果commit发生在记录之前，我们就会放弃这些操作。

我们先来理解一下crash发生的场景。

类似于创建文件，写文件这样的系统操作，包含了多个步骤的写磁盘操作。我们上节课看过了如何创建一个文件，这里的顺序是：

- 分配inode，在磁盘上将inode标记为已分配
- 更新新文件的data block

如果在这两个步骤之间，操作系统crash了。这时可能会使得文件系统的属性被破坏。这里的属性是指，每一个磁盘block要么是空闲的，要么是只分配给了一个文件。即使故障出现在磁盘操作的过程中，我们期望这个属性仍然能够保持。如果这个属性被破坏了，那么重启系统之后程序可能会运行出错，比如：

- 

  操作系统可能又立刻crash了，因为文件系统中的一些数据结构现在可能处于一种文件系统无法处理的状态。

- 

  或者，更可能的是操作系统没有crash，但是数据丢失了或者读写了错误的数据。

![img](Lec15%20File%20System%20Crash.assets/image.png)

我们将会看一些例子来更好的理解出错的场景，但是基本上来说这就是我们需要担心的一些风险。我不知道你们有没有人在日常使用计算机时经历过这些问题，比如说在电力故障之后，你重启电脑或者手机，然后电脑手机就不能用了，这里的一个原因就是文件系统并没有恢复过来。

我们介绍过磁盘数据的排布方式，

![img](Lec15%20File%20System%20Crash.assets/image.png)

super block后是log block，之后是inode block，代表每个文件或目录。然后是bitmap，标记哪些data block是空闲的，最后是data block，记录了真正的文件数据。

在创建文件中，OS和文件系统有很多的交互：

1. 分配inode
2. 初始化inode
3. 更新父目录的inode（因为在当前目录下新增了文件），是将文件x的inode编号写入到x所在目录的inode的data block中
4. 更新root inode，因为文件x创建在根目录，所以需要更新根目录的inode的size字段，以包含这里新创建的文件x
5. 更新文件的inode



现在我们想知道，哪里可能出错。假设我们在下面这个位置出现了电力故障或者内核崩溃。

![img](Lec15%20File%20System%20Crash.assets/image.png)

在出现电力故障之后，因为内存数据保存在RAM中，所有的内存数据都丢失了。所有的进程数据，所有的文件描述符，内存中所有的缓存都没有了，因为内存数据不是持久化的。我们唯一剩下的就是磁盘上的数据，因为磁盘的介质是持久化的，所以只有磁盘上的数据能够在电力故障之后存活。基于这些事实，如果我们在上面的位置出现故障，并且没有额外的机制，没有logging，会有多糟糕呢？我们这里会有什么风险？

在这个位置，我们先写了block 33表明inode已被使用，之后出现了电力故障，然后计算机又重启了。这时，我们丢失了刚刚分配给文件x的inode。这个inode虽然被标记为已被分配，但是它并没有放到任何目录中，所以也就没有出现在任何目录中，因此我们也就没办法删除这个inode。所以在这个位置发生电力故障会导致我们丢失inode。

你或许会认为，我们应该改一改代码，将写block的顺序调整一下，这样就不会丢失inode了。所以我们可以先写block 46来更新目录内容，之后再写block 32来更新目录的size字段，最后再将block 33中的inode标记为已被分配。

![img](Lec15%20File%20System%20Crash.assets/image.png)

这里的效果是一样的，只是顺序略有不同。并且这样我们应该可以避免丢失inode的问题。那么问题来了，这里可以工作吗？我们应该问问自己，如果在下面的位置发生了电力故障会怎样？

![img](Lec15%20File%20System%20Crash.assets/image.png)

在这个位置，目录被更新了，但是还没有在磁盘上分配inode（有个问题，如果inode没分配的话，write 46的时候写的是啥）。电力故障之后机器重启，文件系统会是一个什么状态？或者说，如果我们读取根目录下的文件x，会发生什么，因为现在在根目录的data block已经有了文件x的记录？

是的，我们会读取一个未被分配的inode，因为inode在crash之前还未被标记成被分配。更糟糕的是，如果inode之后被分配给一个不同的文件，这样会导致有两个应该完全不同的文件共享了同一个inode。如果这两个文件分别属于用户1和用户2，那么用户1就可以读到用户2的文件了。所以上面的解决方案也不好。

所以调整写磁盘的顺序并不能彻底解决我们的问题，我们只是从一个问题换到了一个新的问题。

让我们再看一个例子，这个例子中会向文件x写入“hi”（注，也就是14.5介绍的第二个部分）

![img](Lec15%20File%20System%20Crash.assets/image.png)

一旦成功的创建了文件x，之后会调用write系统调用，我们在上节课看到了write系统调用也执行了多个写磁盘的操作。

- 

  首先会从bitmap block，也就是block 45中，分配data block，通过从bitmap中分配一个bit，来表明一个data block已被分配。

- 

  上一步分配的data block是block 595，这里将字符“h”写入到block 595。

- 

  将字符“i”写入到block 595。

- 

  最后更新文件夹x的inode来更新size字段。

这里我们也可以问自己一个问题，我们在下面的位置crash了会怎样？

![img](Lec15%20File%20System%20Crash.assets/image.png)

这里我们从bitmap block中分配了一个data block，但是又还没有更新到文件x的inode中。当我们重启之后，磁盘处于一个特殊的状态，这里的风险是什么？是的，我们这里丢失了data block，因为这个data block被分配了，但是却没有出现在任何文件中，因为它还没有被记录在任何inode中。

你或许会想，是因为这里的顺序不对才会导致丢失data block的问题。我们应该先写block 33来更新inode来包含data block 595（同样的问题，这个时候data block都还没有分配怎么知道是595），之后才通过写block 45将data block 595标记为已被分配。

![img](Lec15%20File%20System%20Crash.assets/image.png)

所以，为了避免丢失data block，我们将写block的顺序改成这样。现在我们考虑一下，如果故障发生在这两个操作中间会怎样？

![img](Lec15%20File%20System%20Crash.assets/image.png)

这时inode会认为data block 595属于文件x，但是在磁盘上它还被标记为未被分配的。之后如果另一个文件被创建了，block 595可能会被另一个文件所使用。所以现在两个文件都会在自己的inode中记录block 595。如果两个文件属于两个用户，那么两个用户就可以读写彼此的数据了。很明显，我们不想这样，文件系统应该确保每一个data block要么属于且只属于一个文件，要么是空闲的。所以这里的修改会导致磁盘block在多个文件之间共享的安全问题，这明显是错误的。

所以这里的问题并不在于操作的顺序，而在于我们这里有多个写磁盘的操作，这些操作必须作为一个原子操作出现在磁盘上。

这里的关键是，我们希望创建文件（涉及到多个磁盘读写操作）是一个原子操作，即要么发生，要么不发生。如果在某个时间后方式crash，我们能够补救，就使得该操作发生，反之就放弃该操作。而logging就是实现该操作的一种方式。

## File system logging

今天介绍的logging技术，有两个非常好的属性

1. 原子性

2. 快速恢复。 当crash发生后，我们可以放弃也可以选择恢复（效率最高）。 在重启之后，我们不需要做大量的工作来修复文件系统，只需要非常小的工作量。这里的快速是相比另一个解决方案来说，在另一个解决方案中，你可能需要读取文件系统的所有block，读取inode，bitmap block，并检查文件系统是否还在一个正确的状态，再来修复。而logging可以有快速恢复的属性。

- 最后，原则上来说，它可以非常的高效，尽管我们在XV6中看到的实现不是很高效。

我们会在下节课看一下，如何构建一个logging系统，并同时具有原子性的系统调用，快速恢复和高性能，而今天，我们只会关注前两点。

![img](Lec15%20File%20System%20Crash.assets/image.png)

logging的思想非常简单。你可以将磁盘想象成两部分，一部分是log，另一部分是文件系统。

任何对文件系统读写的操作都不会直接更新文件系统，而是会先将这些操作先写到log中，同时记录下该操作对应于文件系统哪些数据。

（log write）当需要更新文件系统时，我们并不是更新文件系统本身。假设我们在内存中缓存了bitmap block，也就是block 45。当需要更新bitmap时，我们并不是直接写block 45，而是将数据写入到log中，并记录这个更新应该写入到block 45。对于所有的写 block都会有相同的操作，例如更新inode，也会记录一条写block 33的log。

之后在某个时刻，对文件的操作结束后，OS会统一commit op。

（install log）当我们在log中存储了所有写block的内容时，如果我们要真正执行这些操作，只需要将block从log分区移到文件系统分区。我们知道第一个操作该写入到block 45，我们会直接将数据从log写到block45，第二个操作该写入到block 33，我们会将它写入到block 33，依次类推。 因为之前我们记录了这些操作，比如总操作数，对应文件系统的数据等等。之后只需要将数据写入到文件系统中对应的地方即可。

当log中的数据被拷贝到操作系统中后，logging的工作就全部完成了，这时候可以clean log。

总的来说就是这四步：

![img](Lec15%20File%20System%20Crash.assets/image.png)

当然，你会发现，这四步操作使得原来的工作量翻了1倍。

我们来讨论一下这其中的情况：

如果crash发生在commit op之前，我们会丢弃该操作

如果发生在之后，系统恢复后，我们会看到log block中有还没install的block，这时候把后续操作复制上去即可。

如果crash发生在install时，我们会重新install，这没关系，并不影响数据的一致性。

- 在install（第3步）过程中和第4步之前这段时间crash会发生什么？在下次重启的时候，我们会redo log，我们或许会再次将log block中的数据再次拷贝到文件系统。这样也是没问题的，因为log中的数据是固定的，我们就算重复写了文件系统，每次写入的数据也是不变的。重复写入并没有任何坏处，因为我们写入的数据可能本来就在文件系统中，所以多次install log完全没问题。当然在这个时间点，我们不能执行任何文件系统的系统调用。我们应该在重启文件系统之前，在重启或者恢复的过程中完成这里的恢复操作。换句话说，install log是幂等操作（注，idempotence，表示执行多次和执行一次效果一样），你可以执行任意多次，最后的效果都是一样的。

> 学生提问：因为这里的接口只有read/write，但是如果我们做append操作，就不再安全了，对吧？
>
> Frans教授：某种程度来说，append是文件系统层面的操作，在这个层面，我们可以使用上面介绍的logging机制确保其原子性（注，append也可以拆解成底层的read/write）。
>
> 学生提问：当正在commit log的时候crash了会发生什么？比如说你想执行多个写操作，但是只commit了一半。
>
> Frans教授：在上面的第2步，执行commit操作时，你只会在记录了所有的write操作之后，才会执行commit操作。所以在执行commit时，所有的write操作必然都在log中。而commit操作本身也有个有趣的问题，它究竟会发生什么？如我在前面指出的，commit操作本身只会写一个block。文件系统通常可以这么假设，单个block或者单个sector的write是原子操作（注，有关block和sector的区别详见14.3）。这里的意思是，如果你执行写操作，要么整个sector都会被写入，要么sector完全不会被修改。所以sector本身永远也不会被部分写入，并且commit的目标sector总是包含了有效的数据。而commit操作本身只是写log的header，如果它成功了只是在commit header中写入log的长度，例如5，这样我们就知道log的长度为5。这时crash并重启，我们就知道需要重新install 5个block的log。如果commit header没能成功写入磁盘，那这里的数值会是0。我们会认为这一次事务并没有发生过。这里本质上是write ahead rule，它表示logging系统在所有的写操作都记录在log中之前，不能install log。

Logging的实现方式有很多，我这里展示的指示一种非常简单的方案，这个方案中clean log和install log都被推迟了。接下来我会运行这种非常简单的实现方式，之后在下节课我们会看到更加复杂的logging协议。不过所有的这些协议都遵循了**write ahead rule**，也就是说在写入commit记录之前，你需要确保所有的写操作都在log中。在这个范围内，还有大量设计上的灵活性可以用来设计特定的logging协议。

在XV6中，我们会看到数据有两种状态，是在磁盘上还是在内存中。内存中的数据会在crash或者电力故障之后丢失。

![img](Lec15%20File%20System%20Crash.assets/image.png)

log中的数据结构很简单，有一个header block，也就是我们的commit record，记录了有效的log block，以及每个log block实际对应的block编号（用于复制log操作到文件系统）。之后就是log的数据了。也就是每个block的数据，依次为bn0对应的block的数据，bn1对应的block的数据以此类推。这就是log中的内容，并且log也不包含其他内容。

![img](Lec15%20File%20System%20Crash.assets/image.png)

在内存中会有header block的一份拷贝，并且相应的block也会存在block cache中。log中第一个block编号是45，那么在block cache的某个位置，也会有block 45的cache。

![img](Lec15%20File%20System%20Crash.assets/image.png)

## Log 的代码实现

接下来介绍在代码中log 的实现。

我们强调所有的文件系统操作，都是一个事务。 事务具有原子性。即一个事务要么发生要么不发生。对应在log中的实现是，只有在所有的操作都完成后我们再commit log。 这意味着文件系统必须标示事务的开始和结束。

你可以看到在任何一个文件系统的操作中，都有begin_op and end_op来表示这一点。并且事务中的所有写block操作具有原子性。在end_op中我们会调用commit操作来提交所有读写操作。

而在这两者之前的操作，磁盘上的数据会更新，但不会实际改变磁盘。在end_op结束时，我们会将数据写入log中，之后写入log header或者commit。

让我们来看看ialloc （fs.c），

![image-20211121212709081](Lec15%20File%20System%20Crash.assets/image-20211121212709081.png)

这个函数分配inode。可以看到它调用了log_write,标示一个inode已经被分配过。

log_write的工作很简单，我们已经在cache中对某个cache block写入了数据，这时候我们需要在磁盘上更新该操作，而这个操作会首先写入到log 中。可以看到，它只是对log header中的n+1，记录block数量。并且通过bpin将这个cache block固定在cache中。

以上就是log_write的全部工作了。任何文件系统调用，如果需要更新block或者说更新block cache中的block，都会将block编号加在这个内存数据中（注，也就是log header在内存中的cache），除非编号已经存在。

> 学生提问：这是不是意味着，bwrite不能直接使用？
>
> Frans教授：是的，可以这么认为，文件系统中的所有bwrite都需要被log_write替换。

## end_op

在每个文件系统操作最后都会调用end_op,它会commit

end_op()会做一些简单的判断，但最后会调用commit函数，

commit函数会调用一些函数做以下事情

1. write_log：把modified block的编号从从cache中拷贝到log中
2. write_head：把将内存中的log header写到disk中
3. install 所有操作
4. clean log

write_log遍历所有block，把内存中的cache block写到log中。

![image-20211121215605732](Lec15%20File%20System%20Crash.assets/image-20211121215605732.png)

函数中依次遍历log中记录的block，并写入到log中。它首先读出log block，将cache中的block拷贝到log block，最后再将log block写回到磁盘中。这样可以确保需要写入的block都记录在log中。但是在这个位置，我们还没有commit，现在我们只是将block存放在了log中。如果我们在这个位置也就是在write_head之前crash了，那么最终的表现就像是transaction从来没有发生过。

再来看看write_head,我们称之为commit point.它拷贝了log header到磁盘中。这等价于commit。

![image-20211121215559095](Lec15%20File%20System%20Crash.assets/image-20211121215559095.png)

其中bwrite是真正的commit point，如果在这之前发生crash，会丢失所有操作，而之后，则会被记录下来，下次恢复。

回到commit函数，在commit point之后，就会实际应用transaction。这里很直观，就是读取log block再查看header这个block属于文件系统中的哪个block，最后再将log block写入到文件系统相应的位置。让我们看一下install_trans函数，

![img](https://mit-public-courses-cn-translatio.gitbook.io/~/files/v0/b/gitbook-28427.appspot.com/o/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MSeczlhbFKSwLmq0egq%2F-MSjgrFOOOtGDmrKJ0xQ%2Fimage.png?alt=media&token=e9f0238c-6f4f-4d98-8a39-a0778ded6d9e)

这里先读取log block，再读取文件系统对应的block。将数据从log拷贝到文件系统，最后将文件系统block缓存落盘。这里实际上就是将block数据从log中拷贝到了实际的文件系统block中。当然，可能在这里代码的某个位置会出现问题，但是这应该也没问题，因为在恢复的时候，我们会从最开始重新执行过。

在commit函数中，install结束之后，会将log header中的n设置为0，再将log header写回到磁盘中。将n设置为0的效果就是清除log。

> 学生提问：install_trans函数在写block的时候，先写的缓存。可不可以优化一下直接写磁盘而不写缓存让代码运行的更快一些？
>
> Frans教授：这里的接口是不太好。你可能会想问反正都要写入新数据，为什么要先读出目标block来。这里的代码肯定还有很多优化空间，但是为了看起来简单我们并没有这么做。

以上就是commit内容。

## recovery

如果crash发生，xv6启动后第一件事情就是调用initlog，调用recover_from_log,它重新执行install_log,

recover_from_log先调用read_head函数从磁盘中读取header，之后调用install_trans函数。这个函数之前在commit函数中也调用过，它就是读取log header中的n，然后根据n将所有的log block拷贝到文件系统的block中。recover_from_log在最后也会跟之前一样清除log。

这就是恢复的全部流程。如果我们在install_trans函数中又crash了，也不会有问题，因为之后再重启时，XV6会再次调用initlog函数，再调用recover_from_log来重新install log。如果我们在commit之前crash了多次，在最终成功commit时，log可能会install多次。

> 学生提问：如果一个进程向磁盘写了一些数据，但是在commit之前进程出现了故障，假设故障之后进程退出了，这样会有问题吗？
>
> Frans教授：简单回答是没问题，因此磁盘不会被更新，所以效果就像文件系统操作没有发生过一样。并且进程并不能在故障后恢复，唯一能在故障之后还能保持的是保存在磁盘中的状态。（注，应该是没有理解问题。进程通过write系统调用成功写入的数据，就算在成功落盘之前进程异常退出了，内核还是会写入到磁盘中，前提是内核还在运行。）
