---
title: Ensuring the Memory Safety of FreeRTOS Part 2
date: 
feature: blog
categories:
  - Long term support
authors: 
  - ncchong
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---


by [Nathan Chong](../author/ncchong) on 07 May 2020

In [Part 1](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1), we discussed how FreeRTOS is addressing 
an important source of security issues --- buffer overflows --- by ensuring the memory safety of the 
TCP/IP, ARP, DHCP, DNS, and HTTPS header parsing in the FreeRTOS-Plus-TCP TCP/IP stack. We described 
how we're using an automated reasoning technique, **software model checking**, and how the level of 
assurance that we obtain from the technique is different from what we could obtain through bug-finding 
tools.

In this follow-up, we'll look at software model checking in more detail: giving you some intuition for 
the problem it solves and how software model checking tools tackle this problem in practice. Similar 
to other automated reasoning techniques, the goal of software model checking is to give a guarantee 
that a program is correct with respect to a **specification**. A specification is a property that the 
program must always adhere to (no matter what) such as never dereferencing a NULL pointer or writing-past 
the end of a buffer. In order to give this level of assurance, we need a way to effectively reason about 
every execution path through a program on every input, searching for executions that violate the 
specification.

Let's start by characterizing the problem. The following diagram (reproduced from John Regehr’s 
talk  ["SQLite with a fine toothed comb"](https://www.youtube.com/watch?v=LXdyD_mhbzk)  which we highly 
recommend), shows the *state space* of a program. A state is an assignment of the program’s variables 
to values. Think of a state as a snapshot of the program's variables that you could examine if you 
stepped-through the program in a debugger. For example, in a program with two integer variables `x` 
and `y` and a pointer `p`, one possible state is `(x=1, y=2, p=NULL)`. The state space is the space 
of possible states that the program *might* take. So in the diagram, the state space is *any* point 
within the box.

Continuing this analogy, an execution of the program is a *path* through the state space. In the diagram, 
one possible execution is shown as a series of white arrows with the particular states *reached* by the 
execution as white dots. This execution could, for example, be the result of running a unit test that 
starts with the state `(x=0, y=0, p=NULL)` and increments `x` four times to end with the 
state `(x=4, y=0, p=NULL)`.

As programmers, we know that some states are desirable and some are not. Let's make this more precise. 
First, the blue shape represents the *feasible states* of the program: ones that the program can reach 
by some execution. For example, imagine that the program saturates the values of `x` and `y` at `1024`. 
In this case `(x=1024, y=1024, p=NULL)` is a feasible state (i.e., inside the blue shape) 
and `(x=1024, y=102**5**, p=NULL)` is an *in*feasible state (i.e., outside of the blue shape).

![](/media/2020/cmbc-ensuring-memory-pt-2-pic1.png)   
Secondly, let's say an *error state* is any state that violates the specification, such as memory safety, 
that we are trying to prove. For example, the program might dereference `p` whenever some, perhaps complicated, 
condition over `x` and `y` holds. If `p` is also `NULL` then the state is an error state. In the second 
diagram, below, error states are represented by the collection of red shapes. Note that the existence of 
such erroneous states is not a problem. The key question is whether they are *feasible* as well.

![](/media/2020/cmbc-ensuring-memory-pt2-pic2.png)   
With this setup, we can characterize a *bug* as an undesirable state that is both erroneous (red) and 
feasible (blue). The problem of finding all bugs can be seen as finding all states in the intersection 
of the red and blue shapes, such as in the bottom left corner. Put another way, the problem of proving 
the *absence* of a whole class of bugs is to show that no such states exist: that the red and blue 
shapes *never* intersect.

This sounds straightforward except (1) it is difficult to determine whether any arbitrary state is feasible 
or not, and (2) the number of states, even for modest programs, can be astronomical. For example, the 
simple program we've been considering throughout this post has only three variables but `2^32 * 2^32 * 2^32` 
different states (if each integer and the pointer are 32-bits). Thinking about all of the possible corner-cases 
of a program can be difficult even for expert programmers. Additionally, the program only gives us the 
reachable states implicitly. Hence, it is the job of an automated verification technique to reason about 
the state space efficiently.

How do software model checkers tackle this problem? The key idea is to translate the program into 
a *logical formula* that describes the set of feasible program states and specification. A logical 
formula is an expression that uses Boolean variables and other connectives, such as logical-and, 
logical-or and negation, and can be evaluated to true or false by giving each variable an assignment (of 
true or false). The translation is carefully constructed to ensure there is a correspondence between 
the formula and the feasible program states. In particular, if there is a solution, an assignment of 
the variables so that the formula evaluates to true, then this corresponds to a feasible program state 
that violates the specification. Conversely, if there are no solutions then this certifies that it is 
impossible for the program to reach an error state. The translation reduces the problem of finding bugs 
to solving a formula.

This problem of solving a Boolean formula is known as SAT. In principle, this is a famously intractable 
problem: the number of assignments grows exponentially, doubling with each variable in the formula. However, 
the automated reasoning community has built constraint solvers that are remarkably effective on the formulas 
encountered in practice. These SAT solvers (and SMT solvers, which allow for richer expressions involving 
features such as integers, arrays and strings) are the foundation of many automated reasoning tools, 
including software model checkers.

Thank you for joining me on this short tour under the hood of software model checking. We hope this article 
has given you more context about our proofs of memory safety in FreeRTOS. As we wrote in the first part, 
we are excited about pushing automated reasoning techniques even further to provide even stronger assurances 
to our customers and supporting a community of developers interested in adopting these techniques to develop 
high-quality code themselves.

* John Regehr, ["SQLite with a fine toothed comb"](https://www.youtube.com/watch?v=LXdyD_mhbzk)
* Sharad Malik and Lintao Zhang ["Boolean Satisfiability: From Theoretical Hardness to Practical Success"](https://cacm.acm.org/magazines/2009/8/34498-boolean-satisfiability-from-theoretical-hardness-to-practical-success/fulltext)
* Leonardo De Moura and Nikolaj Bjørner, ["Satisfiability Modulo Theories: Introduction and Applications"](https://cacm.acm.org/magazines/2011/9/122785-satisfiability-modulo-theories/fulltext)


## About the author

![](https://secure.gravatar.com/avatar/bd7191d11f35f3d6d9b292b87dbbaaa1?s=200&d=mm&r=g)   
Nathan Chong is a Principal Engineer with the Automated Reasoning Group at Amazon Web Services. His work 
focuses on the correctness of concurrent systems code, particularly at the hardware-software boundary.   
[View articles by this author](../author/ncchong) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
