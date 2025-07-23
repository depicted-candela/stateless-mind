# Table of Contents

**Computer Organization and Design: The Hardware/Software Interface**  
*David A. Patterson, University of California, Berkeley, Google, Inc.*  
*John L. Hennessy, Stanford University*

## Contents

Preface xv

## Chapters

### 1. Computer Abstractions and Technology 2

1.1 Introduction 3  
1.2 Seven Great Ideas in Computer Architecture 10  
1.3 Below Your Program 13  
1.4 Under the Covers 16  
1.5 Technologies for Building Processors and Memory 24  
1.6 Performance 28  
1.7 The Power Wall 40  
1.8 The Sea Change: The Switch from Uniprocessors to Multiprocessors 43  
1.9 Real Stuff: Benchmarking the Intel Core i7 46  
1.10 Going Faster: Matrix Multiply in Python 49  
1.11 Fallacies and Pitfalls 50  
1.12 Concluding Remarks 53  
1.13 Historical Perspective and Further Reading 55  
1.14 Self-Study 55  
1.15 Exercises 59  

### 2. Instructions: Language of the Computer 66

2.1 Introduction 68  
2.2 Operations of the Computer Hardware 69  
2.3 Operands of the Computer Hardware 72  
2.4 Signed and Unsigned Numbers 79  
2.5 Representing Instructions in the Computer 86  
2.6 Logical Operations 93  
2.7 Instructions for Making Decisions 96  
2.8 Supporting Procedures in Computer Hardware 102  
2.9 Communicating with People 112  
2.10 MIPS Addressing for 32-Bit Immediates and Addresses 118  
2.11 Parallelism and Instructions: Synchronization 127  
2.12 Translating and Starting a Program 129  
2.13 A C Sort Example to Put It All Together 138  
2.14 Arrays versus Pointers 147  
2.15 Advanced Material: Compiling C and Interpreting Java 151  
2.16 Real Stuff: ARMv7 (32-bit) Instructions 151  
2.17 Real Stuff: ARMv8 (64-bit) Instructions 155  
2.18 Real Stuff: RISC-V Instructions 156  
2.19 Real Stuff: x86 Instructions 157  
2.20 Going Faster: Matrix Multiply in C 166  
2.21 Fallacies and Pitfalls 167  
2.22 Concluding Remarks 169  
2.23 Historical Perspective and Further Reading 172  
2.24 Self Study 172  
2.25 Exercises 175  

### 3. Arithmetic for Computers 186

3.1 Introduction 188  
3.2 Addition and Subtraction 188  
3.3 Multiplication 193  
3.4 Division 199  
3.5 Floating Point 206  
3.6 Parallelism and Computer Arithmetic: Subword Parallelism 232  
3.7 Real Stuff: Streaming SIMD Extensions and Advanced Vector Extensions in x86 234  
3.8 Going Faster: Subword Parallelism and Matrix Multiply 235  
3.9 Fallacies and Pitfalls 237  
3.10 Concluding Remarks 241  
3.11 Historical Perspective and Further Reading 245  
3.12 Self Study 245  
3.13 Exercises 248  

### 4. The Processor 254

4.1 Introduction 256  
4.2 Logic Design Conventions 260  
4.3 Building a Datapath 263  
4.4 A Simple Implementation Scheme 271  
4.5 A Multicycle Implementation 284  
4.6 An Overview of Pipelining 285  
4.7 Pipelined Datapath and Control 298  
4.8 Data Hazards: Forwarding versus Stalling 315  
4.9 Control Hazards 328  
4.10 Exceptions 337  
4.11 Parallelism via Instructions 344  
4.12 Putting It All Together: The Intel Core i7 6700 and ARM Cortex-A53 358  
4.13 Going Faster: Instruction-Level Parallelism and Matrix Multiply 366  
4.14 Advanced Topic: An Introduction to Digital Design Using a Hardware Design Language to Describe and Model a Pipeline and More Pipelining Illustrations 368  
4.15 Fallacies and Pitfalls 369  
4.16 Concluding Remarks 370  
4.17 Historical Perspective and Further Reading 371  
4.18 Self-Study 371  
4.19 Exercises 372  

### 5. Large and Fast: Exploiting Memory Hierarchy 390

