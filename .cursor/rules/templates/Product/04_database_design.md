# Database Design Template

## Database Overview

- **Database Type**: [Relational, NoSQL, Hybrid, etc.]
- **Database Technology**: [PostgreSQL, MongoDB, etc.]
- **Database Version**: [Version requirements]
- **Purpose**: [Primary purpose of this database]

## Schema Organization

- **Schemas/Namespaces**: [How schemas are organized]
- **Schema Ownership**: [Which components own which schemas]
- **Cross-Schema Access Patterns**: [How cross-schema access is managed]
- **Schema Isolation Principles**: [Principles for schema isolation]

## Table/Collection Design

- **Entity Tables**: [Tables representing primary business entities]
- **Relationship Tables**: [Tables representing relationships between entities]
- **Reference Tables**: [Tables containing reference/lookup data]
- **Audit Tables**: [Tables for audit/history tracking]
- **Temporary/Staging Tables**: [Tables for temporary data processing]

## Data Types and Constraints

- **Standard Data Types**: [Standard data types used across the database]
- **Custom Data Types**: [Any custom data types]
- **Constraints**: [Common constraints applied]
- **Default Values**: [Default value conventions]
- **Validation Rules**: [Rules for data validation]

## Indexing Strategy

- **Primary Keys**: [Primary key conventions]
- **Foreign Keys**: [Foreign key conventions]
- **Performance Indexes**: [Indexes for query performance]
- **Unique Indexes**: [Indexes enforcing uniqueness]
- **Composite Indexes**: [Multi-column indexes]
- **Special Indexes**: [Full-text search, spatial, etc.]

## Query Patterns

- **Common Queries**: [Frequently executed queries]
- **Complex Queries**: [Complex queries and their optimization]
- **Reporting Queries**: [Queries used for reporting]
- **Analytical Queries**: [Queries used for analytics]

## Performance Optimization

- **Query Optimization**: [Strategies for optimizing queries]
- **Partitioning**: [Table partitioning approach]
- **Materialized Views**: [Use of materialized views]
- **Stored Procedures**: [Use of stored procedures]
- **Database Functions**: [Custom database functions]

## Data Access Patterns

- **Read Patterns**: [How data is read]
- **Write Patterns**: [How data is written]
- **Concurrency Control**: [How concurrent access is managed]
- **Transaction Management**: [Transaction boundaries and isolation levels]

## Data Lifecycle Management

- **Data Retention**: [Data retention policies]
- **Archiving Strategy**: [How data is archived]
- **Purging Strategy**: [How data is purged]
- **Historical Data Access**: [How historical data is accessed]

## Security and Permissions

- **Access Control**: [Database-level access control]
- **Role-Based Permissions**: [Roles and their permissions]
- **Row-Level Security**: [Row-level security policies]
- **Column-Level Security**: [Column-level security policies]
- **Data Encryption**: [Encryption of sensitive data]

## Migration and Change Management

- **Schema Migration Strategy**: [How schema changes are applied]
- **Versioning Approach**: [How database versions are managed]
- **Rollback Procedures**: [How changes are rolled back if needed]
- **Test Data Management**: [Management of test data during migration]

---

This template follows MECE principles by addressing all distinct aspects of database design without overlap, ensuring a comprehensive database design specification.
