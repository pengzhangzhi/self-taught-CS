

# Introduction

The key functionalities that an O/S should provide are the following:

1.  Support several activities at once. For example, `fork()` can start a child process based on a parent process.
2. The O/S must time-share the resources of computer so that every processes get a chance to execute.
3. Isolation. Make sure a bugy process won’t affect other processes or break down the computer.

This note will introduce how a O/S are organized to achieve those requirements.

Specifically, we will talk about the following four topics.

- Isolation
- Kernel and User mode
- System calls
- How does those design work in xv6

# Recap

In the first lecture, you should have a basic understanding of O/S.

First, you are formilar with `shell`, `echo`, `find` etc. Those programs run on the top of an O/S.

Second, O/S abstract hardware resources like CPU and disk.

Third, There is a interface between O/S and apps called system call interface (or system call in short). 

![img](https://gblobscdn.gitbook.com/assets%2F-MHZoT2b_bcLghjAOPsJ%2F-MIh_lLv4sI790Kw_cTT%2F-MIn4HtztTgrF0S7cUjs%2Fimage.png?alt=media&token=1182ec32-78aa-4e00-aba8-82c90c050982)

![image-20210926161531420](Lec03%20OS%20Organization%20and%20System%20Calls%20(Frans).assets/image-20210926161531420.png)

# Isolation

What is isolation? Why it is important?

Let say you are running `find` through a `shell`. You do not want the case that  the bug of `find` program terminate your `shell`. Or if the shell program have a serious problem, you do not want it to kill other processes. Similarly, If apps have problem, you do not want it to terminate your O/S. So isolation is important to make sure your programs and O/S work in a correct way.

What if there is no O/S in a computer? So every programs directly manipulate hardware resources. If a program has a dead for loop, it will occupy the CPU resources all the time so that other programs have no chance to run. In practice, we want a program run for a while are release the resource so the other programs can run. In other case, if apps directly run on the hardware, two apps share the same pecies of memory.  If one apps modfiy the content of a address, the other one would not know it. 

One reason why we use O/S is to implement multiplexing and memory isolation. 

## e.g. 1, process and cpu

Process is a abstract of CPU.  Apps can not interact with cpu. It must interact with process. O/S kernels switch to different process in CPU so that every programs have a chance to execute.

## e.g.2, Vitural Memory

When we use exec to execute a program, we will feed a finlename which relates to a memory image. The program instrcutions and global data are stored in that memory. Apps can expand or shirk their memory. But they have no rights to directly interact with physical memory. There is a middle layer that help apps to control physical memory.

## e.g.3, Files

Apps can not directly read and write contents of disk. The only way to do that is using files. You can modify the files as you like and O/S will decide how to translate your operations to the disk.

# Defensive

One O/S must have defensive. It should be ready to deal wtih attacts both intentional or not. It is necessary to have a strong isolation between apps and O/S.  So that the errors in apps won’t distory O/S.

Usually, we use hardware to implement strong isolation.

1. Use/kernel mode ( kernel mode is also called supervisor mode in RISC-V)
2. Vitural memory (page table)

# user/kernle mode

A CPU runs under two mdoe: user mode and kernel mode. In user mode, the cpu are alllowed to do basic instructions like addiing the value of two registers. Under kernel mode,  the cpu ca nrun privileged instructions like setting page table registers or changing state of hardware.

Actually, there is  another mode called machine mode that sopport much lower instrcutions.

# Vitural memory

Vitural memory implement the abstract of physical memory.  In fact, there is a page table that map a vitural memory to a physical memory. So the apps can only manipulate vitural memories and O/S will translate it to physical memory.

Each process has a seperate page table. That is, each process can only access the physical memory of its own page table. O/S will help apps to set up its page table. The apps are not allowed to do so or make up one.

As shown in the figure below, that the two processes have two virtural memory that start from 0. 

![image-20210926175505346](Lec03%20OS%20Organization%20and%20System%20Calls%20(Frans).assets/image-20210926175505346.png)

# User/Kernel mode switch

In some cases that the apps want to use system calls. For example,  the shell need to call `exec` to run another program. So it is neccesary for apps to switch to kernel mode.

How unix implement this?

When a app wants to call a system call, it will first call an instruction ECALL that takes a numerical parameter. The parameter indicate the system call.

After that, ECALL will jump to a place in the kernel side where there is a function named syscall inside syscall.c. Every system call that called by apps will eventually call this function. syscall will evaluate the parameter of ECALL which in our case is fork.

# Monolithic Kernel vs Micro Kernel

Obviously this design  User/Kernel mode switch may cause potential problems because a bugy apps also can use system calls. Don’t worry, the kernel would help you evaluate parameters and others.

So we the nerl space is also called Trusted Computing Base(TCB).

If a kernel can be called TCB, it must have no bugs in the kernel. If there is a bug, the hacker may take advantage of that bug and cause serious problems.

In addition, the kernel should serve other apps as malicious.

However, it is impossible for a kernel to have 0 bug. Because a kernel is a complex system. It is really easy to fix a bug and cause another one. You can’t make everybody happy.

## An interesting question is: What kinds of apps should run in kernel mode? 

One option is all the kernel codes are run in kernel code. This is called monolithic kernel design.

Such design has pros and cons.

- Cons:  If we put a huge amount of code into TCB, there would have much more bugs. Statistically, every 3000 lines of code would have few bugs. This may cause serious security problems.
- Pros: An O/S has multiple modules that implement different functionalities. Putting them togather will make modules work tightly so that the O/S can have better performance.

Another design is Micro Kernel Design. Under this design, we want the kernel mode to run as less code as possible. So there are a few key modules in the kernel (e.g. virtual memory) while most of modules are put in user mode (e.g. file system).  

The pros is obvious that there is less bugs in the kernel. The O/S is much secure.

The cons is worse performance because each module must work in a much complex way.

