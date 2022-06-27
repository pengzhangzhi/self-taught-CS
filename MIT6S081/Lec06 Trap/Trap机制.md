# Trap

In most cases, O/S needs to switch from user space to kernel space. For example, when a device interupt occurs , O/S have to switch to kernel space to handle it. Another example is that when your process call a sys call, the process itself have no previledge to implement it, so it transfer the call to kernel. Such transistion from user space to kerenel space is called trap. Here are the three cases that we need trap.

To preserve the isolation and performance of OS, we need to carefully design the Trap.

Let is figure out what need to accomplish.

1. Save 32 registers and PC.
2. Switch to supervisor mode
3. Switch to kernel page table
4. Switch to kernel stack 
5. Jump to kernel C code

Our goals here is make trap transparent to users so that resume without bother. And, make sure that user code can not be executed in supervisor mode.

What functionalities does CPU’s mode support?

Supervisor can use cpu control registers:

1. satp: page table physical address
2. stvec: ecall jump here in kernel; point to trampoline
3. sepc: ecall saves pc here
4. sscratch: address of trampoline

In addition, supervisor can use PTEs that have no PTE_U flag.

But supervisor has no other powers!

Here list the codes that we are going to look at. Our focus is the transition from user space to kernel space. But the following has to be careful and secure also.

```
preview:
  write()                        write() returns              User
  -----------------------------------------------------------------
  uservec() in trampoline.S      userret() in trampoline.S   Kernel
  usertrap() in trap.c           usertrapret() in trap.c
  syscall() in syscall.c           ^
  sys_write() in sysfile.c      ---|
```

Considering this senario that we are using shell to call `write`. write is a system call.

Before calling write, we are in use space. a7 register tells the kernel what sys call that we want. SYS_write = 16.

then `write` will call `ecall`that triggers the user/kernel transition.

before that, let’s look at the state of current registers.

now pc and sp are at low addresses, because they are in user memory which starts at  zero.

Function arugments are put in a0, a1, a2 that refer to fd, buf, size respectively.

What page table is in use?

`info mem` can print page table. 

You will find few PTEs and two PTEs at bottom are trapframe and trampoline.

There are no mappings for kernel memory and devices, means it is process page table.

Let’s execute the ecall, and check out them again. You will find a lot of differences.

Look at pc, you will find we are at a very high address.

There are the instructions we are about to execute.

uservec in kernke/trampoline.S, it is the start of kernel’s trap handling code.

ecall does not switch page tables, so thse kernel insturction have to exist somewhere in user page table. The trampoline is the answer: the kernel maps it at every user page table. The kernel sets stvec to the trampoline page address. The trampoline is protected: no PTE_U flag.

How did we get here?

ecall did three things:

1. change the mode from user to supervisor
2. save pc in sepc
3. jump to stvec (trampoline code)

What needs to happen next?

1. save 32 register values (for later transparent resume).
2. Switch to kernel page table
3. Set kernel stack for kernel c code 
4. jump to kernel C code

Why didn’t RISC-V have ecall do these things for us?

Theoritically, RISC-V can do these things. But the RISC-V designer want to give OS as much flexibility as they can.

Becasue not every trap require saving registers or set up kernel stack. These steps are very time-comsuming. 



What are our options for saving user registers?

Can we save in somewhre in the physical memory? No, even supervisor is constrained to use page table.

  can we first set satp to the kernel page table?
    	supervisor mode is allowed to set satp...
   	 but we don't know the address of the kernel page table at this point!
  	  and we need a free register to even execute csrw satp, $xx

The solution for where to save 32 registers:

1. xv6 maps a 2nd kernel page, the trapframe, into every use page table. It has space to hold user regsisters.

   The kernel gives every process a different trapframe page. 

```
     the page at 0x3fffffe000 is the trapframe page
```

2. RISC-V provides the sscratch register that point to the trapframe. Before entering use space, supervisor code can swap any register with sscratch thus both getting hold of the value in sscratch, and simultaneously saving the registers’s user vlaue.

   Specifically, RISC-V will exchange the value of a0 and sscratch.  Thus a0 contains the adress of trapframe. the following steps are to save 32 registers to trapframe.

