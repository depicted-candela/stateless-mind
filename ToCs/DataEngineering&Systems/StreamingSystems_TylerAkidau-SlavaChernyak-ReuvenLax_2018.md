# Table of Contents

**Streaming Systems: What, Where, When, and How of Large-Scale Data Processing**  
*by Tyler Akidau, Slava Chernyak, and Reuven Lax (2018)*

## Preface

Or: What Are You Getting Yourself Into Here? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . vii

## Part I. The Beam Model

### 1. Streaming 101 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3

- Terminology: What Is Streaming? 4
- On the Greatly Exaggerated Limitations of Streaming 6
- Event Time Versus Processing Time 8
- Data Processing Patterns 12
  - Bounded Data 12
  - Unbounded Data: Batch 13
  - Unbounded Data: Streaming 14
- Summary 22

### 2. The What, Where, When, and How of Data Processing . . . . . . . . . . . . . . . . . . . . . . . . . . . 25

- Roadmap 26
- Batch Foundations: What and Where 28
  - What: Transformations 28
  - Where: Windowing 32
- Going Streaming: When and How 34
  - When: The Wonderful Thing About Triggers Is Triggers Are Wonderful Things! 34
  - When: Watermarks 39
  - When: Early/On-Time/Late Triggers FTW! 44
  - When: Allowed Lateness (i.e., Garbage Collection) 47
  - How: Accumulation 50
- Summary 55

### 3. Watermarks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 59

- Definition 59
- Source Watermark Creation 62
  - Perfect Watermark Creation 64
  - Heuristic Watermark Creation 65
- Watermark Propagation 67
  - Understanding Watermark Propagation 69
  - Watermark Propagation and Output Timestamps 75
  - The Tricky Case of Overlapping Windows 80
- Percentile Watermarks 81
- Processing-Time Watermarks 84
- Case Studies 86
  - Case Study: Watermarks in Google Cloud Dataflow 87
  - Case Study: Watermarks in Apache Flink 88
  - Case Study: Source Watermarks for Google Cloud Pub/Sub 90
- Summary 93

### 4. Advanced Windowing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 95

- When/Where: Processing-Time Windows 95
- Event-Time Windowing 97
- Processing-Time Windowing via Triggers 98
- Processing-Time Windowing via Ingress Time 100
- Where: Session Windows 103
- Where: Custom Windowing 107
  - Variations on Fixed Windows 108
  - Variations on Session Windows 115
- One Size Does Not Fit All 119
- Summary 119

### 5. Exactly-Once and Side Effects . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 121

- Why Exactly Once Matters 121
- Accuracy Versus Completeness 122
- Side Effects 123
- Problem Definition 123
- Ensuring Exactly Once in Shuffle 125
- Addressing Determinism 126
- Performance 127
  - Graph Optimization 127
  - Bloom Filters 128
  - Garbage Collection 129
- Exactly Once in Sources 130
- Exactly Once in Sinks 131
- Use Cases 133
  - Example Source: Cloud Pub/Sub 133
  - Example Sink: Files 134
  - Example Sink: Google BigQuery 135
- Other Systems 136
  - Apache Spark Streaming 136
  - Apache Flink 136
- Summary 138

## Part II. Streams and Tables

### 6. Streams and Tables . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 141

- Stream-and-Table Basics Or: a Special Theory of Stream and Table Relativity 142
- Toward a General Theory of Stream and Table Relativity 143
- Batch Processing Versus Streams and Tables 144
- A Streams and Tables Analysis of MapReduce 144
- Reconciling with Batch Processing 150
- What, Where, When, and How in a Streams and Tables World 150
  - What: Transformations 150
  - Where: Windowing 154
  - When: Triggers 157
  - How: Accumulation 165
- A Holistic View of Streams and Tables in the Beam Model 166
- A General Theory of Stream and Table Relativity 171
- Summary 172

### 7. The Practicalities of Persistent State . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 175

- Motivation 175
- The Inevitability of Failure 176
- Correctness and Efficiency 177
- Implicit State 178
- Raw Grouping 179
- Incremental Combining 181
- Generalized State 184
- Case Study: Conversion Attribution 186
  - Conversion Attribution with Apache Beam 189
- Summary 199

### 8. Streaming SQL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201

- What Is Streaming SQL? 201
- Relational Algebra 202
- Time-Varying Relations 203
- Streams and Tables 207
- Looking Backward: Stream and Table Biases 214
  - The Beam Model: A Stream-Biased Approach 214
  - The SQL Model: A Table-Biased Approach 218
- Looking Forward: Toward Robust Streaming SQL 226
  - Stream and Table Selection 227
  - Temporal Operators 228
- Summary 249

### 9. Streaming Joins . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 253

- All Your Joins Are Belong to Streaming 253
- Unwindowed Joins 254
  - FULL OUTER 255
  - LEFT OUTER 258
  - RIGHT OUTER 259
  - INNER 259
  - ANTI 261
  - SEMI 262
- Windowed Joins 266
  - Fixed Windows 267
  - Temporal Validity 269
- Summary 282

### 10. The Evolution of Large-Scale Data Processing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 283

- MapReduce 284
- Hadoop 288
- Flume 289
- Storm 294
- Spark 297
- MillWheel 300
- Kafka 304
- Cloud Dataflow 307
- Flink 309
- Beam 313
- Summary 316

## Index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 319