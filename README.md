This course was developed for Debian 12 users, but you can take the lectures and complete the exercises on other operating systems like Windows or macOS. However, it is important to understand that certain critical technologies in the curriculum, such as Docker, fall into a category known as **OS-level virtualization**. These tools are not simple applications; they are deeply integrated with and dependent on specific features of the host operating system's kernel.

When you use Docker on Windows or macOS, it runs within a lightweight Linux virtual machine (VM) that is managed for you. Therefore, to truly grasp the material and troubleshoot effectively, a foundational knowledge of virtualization becomes essential. This extra layer of abstraction is particularly relevant when studying topics such as:

*   **Hardware and software failure types**: You must be able to distinguish between a failure in your application, the container, the Docker daemon, or the underlying VM.
*   **Vertical vs. horizontal scaling trade-offs**: The performance and resource limits of your containers are influenced by the resources allocated to the host VM.
*   **Recovery mechanisms (e.g., failover, snapshots)**: Understanding the full system stack, including the virtualization layer, is critical for designing robust recovery strategies.
*   **Deployment and monitoring**: Observability pipelines must account for metrics from both the containers and the VM they run inside.

Using a Debian environment provides the most direct and un-abstracted learning experience for these topics, allowing you to interact with the technologies as they were designed to run natively.

**For increased user experience, clone this repository and enjoy the lectures with VS Code**

# Stateless Mind: Architecting Serverless Blueprints and Probabilistic Intelligence

## **World-Class Data Engineering**

### Own Objectives

1. **Master Data Engineering Fundamentals**: Gain expertise in designing scalable, reliable, and fault-tolerant data systems, including data ingestion, storage, transformation, and serving, using tools like PostgreSQL, Apache Spark, Kafka, Airflow, and dbt.
2. **Develop Advanced Mathematical Skills**: Build proficiency in linear algebra, probability, statistics, optimization, numerical methods, information theory, stochastic processes, and heuristic algorithms to support high-quality data algorithms and decision-making.
3. **Architect Enterprise-Grade AI Data Systems**: Learn to create robust data pipelines for AI models and ML systems, focusing on feature engineering, MLOps, and minimal deep learning data preprocessing (e.g., text embeddings) for production-ready systems.
4. **Apply Theoretical Knowledge Practically**: Implement real-world projects (e.g., ETL pipelines, streaming systems, recommendation systems) using Python, SQL, and open-source technologies to solve enterprise-scale challenges.
5. **Understand Hardware and Systems**: Gain insights into memory hierarchy and programming (low level: C and C++; high level: Rust and Python) to optimize data system performance and resource allocation.
6. **Specialize in Real-Time or AI Systems**: Choose a track to master either real-time data processing (e.g., Kafka streaming) or AI/ML systems (e.g., MLOps, RL basics), applying dynamical systems and optimization for advanced applications.
7. **Build a Professional Portfolio**: Create an end-to-end data pipeline project for an AI application, integrating dbt, Spark, Docker, and mathematical techniques, to demonstrate expertise to employers or collaborators.

## Community Objectives

1. **Develop Practice Datasets**: Create and share curated datasets for data engineering and AI tasks (e.g., retail sales for star schemas, streaming logs for Kafka, text data for embeddings) to support hands-on learning.
2. **Design Coding Exercises**: Produce Python, SQL, and C exercises for data pipeline development, numerical methods (e.g., Gauss-Seidel solver), and optimization (e.g., linear programming), with solutions for community use.
3. **Create Mathematical Problem Sets**: Develop problem sets on probability, convex optimization, stochastic processes, and dynamical systems, tailored for data engineering applications, with detailed explanations.
4. **Share Pipeline Templates**: Build and distribute reusable templates for ETL/ELT pipelines (e.g., dbt models, Airflow DAGs, Spark jobs) to help learners practice enterprise-grade system design.
5. **Produce Tutorial Guides**: Write concise guides on key topics (e.g., setting up PostgreSQL, implementing Huffman coding, modeling streaming with Poisson processes) for self-paced learning.
6. **Contribute to Educational Platforms**: Share practice materials (datasets, exercises, templates) on platforms like GitHub or MIT OpenCourseWare, enhancing resources for data engineering and AI education.

**Total Duration**: Approximately 14-20 months, assuming 10-15 hours per week.

---

## Phase 1: Foundations (3-4 months)

**Objective**: Establish a solid base in data system internals, modern data engineering practices, programming, foundational mathematics, and minimal deep learning data needs.

### Section 1.1: Data System Internals

