# The Rust Programming Language

## Foreword

## Introduction

## 1. Getting Started
### 1.1. Installation
### 1.2. Hello, World!
### 1.3. Hello, Cargo!

## 2. Programming a Guessing Game

## 3. Common Programming Concepts
### 3.1. Variables and Mutability
### 3.2. Data Types
### 3.3. Functions
### 3.4. Comments
### 3.5. Control Flow

## 4. Understanding Ownership
### 4.1. What is Ownership?
### 4.2. References and Borrowing
### 4.3. The Slice Type

## 5. Using Structs to Structure Related Data
### 5.1. Defining and Instantiating Structs
### 5.2. An Example Program Using Structs
### 5.3. Method Syntax

## 6. Enums and Pattern Matching
### 6.1. Defining an Enum
### 6.2. The match Control Flow Construct
### 6.3. Concise Control Flow with if let and let else

## 7. Managing Growing Projects with Packages, Crates, and Modules
### 7.1. Packages and Crates
### 7.2. Defining Modules to Control Scope and Privacy
### 7.3. Paths for Referring to an Item in the Module Tree
### 7.4. Bringing Paths into Scope with the use Keyword
### 7.5. Separating Modules into Different Files

## 8. Common Collections
### 8.1. Storing Lists of Values with Vectors
### 8.2. Storing UTF-8 Encoded Text with Strings
### 8.3. Storing Keys with Associated Values in Hash Maps

## 9. Error Handling
### 9.1. Unrecoverable Errors with panic!
### 9.2. Recoverable Errors with Result
### 9.3. To panic or Not to panic

## 10. Generic Types, Traits, and Lifetimes
### 10.1. Generic Data Types
### 10.2. Traits: Defining Shared Behavior
### 10.3. Validating References with Lifetimes

## 11. Writing Automated Tests
### 11.1. How to Write Tests
### 11.2. Controlling How Tests Are Run
### 11.3. Test Organization

## 12. An I/O Project: Building a Command Line Program
### 12.1. Accepting Command Line Arguments
### 12.2. Reading a File
### 12.3. Refactoring to Improve Modularity and Error Handling
### 12.4. Developing the Library’s Functionality with Test Driven Development
### 12.5. Working with Environment Variables
### 12.6. Writing Error Messages to Standard Error Instead of Standard Output

## 13. Functional Language Features: Iterators and Closures
### 13.1. Closures: Anonymous Functions that Capture Their Environment
### 13.2. Processing a Series of Items with Iterators
### 13.3. Improving Our I/O Project
### 13.4. Comparing Performance: Loops vs. Iterators

## 14. More about Cargo and Crates.io
### 14.1. Customizing Builds with Release Profiles
### 14.2. Publishing a Crate to Crates.io
### 14.3. Cargo Workspaces
### 14.4. Installing Binaries from Crates.io with cargo install
### 14.5. Extending Cargo with Custom Commands

## 15. Smart Pointers
### 15.1. Using Box<T> to Point to Data on the Heap
### 15.2. Treating Smart Pointers Like Regular References with Deref
### 15.3. Running Code on Cleanup with the Drop Trait
### 15.4. Rc<T>, the Reference Counted Smart Pointer
### 15.5. RefCell<T> and the Interior Mutability Pattern
### 15.6. Reference Cycles Can Leak Memory

## 16. Fearless Concurrency
### 16.1. Using Threads to Run Code Simultaneously
### 16.2. Using Message Passing to Transfer Data Between Threads
### 16.3. Shared-State Concurrency
### 16.4. Extensible Concurrency with the Send and Sync Traits

## 17. Fundamentals of Asynchronous Programming: Async, Await, Futures, and Streams
### 17.1. Futures and the Async Syntax
### 17.2. Applying Concurrency with Async
### 17.3. Working With Any Number of Futures
### 17.4. Streams: Futures in Sequence
### 17.5. A Closer Look at the Traits for Async
### 17.6. Futures, Tasks, and Threads

## 18. Object Oriented Programming Features of Rust
### 18.1. Characteristics of Object-Oriented Languages
### 18.2. Using Trait Objects That Allow for Values of Different Types
### 18.3. Implementing an Object-Oriented Design Pattern

## 19. Patterns and Matching
### 19.1. All the Places Patterns Can Be Used
### 19.2. Refutability: Whether a Pattern Might Fail to Match
### 19.3. Pattern Syntax

## 20. Advanced Features
### 20.1. Unsafe Rust
### 20.2. Advanced Traits
### 20.3. Advanced Types
### 20.4. Advanced Functions and Closures
### 20.5. Macros

## 21. Final Project: Building a Multithreaded Web Server
### 21.1. Building a Single-Threaded Web Server
### 21.2. Turning Our Single-Threaded Server into a Multithreaded Server
### 21.3. Graceful Shutdown and Cleanup

## 22. Appendix
### 22.1. A - Keywords
### 22.2. B - Operators and Symbols
### 22.3. C - Derivable Traits
### 22.4. D - Useful Development Tools
### 22.5. E - Editions
### 22.6. F - Translations of the Book
### 22.7. G - How Rust Is Made and "Nightly Rust"