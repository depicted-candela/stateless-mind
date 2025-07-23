# Fundamentals of Data Engineering: Plan and Build Robust Data Systems

## Table of Contents

Preface. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xiii

### Part I. Foundation and Building Blocks

1. **Data Engineering Described**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3  
   What Is Data Engineering? 3  
   Data Engineering Defined 4  
   The Data Engineering Lifecycle 5  
   Evolution of the Data Engineer 6  
   Data Engineering and Data Science 11  
   Data Engineering Skills and Activities 13  
   Data Maturity and the Data Engineer 13  
   The Background and Skills of a Data Engineer 17  
   Business Responsibilities 18  
   Technical Responsibilities 19  
   The Continuum of Data Engineering Roles, from A to B 21  
   Data Engineers Inside an Organization 22  
   Internal-Facing Versus External-Facing Data Engineers 23  
   Data Engineers and Other Technical Roles 24  
   Data Engineers and Business Leadership 28  
   Conclusion 31  
   Additional Resources 32  

2. **The Data Engineering Lifecycle**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33  
   What Is the Data Engineering Lifecycle? 33  
   The Data Lifecycle Versus the Data Engineering Lifecycle 34  
   Generation: Source Systems 35  
   Storage 38  
   Ingestion 39  
   Transformation 43  
   Serving Data 44  
   Major Undercurrents Across the Data Engineering Lifecycle 48  
   Security 49  
   Data Management 50  
   DataOps 59  
   Data Architecture 64  
   Orchestration 64  
   Software Engineering 66  
   Conclusion 68  
   Additional Resources 69  

3. **Designing Good Data Architecture**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 71  
   What Is Data Architecture? 71  
   Enterprise Architecture Defined 72  
   Data Architecture Defined 75  
   “Good” Data Architecture 76  
   Principles of Good Data Architecture 77  
   Principle 1: Choose Common Components Wisely 78  
   Principle 2: Plan for Failure 79  
   Principle 3: Architect for Scalability 80  
   Principle 4: Architecture Is Leadership 80  
   Principle 5: Always Be Architecting 81  
   Principle 6: Build Loosely Coupled Systems 81  
   Principle 7: Make Reversible Decisions 83  
   Principle 8: Prioritize Security 84  
   Principle 9: Embrace FinOps 85  
   Major Architecture Concepts 87  
   Domains and Services 87  
   Distributed Systems, Scalability, and Designing for Failure 88  
   Tight Versus Loose Coupling: Tiers, Monoliths, and Microservices 90  
   User Access: Single Versus Multitenant 94  
   Event-Driven Architecture 95  
   Brownfield Versus Greenfield Projects 96  
   Examples and Types of Data Architecture 98  
   Data Warehouse 98  
   Data Lake 101  
   Convergence, Next-Generation Data Lakes, and the Data Platform 102  
   Modern Data Stack 103  
   Lambda Architecture 104  
   Kappa Architecture 105  
   The Dataflow Model and Unified Batch and Streaming 105  
   Architecture for IoT 106  
   Data Mesh 109  
   Other Data Architecture Examples 110  
   Who’s Involved with Designing a Data Architecture? 111  
   Conclusion 111  
   Additional Resources 111  

4. **Choosing Technologies Across the Data Engineering Lifecycle**. . . . . . . . . . . . . . . . . . . . 115  
   Team Size and Capabilities 116  
   Speed to Market 117  
   Interoperability 117  
   Cost Optimization and Business Value 118  
   Total Cost of Ownership 118  
   Total Opportunity Cost of Ownership 119  
   FinOps 120  
   Today Versus the Future: Immutable Versus Transitory Technologies 120  
   Our Advice 122  
   Location 123  
   On Premises 123  
   Cloud 124  
   Hybrid Cloud 127  
   Multicloud 128  
   Decentralized: Blockchain and the Edge 129  
   Our Advice 129  
   Cloud Repatriation Arguments 130  
   Build Versus Buy 132  
   Open Source Software 133  
   Proprietary Walled Gardens 137  
   Our Advice 138  
   Monolith Versus Modular 139  
   Monolith 139  
   Modularity 140  
   The Distributed Monolith Pattern 142  
   Our Advice 142  
   Serverless Versus Servers 143  
   Serverless 143  
   Containers 144  
   How to Evaluate Server Versus Serverless 145  
   Our Advice 146  
   Optimization, Performance, and the Benchmark Wars 147  
   Big Data...for the 1990s 148  
   Nonsensical Cost Comparisons 148  
   Asymmetric Optimization 148  
   Caveat Emptor 149  
   Undercurrents and Their Impacts on Choosing Technologies 149  
   Data Management 149  
   DataOps 149  
   Data Architecture 150  
   Orchestration Example: Airflow 150  
   Software Engineering 151  
   Conclusion 151  
   Additional Resources 151  

