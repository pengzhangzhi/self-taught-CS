# Page Table & Virtual Memory

What is page table and why page table?

- A table that map virtual memory address to physical memory address

- Implement Isolation

This article covers the following topics:

1. Address space
2. paging hardware (RISC-V)
3. xv6 virtual memory code + layout

# Address spcae 

## Isolation

We can implement two kinds of Isolation with virtual memory: 1. per process isolation 2. process and kernel isolation. 

Each program including kernel has a private and unique address that start from 0 to n.

![image-20210928135845698](Lec4%20Page%20Table.assets/image-20210928135845698.png)

If `cat` program wants to write a data to address 100, it will write to its own adress 100 instead of `shell`'s address.

In fact, `cat` can not see the adress space of `shell`.

Therefore, the question is how to split a entire physical memory into different memory spaces.

One solution is page table. 

## Page Table

Page Table is implemented by Memory Management Unit (MMU) that translate virtual memory address to physical address. 

When CPU is executing an instruction: sd $7 (a0), it should see the address as virtual memory address. Let say the address in a0 is 0x1000, the MMU would translate it to physical memory address which can be used to index data.

To realize such translation, MMU have a table. One side is virtual memory address and the other side is physical memory address.

Usually page tables are stored in memory. Therefore, there are some registers in CPU stores the physical address of those tables. In RISC-V, that register is SATP.  When receiving a virtual memory address, the cpu will inform MMU the table address (stored in SATP) and MMU will translate address.![image-20210928141715420](Lec4%20Page%20Table.assets/image-20210928141715420.png)

Every process maintains their own page table. That is, if we switch to anothe process, the cpu also need to replace the content of SATP.

Let’s dive deeper. 

### Per-page Index

From the perspective of MMU, it takes a page table (from register SATP) and a input virtual memory address, the target is to translate it to physical memory address.

The form of virtual memory address is shown as follows.

![image-20210928151726293](Lec4%20Page%20Table.assets/image-20210928151726293.png)

The first 25 bits EXT are unused. The middle 27 bits index is the index of page. The last 12 bits are offset. The final physical address is the base address plusing offset.

The form of physical memory address is shown as follows.

![image-20210928151958967](Lec4%20Page%20Table.assets/image-20210928151958967.png)

There are 56bits in total. The first 44bits are the page number and the last 12 bits are offset (the same as virtual memory address).

To implement address translation, MMU only need to take the index field of virtual address, look up the page table, translate it to 44 bits page number. The last 12 bits can directly take the offset field of virtual address.

![image-20210928152155360](Lec4%20Page%20Table.assets/image-20210928152155360.png)

As shown in the figure, one index corresponds to a PNN(physical page number).

The reason why we have such a design is the physical memory is sliced into multiple pages. Each page has size of 2^12 (2096) byte. That said, if one wants to access a physical memory, the first thing is to specify which page. The second thing is specifying the location of that page which can use offset to implement.

As you see in the above, the two address have different length. The virtual address has 64 bits and the physiocal address has 56.  Don’t panic. This is determined by hardware design.  While we mentioned that the first 25 bits in virtual address is unused. The valid number of virtual address is 2^(27+12) = 2^(39), less than number of physical address (2^56). That said, the virtual memory does not completely split all the physical address.

> 同一个学生：图中的56bit又是根据什么确定的？
>
> Frans教授：这是由硬件设计人员决定的。所以RISC-V的设计人员认为56bit的物理内存地址是个不错的选择。可以假定，他们是通过技术发展的趋势得到这里的数字。比如说，设计是为了满足5年的需求，可以预测物理内存在5年内不可能超过2^56这么大。或许，他们预测是的一个小得多的数字，但是为了防止预测错误，他们选择了像2^56这么大的数字。这里说的通吗？很多同学都问了这个问题。
>
> 学生提问：如果虚拟内存最多是2^27（最多应该是2^39），而物理内存最多是2^56，这样我们可以有多个进程都用光了他们的虚拟内存，但是物理内存还有剩余，对吗？
>
> Frans教授：是的，完全正确。
>
> 学生提问：因为这是一个64bit的机器，为什么硬件设计人员本可以用64bit但是却用了56bit？
>
> Frans教授：选择56bit而不是64bit是因为在主板上只需要56根线。

