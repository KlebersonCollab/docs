# Database Selection: Quick Reference Guide

## 🎯 **Overview**

This quick reference guide provides essential information for database selection decisions during interviews, architecture discussions, and system design sessions.

## 📊 **Database Classification Matrix**

| Database | CAP/PACELC | Type | Best For | Avoid For |
|----------|------------|------|----------|-----------|
| **Cassandra** | A+L | Columnar | Social media, IoT, Time series | Complex queries, ACID transactions |
| **MongoDB** | C+C | Document | E-commerce, Content management | High availability requirements |
| **PostgreSQL** | CA (Single node) | Relational | Traditional apps, Complex queries | Distributed systems |
| **CockroachDB** | C+C | Distributed Relational | Financial systems, Global apps | High write throughput |
| **Redis** | A+L | Key-Value | Caching, Sessions, Real-time | Persistent storage, Complex data |
| **Google Spanner** | C+C | Global Relational | Global financial, Multi-region | Cost-sensitive projects |

## 🧮 **Mathematical Foundations**

### **CAP Theorem**
- **C**onsistency: All nodes see same data
- **A**vailability: System remains operational  
- **P**artition Tolerance: Continues despite network failures

**Key Point**: In distributed systems, you must choose between Consistency and Availability.

### **PACELC Theorem**
- **P**artition → Choose **A**vailability or **C**onsistency
- **E**lse (no partition) → Choose **L**atency or **C**onsistency

## 🎯 **Decision Framework**

### **Step 1: Identify Requirements**
```
Is this a distributed system?
├── No → PostgreSQL/MySQL
└── Yes → Continue analysis

What happens during network partitions?
├── Need Availability → Cassandra, Redis
└── Need Consistency → MongoDB, CockroachDB

What's more important during normal operation?
├── Low Latency → Cassandra, Redis
└── Strong Consistency → MongoDB, CockroachDB
```

### **Step 2: Data Pattern Analysis**
- **Read-heavy**: Consider read replicas
- **Write-heavy**: Consider write-optimized databases
- **Complex relationships**: Relational databases
- **Simple relationships**: Document databases
- **No relationships**: Key-value stores

### **Step 3: Operational Considerations**
- **Team expertise**: SQL vs NoSQL
- **Infrastructure**: Cloud vs on-premises
- **Cost**: Licensing, hosting, maintenance
- **Scalability**: Current and future needs

## 🗄️ **Database Types and Use Cases**

### **Columnar Databases (Cassandra)**
**Characteristics:**
- Data stored in columns, not rows
- Excellent for time-series data
- High write throughput
- Tunable consistency

**Use Cases:**
- Social media platforms
- IoT sensor data
- Analytics and reporting
- Content catalogs

**Example Configuration:**
```java
// High availability
session.execute(statement.setConsistencyLevel(ConsistencyLevel.ONE));

// Strong consistency  
session.execute(statement.setConsistencyLevel(ConsistencyLevel.QUORUM));
```

### **Document Databases (MongoDB)**
**Characteristics:**
- JSON-like documents
- Flexible schema
- ACID compliance (limited)
- Strong consistency by default

**Use Cases:**
- E-commerce catalogs
- Content management
- User profiles
- Product catalogs

**Example Configuration:**
```javascript
// Strong consistency
db.collection.find().readConcern("majority");

// Eventual consistency
db.collection.find().readConcern("local");
```

### **Distributed Relational (CockroachDB)**
**Characteristics:**
- Traditional SQL interface
- ACID compliance
- Horizontal scaling
- Global distribution

**Use Cases:**
- Financial applications
- Banking systems
- Global inventory
- Multi-region applications

**Example Configuration:**
```sql
-- ACID transaction
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 'user1';
UPDATE accounts SET balance = balance + 100 WHERE id = 'user2';
COMMIT;
```

### **Key-Value Stores (Redis)**
**Characteristics:**
- Ultra-low latency
- In-memory storage
- Simple data model
- High throughput

**Use Cases:**
- Session management
- Caching
- Real-time analytics
- Rate limiting

**Example Configuration:**
```python
# Set with expiration
redis.setex("session:123", 3600, session_data)

# Atomic operations
redis.incr("page_views:today")
```

## ⚡ **Performance Characteristics**

### **Latency Comparison**
| Database | Read Latency | Write Latency | Notes |
|----------|--------------|---------------|-------|
| **Redis** | <1ms | <1ms | In-memory |
| **Cassandra** | 3-5ms | 5-10ms | Tunable consistency |
| **MongoDB** | 10-15ms | 15-25ms | Strong consistency |
| **CockroachDB** | 20-30ms | 25-50ms | ACID compliance |