### Part II. The Data Engineering Lifecycle in Depth

5. **Data Generation in Source Systems**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 155  
   Sources of Data: How Is Data Created? 156  
   Source Systems: Main Ideas 156  
   Files and Unstructured Data 156  
   APIs 157  
   Application Databases (OLTP Systems) 157  
   Online Analytical Processing System 159  
   Change Data Capture 159  
   Logs 160  
   Database Logs 161  
   CRUD 162  
   Insert-Only 162  
   Messages and Streams 163  
   Types of Time 164  
   Source System Practical Details 165  
   Databases 166  
   APIs 174  
   Data Sharing 176  
   Third-Party Data Sources 177  
   Message Queues and Event-Streaming Platforms 177  
   Whom You’ll Work With 181  
   Undercurrents and Their Impact on Source Systems 183  
   Security 183  
   Data Management 184  
   DataOps 184  
   Data Architecture 185  
   Orchestration 186  
   Software Engineering 187  
   Conclusion 187  
   Additional Resources 188  

6. **Storage**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 189  
   Raw Ingredients of Data Storage 191  
   Magnetic Disk Drive 191  
   Solid-State Drive 193  
   Random Access Memory 194  
   Networking and CPU 195  
   Serialization 195  
   Compression 196  
   Caching 197  
   Data Storage Systems 197  
   Single Machine Versus Distributed Storage 198  
   Eventual Versus Strong Consistency 198  
   File Storage 199  
   Block Storage 202  
   Object Storage 205  
   Cache and Memory-Based Storage Systems 211  
   The Hadoop Distributed File System 211  
   Streaming Storage 212  
   Indexes, Partitioning, and Clustering 213  
   Data Engineering Storage Abstractions 215  
   The Data Warehouse 215  
   The Data Lake 216  
   The Data Lakehouse 216  
   Data Platforms 217  
   Stream-to-Batch Storage Architecture 217  
   Big Ideas and Trends in Storage 218  
   Data Catalog 218  
   Data Sharing 219  
   Schema 219  
   Separation of Compute from Storage 220  
   Data Storage Lifecycle and Data Retention 223  
   Single-Tenant Versus Multitenant Storage 226  
   Whom You’ll Work With 227  
   Undercurrents 228  
   Security 228  
   Data Management 228  
   DataOps 229  
   Data Architecture 230  
   Orchestration 230  
   Software Engineering 230  
   Conclusion 230  
   Additional Resources 231  

7. **Ingestion**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 233  
   What Is Data Ingestion? 234  
   Key Engineering Considerations for the Ingestion Phase 235  
   Bounded Versus Unbounded Data 236  
   Frequency 237  
   Synchronous Versus Asynchronous Ingestion 238  
   Serialization and Deserialization 239  
   Throughput and Scalability 239  
   Reliability and Durability 240  
   Payload 241  
   Push Versus Pull Versus Poll Patterns 244  
   Batch Ingestion Considerations 244  
   Snapshot or Differential Extraction 246  
   File-Based Export and Ingestion 246  
   ETL Versus ELT 246  
   Inserts, Updates, and Batch Size 247  
   Data Migration 247  
   Message and Stream Ingestion Considerations 248  
   Schema Evolution 248  
   Late-Arriving Data 248  
   Ordering and Multiple Delivery 248  
   Replay 249  
   Time to Live 249  
   Message Size 249  
   Error Handling and Dead-Letter Queues 249  
   Consumer Pull and Push 250  
   Location 250  
   Ways to Ingest Data 250  
   Direct Database Connection 251  
   Change Data Capture 252  
   APIs 254  
   Message Queues and Event-Streaming Platforms 255  
   Managed Data Connectors 256  
   Moving Data with Object Storage 257  
   EDI 257  
   Databases and File Export 257  
   Practical Issues with Common File Formats 258  
   Shell 258  
   SSH 259  
   SFTP and SCP 259  
   Webhooks 259  
   Web Interface 260  
   Web Scraping 260  
   Transfer Appliances for Data Migration 261  
   Data Sharing 262  
   Whom You’ll Work With 262  
   Upstream Stakeholders 262  
   Downstream Stakeholders 263  
   Undercurrents 263  
   Security 264  
   Data Management 264  
   DataOps 266  
   Orchestration 268  
   Software Engineering 268  
   Conclusion 268  
   Additional Resources 269  

