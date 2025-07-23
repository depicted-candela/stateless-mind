# Table of Contents

Preface ............................................................ vii  
1. Analytics Engineering ...................................... 1  
   Databases and Their Impact on Analytics Engineering ............ 3  
   Cloud Computing and Its Impact on Analytics Engineering ....... 5  
   The Data Analytics Lifecycle ................................... 8  
   The New Role of Analytics Engineer ............................ 11  
   Responsibilities of an Analytics Engineer ...................... 12  
   Enabling Analytics in a Data Mesh ............................. 13  
   Data Products ................................................ 14  
   dbt as a Data Mesh Enabler ................................... 15  
   The Heart of Analytics Engineering ........................... 16  
   The Legacy Processes ......................................... 17  
   Using SQL and Stored Procedures for ETL/ELT .................. 18  
   Using ETL Tools .............................................. 19  
   The dbt Revolution ........................................... 20  
   Summary ..................................................... 22  

2. Data Modeling for Analytics ............................... 23  
   A Brief on Data Modeling ..................................... 24  
   The Conceptual Phase of Modeling ............................. 25  
   The Logical Phase of Modeling ................................ 28  
   The Physical Phase of Modeling ............................... 30  
   The Data Normalization Process ............................... 31  
   Dimensional Data Modeling .................................... 35  
   Modeling with the Star Schema ................................ 36  
   Modeling with the Snowflake Schema .......................... 40  
   Modeling with Data Vault ..................................... 42  
   Monolith Data Modeling ...................................... 45  
   Building Modular Data Models ................................ 47  
   Enabling Modular Data Models with dbt ....................... 49  
   Testing Your Data Models ..................................... 57  
   Generating Data Documentation ............................... 59  
   Debugging and Optimizing Data Models ........................ 60  
   Medallion Architecture Pattern ............................... 63  
   Summary ..................................................... 66  

3. SQL for Analytics ......................................... 67  
   The Resiliency of SQL ........................................ 68  
   Database Fundamentals ....................................... 70  
   Types of Databases ........................................... 72  
   Database Management System .................................. 75  
   “Speaking” with a Database ................................... 77  
   Creating and Managing Your Data Structures with DDL ......... 78  
   Manipulating Data with DML .................................. 82  
   Inserting Data with INSERT ................................... 83  
   Selecting Data with SELECT ................................... 85  
   Updating Data with UPDATE ................................... 96  
   Deleting Data with DELETE ................................... 97  
   Storing Queries as Views ..................................... 98  
   Common Table Expressions ................................... 101  
   Window Functions ........................................... 105  
   SQL for Distributed Data Processing ......................... 109  
   Data Manipulation with DuckDB .............................. 113  
   Data Manipulation with Polars ............................... 117  
   Data Manipulation with FugueSQL ............................ 122  
   Bonus: Training Machine Learning Models with SQL ........... 129  
   Summary .................................................... 133  

4. Data Transformation with dbt .............................. 135  
   dbt Design Philosophy ....................................... 136  
   dbt Data Flow ............................................... 138  
   dbt Cloud ................................................... 139  
   Setting Up dbt Cloud with BigQuery and GitHub ............... 140  
   Using the dbt Cloud UI ...................................... 153  
   Using the dbt Cloud IDE ..................................... 163  
   Structure of a dbt Project ................................... 165  
   Jaffle Shop Database ........................................ 168  
   YAML Files .................................................. 168  
   Models ...................................................... 174  
   Sources ..................................................... 184  
   Tests ....................................................... 189  
   Analyses .................................................... 197  
   Seeds ....................................................... 198  
   Documentation .............................................. 200  
   dbt Commands and Selection Syntax .......................... 209  
   Jobs and Deployment ........................................ 212  
   Summary .................................................... 221  

5. dbt Advanced Topics ....................................... 223  
   Model Materializations ...................................... 223  
   Tables, Views, and Ephemeral Models ........................ 224  
   Incremental Models ......................................... 227  
   Materialized Views ......................................... 229  
   Snapshots .................................................. 230  
   Dynamic SQL with Jinja ..................................... 233  
   Using SQL Macros ........................................... 236  
   dbt Packages ............................................... 242  
   Installing Packages ......................................... 242  
   Exploring the dbt_utils Package ............................. 244  
   Using Packages Inside Macros and Models .................... 244  
   dbt Semantic Layer ......................................... 246  
   Summary .................................................... 250  

6. Building an End-to-End Analytics Engineering Use Case ....... 253  
   Problem Definition: An Omnichannel Analytics Case ........... 254  
   Operational Data Modeling ................................... 254  
   Conceptual Model ........................................... 254  
   Logical Model ............................................... 255  
   Physical Model .............................................. 256  
   High-Level Data Architecture ................................ 260  
   Analytical Data Modeling .................................... 265  
   Identify the Business Processes ............................. 266  
   Identify Facts and Dimensions in the Dimensional Data Model . 267  
   Identify the Attributes for Dimensions ....................... 269  
   Define the Granularity for Business Facts .................... 270  
   Creating Our Data Warehouse with dbt ....................... 271  
   Tests, Documentation, and Deployment with dbt .............. 280  
   Data Analytics with SQL .................................... 291  
   Conclusion ................................................. 296  

Index ............................................................ 297