### Hierarchical Page Directory

For a page table, there are 2^27 (27 is the lenght of virtual memory index field) pages.  Each process owns a page table, the total amount of page table is gigantic. It is important to come up a better solution for storing page table.

Above we mentioned that index refers to the PPN. In fact, it is not a one-to-one correspondence. There are three level of index. Such hierarchical approach can exponentially increase the index range.

The 27 bits index consists of three 9 bits elements: L2, L1, L0. 

The first paeg directory address is given by the register `satp`. Then use L2 to index the PPN of the first page directory.  This PPN is the address of second page directory. Similarly with second page directory and L1 we can get the address of third page dirctory. In the third page dirctory, the final PPN is indexed by L0. 

![image-20210928163343659](Lec4%20Page%20Table.assets/image-20210928163343659.png)

### Flags

There are 10 bits flag field that indicate the state of a PTE (page table entry). A PTE refers to a page.

![image-20210928163351356](Lec4%20Page%20Table.assets/image-20210928163351356.png)

### Translation Lookaside Buffer

 Three level table makes us to look up three times to retrieve a physical address compared to orginal design.

To optimize this, a solution is Translation Lookside Buffer (TLB).

The first time you do the lookup as normal. And TLB would save the virtual-physical memory pair as a buffer. If you access the same virtual memory next time, TLB will directly return the saved corresponding physical memory.

在我们介绍XV6之前，有关page table我还想说一点。用时髦的话说，page table提供了一层抽象（[level of indirection](https://en.wikipedia.org/wiki/Indirection)）。我这里说的抽象就是指从虚拟地址到物理地址的映射。这里的映射关系完全由操作系统控制。

因为操作系统对于这里的地址翻译有完全的控制，它可以实现各种各样的功能。比如，当一个PTE是无效的，硬件会返回一个page fault，对于这个page fault，操作系统可以更新 page table并再次尝试指令。所以，通过操纵page table，在运行时有各种各样可以做的事情。我们在之后有一节课专门会讲，当出现page fault的时候，操作系统可以做哪些有意思的事情。现在只需要记住，page table是一个无比强大的机制，它为操作系统提供了非常大的灵活性。这就是为什么page table如此流行的一个原因。

## Kernel Page Layout

![image-20210928165431848](Lec4%20Page%20Table.assets/image-20210928165431848.png)

On the left is the virtual addresses, the right is the physical addresss. To mike things simple, xv6 use identity mapping in most cases, which means the virtual address is the same as physical address.

Addresses below 0x800000 are device address. Addresses between KERNBASE and PHYSTOP are mapped to addresses from DRAM. Vritual memory address in this range are stored kernel data and the free memory are stored user data.

On the top is the kernel stack, Noticed that there are Guard pages that are used to avoid overflow problems. When the kstack overflow, the address would reach to Guard page that is marked invalid. So O/S will know that there is a page fault. 

The RW is the authority.

![image-20210928223150665](Lec4%20Page%20Table.assets/image-20210928223150665.png)



## How XV6 code implement page table?

When xv6 is booted, it will call a function `kvminit` that set up the kernel address space.![image-20210928223418600](Lec4%20Page%20Table.assets/image-20210928223418600.png)

`kalloc() `intialize a page table, the next line of code set the content to 0.

The following function `kvmmap` set up the map of deivce.

Next it will call `kvminithart` . this function first set up the register satp that switch h/w page table to kernel page table. Before this function is called, the physical page table is intialized but can not be used because the cpu do not know its address. So this function tells CPU the address of intialized page table.

![image-20210928224243613](Lec4%20Page%20Table.assets/image-20210928224243613.png)

After the function worked, all addresses are virtual addresses.

### `walk()` function

`walk` has the same functionality as MMU that returns a pointer to a PTE of a given virtual address.

![image-20210928225332568](Lec4%20Page%20Table.assets/image-20210928225332568.png)