### **Throughput Comparison**
| Database | Read OPS | Write OPS | Notes |
|----------|----------|-----------|-------|
| **Redis** | 1M+ | 500K+ | Single node |
| **Cassandra** | 200K+ | 100K+ | Distributed |
| **MongoDB** | 100K+ | 50K+ | Replica sets |
| **CockroachDB** | 80K+ | 30K+ | ACID overhead |

## 🔧 **Consistency Levels**

### **Cassandra Consistency Levels**
```java
ConsistencyLevel.ONE        // Fastest, least consistent
ConsistencyLevel.QUORUM     // Balanced (RF/2 + 1)
ConsistencyLevel.ALL        // Strongest, slowest
ConsistencyLevel.LOCAL_QUORUM // Within data center
```

### **MongoDB Read/Write Concerns**
```javascript
// Write concerns
{ w: 1 }           // Primary only
{ w: "majority" }  // Majority of replicas
{ w: "all" }       // All replicas

// Read concerns
"local"            // Any available node
"majority"         // Majority of nodes
"linearizable"     // Strongest consistency
```

## 🚨 **Common Interview Questions**

### **Q: How do you choose between PostgreSQL and MongoDB?**
**A:** It's not about relational vs non-relational. Consider:
- **Distributed system?** → Use distributed databases
- **ACID requirements?** → CockroachDB for distributed, PostgreSQL for single-node
- **High availability?** → Cassandra or Redis
- **Complex queries?** → Relational databases
- **Flexible schema?** → Document databases

### **Q: What's the difference between CAP and PACELC?**
**A:** 
- **CAP**: Choose 2 of 3 (Consistency, Availability, Partition tolerance)
- **PACELC**: More nuanced - considers both partition and non-partition scenarios
- **Key insight**: Partition tolerance is mandatory in distributed systems

### **Q: When would you use eventual consistency?**
**A:** When availability is more important than immediate consistency:
- Social media posts/comments
- IoT sensor data
- Analytics and reporting
- Content recommendations

### **Q: How do you handle consistency in Cassandra?**
**A:** Use tunable consistency levels:
- **ONE**: High availability, eventual consistency
- **QUORUM**: Balanced consistency/availability
- **ALL**: Strong consistency, lower availability

## 📋 **Checklist for Database Selection**

### **Requirements Analysis**
- [ ] Is this a distributed system?
- [ ] What are the consistency requirements?
- [ ] What are the availability requirements?
- [ ] What are the latency requirements?
- [ ] What's the read/write ratio?
- [ ] What are the data relationships?

### **Technical Considerations**
- [ ] Team expertise with the database
- [ ] Operational complexity
- [ ] Cost implications
- [ ] Scalability requirements
- [ ] Integration with existing systems

### **Performance Requirements**
- [ ] Expected throughput
- [ ] Latency requirements
- [ ] Storage requirements
- [ ] Memory requirements
- [ ] Network requirements

## 🎯 **Quick Decision Tree**

```
Start: Database Selection

Is this a distributed system?
├── No → PostgreSQL/MySQL
└── Yes → Continue

Network partition scenario:
├── Need Availability → Cassandra, Redis
└── Need Consistency → MongoDB, CockroachDB

Normal operation priority:
├── Low Latency → Cassandra, Redis
└── Strong Consistency → MongoDB, CockroachDB

Data relationships:
├── Complex → Relational (CockroachDB)
├── Simple → Document (MongoDB)
└── None → Key-Value (Redis)

Final considerations:
├── Team expertise
├── Operational complexity
├── Cost
└── Scalability
```

## 📚 **Key Concepts to Remember**

### **Mathematical Foundations**
- **CAP Theorem**: Consistency, Availability, Partition tolerance
- **PACELC Theorem**: Partition (A/C), Else (L/C)
- **Quorum**: (Replication Factor / 2) + 1
- **Eventual Consistency**: Data becomes consistent over time

### **Database Characteristics**
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **BASE**: Basically Available, Soft state, Eventual consistency
- **Sharding**: Horizontal partitioning of data
- **Replication**: Copying data across multiple nodes

### **Performance Metrics**
- **Latency**: Time for single operation
- **Throughput**: Operations per second
- **Consistency**: Data accuracy across nodes
- **Availability**: System uptime percentage

## 🔗 **Quick Links**

### **Documentation**
- [Database Selection Guide](./database-selection-guide.md)
- [Implementation Examples](./database-selection-examples.md)
- [Architecture Templates](../templates/)

### **External Resources**
- [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)
- [PACELC Theorem](https://en.wikipedia.org/wiki/PACELC_theorem)
- [Cassandra Documentation](https://cassandra.apache.org/doc/latest/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [CockroachDB Documentation](https://www.cockroachlabs.com/docs/)

---

**Last Updated**: January 2025  
**Maintainer**: Skynet Team  
**Version**: 1.0  
**Next Review**: March 2025
