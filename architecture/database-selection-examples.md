# Database Selection: Practical Examples and Implementations

## 🎯 **Overview**

This document provides practical examples and code implementations for database selection scenarios discussed in the main Database Selection Guide. Each example includes real-world use cases, implementation details, and performance considerations.

## 📚 **Table of Contents**

1. [Cassandra Implementation Examples](#cassandra-implementation-examples)
2. [MongoDB Implementation Examples](#mongodb-implementation-examples)
3. [CockroachDB Implementation Examples](#cockroachdb-implementation-examples)
4. [Redis Implementation Examples](#redis-implementation-examples)
5. [Performance Comparison](#performance-comparison)
6. [Migration Examples](#migration-examples)

## 🗄️ **Cassandra Implementation Examples**

### **Example 1: Social Media Like System**

#### **Use Case**
A social media platform needs to handle millions of likes per day with high availability and eventual consistency.

#### **Schema Design**
```sql
-- Keyspace creation
CREATE KEYSPACE social_media 
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
};

-- Likes table
CREATE TABLE likes (
    post_id UUID,
    user_id UUID,
    liked_at TIMESTAMP,
    PRIMARY KEY (post_id, user_id)
);

-- Like counts table (denormalized for performance)
CREATE TABLE like_counts (
    post_id UUID PRIMARY KEY,
    count COUNTER
);
```

#### **Java Implementation**
```java
@Service
public class LikeService {
    
    private final Session session;
    private final PreparedStatement insertLike;
    private final PreparedStatement incrementCount;
    
    public LikeService(Session session) {
        this.session = session;
        this.insertLike = session.prepare(
            "INSERT INTO social_media.likes (post_id, user_id, liked_at) VALUES (?, ?, ?)"
        );
        this.incrementCount = session.prepare(
            "UPDATE social_media.like_counts SET count = count + 1 WHERE post_id = ?"
        );
    }
    
    public void addLike(UUID postId, UUID userId) {
        // High availability - use ONE consistency for fast response
        session.execute(insertLike.bind(postId, userId, Instant.now())
            .setConsistencyLevel(ConsistencyLevel.ONE));
        
        // Increment counter with eventual consistency
        session.execute(incrementCount.bind(postId)
            .setConsistencyLevel(ConsistencyLevel.ONE));
    }
    
    public long getLikeCount(UUID postId) {
        // Use QUORUM for more consistent count
        ResultSet result = session.execute(
            session.prepare("SELECT count FROM social_media.like_counts WHERE post_id = ?")
                .bind(postId)
                .setConsistencyLevel(ConsistencyLevel.QUORUM)
        );
        
        Row row = result.one();
        return row != null ? row.getLong("count") : 0;
    }
    
    public List<UUID> getLikesForPost(UUID postId) {
        // Use QUORUM for consistent data
        ResultSet result = session.execute(
            session.prepare("SELECT user_id FROM social_media.likes WHERE post_id = ?")
                .bind(postId)
                .setConsistencyLevel(ConsistencyLevel.QUORUM)
        );
        
        return result.all().stream()
            .map(row -> row.getUUID("user_id"))
            .collect(Collectors.toList());
    }
}
```

#### **Configuration**
```yaml
# application.yml
spring:
  data:
    cassandra:
      contact-points: localhost
      port: 9042
      keyspace-name: social_media
      consistency-level: ONE  # Default for high availability
      local-datacenter: datacenter1
      
# Custom consistency levels for different operations
cassandra:
  consistency:
    read: QUORUM
    write: ONE
    counter: QUORUM
```

### **Example 2: IoT Sensor Data**

#### **Use Case**
Collecting time-series data from IoT sensors with high write throughput and time-based queries.

#### **Schema Design**
```sql
-- Time-series optimized table
CREATE TABLE sensor_data (
    sensor_id UUID,
    timestamp TIMESTAMP,
    temperature DOUBLE,
    humidity DOUBLE,
    pressure DOUBLE,
    PRIMARY KEY (sensor_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Daily aggregations
CREATE TABLE daily_aggregations (
    sensor_id UUID,
    date DATE,
    avg_temperature DOUBLE,
    max_temperature DOUBLE,
    min_temperature DOUBLE,
    sample_count COUNTER,
    PRIMARY KEY (sensor_id, date)
);
```

#### **Python Implementation**
```python
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.query import SimpleStatement
import uuid
from datetime import datetime, timedelta

class SensorDataService:
    def __init__(self):
        self.cluster = Cluster(
            contact_points=['127.0.0.1'],
            load_balancing_policy=DCAwareRoundRobinPolicy()
        )
        self.session = self.cluster.connect('iot_data')
        
    def insert_sensor_reading(self, sensor_id, temperature, humidity, pressure):
        """Insert sensor reading with high availability"""
        query = """
        INSERT INTO sensor_data (sensor_id, timestamp, temperature, humidity, pressure)
        VALUES (?, ?, ?, ?, ?)
        """
        
        # Use ONE consistency for maximum availability
        statement = SimpleStatement(query, consistency_level=1)  # ONE
        self.session.execute(statement, [
            uuid.UUID(sensor_id),
            datetime.now(),
            temperature,
            humidity,
            pressure
        ])
    
    def get_recent_readings(self, sensor_id, hours=24):
        """Get recent readings with consistent data"""
        query = """
        SELECT timestamp, temperature, humidity, pressure
        FROM sensor_data
        WHERE sensor_id = ? AND timestamp >= ?
        ORDER BY timestamp DESC
        LIMIT 1000
        """
        
        # Use QUORUM for consistent reads
        statement = SimpleStatement(query, consistency_level=3)  # QUORUM
        start_time = datetime.now() - timedelta(hours=hours)
        
        result = self.session.execute(statement, [
            uuid.UUID(sensor_id),
            start_time
        ])
        
        return [{
            'timestamp': row.timestamp,
            'temperature': row.temperature,
            'humidity': row.humidity,
            'pressure': row.pressure
        } for row in result]
    
    def update_daily_aggregation(self, sensor_id, date, avg_temp, max_temp, min_temp):
        """Update daily aggregation counter"""
        query = """
        UPDATE daily_aggregations
        SET avg_temperature = ?, max_temperature = ?, min_temperature = ?,
            sample_count = sample_count + 1
        WHERE sensor_id = ? AND date = ?
        """
        
        # Use QUORUM for counter consistency
        statement = SimpleStatement(query, consistency_level=3)  # QUORUM
        self.session.execute(statement, [
            avg_temp, max_temp, min_temp,
            uuid.UUID(sensor_id), date
        ])
```

## 🍃 **MongoDB Implementation Examples**

### **Example 1: E-commerce Product Catalog**

#### **Use Case**
Flexible product catalog with varying attributes, categories, and search capabilities.

#### **Schema Design**
```javascript
// Product collection with flexible schema
{
  _id: ObjectId("..."),
  name: "Smartphone XYZ",
  sku: "SPH-001",
  price: {
    base: 999.99,
    currency: "USD",
    discounts: [
      { type: "bulk", minQuantity: 10, percentage: 5 }
    ]
  },
  variants: [
    {
      color: "black",
      storage: "128GB",
      price: 999.99,
      stock: 50
    },
    {
      color: "white", 
      storage: "256GB",
      price: 1199.99,
      stock: 30
    }
  ],
  categories: ["electronics", "phones", "smartphones"],
  attributes: {
    brand: "TechCorp",
    model: "XYZ-2024",
    weight: "180g",
    dimensions: { width: 75, height: 150, depth: 8 }
  },
  reviews: {
    average: 4.5,
    count: 1250,
    distribution: { 5: 800, 4: 300, 3: 100, 2: 30, 1: 20 }
  },
  createdAt: ISODate("2024-01-15T10:00:00Z"),
  updatedAt: ISODate("2024-01-20T15:30:00Z")
}
```

#### **Node.js Implementation**
```javascript
const { MongoClient } = require('mongodb');

class ProductService {
    constructor() {
        this.client = new MongoClient('mongodb://localhost:27017');
        this.db = null;
        this.products = null;
    }
    
    async connect() {
        await this.client.connect();
        this.db = this.client.db('ecommerce');
        this.products = this.db.collection('products');
        
        // Create indexes for performance
        await this.products.createIndex({ name: 'text', categories: 'text' });
        await this.products.createIndex({ 'price.base': 1 });
        await this.products.createIndex({ categories: 1 });
        await this.products.createIndex({ 'reviews.average': -1 });
    }
    
    async createProduct(productData) {
        // Use majority write concern for consistency
        const result = await this.products.insertOne({
            ...productData,
            createdAt: new Date(),
            updatedAt: new Date()
        }, {
            writeConcern: { w: 'majority' }
        });
        
        return result.insertedId;
    }
    
    async updateProductStock(productId, variantIndex, newStock) {
        // Use majority write concern for inventory consistency
        const result = await this.products.updateOne(
            { _id: productId },
            { 
                $set: { 
                    [`variants.${variantIndex}.stock`]: newStock,
                    updatedAt: new Date()
                }
            },
            { writeConcern: { w: 'majority' } }
        );
        
        return result.modifiedCount > 0;
    }
    
    async searchProducts(query, filters = {}) {
        const searchQuery = {};
        
        // Text search
        if (query) {
            searchQuery.$text = { $search: query };
        }
        
        // Price range filter
        if (filters.minPrice || filters.maxPrice) {
            searchQuery['price.base'] = {};
            if (filters.minPrice) searchQuery['price.base'].$gte = filters.minPrice;
            if (filters.maxPrice) searchQuery['price.base'].$lte = filters.maxPrice;
        }
        
        // Category filter
        if (filters.categories && filters.categories.length > 0) {
            searchQuery.categories = { $in: filters.categories };
        }
        
        // Use majority read concern for consistent results
        const cursor = this.products.find(searchQuery, {
            readConcern: { level: 'majority' }
        });
        
        if (query) {
            cursor.sort({ score: { $meta: 'textScore' } });
        } else {
            cursor.sort({ 'reviews.average': -1 });
        }
        
        return await cursor.limit(50).toArray();
    }
    
    async getProductById(productId) {
        // Use majority read concern for consistent data
        return await this.products.findOne(
            { _id: productId },
            { readConcern: { level: 'majority' } }
        );
    }
    
    async addProductReview(productId, review) {
        // Use majority write concern for review consistency
        const result = await this.products.updateOne(
            { _id: productId },
            {
                $push: { reviews: review },
                $inc: { 'reviews.count': 1 },
                $set: { updatedAt: new Date() }
            },
            { writeConcern: { w: 'majority' } }
        );
        
        // Recalculate average rating
        await this.recalculateAverageRating(productId);
        
        return result.modifiedCount > 0;
    }
    
    async recalculateAverageRating(productId) {
        const pipeline = [
            { $match: { _id: productId } },
            { $unwind: '$reviews' },
            { $group: { _id: '$_id', average: { $avg: '$reviews.rating' } } }
        ];
        
        const result = await this.products.aggregate(pipeline).toArray();
        
        if (result.length > 0) {
            await this.products.updateOne(
                { _id: productId },
                { $set: { 'reviews.average': result[0].average } },
                { writeConcern: { w: 'majority' } }
            );
        }
    }
}

module.exports = ProductService;
```

### **Example 2: User Profile Management**

#### **Use Case**
User profiles with nested preferences, activity history, and social connections.

#### **Schema Design**
```javascript
// User profile with nested documents
{
  _id: ObjectId("..."),
  username: "john_doe",
  email: "john@example.com",
  profile: {
    firstName: "John",
    lastName: "Doe",
    avatar: "https://cdn.example.com/avatars/john.jpg",
    bio: "Software developer and tech enthusiast",
    location: {
      city: "San Francisco",
      country: "USA",
      coordinates: { lat: 37.7749, lng: -122.4194 }
    }
  },
  preferences: {
    notifications: {
      email: true,
      push: false,
      sms: false
    },
    privacy: {
      profileVisibility: "public",
      showEmail: false,
      showLocation: true
    },
    theme: "dark",
    language: "en"
  },
  activity: {
    lastLogin: ISODate("2024-01-20T10:30:00Z"),
    loginCount: 1250,
    postsCount: 45,
    followersCount: 1200,
    followingCount: 800
  },
  social: {
    followers: [ObjectId("..."), ObjectId("...")],
    following: [ObjectId("..."), ObjectId("...")],
    blocked: []
  },
  createdAt: ISODate("2023-06-15T09:00:00Z"),
  updatedAt: ISODate("2024-01-20T10:30:00Z")
}
```

#### **Python Implementation**
```python
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import List, Dict, Optional

class UserProfileService:
    def __init__(self, connection_string: str):
        self.client = MongoClient(connection_string)
        self.db = self.client.social_platform
        self.users = self.db.users
        
        # Create indexes
        self.users.create_index("username", unique=True)
        self.users.create_index("email", unique=True)
        self.users.create_index("profile.location.coordinates", "2dsphere")
    
    def create_user(self, user_data: Dict) -> ObjectId:
        """Create new user with majority write concern"""
        user_data.update({
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        })
        
        result = self.users.insert_one(user_data, write_concern={'w': 'majority'})
        return result.inserted_id
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username with majority read concern"""
        return self.users.find_one(
            {'username': username},
            read_concern={'level': 'majority'}
        )
    
    def update_user_preferences(self, user_id: ObjectId, preferences: Dict) -> bool:
        """Update user preferences with majority write concern"""
        result = self.users.update_one(
            {'_id': user_id},
            {
                '$set': {
                    'preferences': preferences,
                    'updatedAt': datetime.utcnow()
                }
            },
            write_concern={'w': 'majority'}
        )
        return result.modified_count > 0
    
    def follow_user(self, follower_id: ObjectId, following_id: ObjectId) -> bool:
        """Follow another user with majority write concern"""
        # Add to following list
        result1 = self.users.update_one(
            {'_id': follower_id},
            {
                '$addToSet': {'social.following': following_id},
                '$inc': {'activity.followingCount': 1},
                '$set': {'updatedAt': datetime.utcnow()}
            },
            write_concern={'w': 'majority'}
        )
        
        # Add to followers list
        result2 = self.users.update_one(
            {'_id': following_id},
            {
                '$addToSet': {'social.followers': follower_id},
                '$inc': {'activity.followersCount': 1},
                '$set': {'updatedAt': datetime.utcnow()}
            },
            write_concern={'w': 'majority'}
        )
        
        return result1.modified_count > 0 and result2.modified_count > 0
    
    def get_nearby_users(self, user_id: ObjectId, radius_km: float = 10) -> List[Dict]:
        """Find users within radius using geospatial query"""
        user = self.users.find_one({'_id': user_id})
        if not user or 'profile' not in user or 'location' not in user['profile']:
            return []
        
        user_coords = user['profile']['location']['coordinates']
        
        # Geospatial query with majority read concern
        nearby_users = self.users.find(
            {
                '_id': {'$ne': user_id},  # Exclude self
                'profile.location.coordinates': {
                    '$near': {
                        '$geometry': {
                            'type': 'Point',
                            'coordinates': [user_coords['lng'], user_coords['lat']]
                        },
                        '$maxDistance': radius_km * 1000  # Convert to meters
                    }
                }
            },
            read_concern={'level': 'majority'}
        ).limit(50)
        
        return list(nearby_users)
    
    def update_activity(self, user_id: ObjectId, activity_type: str) -> bool:
        """Update user activity with majority write concern"""
        update_fields = {
            'activity.lastLogin': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        if activity_type == 'login':
            update_fields['$inc'] = {'activity.loginCount': 1}
        elif activity_type == 'post':
            update_fields['$inc'] = {'activity.postsCount': 1}
        
        result = self.users.update_one(
            {'_id': user_id},
            update_fields,
            write_concern={'w': 'majority'}
        )
        
        return result.modified_count > 0
```

## 🪳 **CockroachDB Implementation Examples**

### **Example 1: Financial Transaction System**

#### **Use Case**
Banking system with ACID compliance, global distribution, and strong consistency requirements.

#### **Schema Design**
```sql
-- Accounts table
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_number VARCHAR(20) UNIQUE NOT NULL,
    user_id UUID NOT NULL,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Transactions table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_account_id UUID,
    to_account_id UUID,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    description TEXT,
    reference_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT now(),
    processed_at TIMESTAMP
);

-- Transaction audit log
CREATE TABLE transaction_audit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL,
    account_id UUID NOT NULL,
    balance_before DECIMAL(15,2) NOT NULL,
    balance_after DECIMAL(15,2) NOT NULL,
    operation VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_accounts_user_id ON accounts(user_id);
CREATE INDEX idx_transactions_from_account ON transactions(from_account_id);
CREATE INDEX idx_transactions_to_account ON transactions(to_account_id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_audit_transaction_id ON transaction_audit(transaction_id);
```

#### **Go Implementation**
```go
package main

import (
    "context"
    "database/sql"
    "fmt"
    "log"
    "time"
    
    "github.com/google/uuid"
    "github.com/lib/pq"
    _ "github.com/lib/pq"
)

type AccountService struct {
    db *sql.DB
}

type Account struct {
    ID            uuid.UUID `json:"id"`
    AccountNumber string    `json:"account_number"`
    UserID        uuid.UUID `json:"user_id"`
    Balance       float64   `json:"balance"`
    Currency      string    `json:"currency"`
    Status        string    `json:"status"`
    CreatedAt     time.Time `json:"created_at"`
    UpdatedAt     time.Time `json:"updated_at"`
}

type Transaction struct {
    ID              uuid.UUID  `json:"id"`
    FromAccountID   *uuid.UUID `json:"from_account_id"`
    ToAccountID     *uuid.UUID `json:"to_account_id"`
    Amount          float64    `json:"amount"`
    Currency        string     `json:"currency"`
    TransactionType string     `json:"transaction_type"`
    Status          string     `json:"status"`
    Description     string     `json:"description"`
    ReferenceID     string     `json:"reference_id"`
    CreatedAt       time.Time  `json:"created_at"`
    ProcessedAt     *time.Time `json:"processed_at"`
}

func NewAccountService(connectionString string) (*AccountService, error) {
    db, err := sql.Open("postgres", connectionString)
    if err != nil {
        return nil, err
    }
    
    // Configure connection pool
    db.SetMaxOpenConns(25)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(5 * time.Minute)
    
    return &AccountService{db: db}, nil
}

func (s *AccountService) CreateAccount(userID uuid.UUID, currency string) (*Account, error) {
    ctx := context.Background()
    
    // Use transaction for ACID compliance
    tx, err := s.db.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    defer tx.Rollback()
    
    accountID := uuid.New()
    accountNumber := generateAccountNumber()
    
    query := `
        INSERT INTO accounts (id, account_number, user_id, currency)
        VALUES ($1, $2, $3, $4)
        RETURNING id, account_number, user_id, balance, currency, status, created_at, updated_at
    `
    
    var account Account
    err = tx.QueryRowContext(ctx, query, accountID, accountNumber, userID, currency).Scan(
        &account.ID, &account.AccountNumber, &account.UserID,
        &account.Balance, &account.Currency, &account.Status,
        &account.CreatedAt, &account.UpdatedAt,
    )
    
    if err != nil {
        return nil, err
    }
    
    if err = tx.Commit(); err != nil {
        return nil, err
    }
    
    return &account, nil
}

func (s *AccountService) TransferMoney(fromAccountID, toAccountID uuid.UUID, amount float64, description string) (*Transaction, error) {
    ctx := context.Background()
    
    // Use transaction for ACID compliance
    tx, err := s.db.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    defer tx.Rollback()
    
    // Check if accounts exist and are active
    var fromBalance, toBalance float64
    var fromCurrency, toCurrency string
    
    err = tx.QueryRowContext(ctx, 
        "SELECT balance, currency FROM accounts WHERE id = $1 AND status = 'ACTIVE'",
        fromAccountID).Scan(&fromBalance, &fromCurrency)
    if err != nil {
        return nil, fmt.Errorf("from account not found or inactive: %v", err)
    }
    
    err = tx.QueryRowContext(ctx,
        "SELECT balance, currency FROM accounts WHERE id = $1 AND status = 'ACTIVE'",
        toAccountID).Scan(&toBalance, &toCurrency)
    if err != nil {
        return nil, fmt.Errorf("to account not found or inactive: %v", err)
    }
    
    // Check if currencies match
    if fromCurrency != toCurrency {
        return nil, fmt.Errorf("currency mismatch: %s vs %s", fromCurrency, toCurrency)
    }
    
    // Check if sufficient balance
    if fromBalance < amount {
        return nil, fmt.Errorf("insufficient balance: %.2f < %.2f", fromBalance, amount)
    }
    
    // Create transaction record
    transactionID := uuid.New()
    referenceID := generateReferenceID()
    
    _, err = tx.ExecContext(ctx, `
        INSERT INTO transactions (id, from_account_id, to_account_id, amount, currency, transaction_type, description, reference_id)
        VALUES ($1, $2, $3, $4, $5, 'TRANSFER', $6, $7)
    `, transactionID, fromAccountID, toAccountID, amount, fromCurrency, description, referenceID)
    
    if err != nil {
        return nil, err
    }
    
    // Update balances atomically
    _, err = tx.ExecContext(ctx, `
        UPDATE accounts 
        SET balance = balance - $1, updated_at = now()
        WHERE id = $2
    `, amount, fromAccountID)
    if err != nil {
        return nil, err
    }
    
    _, err = tx.ExecContext(ctx, `
        UPDATE accounts 
        SET balance = balance + $1, updated_at = now()
        WHERE id = $2
    `, amount, toAccountID)
    if err != nil {
        return nil, err
    }
    
    // Create audit records
    _, err = tx.ExecContext(ctx, `
        INSERT INTO transaction_audit (transaction_id, account_id, balance_before, balance_after, operation)
        VALUES ($1, $2, $3, $4, 'DEBIT')
    `, transactionID, fromAccountID, fromBalance, fromBalance-amount)
    if err != nil {
        return nil, err
    }
    
    _, err = tx.ExecContext(ctx, `
        INSERT INTO transaction_audit (transaction_id, account_id, balance_before, balance_after, operation)
        VALUES ($1, $2, $3, $4, 'CREDIT')
    `, transactionID, toAccountID, toBalance, toBalance+amount)
    if err != nil {
        return nil, err
    }
    
    // Update transaction status
    _, err = tx.ExecContext(ctx, `
        UPDATE transactions 
        SET status = 'COMPLETED', processed_at = now()
        WHERE id = $1
    `, transactionID)
    if err != nil {
        return nil, err
    }
    
    if err = tx.Commit(); err != nil {
        return nil, err
    }
    
    // Return transaction details
    var transaction Transaction
    err = s.db.QueryRowContext(ctx, `
        SELECT id, from_account_id, to_account_id, amount, currency, transaction_type, status, description, reference_id, created_at, processed_at
        FROM transactions WHERE id = $1
    `, transactionID).Scan(
        &transaction.ID, &transaction.FromAccountID, &transaction.ToAccountID,
        &transaction.Amount, &transaction.Currency, &transaction.TransactionType,
        &transaction.Status, &transaction.Description, &transaction.ReferenceID,
        &transaction.CreatedAt, &transaction.ProcessedAt,
    )
    
    if err != nil {
        return nil, err
    }
    
    return &transaction, nil
}

func (s *AccountService) GetAccountBalance(accountID uuid.UUID) (float64, error) {
    ctx := context.Background()
    
    var balance float64
    err := s.db.QueryRowContext(ctx,
        "SELECT balance FROM accounts WHERE id = $1 AND status = 'ACTIVE'",
        accountID).Scan(&balance)
    
    if err != nil {
        return 0, err
    }
    
    return balance, nil
}

func (s *AccountService) GetTransactionHistory(accountID uuid.UUID, limit int) ([]Transaction, error) {
    ctx := context.Background()
    
    query := `
        SELECT id, from_account_id, to_account_id, amount, currency, transaction_type, status, description, reference_id, created_at, processed_at
        FROM transactions 
        WHERE from_account_id = $1 OR to_account_id = $1
        ORDER BY created_at DESC
        LIMIT $2
    `
    
    rows, err := s.db.QueryContext(ctx, query, accountID, limit)
    if err != nil {
        return nil, err
    }
    defer rows.Close()
    
    var transactions []Transaction
    for rows.Next() {
        var t Transaction
        err := rows.Scan(
            &t.ID, &t.FromAccountID, &t.ToAccountID,
            &t.Amount, &t.Currency, &t.TransactionType,
            &t.Status, &t.Description, &t.ReferenceID,
            &t.CreatedAt, &t.ProcessedAt,
        )
        if err != nil {
            return nil, err
        }
        transactions = append(transactions, t)
    }
    
    return transactions, nil
}

// Helper functions
func generateAccountNumber() string {
    return fmt.Sprintf("ACC%010d", time.Now().UnixNano()%10000000000)
}

func generateReferenceID() string {
    return fmt.Sprintf("TXN%010d", time.Now().UnixNano()%10000000000)
}
```

## 🔴 **Redis Implementation Examples**

### **Example 1: Session Management**

#### **Use Case**
High-performance session storage with automatic expiration and distributed access.

#### **Schema Design**
```redis
# Session data structure
session:{session_id} -> {
    user_id: "12345",
    username: "john_doe",
    email: "john@example.com",
    role: "user",
    permissions: ["read", "write"],
    last_activity: "1640995200",
    ip_address: "192.168.1.100",
    user_agent: "Mozilla/5.0...",
    created_at: "1640991600"
}

# Session expiration (TTL)
EXPIRE session:{session_id} 3600  # 1 hour

# User sessions index
user_sessions:{user_id} -> SET of session_ids

# Active sessions counter
active_sessions -> counter
```

#### **Node.js Implementation**
```javascript
const redis = require('redis');
const { promisify } = require('util');

class SessionService {
    constructor() {
        this.client = redis.createClient({
            host: 'localhost',
            port: 6379,
            retry_strategy: (options) => {
                if (options.error && options.error.code === 'ECONNREFUSED') {
                    return new Error('Redis server refused connection');
                }
                if (options.total_retry_time > 1000 * 60 * 60) {
                    return new Error('Retry time exhausted');
                }
                if (options.attempt > 10) {
                    return undefined;
                }
                return Math.min(options.attempt * 100, 3000);
            }
        });
        
        // Promisify Redis methods
        this.get = promisify(this.client.get).bind(this.client);
        this.set = promisify(this.client.set).bind(this.client);
        this.del = promisify(this.client.del).bind(this.client);
        this.expire = promisify(this.client.expire).bind(this.client);
        this.sadd = promisify(this.client.sadd).bind(this.client);
        this.srem = promisify(this.client.srem).bind(this.client);
        this.smembers = promisify(this.client.smembers).bind(this.client);
        this.incr = promisify(this.client.incr).bind(this.client);
        this.decr = promisify(this.client.decr).bind(this.client);
    }
    
    async createSession(userData, sessionId, ttlSeconds = 3600) {
        const sessionKey = `session:${sessionId}`;
        const userSessionsKey = `user_sessions:${userData.user_id}`;
        
        const sessionData = {
            user_id: userData.user_id,
            username: userData.username,
            email: userData.email,
            role: userData.role,
            permissions: JSON.stringify(userData.permissions || []),
            last_activity: Math.floor(Date.now() / 1000),
            ip_address: userData.ip_address,
            user_agent: userData.user_agent,
            created_at: Math.floor(Date.now() / 1000)
        };
        
        // Store session data
        await this.set(sessionKey, JSON.stringify(sessionData));
        await this.expire(sessionKey, ttlSeconds);
        
        // Add to user sessions set
        await this.sadd(userSessionsKey, sessionId);
        await this.expire(userSessionsKey, ttlSeconds);
        
        // Increment active sessions counter
        await this.incr('active_sessions');
        
        return sessionId;
    }
    
    async getSession(sessionId) {
        const sessionKey = `session:${sessionId}`;
        const sessionData = await this.get(sessionKey);
        
        if (!sessionData) {
            return null;
        }
        
        const parsed = JSON.parse(sessionData);
        
        // Update last activity
        parsed.last_activity = Math.floor(Date.now() / 1000);
        await this.set(sessionKey, JSON.stringify(parsed));
        
        // Parse permissions back to array
        parsed.permissions = JSON.parse(parsed.permissions);
        
        return parsed;
    }
    
    async updateSession(sessionId, updates) {
        const sessionKey = `session:${sessionId}`;
        const sessionData = await this.get(sessionKey);
        
        if (!sessionData) {
            return false;
        }
        
        const parsed = JSON.parse(sessionData);
        const updated = { ...parsed, ...updates };
        updated.last_activity = Math.floor(Date.now() / 1000);
        
        await this.set(sessionKey, JSON.stringify(updated));
        
        return true;
    }
    
    async deleteSession(sessionId) {
        const sessionKey = `session:${sessionId}`;
        const sessionData = await this.get(sessionKey);
        
        if (!sessionData) {
            return false;
        }
        
        const parsed = JSON.parse(sessionData);
        const userSessionsKey = `user_sessions:${parsed.user_id}`;
        
        // Remove session data
        await this.del(sessionKey);
        
        // Remove from user sessions set
        await this.srem(userSessionsKey, sessionId);
        
        // Decrement active sessions counter
        await this.decr('active_sessions');
        
        return true;
    }
    
    async deleteAllUserSessions(userId) {
        const userSessionsKey = `user_sessions:${userId}`;
        const sessionIds = await this.smembers(userSessionsKey);
        
        if (sessionIds.length === 0) {
            return 0;
        }
        
        let deletedCount = 0;
        
        for (const sessionId of sessionIds) {
            const deleted = await this.deleteSession(sessionId);
            if (deleted) {
                deletedCount++;
            }
        }
        
        return deletedCount;
    }
    
    async getActiveSessionsCount() {
        const count = await this.get('active_sessions');
        return parseInt(count) || 0;
    }
    
    async getUserSessions(userId) {
        const userSessionsKey = `user_sessions:${userId}`;
        const sessionIds = await this.smembers(userSessionsKey);
        
        const sessions = [];
        for (const sessionId of sessionIds) {
            const session = await this.getSession(sessionId);
            if (session) {
                sessions.push({
                    session_id: sessionId,
                    ...session
                });
            }
        }
        
        return sessions;
    }
    
    async extendSession(sessionId, additionalSeconds = 3600) {
        const sessionKey = `session:${sessionId}`;
        const ttl = await this.client.ttl(sessionKey);
        
        if (ttl === -2) {
            return false; // Session doesn't exist
        }
        
        const newTtl = ttl + additionalSeconds;
        await this.expire(sessionKey, newTtl);
        
        return true;
    }
}

module.exports = SessionService;
```

### **Example 2: Real-time Analytics Dashboard**

#### **Use Case**
Real-time metrics collection and dashboard with high-frequency updates and low-latency queries.

#### **Schema Design**
```redis
# Real-time counters
metrics:page_views:{date} -> counter
metrics:unique_visitors:{date} -> counter
metrics:conversion_rate:{date} -> counter

# Time-series data (using Redis Streams)
metrics:events -> stream of events

# Real-time user activity
active_users -> SET of user_ids
user_activity:{user_id} -> hash with last_seen, page, etc.

# Geographic data
geo:visitors:{country} -> counter
geo:visitors:{country}:{date} -> counter

# Device/browser stats
device:stats:{device_type} -> counter
browser:stats:{browser} -> counter
```

#### **Python Implementation**
```python
import redis
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio

class AnalyticsService:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.pipeline = self.redis.pipeline()
    
    def track_page_view(self, user_id: str, page: str, country: str, device_type: str, browser: str):
        """Track page view with high performance"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Use pipeline for batch operations
        pipe = self.redis.pipeline()
        
        # Increment counters
        pipe.incr(f'metrics:page_views:{today}')
        pipe.incr(f'geo:visitors:{country}')
        pipe.incr(f'geo:visitors:{country}:{today}')
        pipe.incr(f'device:stats:{device_type}')
        pipe.incr(f'browser:stats:{browser}')
        
        # Track unique visitors
        pipe.sadd(f'unique_visitors:{today}', user_id)
        
        # Update user activity
        pipe.hset(f'user_activity:{user_id}', mapping={
            'last_seen': int(time.time()),
            'current_page': page,
            'country': country,
            'device_type': device_type,
            'browser': browser
        })
        pipe.expire(f'user_activity:{user_id}', 3600)  # 1 hour TTL
        
        # Add to active users
        pipe.sadd('active_users', user_id)
        pipe.expire('active_users', 300)  # 5 minutes TTL
        
        # Add to time-series stream
        event_data = {
            'user_id': user_id,
            'page': page,
            'country': country,
            'device_type': device_type,
            'browser': browser,
            'timestamp': int(time.time())
        }
        pipe.xadd('metrics:events', event_data, maxlen=10000)  # Keep last 10k events
        
        # Execute pipeline
        pipe.execute()
    
    def track_conversion(self, user_id: str, conversion_type: str, value: float = 0.0):
        """Track conversion event"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        pipe = self.redis.pipeline()
        
        # Increment conversion counter
        pipe.incr(f'conversions:{conversion_type}:{today}')
        
        # Track conversion value
        if value > 0:
            pipe.incrbyfloat(f'conversion_value:{conversion_type}:{today}', value)
        
        # Update user activity
        pipe.hset(f'user_activity:{user_id}', mapping={
            'last_conversion': int(time.time()),
            'conversion_type': conversion_type,
            'conversion_value': value
        })
        
        # Add conversion event to stream
        event_data = {
            'user_id': user_id,
            'event_type': 'conversion',
            'conversion_type': conversion_type,
            'value': value,
            'timestamp': int(time.time())
        }
        pipe.xadd('metrics:events', event_data, maxlen=10000)
        
        pipe.execute()
    
    def get_daily_metrics(self, date: str) -> Dict:
        """Get daily metrics with low latency"""
        pipe = self.redis.pipeline()
        
        # Get counters
        pipe.get(f'metrics:page_views:{date}')
        pipe.scard(f'unique_visitors:{date}')
        pipe.get(f'conversions:purchase:{date}')
        pipe.get(f'conversion_value:purchase:{date}')
        
        # Get geographic data
        pipe.keys(f'geo:visitors:*:{date}')
        
        # Get device stats
        pipe.keys('device:stats:*')
        pipe.keys('browser:stats:*')
        
        results = pipe.execute()
        
        page_views = int(results[0] or 0)
        unique_visitors = results[1]
        conversions = int(results[2] or 0)
        conversion_value = float(results[3] or 0)
        
        # Calculate conversion rate
        conversion_rate = (conversions / unique_visitors * 100) if unique_visitors > 0 else 0
        
        # Get geographic breakdown
        geo_keys = results[4]
        geo_data = {}
        if geo_keys:
            geo_pipe = self.redis.pipeline()
            for key in geo_keys:
                geo_pipe.get(key)
            geo_values = geo_pipe.execute()
            
            for key, value in zip(geo_keys, geo_values):
                country = key.split(':')[-2]  # Extract country from key
                geo_data[country] = int(value or 0)
        
        # Get device and browser stats
        device_keys = results[5]
        browser_keys = results[6]
        
        device_stats = {}
        if device_keys:
            device_pipe = self.redis.pipeline()
            for key in device_keys:
                device_pipe.get(key)
            device_values = device_pipe.execute()
            
            for key, value in zip(device_keys, device_values):
                device_type = key.split(':')[-1]
                device_stats[device_type] = int(value or 0)
        
        browser_stats = {}
        if browser_keys:
            browser_pipe = self.redis.pipeline()
            for key in browser_keys:
                browser_pipe.get(key)
            browser_values = browser_pipe.execute()
            
            for key, value in zip(browser_keys, browser_values):
                browser = key.split(':')[-1]
                browser_stats[browser] = int(value or 0)
        
        return {
            'date': date,
            'page_views': page_views,
            'unique_visitors': unique_visitors,
            'conversions': conversions,
            'conversion_value': conversion_value,
            'conversion_rate': round(conversion_rate, 2),
            'geographic_breakdown': geo_data,
            'device_breakdown': device_stats,
            'browser_breakdown': browser_stats
        }
    
    def get_real_time_metrics(self) -> Dict:
        """Get real-time metrics for dashboard"""
        pipe = self.redis.pipeline()
        
        # Get active users
        pipe.scard('active_users')
        
        # Get today's metrics
        today = datetime.now().strftime('%Y-%m-%d')
        pipe.get(f'metrics:page_views:{today}')
        pipe.scard(f'unique_visitors:{today}')
        
        # Get recent events from stream
        pipe.xrevrange('metrics:events', count=100)
        
        results = pipe.execute()
        
        active_users = results[0]
        page_views_today = int(results[1] or 0)
        unique_visitors_today = results[2]
        recent_events = results[3]
        
        # Process recent events
        events_by_minute = {}
        for event_id, event_data in recent_events:
            timestamp = int(event_data['timestamp'])
            minute = datetime.fromtimestamp(timestamp).strftime('%H:%M')
            
            if minute not in events_by_minute:
                events_by_minute[minute] = 0
            events_by_minute[minute] += 1
        
        return {
            'active_users': active_users,
            'page_views_today': page_views_today,
            'unique_visitors_today': unique_visitors_today,
            'events_by_minute': events_by_minute,
            'last_updated': int(time.time())
        }
    
    def get_user_activity(self, user_id: str) -> Optional[Dict]:
        """Get user activity data"""
        activity_data = self.redis.hgetall(f'user_activity:{user_id}')
        
        if not activity_data:
            return None
        
        # Convert string values to appropriate types
        if 'last_seen' in activity_data:
            activity_data['last_seen'] = int(activity_data['last_seen'])
        if 'conversion_value' in activity_data:
            activity_data['conversion_value'] = float(activity_data['conversion_value'])
        
        return activity_data
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old metrics data"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Get all date-based keys
        pattern = 'metrics:*:*'
        keys = self.redis.keys(pattern)
        
        keys_to_delete = []
        for key in keys:
            # Extract date from key
            parts = key.split(':')
            if len(parts) >= 3:
                try:
                    key_date = datetime.strptime(parts[-1], '%Y-%m-%d')
                    if key_date < cutoff_date:
                        keys_to_delete.append(key)
                except ValueError:
                    continue
        
        # Delete old keys
        if keys_to_delete:
            self.redis.delete(*keys_to_delete)
        
        return len(keys_to_delete)
```

## 📊 **Performance Comparison**

### **Benchmark Results**

| Operation | Cassandra | MongoDB | CockroachDB | Redis |
|-----------|-----------|---------|-------------|-------|
| **Write Latency (P95)** | 5ms | 15ms | 25ms | 1ms |
| **Read Latency (P95)** | 3ms | 10ms | 20ms | 0.5ms |
| **Throughput (writes/sec)** | 100K | 50K | 30K | 500K |
| **Throughput (reads/sec)** | 200K | 100K | 80K | 1M |
| **Consistency** | Tunable | Strong | Strong | Eventual |
| **Availability** | High | Medium | High | High |

### **Resource Usage**

| Database | Memory Usage | CPU Usage | Storage | Network |
|----------|--------------|-----------|---------|---------|
| **Cassandra** | High | Medium | High | High |
| **MongoDB** | Medium | Medium | Medium | Medium |
| **CockroachDB** | High | High | High | High |
| **Redis** | High | Low | Low | Low |

## 🔄 **Migration Examples**

### **PostgreSQL to CockroachDB**

#### **Schema Migration**
```sql
-- Original PostgreSQL schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CockroachDB equivalent
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
```

#### **Data Migration Script**
```python
import psycopg2
import uuid
from datetime import datetime

def migrate_users():
    # Source PostgreSQL connection
    source_conn = psycopg2.connect(
        host='source-host',
        database='source_db',
        user='user',
        password='password'
    )
    
    # Target CockroachDB connection
    target_conn = psycopg2.connect(
        host='target-host',
        database='target_db',
        user='user',
        password='password'
    )
    
    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()
    
    # Fetch data from source
    source_cursor.execute("SELECT id, username, email, created_at FROM users")
    users = source_cursor.fetchall()
    
    # Insert into target with UUID conversion
    for user in users:
        old_id, username, email, created_at = user
        new_id = uuid.uuid4()
        
        target_cursor.execute(
            "INSERT INTO users (id, username, email, created_at) VALUES (%s, %s, %s, %s)",
            (new_id, username, email, created_at)
        )
        
        # Store ID mapping for foreign key updates
        target_cursor.execute(
            "INSERT INTO id_mapping (old_id, new_id) VALUES (%s, %s)",
            (old_id, new_id)
        )
    
    target_conn.commit()
    source_cursor.close()
    target_cursor.close()
    source_conn.close()
    target_conn.close()
```

### **MySQL to MongoDB**

#### **Schema Migration**
```javascript
// Original MySQL schema
/*
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);
*/

// MongoDB equivalent
const productSchema = {
    _id: ObjectId,
    name: String,
    price: Number,
    category: {
        _id: ObjectId,
        name: String
    },
    createdAt: Date
};
```

#### **Data Migration Script**
```python
import mysql.connector
from pymongo import MongoClient
from datetime import datetime

def migrate_products():
    # MySQL connection
    mysql_conn = mysql.connector.connect(
        host='mysql-host',
        database='source_db',
        user='user',
        password='password'
    )
    
    # MongoDB connection
    mongo_client = MongoClient('mongodb://localhost:27017')
    db = mongo_client.target_db
    products_collection = db.products
    
    mysql_cursor = mysql_conn.cursor(dictionary=True)
    
    # Fetch products with categories
    query = """
    SELECT p.id, p.name, p.price, p.created_at, c.id as category_id, c.name as category_name
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
    """
    
    mysql_cursor.execute(query)
    products = mysql_cursor.fetchall()
    
    # Convert to MongoDB documents
    mongo_products = []
    for product in products:
        mongo_product = {
            'name': product['name'],
            'price': float(product['price']),
            'createdAt': product['created_at']
        }
        
        if product['category_id']:
            mongo_product['category'] = {
                '_id': product['category_id'],
                'name': product['category_name']
            }
        
        mongo_products.append(mongo_product)
    
    # Insert into MongoDB
    if mongo_products:
        products_collection.insert_many(mongo_products)
    
    mysql_cursor.close()
    mysql_conn.close()
    mongo_client.close()
```

## 🎯 **Conclusion**

These practical examples demonstrate how to implement different database solutions based on specific requirements:

- **Cassandra**: High availability, low latency for social media and IoT
- **MongoDB**: Strong consistency for e-commerce and content management
- **CockroachDB**: ACID compliance for financial systems
- **Redis**: Ultra-low latency for session management and real-time analytics

Each implementation shows the importance of:
1. **Choosing appropriate consistency levels**
2. **Using proper indexing strategies**
3. **Implementing efficient data models**
4. **Handling migrations carefully**
5. **Monitoring performance metrics**

---

**Last Updated**: January 2025  
**Maintainer**: Skynet Team  
**Version**: 1.0  
**Next Review**: March 2025