5.1 Introduction 392  
5.2 Memory Technologies 396  
5.3 The Basics of Caches 401  
5.4 Measuring and Improving Cache Performance 416  
5.5 Dependable Memory Hierarchy 436  
5.6 Virtual Machines 442  
5.7 Virtual Memory 446  
5.8 A Common Framework for Memory Hierarchy 472  
5.9 Using a Finite-State Machine to Control a Simple Cache 479  
5.10 Parallelism and Memory Hierarchies: Cache Coherence 484  
5.11 Parallelism and Memory Hierarchy: Redundant Arrays of Inexpensive Disks 488  
5.12 Advanced Material: Implementing Cache Controllers 488  
5.13 Real Stuff: The ARM Cortex-A8 and Intel Core i7 Memory Hierarchies 489  
5.14 Going Faster: Cache Blocking and Matrix Multiply 494  
5.15 Fallacies and Pitfalls 496  
5.16 Concluding Remarks 500  
5.17 Historical Perspective and Further Reading 501  
5.18 Self-Study 501  
5.19 Exercises 506  

### 6. Parallel Processors from Client to Cloud 524

6.1 Introduction 526  
6.2 The Difficulty of Creating Parallel Processing Programs 528  
6.3 SISD, MIMD, SIMD, SPMD, and Vector 533  
6.4 Hardware Multithreading 540  
6.5 Multicore and Other Shared Memory Multiprocessors 543  
6.6 Introduction to Graphics Processing Units 548  
6.7 Domain Specific Architectures 555  
6.8 Clusters, Warehouse Scale Computers, and Other Message-Passing Multiprocessors 558  
6.9 Introduction to Multiprocessor Network Topologies 563  
6.10 Communicating to the Outside World: Cluster Networking 566  
6.11 Multiprocessor Benchmarks and Performance Models 567  
6.12 Real Stuff: Benchmarking the Google TPUv3 Supercomputer and an NVIDIA Volta GPU Cluster 577  
6.13 Going Faster: Multiple Processors and Matrix Multiply 586  
6.14 Fallacies and Pitfalls 589  
6.15 Concluding Remarks 592  
6.16 Historical Perspective and Further Reading 594  
6.17 Self Study 594  
6.18 Exercises 596  

## Appendices

### A. Assemblers, Linkers, and the SPIM Simulator A-610

A.1 Introduction A-611  
A.2 Assemblers A-618  
A.3 Linkers A-626  
A.4 Loading A-627  
A.5 Memory Usage A-628  
A.6 Procedure Call Convention A-630  
A.7 Exceptions and Interrupts A-641  
A.8 Input and Output A-646  
A.9 SPIM A-648  
A.10 MIPS R2000 Assembly Language A-653  
A.11 Concluding Remarks A-689  
A.12 Exercises A-690  

### B. The Basics of Logic Design B-692

B.1 Introduction B-693  
B.2 Gates, Truth Tables, and Logic Equations B-694  
B.3 Combinational Logic B-699  
B.4 Using a Hardware Description Language B-710  
B.5 Constructing a Basic Arithmetic Logic Unit B-716  
B.6 Faster Addition: Carry Lookahead B-728  
B.7 Clocks B-738  
B.8 Memory Elements: Flip-Flops, Latches, and Registers B-740  
B.9 Memory Elements: SRAMs and DRAMs B-748  
B.10 Finite-State Machines B-757  
B.11 Timing Methodologies B-762  
B.12 Field Programmable Devices B-768  
B.13 Concluding Remarks B-769  
B.14 Exercises B-770  

## Online Content

### C. Graphics and Computing GPUs C-2

C.1 Introduction C-3  
C.2 GPU System Architectures C-7  
C.3 Programming GPUs C-12  
C.4 Multithreaded Multiprocessor Architecture C-25  
C.5 Parallel Memory System C-36  
C.6 Floating Point Arithmetic C-41  
C.7 Real Stuff: The NVIDIA GeForce 8800 C-46  
C.8 Real Stuff: Mapping Applications to GPUs C-55  
C.9 Fallacies and Pitfalls C-72  
C.10 Concluding Remarks C-76  
C.11 Historical Perspective and Further Reading C-77  

### D. Mapping Control to Hardware D-2

D.1 Introduction D-3  
D.2 Implementing Combinational Control Units D-4  
D.3 Implementing Finite-State Machine Control D-8  
D.4 Implementing the Next-State Function with a Sequencer D-22  
D.5 Translating a Microprogram to Hardware D-28  
D.6 Concluding Remarks D-32  
D.7 Exercises D-33  

### E. Survey of Instruction Set Architectures E-2

E.1 Introduction E-3  
E.2 A Survey of RISC Architecture for Desktop, Server, and Embedded Computers E-4  
E.3 The Intel 80x86 E-30  
E.4 The VAX Architecture E-50  
E.5 The IBM 360/370 Architecture for Mainframe Computers E-69  
E.6 Historical Perspective and References E-73  

## Additional Sections

Glossary G-1  
Further Reading FR-1  

*Copyright Elsevier 2024*