- **Books**: *Designing Data-Intensive Applications* by Martin Kleppmann, *Readings in Database Systems (The "Red Book")* edited by Bailis, Hellerstein, and Stonebraker
- **1.1.1 Reliability and Fault Tolerance**
  - **Hardware and software failure types**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 8: The Trouble with Distributed Systems (fault models, failure detection)
      - *Computer Organization and Design*: Chapter 5: Large and Fast: Exploiting Memory Hierarchy, Section 5.5 Dependable Memory Hierarchy (page 436)
      - *Readings in Database Systems*: Section "Techniques Everyone Should Know" for practical fault tolerance strategies.
    - **Technologies/Programming**: Python (logging, error handling; see *Python for Data Analysis*: Ch. 3), C (system-level fault detection using signals; see *The C Programming Language*: Appendix B, `<signal.h>`)
    - **Training Application**: Simulate hardware failures using Python scripts to log and handle errors; implement signal handling in C for crash recovery based on concepts from *The C Programming Language*: Chapter 7 (Error Handling).
  - **Replication strategies (e.g., leader-follower, multi-leader)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 5: Replication (leader-based, multi-leader replication), Chapter 9: Consistency and Consensus (replication consistency)
      - *Readings in Database Systems*: Section "Weak Isolation and Distribution" for replication models and trade-offs.
    - **Technologies/Programming**: PostgreSQL (replication setup), Python (psycopg2 for replication monitoring; see *Python for Data Analysis*: Ch. 6), docker compose [reference](https://github.com/docker/compose/tree/main/docs/reference) and docker rootless [tutorial](https://docs.docker.com/engine/security/rootless/)
    - **Training Application**: Configure PostgreSQL leader-follower replication as described in *Designing Data-Intensive Applications*: Ch. 5, and write Python scripts to monitor replication lag.
  - **Recovery mechanisms (e.g., failover, snapshots)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 5 (Handling Node Outages), Chapter 8 (Detecting Faults)
      - *Fundamentals of Data Engineering*: Chapter 3: Designing Good Data Architecture (Plan for Failure)
      - *Readings in Database Systems*: Section "Techniques Everyone Should Know" for snapshot and recovery mechanisms.
      - **Streaming Systems (Akidau et al.)**: Chapter 7: "The Practicalities of Persistent State" and Chapter 5: "Exactly-Once and Side Effects". These chapters are canonical for understanding stateful recovery in modern streaming.
    - **Technologies/Programming**: PostgreSQL (point-in-time recovery), Python (backup scripts), **Apache Flink**: Document its state backends and checkpointing mechanism.
    - **Training Application**: Implement a PostgreSQL snapshot and recovery process, automated with Python scripts, applying principles from *DDIA*: Ch. 5. Contrast this by building a stateful Flink job (e.g., a simple counter) and demonstrate its recovery from a failure by observing its checkpoint/restore mechanism.
- **1.1.2 Scalability**
  - **Load parameters (e.g., throughput, latency)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 1: Reliable, Scalable, and Maintainable Applications (scalability metrics), Chapter 6: Partitioning (load balancing)
      - *Fundamentals of Data Engineering*: Chapter 3: Designing Good Data Architecture (Architect for Scalability)
      - *Readings in Database Systems*: Section "Large-Scale Dataflow Engines" for scalability in distributed systems.
    - **Technologies/Programming**: Apache Spark (job monitoring), Python (performance profiling with `timeit`, `cProfile`; see *Python Library Reference*: Ch. 28)
    - **Training Application**: Measure throughput and latency in a Spark job using Python to analyze performance metrics, guided by concepts in *DDIA*: Ch. 1.
  - **Vertical vs. horizontal scaling trade-offs**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 1: Reliable, Scalable, and Maintainable Applications (Approaches for Coping with Load)
      - *Fundamentals of Data Engineering*: Chapter 3: Designing Good Data Architecture
    - **Technologies/Programming**: Docker (container scaling), Python (resource monitoring with `psutil`)
    - **Training Application**: Deploy a Dockerized application and compare vertical vs. horizontal scaling using Python scripts to monitor resource usage.
  - **Data partitioning techniques (e.g., range, hash)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 6: Partitioning (Partitioning by Key Range, Partitioning by Hash of Key)
      - *Mining of Massive Datasets*: Chapter 2: Map-Reduce and the New Software Stack (partitioning in MapReduce)
      - *Readings in Database Systems*: Section "New DBMS Architectures" for partitioning strategies.
    - **Technologies/Programming**: Apache Spark (partitioning data), Python (PySpark for partition management)
    - **Training Application**: Implement range and hash partitioning in Spark using PySpark to distribute a dataset, following the models in *DDIA*: Ch. 6.
- **1.1.3 Consistency and Consensus**
  - **Consistency models (e.g., eventual, strong)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 9: Consistency and Consensus (Consistency Guarantees, Linearizability)
      - *Readings in Database Systems*: Section "Weak Isolation and Distribution" for consistency trade-offs (CAP theorem).
    - **Technologies/Programming**: PostgreSQL (transaction isolation), Python (consistency checks)
    - **Training Application**: Configure PostgreSQL transaction isolation levels as discussed in *DDIA*: Ch. 7 (Weak Isolation Levels) and write Python scripts to verify consistency models.
  - **Distributed transactions and two-phase commit**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 7: Transactions (ACID), Chapter 9: Consistency and Consensus (two-phase commit)
      - *Readings in Database Systems*: Section "Weak Isolation and Distribution" for transaction protocols.
    - **Technologies/Programming**: PostgreSQL (distributed transactions), Python (SQLAlchemy for transaction management)
    - **Training Application**: Implement a two-phase commit in PostgreSQL using Python and SQLAlchemy, based on the description in *DDIA*: Ch. 9.
  - **Consensus algorithms (e.g., Paxos, Raft)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 9: Consistency and Consensus (fault-tolerant consensus, Paxos, Raft)
      - *Readings in Database Systems*: Section "Weak Isolation and Distribution" covering consensus protocols.
    - **Technologies/Programming**: Python (simulating Raft), C++ (low-level consensus implementation)
    - **Training Application**: Simulate a Raft consensus algorithm in Python; implement a simplified version in C++ for performance.
- **1.1.4 Storage and Retrieval**
  - **Data structures (e.g., B-Trees, LSM-Trees)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 3: Storage and Retrieval (Hash Indexes, SSTables and LSM-Trees, B-Trees)
      - *Readings in Database Systems*: Section "Techniques Everyone Should Know" for indexing structures.
    - **Technologies/Programming**: C (B-Tree implementation), Python (LSM-Tree simulation)
    - **Training Application**: Implement a B-Tree in C using structs and pointers (*K&R*: Ch. 6) to understand the mechanics described in *DDIA*: Ch. 3; simulate an LSM-Tree in Python.
  - **Indexing strategies (e.g., primary, secondary)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 3: Storage and Retrieval (indexing techniques, column-oriented storage)
      - *Readings in Database Systems*: Section "Techniques Everyone Should Know" for index optimization.
    - **Technologies/Programming**: PostgreSQL (index creation), Python (index performance testing)
    - **Training Application**: Create primary and secondary indexes in PostgreSQL and test their performance with Python, validating the trade-offs discussed in *DDIA*: Ch. 3.
  - **OLTP vs. OLAP systems**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 3: Storage and Retrieval (Transaction Processing or Analytics?)
      - *The Data Warehouse Toolkit*: Chapter 1: Data Warehousing, Business Intelligence, and Dimensional Modeling Primer
      - *Readings in Database Systems*: Section "Traditional RDBMS Systems" for OLTP and "New DBMS Architectures" for OLAP.
    - **Technologies/Programming**: PostgreSQL (OLTP), Snowflake (OLAP), Python (query comparison)
    - **Training Application**: Compare OLTP and OLAP query performance using PostgreSQL and Snowflake, scripted in Python, to see the practical differences outlined in *DDIA*: Ch. 3.
- **1.1.5 Encoding and Evolution**
  - **Schema evolution principles**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 4: Encoding and Evolution (The Merits of Schemas, Modes of Dataflow)
    - **Technologies/Programming**: Apache Avro (schema management), Python (Avro serialization)
    - **Training Application**: Implement schema evolution using Avro in Python to handle data versioning, as described in *DDIA*: Ch. 4.
  - **Data formats (e.g., Avro, Protobuf, JSON)**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 4: Encoding and Evolution (JSON, XML, Thrift, Protocol Buffers, Avro)
    - **Technologies/Programming**: Python (Avro, Protobuf libraries), JSON parsing (see *Python Library Reference*: Ch. 20.2 `json`)
    - **Training Application**: Serialize and deserialize data in Avro, Protobuf, and JSON using Python, comparing their performance and features as discussed in *DDIA*: Ch. 4.
  - **Backward and forward compatibility**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 4: Encoding and Evolution (schema evolution compatibility)
    - **Technologies/Programming**: Python (Avro for compatibility), JSON Schema
    - **Training Application**: Implement backward and forward compatibility for a dataset using Avro in Python.
- **Practice**: Design a distributed system architecture with fault tolerance and scalability using PostgreSQL and Python.
- **Duration**: 4-6 weeks.

### Section 1.2: Modern Data Engineering Lifecycle

- **Books**: *Fundamentals of Data Engineering* by Joe Reis and Matt Housley, *Analytics Engineering with SQL and dbt* by Rui Machado and Hélder Russa, *Designing Data-Intensive Applications* by Martin Kleppmann
- **1.2.1 Data Engineering Overview**
  - **Role and responsibilities of data engineers**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 1: Data Engineering Described
      - *Analytics Engineering with SQL and dbt*: Chapter 1: Analytics Engineering
    - **Technologies/Programming**: None (theoretical)
    - **Training Application**: Write a Python script to document data engineering workflows based on the roles defined in *Fundamentals of Data Engineering*.
  - **Data lifecycle stages (generation, storage, processing, analysis)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle
    - **Technologies/Programming**: Python (workflow simulation)
    - **Training Application**: Simulate the data lifecycle stages using Python scripts to mimic the flow described in *Fundamentals of Data Engineering*: Ch. 2.
  - **Modern data stack components (e.g., ingestion, storage, compute)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 3: Designing Good Data Architecture (Modern Data Stack)
    - **Technologies/Programming**: Python (tool integration), Docker
    - **Training Application**: Deploy a modern data stack with Docker and Python to integrate ingestion, storage, and compute tools.
- **1.2.2 Data Ingestion**
  - **Batch vs. streaming ingestion**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 7: Ingestion
      - *Designing Data-Intensive Applications*: Chapter 10: Batch Processing, Chapter 11: Stream Processing
      - *Streaming Systems*: Chapter 1: Streaming 101 (bounded vs. unbounded data)
    - **Technologies/Programming**: Apache Kafka (streaming), Python (batch processing with Pandas, see *Python for Data Analysis*: Ch. 6)
    - **Training Application**: Implement batch ingestion with Pandas and streaming ingestion with Kafka using Python, contrasting the approaches discussed in *DDIA*.
  - **Tools (e.g., Apache Kafka, AWS Kinesis)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 7: Ingestion
      - *Streaming Systems*: Chapter 10: The Evolution of Large-Scale Data Processing (Kafka, Flume)
    - **Technologies/Programming**: Apache Kafka, AWS SDK for Python (boto3)
    - **Training Application**: Ingest data using Kafka and AWS Kinesis with Python scripts.
  - **Data quality validation (e.g., schema checks, completeness)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle (Data Management section)
      - *Analytics Engineering with SQL and dbt*: Chapter 2: Data Modeling for Analytics (Testing Your Data Models)
    - **Technologies/Programming**: Python (Great Expectations for validation), dbt (schema tests)
    - **Training Application**: Validate data quality using Great Expectations in Python and implement schema tests as described in *Analytics Engineering with SQL and dbt*: Ch. 2.
- **1.2.3 Data Storage**
  - **Data lakes (e.g., S3, GCS)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 6: Storage (Data Lake)
    - **Technologies/Programming**: AWS S3, Google Cloud Storage, Python (boto3, google-cloud-storage)
    - **Training Application**: Store datasets in S3 and GCS using Python SDKs.
  - **Data warehouses (e.g., Snowflake, BigQuery)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 6: Storage (Data Warehouse)
      - *The Data Warehouse Toolkit*: Chapter 1: Data Warehousing, Business Intelligence, and Dimensional Modeling Primer
    - **Technologies/Programming**: Snowflake, BigQuery, SQL
    - **Training Application**: Query data in Snowflake and BigQuery using SQL, applying dimensional modeling concepts from *The Data Warehouse Toolkit*.
  - **Lakehouses (e.g., Delta Lake, Apache Iceberg)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 6: Storage (The Data Lakehouse)
    - **Technologies/Programming**: Delta Lake, Apache Iceberg, Python (PySpark)
    - **Training Application**: Implement a lakehouse using Delta Lake and PySpark.
- **1.2.4 Data Transformation**
  - **ETL vs. ELT processes**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 8: Queries, Modeling, and Transformation (ETL vs. ELT)
      - *Analytics Engineering with SQL and dbt*: Chapter 1: Analytics Engineering (The Legacy Processes)
      - *The Data Warehouse Toolkit*: Chapter 1: Data Warehousing, Business Intelligence, and Dimensional Modeling Primer (ETL System)
    - **Technologies/Programming**: Python (Pandas for ETL; see *Python for Data Analysis*: Ch. 7 & 8), dbt (ELT)
    - **Training Application**: Build an ETL pipeline with Pandas and an ELT pipeline with dbt.
  - **Transformation tools (e.g., dbt, Apache Spark)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 8: Queries, Modeling, and Transformation
      - *Analytics Engineering with SQL and dbt*: Chapter 4: Data Transformation with dbt
    - **Technologies/Programming**: dbt, Apache Spark, Python (PySpark)
    - **Training Application**: Transform data using dbt and Spark with PySpark.
  - **Workflow orchestration (e.g., Apache Airflow)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle (Orchestration)
    - **Technologies/Programming**: Apache Airflow, Python
    - **Training Application**: Orchestrate a transformation pipeline using Airflow and Python.
- **1.2.5 Data Serving**
  - **Serving layers (e.g., REST APIs, dashboards)**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 9: Serving Data for Analytics, Machine Learning, and Reverse ETL
    - **Technologies/Programming**: Python (FastAPI for REST APIs), Tableau (dashboards)
    - **Training Application**: Build a REST API with FastAPI and a dashboard with Tableau.
  - **Real-time analytics with tools like Druid**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 9: Serving Data for Analytics, Machine Learning, and Reverse ETL
      - *Designing Data-Intensive Applications*: Chapter 11: Stream Processing
    - **Technologies/Programming**: Apache Druid, Python
    - **Training Application**: Implement real-time analytics with Druid using Python to query streaming data.
- **Practice**: Build an ETL pipeline using Python, Airflow, and dbt, ingesting data into a data lake.
- **Technology**: Python, Apache Airflow, dbt.
- **Duration**: 4-6 weeks.

### Section 1.3: Programming for Data Engineering

- **Books**: *Python for Data Analysis* by Wes McKinney, *SQL for Data Scientists* by Renee M. P. Teate, *The C Programming Language* by Kernighan and Ritchie, *The Rust Programming Language*
- **1.3.1 Python Basics**
  - **Data types and structures (e.g., lists, dictionaries)**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 3: Built-In Data Structures, Functions, and Files
      - **Python 3.13 Docs (tutorial.pdf)**: Chapters 3, 4, 5 for a comprehensive introduction to data structures, control flow, and modules.
      - **Python 3.13 Docs (library.pdf)**: Chapter 4: "Built-in Types" for an authoritative reference.
      - **Python 3.13 Docs (howto-functional.pdf)**: To introduce functional programming concepts like iterators and generators, which are fundamental to efficient data processing.
    - **Technologies/Programming**: Python (core syntax; see *Python Tutorial*: Ch. 3 & 5)
    - **Training Application**: Implement list and dictionary operations in Python for data processing.
  - **Control flow (e.g., loops, conditionals)**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 2: Python Language Basics, IPython, and Jupyter Notebooks
    - **Technologies/Programming**: Python (core syntax; see *Python Tutorial*: Ch. 4)
    - **Training Application**: Write Python scripts with loops and conditionals to process datasets.
  - **Functions and object-oriented programming**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 3: Built-In Data Structures, Functions, and Files
    - **Technologies/Programming**: Python (OOP with classes; see *Python Tutorial*: Ch. 9)
    - **Training Application**: Create a Python class for data pipeline components.
- **1.3.2 Data Manipulation with Pandas**
  - **DataFrames and Series operations**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 5: Getting Started with pandas
    - **Technologies/Programming**: Python (Pandas)
    - **Training Application**: Perform DataFrame operations in Pandas for data cleaning.
  - **Indexing, merging, and aggregation**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 8: Data Wrangling: Join, Combine, and Reshape, Chapter 10: Data Aggregation and Group Operations
    - **Technologies/Programming**: Python (Pandas)
    - **Training Application**: Merge and aggregate datasets using Pandas.
  - **Data cleaning and preparation**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 7: Data Cleaning and Preparation
    - **Technologies/Programming**: Python (Pandas)
    - **Training Application**: Clean a dataset with missing values using Pandas.
- **1.3.3 NumPy for Numerical Computing**
  - **Array creation and manipulation**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 4: NumPy Basics: Arrays and Vectorized Computation
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Create and manipulate arrays in NumPy for numerical tasks.
  - **Broadcasting and vectorized operations**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 4: NumPy Basics: Arrays and Vectorized Computation
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Implement vectorized operations in NumPy for performance optimization.
- **1.3.4 SQL Fundamentals**
  - **SELECT statements and filtering**
    - **Chapters**:
      - *SQL for Data Scientists*: Chapter 2: The SELECT Statement, Chapter 3: The WHERE Clause
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Write SELECT queries with filtering in PostgreSQL.
  - **JOINs (e.g., inner, outer)**
    - **Chapters**:
      - *SQL for Data Scientists*: Chapter 5: SQL JOINs
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Perform JOIN operations in PostgreSQL for data integration.
  - **Window functions**
    - **Chapters**:
      - *SQL for Data Scientists*: Chapter 7: Window Functions and Subqueries
      - *Analytics Engineering with SQL and dbt*: Chapter 3: SQL for Analytics (Window Functions)
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Implement window functions in PostgreSQL for running totals.
- **1.3.5 Advanced SQL**
  - **Indexing for performance**
    - **Chapters**:
      - *Designing Data-Intensive Applications*: Chapter 3: Storage and Retrieval
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Optimize query performance with indexes in PostgreSQL.
  - **Query optimization techniques**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Query Optimization"
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Rewrite inefficient SQL queries for performance in PostgreSQL.
  - **Stored procedures and triggers**
    - **Chapters**:
      - *SQL for Data Scientists*: Chapter 14: Storing and Modifying Data
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Create stored procedures and triggers in PostgreSQL.
- **1.3.6 Low-Level Programming**
  - **Pointers and memory allocation**
    - **Chapters**:
      - *The C Programming Language*: Chapter 5: Pointers and Arrays, Chapter 8: The UNIX System Interface (Storage Allocator)
      - *The Rust Programming Language*: Chapter 4: Understanding Ownership, Chapter 15: Smart Pointers
      - *The Rust Reference*: Section 10.1.13: Pointer types, Section 13.1: Memory allocation and lifetime
      - **Computer Organization and Design (Patterson & Hennessy)**: Chapter 5: "Large and Fast: Exploiting Memory Hierarchy".
    - **Technologies/Programming**: C (pointer arithmetic), Rust (ownership, smart pointers)
    - **Training Application**: Implement a dynamic array in C using pointers and memory allocation; rewrite it in Rust using smart pointers to compare memory safety models. Then, write a simple C program that demonstrates cache misses vs. cache hits (e.g., by iterating through a large 2D array row-wise vs. column-wise) and explain the performance difference using concepts from Patterson & Hennessy, Chapter 5.
  - **System calls in C**
    - **Chapters**:
      - *The C Programming Language*: Chapter 7: Input and Output, Chapter 8: The UNIX System Interface
    - **Technologies/Programming**: C (system calls)
    - **Training Application**: Write C code to interact with file systems using system calls.
- **Practice**: Clean and analyze a dataset with Python (Pandas, NumPy); write complex SQL queries in PostgreSQL; implement a C program for memory management.
- **Technology**: Python (Pandas, NumPy), PostgreSQL, C, Rust.
- **Duration**: 5-7 weeks.

### Section 1.4: Open-Source Technologies

- **Books**: *Designing Data-Intensive Applications* by Martin Kleppmann, *Readings in Database Systems (The "Red Book")* edited by Bailis, Hellerstein, and Stonebraker, *Python for Data Analysis* by Wes McKinney
- **1.4.1 PostgreSQL Setup and Management**
  - **Installation and configuration**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Traditional RDBMS Systems" (PostgreSQL architecture)
    - **Technologies/Programming**: PostgreSQL (configuration), Bash (installation scripts)
    - **Training Application**: Install and configure PostgreSQL using Bash scripts.
  - **User and permission management**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Traditional RDBMS Systems" (access control)
    - **Technologies/Programming**: SQL (PostgreSQL), Python (psycopg2 for user management)
    - **Training Application**: Manage PostgreSQL users and permissions with SQL and Python.
- **1.4.2 Database Design**
  - **Normalization (e.g., 1NF, 2NF, 3NF)**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Techniques Everyone Should Know" (normalization)
      - *Designing Data-Intensive Applications*: Chapter 2: Data Models and Query Languages (Relational Model vs Document Model)
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Design a normalized database schema in PostgreSQL.
  - **Indexing and schema design**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Techniques Everyone Should Know" (indexing)
      - *Designing Data-Intensive Applications*: Chapter 3: Storage and Retrieval
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Create indexes for a PostgreSQL schema to optimize queries.
- **1.4.3 Python Integration**
  - **Libraries (e.g., psycopg2, SQLAlchemy)**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 6: Data Loading, Storage, and File Formats
    - **Technologies/Programming**: Python (psycopg2, SQLAlchemy)
    - **Training Application**: Connect to PostgreSQL using psycopg2 and SQLAlchemy in Python.
  - **CRUD operations via Python**
    - **Chapters**:
      - *Python for Data Analysis*: Chapter 6: Data Loading, Storage, and File Formats
    - **Technologies/Programming**: Python (psycopg2, SQLAlchemy)
    - **Training Application**: Implement CRUD operations in PostgreSQL using Python.
- **Practice**: Set up PostgreSQL, design a schema, and use Python to perform CRUD operations.
- **Technology**: PostgreSQL, Python (psycopg2, SQLAlchemy).
- **Duration**: 2-3 weeks.

### Section 1.5: Mathematical Foundations

- **Books**: *Mathematics for Machine Learning* by Deisenroth et al., *Calculus, Vol. I and II* by Tom M. Apostol, *Concrete Mathematics* by Graham, Knuth, and Patashnik
- **1.5.1 Linear Algebra Basics**
  - **Vectors and matrices**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 2: Linear Algebra
      - *Linear Algebra and Its Applications*: Chapter 1: Vector Equations, Chapter 2: Matrix Algebra
      - *Linear Algebra Done Right*: Chapter 1: Vector Spaces, Chapter 2: Finite-Dimensional Vector Spaces
      - *Calculus, Vol. I*: Chapter 13: Vector Algebra
    - **Technologies/Programming**: Python (NumPy; see *Python for Data Analysis*: Ch. 4)
    - **Training Application**: Perform vector and matrix operations in NumPy for data transformations.
  - **Matrix operations (e.g., addition, multiplication)**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 2: Linear Algebra
      - *Linear Algebra and Its Applications*: Chapter 2: Matrix Operations
      - *Linear Algebra Done Right*: Chapter 3: Linear Maps
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Implement matrix multiplication in NumPy for data processing.
- **1.5.2 Vector Calculus**
  - **Gradients and partial derivatives**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 5: Vector Calculus
      - *Calculus, Vol. I*: Chapter 5: Differential Calculus
      - *Calculus, Vol. II*: Part III: Nonlinear Analysis (Differential Calculus of Scalar and Vector Fields)
      - **Introduction to Calculus and Analysis Vol II (Courant & John)**: Chapter 1: "Functions of Several Variables and Their Derivatives" and Chapter 3: "Developments and Applications of the Differential Calculus".
    - **Technologies/Programming**: Python (SymPy for symbolic computation)
    - **Training Application**: Compute gradients using SymPy, a key step in optimization algorithms covered in *Mathematics for Machine Learning*: Ch. 7. Solve selected exercises from Courant & John Vol II, Chapter 3 to build a stronger theoretical intuition for how gradients relate to surfaces and optimization.
  - **Optimization basics (e.g., minima, maxima)**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 7: Continuous Optimization
      - *Calculus, Vol. I*: Chapter 5: Applications of differentiation to extreme values
    - **Technologies/Programming**: Python (SciPy for optimization)
    - **Training Application**: Find minima/maxima of a function using `scipy.optimize`, applying the theory from *Calculus, Vol. I*.
- **1.5.3 Probability Basics**
  - **Probability spaces and axioms**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 6: Probability and Distribution
      - *Introduction to Probability* (Bertsekas & Tsitsiklis): Chapter 1: Sample Space and Probability
      - *Introduction to Probability* (Blitzstein & Hwang): Chapter 1: Probability and Counting
      - *All of Statistics*: Chapter 1: Probability
    - **Technologies/Programming**: Python (SciPy for probability distributions)
    - **Training Application**: Simulate probability spaces and verify axioms using SciPy.
  - **Random variables and distributions (e.g., normal, binomial)**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 6: Probability and Distribution
      - *Introduction to Probability* (Bertsekas & Tsitsiklis): Chapter 2: Discrete Random Variables, Chapter 3: General Random Variables
      - *Introduction to Probability* (Blitzstein & Hwang): Chapter 3: Random Variables and Their Distributions
      - *All of Statistics*: Chapter 2: Random Variables
    - **Technologies/Programming**: Python (SciPy for distributions)
    - **Training Application**: Model normal and binomial distributions in SciPy and calculate probabilities.
- **1.5.4 Calculus Foundations**
  - **Limits, derivatives, integrals**
    - **Chapters**:
      - *Calculus, Vol. I*: Chapter 4: Continuous Functions (limits), Chapter 5: Differential Calculus (derivatives), Chapter 2: The Concepts of Integral Calculus
      - *Concrete Mathematics*: Chapter 2: Sums (discrete analogs to integrals)
    - **Technologies/Programming**: Python (SymPy for calculus)
    - **Training Application**: Compute limits, derivatives, and integrals using SymPy to solve problems from *Apostol's Calculus*.
  - **Multivariable calculus for optimization**
    - **Chapters**:
      - *Calculus, Vol. II*: Part III: Nonlinear Analysis (Applications of the Differential Calculus)
    - **Technologies/Programming**: Python (SymPy, SciPy)
    - **Training Application**: Solve multivariable optimization problems using SciPy, applying concepts of gradients from *Calculus, Vol. II*.
- **Practice**: Solve exercises on matrix operations, gradients, probability, and multivariable calculus using Python (NumPy, SciPy, SymPy).
- **Technology**: Python (NumPy, SciPy, SymPy).
- **Duration**: 4-6 weeks.

### Section 1.6: Introduction to Deep Learning Data Needs

- **Books**: *Deep Learning with Python* by François Chollet, *Designing Machine Learning Systems* by Chip Huyen
- **1.6.1 Fundamentals of Machine Learning**
  - **Supervised vs. unsupervised learning**
    - **Chapters**:
      - *Deep Learning with Python*: Chapter 5: Fundamentals of machine learning
      - *Designing Machine Learning Systems*: Chapter 1: Overview of Machine Learning Systems
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Implement supervised and unsupervised models using scikit-learn on a sample dataset.
  - **Overfitting and model evaluation metrics**
    - **Chapters**:
      - *Deep Learning with Python*: Chapter 5: Fundamentals of machine learning
      - *Designing Machine Learning Systems*: Chapter 6: Model Development and Offline Evaluation
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Evaluate models for overfitting using scikit-learn metrics as described in *Deep Learning with Python*: Ch. 5.
- **1.6.2 Data Preprocessing for Neural Networks**
  - **Normalization and standardization**
    - **Chapters**:
      - *Deep Learning with Python*: Chapter 5: Fundamentals of machine learning
      - *Designing Machine Learning Systems*: Chapter 5: Feature Engineering
    - **Technologies/Programming**: Python (scikit-learn, Keras)
    - **Training Application**: Normalize and standardize data using `sklearn.preprocessing` before feeding it into a Keras model.
  - **Encoding categorical data and handling missing values**
    - **Chapters**:
      - *Deep Learning with Python*: Chapter 5: Fundamentals of machine learning
      - *Designing Machine Learning Systems*: Chapter 5: Feature Engineering
    - **Technologies/Programming**: Python (Pandas, scikit-learn)
    - **Training Application**: Use Pandas for one-hot encoding and scikit-learn for imputing missing values, a common task discussed in *Designing ML Systems*: Ch. 5.
- **Practice**: Preprocess a dataset for a neural network using Python (Keras, scikit-learn, Pandas).
- **Technology**: Python (Keras, scikit-learn, Pandas).
- **Duration**: 1-2 weeks.

---

## Phase 2: Data Modeling and Transformation (3-4 months)

**Objective**: Master data modeling, transformation, and advanced mathematics.

### Section 2.1: Analytical Data Modeling

- **Books**: *The Data Warehouse Toolkit* by Ralph Kimball, *Analytics Engineering with SQL and dbt* by Rui Machado and Hélder Russa
- **2.1.1 Dimensional Modeling**
  - **Fact and dimension tables**
    - **Chapters**:
      - *The Data Warehouse Toolkit*: Chapter 1: Data Warehousing, Business Intelligence, and Dimensional Modeling Primer, Chapter 2: Kimball Dimensional Modeling Techniques Overview
      - *Analytics Engineering with SQL and dbt*: Chapter 2: Data Modeling for Analytics
    - **Technologies/Programming**: SQL (PostgreSQL), dbt
    - **Training Application**: Design fact and dimension tables in PostgreSQL using dbt, following the four-step process from *The Data Warehouse Toolkit*: Ch. 2.
  - **Star schema design**
    - **Chapters**:
      - *The Data Warehouse Toolkit*: Chapter 1: Fact Tables and Dimensions Joined in a Star Schema
      - *Analytics Engineering with SQL and dbt*: Chapter 2: Modeling with the Star Schema
      - *Fundamentals of Data Engineering*: Chapter 8: Queries, Modeling, and Transformation (Techniques for Modeling Batch Analytical Data)
      - **Fundamentals of Data Engineering (Reis & Housley)**: Chapter 8: "Queries, Modeling, and Transformation", section on "Techniques for Modeling Batch Analytical Data".
    - **Technologies/Programming**: SQL (PostgreSQL), dbt
    - **Training Application**: Implement a star schema in PostgreSQL with dbt.
- **2.1.2 Slowly Changing Dimensions**
  - **Type 1, Type 2, and Type 3 changes**
    - **Chapters**:
      - *The Data Warehouse Toolkit*: Chapter 5: Procurement (Slowly Changing Dimension Basics)
    - **Technologies/Programming**: SQL (PostgreSQL), dbt
    - **Training Application**: Implement Type 1, 2, and 3 SCDs in PostgreSQL using dbt, as detailed in *The Data Warehouse Toolkit*.
- **2.1.3 Advanced Modeling Techniques**
  - **Snowflake schemas**
    - **Chapters**:
      - *The Data Warehouse Toolkit*: Chapter 3: Resisting Normalization Urges (Snowflake Schemas)
      - *Analytics Engineering with SQL and dbt*: Chapter 2: Modeling with the Snowflake Schema
    - **Technologies/Programming**: SQL (PostgreSQL), dbt
    - **Training Application**: Design a snowflake schema in PostgreSQL with dbt.
  - **Bridge tables and hierarchies**
    - **Chapters**:
      - *The Data Warehouse Toolkit*: Chapter 2: Kimball Dimensional Modeling Techniques Overview (Dealing with Dimension Hierarchies, Multivalued Dimensions and Bridge Tables)
    - **Technologies/Programming**: SQL (PostgreSQL), dbt
    - **Training Application**: Create bridge tables for hierarchies in PostgreSQL using dbt.
- **Practice**: Design a star schema for a retail sales use case using PostgreSQL and dbt.
- **Technology**: PostgreSQL, dbt.
- **Duration**: 4-6 weeks.

### Section 2.2: Modern Data Transformation

- **Books**: *Analytics Engineering with SQL and dbt* by Rui Machado and Hélder Russa, *Fundamentals of Data Engineering* by Joe Reis and Matt Housley
- **2.2.1 dbt Fundamentals**
  - **Project structure and configuration**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 4: Data Transformation with dbt (Structure of a dbt Project)
    - **Technologies/Programming**: dbt, YAML
    - **Training Application**: Configure a dbt project with YAML files (`dbt_project.yml`, `profiles.yml`).
  - **Models, tests, and documentation**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 4: Data Transformation with dbt (Models, Tests, Documentation)
    - **Technologies/Programming**: dbt, SQL
    - **Training Application**: Create dbt models, add generic and singular tests, and generate project documentation.
- **2.2.2 Version Control and CI/CD**
  - **Git workflows for dbt**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 4: Setting Up dbt Cloud with BigQuery and GitHub
    - **Technologies/Programming**: Git, Python
    - **Training Application**: Set up a Git workflow (feature branches, PRs) for a dbt project.
  - **CI/CD pipeline integration**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 4: Jobs and Deployment
    - **Technologies/Programming**: GitHub Actions, Python
    - **Training Application**: Build a CI/CD pipeline for a dbt project using GitHub Actions to run `dbt build` on pull requests.
- **2.2.3 Data Modeling with dbt**
  - **Star schema implementation**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 6: Building an End-to-End Analytics Engineering Use Case
      - *The Data Warehouse Toolkit*: Chapter 3: Retail Sales (Case Study)
    - **Technologies/Programming**: dbt, SQL (PostgreSQL)
    - **Training Application**: Implement the retail star schema from *The Data Warehouse Toolkit* using dbt models for PostgreSQL.
  - **Modular SQL and Jinja templating**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 5: dbt Advanced Topics (Dynamic SQL with Jinja, Using SQL Macros)
    - **Technologies/Programming**: dbt, Jinja
    - **Training Application**: Write modular SQL with Jinja in dbt to create reusable transformations.
- **2.2.4 Data Quality and Testing**
  - **dbt tests (uniqueness, not-null)**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 4: Data Transformation with dbt (Tests)
    - **Technologies/Programming**: dbt, SQL
    - **Training Application**: Implement uniqueness, not-null, and relationship tests on a dbt model.
  - **Documentation best practices**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 4: Data Transformation with dbt (Documentation)
    - **Technologies/Programming**: dbt
    - **Training Application**: Generate and serve documentation for a dbt project.
- **2.2.5 Supplemental Learning**
  - **Advanced dbt features (macros, semantic layer)**
    - **Chapters**:
      - *Analytics Engineering with SQL and dbt*: Chapter 5: dbt Advanced Topics (Macros, dbt Semantic Layer)
    - **Technologies/Programming**: dbt, Jinja
    - **Training Application**: Implement dbt macros for reusable logic and explore the semantic layer.
- **Practice**: Build and test a dbt project for a star schema using PostgreSQL and Git.
- **Technology**: dbt, PostgreSQL, Git.
- **Duration**: 4-6 weeks.

### Section 2.3: Orchestration and Automation

- **Books**: *Fundamentals of Data Engineering* by Joe Reis and Matt Housley
- **2.3.1 Airflow Basics**
  - **DAGs and operators**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle (Orchestration)
    - **Technologies/Programming**: Apache Airflow, Python
    - **Training Application**: Create an Airflow DAG with Python operators to run a simple data task.
  - **Task dependencies**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle (Orchestration)
    - **Technologies/Programming**: Apache Airflow, Python
    - **Training Application**: Define task dependencies in an Airflow DAG using Python.
- **2.3.2 Scheduling and Monitoring**
  - **Scheduling workflows**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle (Orchestration)
    - **Technologies/Programming**: Apache Airflow, Python
    - **Training Application**: Schedule an Airflow DAG for daily execution.
  - **Logging and alerting**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle (DataOps section)
    - **Technologies/Programming**: Apache Airflow, Python (logging; see *Python Logging HOWTO*)
    - **Training Application**: Set up logging and alerting for an Airflow pipeline.
- **2.3.3 Advanced Workflows**
  - **Dynamic DAGs and XComs**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle (Orchestration)
    - **Technologies/Programming**: Apache Airflow, Python
    - **Training Application**: Create a dynamic DAG with XComs in Airflow using Python.
  - **SubDAGs for complex workflows**
    - **Chapters**:
      - *Fundamentals of Data Engineering*: Chapter 2: The Data Engineering Lifecycle (Orchestration)
    - **Technologies/Programming**: Apache Airflow, Python
    - **Training Application**: Implement a SubDAG in Airflow for a complex pipeline.
- **Practice**: Automate an ETL pipeline with Airflow, including dbt transformations, using Python.
- **Technology**: Apache Airflow, Python.
- **Duration**: 3-4 weeks.

### Section 2.4: Advanced Mathematical Techniques

- **Books**: *Mathematics for Machine Learning* by Deisenroth et al., *Linear Algebra Done Right* by Sheldon Axler, *Numerical Analysis* by Burden and Faires, *Convex Optimization Theory* by D. P. Bertsekas, *Concrete Mathematics* by Graham, Knuth, and Patashnik
- **2.4.1 Probability and Statistics**
  - **Bayesian inference**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 6: Probability and Distribution
      - *All of Statistics*: Chapter 11: Bayesian Inference
      - *Introduction to Probability* (Bertsekas & Tsitsiklis): Chapter 8: Bayesian Statistical Inference
    - **Technologies/Programming**: Python (PyMC3 for Bayesian modeling)
    - **Training Application**: Implement Bayesian inference for a dataset using PyMC3, applying concepts from *All of Statistics*.
  - **Hypothesis testing and regression**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 8: Linear Regression
      - *All of Statistics*: Chapter 10: Hypothesis Testing and p-values, Chapter 13: Linear and Logistic Regression
      - *Introduction to Probability* (Bertsekas & Tsitsiklis): Chapter 9: Classical Parameter Estimation, Linear Regression
    - **Technologies/Programming**: Python (SciPy, statsmodels)
    - **Training Application**: Perform hypothesis testing and regression analysis using SciPy and statsmodels.
- **2.4.2 Optimization**
  - **Gradient descent variants**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 7: Continuous Optimization
    - **Technologies/Programming**: Python (SciPy, PyTorch)
    - **Training Application**: Implement gradient descent variants in PyTorch for optimization.
  - **Convex and constrained optimization**
    - **Chapters**:
      - *Mathematics for Machine Learning*: Chapter 7: Continuous Optimization
      - *Convex Optimization Theory*: Chapter 3: Basic Concepts of Convex Optimization
      - *Introduction to Linear Optimization*: Chapter 1: Introduction
      - *Linear Algebra and Its Applications*: Chapter 7: Constrained Optimization
    - **Technologies/Programming**: Python (CVXPY)
    - **Training Application**: Solve a constrained optimization problem using CVXPY, modeling it based on principles from *Convex Optimization Theory*.
- **2.4.3 Theoretical Linear Algebra**
  - **Vector spaces and linear transformations**
    - **Chapters**:
      - *Linear Algebra Done Right*: Chapter 1: Vector Spaces, Chapter 3: Linear Maps
      - *Linear Algebra and Its Applications*: Chapter 4: Vector Spaces
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Implement linear transformations in NumPy for data processing.
  - **Eigenvalues and eigenvectors**
    - **Chapters**:
      - *Linear Algebra Done Right*: Chapter 5: Eigenvalues and Eigenvectors
      - *Linear Algebra and Its Applications*: Chapter 5: Eigenvalues and Eigenvectors
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Compute eigenvalues and eigenvectors in NumPy for dimensionality reduction.
- **2.4.4 Numerical Methods**
  - **Solving Linear Systems: Gaussian elimination, Jacobi, Gauss-Seidel**
    - **Chapters**:
      - *Numerical Analysis*: Chapter 6: Direct Methods for Solving Linear Systems, Chapter 7: Iterative Techniques in Matrix Algebra
      - *Linear Algebra and Its Applications*: Chapter 1: Systems of Linear Equations
      - *Concrete Mathematics*: Chapter 2: Sums (as a foundation for iterative methods)
    - **Technologies/Programming**: Python (NumPy, SciPy)
    - **Training Application**: Implement Gaussian elimination and Gauss-Seidel solvers in NumPy based on algorithms in *Numerical Analysis*: Ch. 6 & 7.
  - **Numerical Integration: Trapezoidal rule, Simpson’s rule**
    - **Chapters**:
      - *Numerical Analysis*: Chapter 4: Numerical Differentiation and Integration
    - **Technologies/Programming**: Python (SciPy)
    - **Training Application**: Implement numerical integration using SciPy.
  - **Root-Finding: Newton-Raphson, error analysis**
    - **Chapters**:
      - *Numerical Analysis*: Chapter 2: Solutions of Equations in One Variable
    - **Technologies/Programming**: Python (SciPy)
    - **Training Application**: Implement Newton-Raphson method in SciPy for root-finding.
- **2.4.5 Convex Optimization Theory**
  - **Convex sets and functions**
    - **Chapters**:
      - *Convex Optimization Theory*: Chapter 1: Basic Concepts of Convex Analysis
    - **Technologies/Programming**: Python (CVXPY)
    - **Training Application**: Model convex sets in CVXPY for optimization problems.
  - **Optimality conditions and duality**
    - **Chapters**:
      - *Convex Optimization Theory*: Chapter 5: Duality and Optimization
      - *Introduction to Linear Optimization*: Chapter 4: Duality Theory
    - **Technologies/Programming**: Python (CVXPY)
    - **Training Application**: Solve a dual optimization problem using CVXPY.
- **Practice**: Implement gradient descent, Gauss-Seidel solver, and convex optimization in Python (NumPy, SciPy, CVXPY, PyTorch).
- **Technology**: Python (NumPy, SciPy, CVXPY, PyTorch).
- **Duration**: 6-8 weeks.

---

## Phase 3: Specialization in Real-Time or AI Systems (3-4 months)

**Objective**: Specialize in real-time or AI/ML systems with advanced mathematics.

### Section 3.1: Real-Time Data Processing (Optional Track)

- **Books**: *Streaming Systems* by Tyler Akidau et al., *Differential Equations, Dynamical Systems, and an Introduction to Chaos* by Hirsch, Smale, and Devaney
- **3.1.1 Stream Processing Fundamentals**
  - **Event time vs. processing time**
    - **Chapters**:
      - *Streaming Systems*: Chapter 1: Streaming 101 (Event Time Versus Processing Time)
    - **Technologies/Programming**: Apache Kafka, Python
    - **Training Application**: Process events in Kafka to compare event and processing times using Python.
  - **Stream-table duality**
    - **Chapters**:
      - *Streaming Systems*: Chapter 6: Streams and Tables
    - **Technologies/Programming**: Apache Kafka, SQL (Materialize)
    - **Training Application**: Implement stream-table duality using Kafka and Materialize.
- **3.1.2 Windowing and Watermarks**
  - **Window types (e.g., tumbling, sliding)**
    - **Chapters**:
      - *Streaming Systems*: Chapter 2: The What, Where, When, and How of Data Processing (Windowing), Chapter 4: Advanced Windowing
    - **Technologies/Programming**: Apache Kafka, Apache Flink
    - **Training Application**: Implement tumbling and sliding windows in Flink with Kafka.
  - **Handling late data with watermarks**
    - **Chapters**:
      - *Streaming Systems*: Chapter 3: Watermarks
      - **Introduction to Probability (Blitzstein & Hwang)**: Chapter 13: "Poisson Processes".
    - **Technologies/Programming**: Apache Kafka, Apache Flink, **Python 3.13 Docs (library.pdf)** - Chapter 9.7: statistics
    - **Training Application**: Handle late data in a streaming pipeline using Flink watermarks. Additionally, use Python's scipy.stats to model event arrivals with a Poisson process, helping to predict the expected volume of late data based on concepts from Blitzstein & Hwang.
- **3.1.3 Fault Tolerance in Streams**
  - **Exactly-once processing**
    - **Chapters**:
      - *Streaming Systems*: Chapter 5: Exactly-Once and Side Effects
    - **Technologies/Programming**: Apache Kafka, Apache Flink
    - **Training Application**: Configure exactly-once processing in Kafka and Flink.
  - **State management and recovery**
    - **Chapters**:
      - *Streaming Systems*: Chapter 7: The Practicalities of Persistent State
    - **Technologies/Programming**: Apache Kafka, Apache Flink
    - **Training Application**: Implement state recovery in a Flink streaming application.
- **3.1.4 Dynamical Systems for Streaming**
  - **Differential equations for event dynamics**
    - **Chapters**:
      - *Differential Equations, Dynamical Systems, and an Introduction to Chaos*: Chapter 1: First-Order Equations, Chapter 2: Planar Linear Systems
    - **Technologies/Programming**: Python (SciPy for ODE solving)
    - **Training Application**: Model streaming event dynamics (e.g., arrival rates) using SciPy’s ODE solvers.
  - **Chaos theory for complex systems**
    - **Chapters**:
      - *Differential Equations, Dynamical Systems, and an Introduction to Chaos*: Chapter 7: Nonlinear Systems, Chapter 14: The Lorenz System
    - **Technologies/Programming**: Python (SciPy)
    - **Training Application**: Simulate chaotic behavior (e.g., unpredictable load spikes) in streaming systems using SciPy.
- **Practice**: Build a real-time streaming pipeline with Kafka and Flink; model streaming events with differential equations using SciPy.
- **Technology**: Apache Kafka, Apache Flink, Python (SciPy).
- **Duration**: 6-8 weeks.

### Section 3.2: AI Systems and MLOps (Optional Track)

- **Books**: *Designing Machine Learning Systems* by Chip Huyen, *Deep Learning with Python* by François Chollet, *Reinforcement Learning and Optimal Control* by D. P. Bertsekas
- **3.2.1 MLOps Lifecycle**
  - **Data versioning and model training**
    - **Chapters**:
      - *Designing Machine Learning Systems*: Chapter 4: Training Data, Chapter 6: Model Development and Offline Evaluation
    - **Technologies/Programming**: DVC (data versioning), Python (scikit-learn)
    - **Training Application**: Version datasets with DVC and train models with scikit-learn.
  - **Deployment and monitoring**
    - **Chapters**:
      - *Designing Machine Learning Systems*: Chapter 7: Model Deployment and Prediction Service, Chapter 8: Data Distribution Shifts and Monitoring
      - **Fundamentals of Data Engineering (Reis & Housley)**: Chapter 2: "The Data Engineering Lifecycle", section on "DataOps".
    - **Technologies/Programming**: Docker, Prometheus, Python (howto-logging.pdf and howto-logging-cookbook.pdf)
    - **Training Application**: Deploy a model with Docker and monitor with Prometheus. Implement structured logging within the prediction service using Python's logging module, following the best practices in howto-logging-cookbook.txt, to create monitorable, parseable logs for Prometheus.
- **3.2.2 Feature Engineering for ML**
  - **Feature stores and embeddings**
    - **Chapters**:
      - *Designing Machine Learning Systems*: Chapter 5: Feature Engineering
      - *Deep Learning with Python*: Chapter 11: Deep learning for text (for embeddings)
      - *Mathematics for Machine Learning*: Chapter 9: Dimensionality Reduction with Principal Component Analysis
    - **Technologies/Programming**: Feast (feature store), Python
    - **Training Application**: Implement a feature store with Feast for ML pipelines.
  - **Data augmentation techniques**
    - **Chapters**:
      - *Designing Machine Learning Systems*: Chapter 4: Training Data
      - *Deep Learning with Python*: Chapter 9: Advanced deep learning for computer vision
    - **Technologies/Programming**: Python (Keras)
    - **Training Application**: Apply data augmentation for text data in Keras.
- **3.2.3 Deep Learning for Text**
  - **Tokenization and embeddings**
    - **Chapters**:
      - *Deep Learning with Python*: Chapter 11: Deep learning for text
    - **Technologies/Programming**: Python (Keras, Hugging Face)
    - **Training Application**: Tokenize text and generate embeddings using Hugging Face.
  - **Sequence models (e.g., RNNs, LSTMs)**
    - **Chapters**:
      - *Deep Learning with Python*: Chapter 11: Deep learning for text
    - **Technologies/Programming**: Python (Keras)
    - **Training Application**: Train an LSTM model for text classification using Keras.
- **3.2.4 Reinforcement Learning Basics**
  - **Markov decision processes**
    - **Chapters**:
      - *Reinforcement Learning and Optimal Control*: Chapter 1: Exact Dynamic Programming
    - **Technologies/Programming**: Python (Gym)
    - **Training Application**: Simulate an MDP using Gym in Python.
  - **Q-learning and policy iteration**
    - **Chapters**:
      - *Reinforcement Learning and Optimal Control*: Chapter 4: Infinite Horizon Dynamic Programming (Policy Iteration), Chapter 5: Infinite Horizon Reinforcement Learning (Q-Learning)
    - **Technologies/Programming**: Python (Gym)
    - **Training Application**: Implement Q-learning in Gym for a simple RL problem.
- **Practice**: Build an ML pipeline with Spark, deploy a text model with Docker, and implement Q-learning using Gym in Python.
- **Technologies**: Apache Spark, Docker, Python (Keras, Gym).
- **Duration**: 6-8 weeks.

### Section 3.3: Advanced Probability, Linear Algebra, and Optimization

- **Books**: *Introduction to Probability* by Blitzstein and Hwang, *Linear Algebra and Its Applications* by Gilbert Strang, *Elements of Information Theory* by Cover and Thomas, *Introduction to Linear Optimization* by Bertsimas and Tsitsiklis
- **3.3.1 Probabilistic Modeling**
  - **Markov chains and Bayesian networks**
    - **Chapters**:
      - *Introduction to Probability* (Blitzstein & Hwang): Chapter 11: Markov Chains
      - *Introduction to Probability* (Bertsekas & Tsitsiklis): Chapter 7: Markov Chains
      - *All of Statistics*: Chapter 17: Directed Graphs and Conditional Independence
    - **Technologies/Programming**: Python (pgmpy for Bayesian networks)
    - **Training Application**: Model a Markov chain and Bayesian network using pgmpy.
  - **Monte Carlo methods**
    - **Chapters**:
      - *Introduction to Probability* (Blitzstein & Hwang): Chapter 12: Markov Chain Monte Carlo
      - *All of Statistics*: Chapter 24: Simulation Methods
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Implement Monte Carlo simulations in NumPy.
- **3.3.2 Practical Linear Algebra**
  - **Matrix factorizations (e.g., QR, LU)**
    - **Chapters**:
      - *Linear Algebra and Its Applications*: Chapter 2: Matrix Factorizations
      - *Numerical Analysis*: Chapter 6: Matrix Factorization
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Perform QR and LU factorizations in NumPy.
  - **Least squares and ML applications**
    - **Chapters**:
      - *Linear Algebra and Its Applications*: Chapter 6: Orthogonality and Least Squares
      - *Mathematics for Machine Learning*: Chapter 8: Linear Regression
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Apply least squares in scikit-learn for regression.
- **3.3.3 Information Theory**
  - **Entropy and mutual information**
    - **Chapters**:
      - *Elements of Information Theory* is the primary text.
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Compute entropy and mutual information for a dataset in NumPy.
  - **Data compression (Huffman, arithmetic coding)**
    - **Chapters**:
      - *Elements of Information Theory* is the primary text.
    - **Technologies/Programming**: Python (custom implementations)
    - **Training Application**: Implement Huffman coding in Python for data compression.
- **3.3.4 Combinatorial Optimization**
  - **Linear programming (simplex method, duality)**
    - **Chapters**:
      - *Introduction to Linear Optimization*: Chapter 3: The Simplex Method, Chapter 4: Duality Theory
      - *Convex Optimization Theory*: Chapter 5: Duality and Optimization
    - **Technologies/Programming**: Python (PuLP)
    - **Training Application**: Solve a linear programming problem using PuLP.
  - **Network flows (max-flow/min-cut)**
    - **Chapters**:
      - *Introduction to Linear Optimization*: Chapter 7: Network Flow Problems
    - **Technologies/Programming**: Python (NetworkX)
    - **Training Application**: Implement max-flow/min-cut in NetworkX.
- **Practice**: Simulate a Markov chain, implement SVD, perform Huffman coding, and solve a pipeline scheduling problem using Python (NumPy, SciPy, NetworkX, PuLP).
- **Technology**: Python (NumPy, SciPy, NetworkX, PuLP, pgmpy).
- **Duration**: 6-8 weeks.

---

## Phase 4: Deep Theoretical Mastery (4-6 months)

**Objective**: Achieve deep theoretical understanding for innovation and foundational connections.

### Section 4.1: Discrete Mathematics and Algorithms

- **Books**: *Concrete Mathematics* by Graham, Knuth, and Patashnik, *Mathematics for Computer Science* by Lehman, Leighton, and Meyer
- **4.1.1 Combinatorics**
  - **Counting principles**
    - **Chapters**:
      - *Mathematics for Computer Science*: Chapter 14: Cardinality Rules
      - *Concrete Mathematics*: Chapter 5: Binomial Coefficients
    - **Technologies/Programming**: Python (itertools; see *Python Library Reference*: Ch. 10.1)
    - **Training Application**: Compute combinations using Python’s itertools.
  - **Permutations and combinations**
    - **Chapters**:
      - *Mathematics for Computer Science*: Chapter 14: Cardinality Rules
      - *Concrete Mathematics*: Chapter 5: Binomial Coefficients
    - **Technologies/Programming**: Python (itertools)
    - **Training Application**: Generate permutations in Python using itertools.
- **4.1.2 Graph Theory**
  - **Graph representations and traversals**
    - **Chapters**:
      - *Mathematics for Computer Science*: Chapter 9: Directed Graphs & Partial Orders, Chapter 11: Simple Graphs
    - **Technologies/Programming**: Python (NetworkX)
    - **Training Application**: Implement BFS and DFS in NetworkX.
  - **Shortest path algorithms (e.g., Dijkstra’s)**
    - **Chapters**:
      - *Mathematics for Computer Science*: Chapter 11: Simple Walks
    - **Technologies/Programming**: Python (NetworkX)
    - **Training Application**: Implement Dijkstra’s algorithm in NetworkX.
- **4.1.3 Recurrence Relations**
  - **Solving recurrences for algorithm analysis**
    - **Chapters**:
      - *Concrete Mathematics*: Chapter 1: Recurrent Problems, Chapter 2: Sums, Chapter 7: Generating Functions
      - *Mathematics for Computer Science*: Chapter 21: Recurrences
    - **Technologies/Programming**: Python (SymPy)
    - **Training Application**: Solve recurrences using SymPy for algorithm analysis.
- **Practice**: Solve problems on graphs and recurrences; implement Dijkstra’s algorithm using Python (NetworkX, SymPy).
- **Technology**: Python (NetworkX, SymPy).
- **Duration**: 4-6 weeks.

### Section 4.1: Database Systems Theory

- **Books**: *Readings in Database Systems (The "Red Book")* by Bailis et al., *Designing Data-Intensive Applications* by Martin Kleppmann, *Mining of Massive Datasets* by Leskovek et al.
- **4.2.1 Relational Model and Algebra**
  - **Codd’s relational model**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Traditional RDBMS Systems" (relational model foundations)
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Implement a relational model in PostgreSQL.
  - **Relational algebra operations**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Background" (relational algebra)
    - **Technologies/Programming**: SQL (PostgreSQL)
    - **Training Application**: Write relational algebra queries in SQL.
- **4.2.2 Distributed Databases**
  - **CAP theorem and trade-offs**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Weak Isolation and Distribution"
      - *Designing Data-Intensive Applications*: Chapter 9: Consistency and Consensus
    - **Technologies/Programming**: Cassandra, Python
    - **Training Application**: Configure Cassandra for eventual consistency and test with Python.
  - **ACID vs. BASE properties**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Weak Isolation and Distribution"
      - *Designing Data-Intensive Applications*: Chapter 7: Transactions
    - **Technologies/Programming**: PostgreSQL, MongoDB
    - **Training Application**: Compare ACID (PostgreSQL) and BASE (MongoDB) properties.
- **4.2.3 Big Data Systems**
  - **MapReduce and Apache Spark**
    - **Chapters**:
      - *Readings in Database Systems*: Section "Large-Scale Dataflow Engines"
      - *Mining of Massive Datasets*: Chapter 2: Map-Reduce and the New Software Stack
      - *Designing Data-Intensive Applications*: Chapter 10: Batch Processing (MapReduce)
      - *Streaming Systems*: Chapter 10: The Evolution of Large-Scale Data Processing (Hadoop, Spark)
    - **Technologies/Programming**: Apache Spark, Python (PySpark)
    - **Training Application**: Implement a MapReduce job in Spark using PySpark.
  - **NoSQL databases (e.g., Cassandra, MongoDB)**
    - **Chapters**:
      - *Readings in Database Systems*: Section "New DBMS Architectures"
      - *Designing Data-Intensive Applications*: Chapter 2: Data Models and Query Languages (The Birth of NoSQL)
    - **Technologies/Programming**: Cassandra, MongoDB, Python
    - **Training Application**: Query data in Cassandra and MongoDB using Python.
- **Practice**: Summarize the evolution of database systems; implement a MapReduce job in Spark using PySpark.
- **Technology**: Apache Spark, Cassandra, MongoDB, Python.
- **Duration**: 4-6 weeks.

### Section 4.3: Information Retrieval and Search

- **Books**: *Introduction to Information Retrieval* by Manning et al., *Mining of Massive Datasets* by Leskovek et al., *Deep Learning with Python* by François Chollet
- **4.3.1 Indexing and Retrieval Models**
  - **Inverted indexes and TF-IDF**
    - **Chapters**:
      - *Introduction to Information Retrieval*: Chapter 1: Boolean retrieval, Chapter 6: Scoring, term weighting & the vector space model
    - **Technologies/Programming**: Python (Whoosh)
    - **Training Application**: Build an inverted index with TF-IDF using Whoosh.
  - **Vector space models**
    - **Chapters**:
      - *Introduction to Information Retrieval*: Chapter 6: Scoring, term weighting & the vector space model, Chapter 14: Vector space classification
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Implement a vector space model in scikit-learn.
- **4.3.2 Evaluation Metrics**
  - **Precision, recall, and F1-score**
    - **Chapters**:
      - *Introduction to Information Retrieval*: Chapter 8: Evaluation in information retrieval
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Compute precision, recall, and F1-score for a search system using scikit-learn.
- **4.3.3 Advanced Topics**
  - **PageRank and latent semantic indexing**
    - **Chapters**:
      - *Introduction to Information Retrieval*: Chapter 18: Matrix decompositions & latent semantic indexing, Chapter 21: Link analysis
      - *Mining of Massive Datasets*: Chapter 5: Link Analysis
    - **Technologies/Programming**: Python (NetworkX)
    - **Training Application**: Implement PageRank in NetworkX.
  - **Word embeddings**
    - **Chapters**:
      - *Introduction to Information Retrieval*: Chapter 18: Matrix decompositions & latent semantic indexing
      - *Deep Learning with Python*: Chapter 11: Deep learning for text
    - **Technologies/Programming**: Python (Hugging Face)
    - **Training Application**: Generate word embeddings using Hugging Face.
- **Practice**: Build and evaluate a simple search engine in Python using Whoosh and scikit-learn.
- **Technology**: Python (Whoosh, scikit-learn, Hugging Face, NetworkX).
- **Duration**: 4-6 weeks.

### Section 4.4: Big Data Algorithms

- **Books**: *Mining of Massive Datasets* by Leskovek et al., *Introduction to Information Retrieval* by Manning et al.
- **4.4.1 Frequent Itemsets and Association Rules**
  - **Apriori and FP-Growth algorithms**
    - **Chapters**:
      - *Mining of Massive Datasets*: Chapter 6: Frequent Itemsets
    - **Technologies/Programming**: Apache Spark, Python (PySpark)
    - **Training Application**: Implement Apriori in Spark using PySpark.
- **4.4.2 Clustering and Similarity**
  - **K-means and hierarchical clustering**
    - **Chapters**:
      - *Mining of Massive Datasets*: Chapter 7: Clustering
      - *Introduction to Information Retrieval*: Chapter 16: Flat clustering, Chapter 17: Hierarchical clustering
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Apply K-means clustering in scikit-learn.
  - **Locality-sensitive hashing**
    - **Chapters**:
      - *Mining of Massive Datasets*: Chapter 3: Finding Similar Items
    - **Technologies/Programming**: Python (custom implementations)
    - **Training Application**: Implement LSH in Python for similarity search.
- **4.4.3 Recommendation Systems**
  - **Collaborative filtering**
    - **Chapters**:
      - *Mining of Massive Datasets*: Chapter 9: Recommendation Systems
    - **Technologies/Programming**: Apache Spark, Python (PySpark)
    - **Training Application**: Build a collaborative filtering system in Spark.
  - **Matrix factorization techniques**
    - **Chapters**:
      - *Mining of Massive Datasets*: Chapter 9: Recommendation Systems
      - *Introduction to Information Retrieval*: Chapter 18: Matrix decompositions & latent semantic indexing
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Implement matrix factorization in scikit-learn for recommendations.
- **Practice**: Build a recommendation system with Spark and PySpark.
- **Technology**: Apache Spark, Python (PySpark, scikit-learn).
- **Duration**: 4-6 weeks.

### Section 4.5: Hardware and Systems Programming

- **Books**: *Computer Organization and Design* by Patterson and Hennessy, *The C Programming Language* by Kernighan and Ritchie
- **4.5.1 Memory Hierarchy**
  - **Caching and virtual memory**
    - **Chapters**:
      - *Computer Organization and Design*: Chapter 5: Large and Fast: Exploiting Memory Hierarchy
    - **Technologies/Programming**: C (memory management), Python 3.13 Docs (howto-perf_profiling.pdf)
    - **Training Application**: Simulate caching behavior in C. Then, write a Python version of the same logic and use the Linux perf profiler as described in howto-perf_profiling.txt to see if cache effects are visible even at the interpreter level. Discuss why or why not.
  - **Memory management strategies**
    - **Chapters**:
      - *Computer Organization and Design*: Chapter 5: Large and Fast: Exploiting Memory Hierarchy
      - *The C Programming Language*: Chapter 5: Pointers and Arrays, Chapter 8: The UNIX System Interface (A Storage Allocator)
    - **Technologies/Programming**: C (malloc, free)
    - **Training Application**: Implement memory allocation strategies in C.
- **Practice**: Analyze cache performance for a data query using C.
- **Technology**: C.
- **Duration**: 2-3 weeks.

### Section 4.6: Advanced Statistics, Linear Algebra, and Optimization

- **Books**: *All of Statistics* by Larry Wasserman, *Linear Algebra Done Right* by Sheldon Axler, *Introduction to Stochastic Processes* by Gregory F. Lawler, *The Design of Approximation Algorithms* by Williamson and Shmoys, *Linear Algebra and Its Applications* by David C. Lay

- **4.6.1 Statistical Inference**
  
  - **Hypothesis testing and confidence intervals**
    - **Chapters**:
      - *All of Statistics*: Chapter 10: Hypothesis Testing and p-values
    - **Technologies/Programming**: Python (SciPy, statsmodels)
    - **Training Application**: Perform hypothesis testing in statsmodels.
  - **Regression analysis**
    - **Chapters**:
      - *All of Statistics*: Chapter 13: Linear and Logistic Regression
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Implement regression models in scikit-learn.

- **4.6.2 Advanced Linear Algebra**
  
  - **Inner product spaces**
    - **Chapters**:
      - *Linear Algebra Done Right*: Chapter 6: Inner Product Spaces
      - *Linear Algebra and Its Applications*: Chapter 6: Orthogonality and Least Squares
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Compute inner products in NumPy for data analysis.
  - **Singular value decomposition (SVD)**
    - **Chapters**:
      - *Linear Algebra Done Right*: Chapter 7: Operators on Inner Product Spaces
      - *Linear Algebra and Its Applications*: Chapter 7: The Singular Value Decomposition
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Implement SVD in NumPy for dimensionality reduction.

- **4.6.3 Stochastic Processes**
  
  - **Markov chains: Transition matrices, steady states**
    
    - **Chapters**:
      - *Introduction to Stochastic Processes*: Chapter 1: Finite Markov Chains
      - *Introduction to Probability* (Bertsekas & Tsitsiklis): Chapter 7: Markov Chains
      - *Introduction to Probability* (Blitzstein & Hwang): Chapter 11: Markov Chains
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Simulate a Markov chain with transition matrices in NumPy.
  
  - **Poisson processes: Event modeling for streaming**
    
    - **Chapters**:
      
      - *Introduction to Stochastic Processes*: Chapter 6: Renewal Processes (as a generalization)
      
      - *Introduction to Probability* (Bertsekas & Tsitsiklis): Chapter 6: The Bernoulli and Poisson Processes
      
      - *Introduction to Probability* (Blitzstein & Hwang): Chapter 13: Poisson Processes
        
        Introduction to Probability (Bertsekas & Tsitsiklis: Chapter 6: "The Bernoulli and Poisson Processes".
        
        Introduction to Probability (Blitzstein & Hwang: Chapter 13: "Poisson Processes".
    
    - **Technologies/Programming**: Python (SciPy)
    
    - **Training Application**: Model a Poisson process for streaming events in SciPy.
  
  - **Queuing theory: System performance analysis**
    
    - **Chapters**:
      - *Introduction to Stochastic Processes*: Chapter 3: Continuous-Time Markov Chains (relates to queuing)
      - **Introduction to Stochastic Processes (Lawler)**: Chapter 3: "Continuous-Time Markov Chains", as it provides the foundation for many queuing models (e.g., M/M/1 queues).
    - **Technologies/Programming**: Python (SciPy)
    - **Training Application**: Analyze queue performance using SciPy. Simulate a simple M/M/1 queue in Python to model a data processing service. Analyze wait times and system load, applying principles from Lawler's chapter on continuous-time Markov chains.

- **4.6.4 Heuristic and Approximation Algorithms**
  
  - **Greedy algorithms for clustering and scheduling**
    - **Chapters**:
      - *The Design of Approximation Algorithms*: Chapter 2: Greedy Algorithms and Local Search
    - **Technologies/Programming**: Python (scikit-learn)
    - **Training Application**: Implement a greedy clustering algorithm in scikit-learn.
  - **Randomized algorithms for scalability**
    - **Chapters**:
      - *The Design of Approximation Algorithms*: Chapter 5: Random Sampling and Randomized Rounding of Linear Programs
    - **Technologies/Programming**: Python (NumPy)
    - **Training Application**: Implement a randomized algorithm for scalability in NumPy.

- **Practice**: Perform statistical analysis, implement SVD, simulate a Poisson process, and implement a greedy clustering algorithm using Python (NumPy, SciPy, scikit-learn) and Spark.

- **Technology**: Python (NumPy, SciPy, scikit-learn), Apache Spark.

- **Duration**: 6-8 weeks.

---

## Additional Recommendations

- **Time Management**: Allocate 10-15 hours weekly (60% reading, 30% coding/projects, 10% math exercises).
- **Community Engagement**: Join dbt Community (https://www.getdbt.com/community) and follow *Data Engineering Weekly* (https://dataengineeringweekly.substack.com/) for updates.
- **Portfolio Project**: Build an end-to-end data pipeline for an AI model (e.g., recommendation system) using dbt, Spark, Docker, and optimization techniques.
- **Supplemental Resources**: Use dbt Labs documentation (https://docs.getdbt.com/) and MIT OpenCourseWare (https://ocw.mit.edu/) for advanced topics.

## Summary

This enhanced course structure integrates specific chapters from books in "aggregated_reductions.txt," ensuring necessary and sufficient content for each item. Technologies and programming languages (e.g., Python, SQL, C, Apache Spark, dbt) are assigned to train each item, providing practical applications for both concrete and abstract concepts. The curriculum aligns with your goals of mastering data engineering, advanced mathematics, and AI systems, with minimal deep learning focus as requested.