8. **Queries, Modeling, and Transformation**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 271  
   Queries 272  
   What Is a Query? 273  
   The Life of a Query 274  
   The Query Optimizer 275  
   Improving Query Performance 275  
   Queries on Streaming Data 281  
   Data Modeling 287  
   What Is a Data Model? 288  
   Conceptual, Logical, and Physical Data Models 289  
   Normalization 290  
   Techniques for Modeling Batch Analytical Data 294  
   Modeling Streaming Data 307  
   Transformations 309  
   Batch Transformations 310  
   Materialized Views, Federation, and Query Virtualization 323  
   Streaming Transformations and Processing 326  
   Whom You’ll Work With 329  
   Upstream Stakeholders 329  
   Downstream Stakeholders 330  
   Undercurrents 330  
   Security 330  
   Data Management 331  
   DataOps 332  
   Data Architecture 333  
   Orchestration 333  
   Software Engineering 333  
   Conclusion 334  
   Additional Resources 335  

9. **Serving Data for Analytics, Machine Learning, and Reverse ETL**. . . . . . . . . . . . . . . . . 337  
   General Considerations for Serving Data 338  
   Trust 338  
   What’s the Use Case, and Who’s the User? 339  
   Data Products 340  
   Self-Service or Not? 341  
   Data Definitions and Logic 342  
   Data Mesh 343  
   Analytics 344  
   Business Analytics 344  
   Operational Analytics 346  
   Embedded Analytics 348  
   Machine Learning 349  
   What a Data Engineer Should Know About ML 350  
   Ways to Serve Data for Analytics and ML 351  
   File Exchange 351  
   Databases 352  
   Streaming Systems 354  
   Query Federation 354  
   Data Sharing 355  
   Semantic and Metrics Layers 355  
   Serving Data in Notebooks 356  
   Reverse ETL 358  
   Whom You’ll Work With 360  
   Undercurrents 360  
   Security 361  
   Data Management 362  
   DataOps 362  
   Data Architecture 363  
   Orchestration 363  
   Software Engineering 364  
   Conclusion 365  
   Additional Resources 365  

### Part III. Security, Privacy, and the Future of Data Engineering

10. **Security and Privacy**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 369  
    People 370  
    The Power of Negative Thinking 370  
    Always Be Paranoid 370  
    Processes 371  
    Security Theater Versus Security Habit 371  
    Active Security 371  
    The Principle of Least Privilege 372  
    Shared Responsibility in the Cloud 372  
    Always Back Up Your Data 372  
    An Example Security Policy 373  
    Technology 374  
    Patch and Update Systems 374  
    Encryption 375  
    Logging, Monitoring, and Alerting 375  
    Network Access 376  
    Security for Low-Level Data Engineering 377  
    Conclusion 378  
    Additional Resources 378  

11. **The Future of Data Engineering**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 379  
    The Data Engineering Lifecycle Isn’t Going Away 380  
    The Decline of Complexity and the Rise of Easy-to-Use Data Tools 380  
    The Cloud-Scale Data OS and Improved Interoperability 381  
    “Enterprisey” Data Engineering 383  
    Titles and Responsibilities Will Morph... 384  
    Moving Beyond the Modern Data Stack, Toward the Live Data Stack 385  
    The Live Data Stack 385  
    Streaming Pipelines and Real-Time Analytical Databases 386  
    The Fusion of Data with Applications 387  
    The Tight Feedback Between Applications and ML 388  
    Dark Matter Data and the Rise of...Spreadsheets?! 388  
    Conclusion 389  

**Appendix**

A. Serialization and Compression Technical Details. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 391  
B. Cloud Networking. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 399  

**Index**. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 403