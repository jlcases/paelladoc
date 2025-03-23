# Interface Contract Design Guide

## Core Principles

1. **Interface Segregation Principle (ISP)**
   - Keep interfaces small and focused
   - Clients should not depend on methods they don't use
   - Prefer multiple focused interfaces over one general-purpose interface

2. **Explicit Contract**
   - Clearly document preconditions, postconditions, and invariants
   - Define expected error behaviors and exceptions
   - Specify parameter and return value constraints

3. **Consistent Abstraction Level**
   - All methods in an interface should be at the same level of abstraction
   - Avoid mixing high-level and low-level operations
   - Ensure cohesive purpose across all interface methods

## Language-Specific Implementation Guidelines

### TypeScript Interfaces

```typescript
/**
 * Analyzer interface for processing page content.
 * 
 * Implementations must be stateless and thread-safe.
 * All methods must complete within 5 seconds or less.
 */
interface Analyzer {
  /**
   * Analyzes page content to identify issues.
   * 
   * @param context - The analysis context containing page data.
   *                  Must not be null or undefined.
   * @returns AnalysisResult - Contains found issues and metrics.
   *                          Will never return null.
   * @throws AnalysisError - If analysis fails due to invalid content.
   */
  analyze(context: AnalysisContext): AnalysisResult;
  
  /**
   * Provides recommendations based on previous analysis results.
   * Must be called after analyze().
   * 
   * @returns Array of recommendations sorted by priority.
   *          Empty array if no recommendations available.
   */
  getRecommendations(): Recommendation[];
  
  /**
   * Returns the unique identifier for this analyzer.
   * Must be unique across all analyzer implementations.
   * 
   * @returns A non-empty string identifier.
   */
  getId(): string;
}
```

### Java Interfaces

```java
/**
 * Defines operations for data persistence.
 * 
 * Implementations must be thread-safe and handle
 * transaction management internally.
 */
public interface DataRepository<T, ID> {
    /**
     * Finds an entity by its identifier.
     * 
     * @param id The entity identifier, must not be null
     * @return The entity if found
     * @throws NotFoundException if no entity exists with the given id
     * @throws RepositoryException if a persistence error occurs
     */
    T findById(ID id) throws NotFoundException, RepositoryException;
    
    /**
     * Saves an entity to the repository.
     * 
     * @param entity The entity to save, must not be null
     * @return The saved entity with any generated values populated
     * @throws ValidationException if the entity fails validation
     * @throws RepositoryException if a persistence error occurs
     */
    T save(T entity) throws ValidationException, RepositoryException;
    
    /**
     * Deletes an entity from the repository.
     * 
     * @param id The identifier of the entity to delete, must not be null
     * @throws NotFoundException if no entity exists with the given id
     * @throws RepositoryException if a persistence error occurs
     */
    void delete(ID id) throws NotFoundException, RepositoryException;
    
    /**
     * Checks if an entity exists with the given id.
     * 
     * @param id The entity identifier, must not be null
     * @return true if an entity exists, false otherwise
     * @throws RepositoryException if a persistence error occurs
     */
    boolean exists(ID id) throws RepositoryException;
}
```

### Python with Type Hints and ABC

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any

T = TypeVar('T')
ID = TypeVar('ID')

class Repository(Generic[T, ID], ABC):
    """
    Abstract repository interface for data access operations.
    
    All implementations must ensure data consistency and handle
    connection management internally.
    """
    
    @abstractmethod
    def find_by_id(self, id: ID) -> T:
        """
        Retrieve an entity by its identifier.
        
        Args:
            id: The entity identifier, must not be None
            
        Returns:
            The entity instance
            
        Raises:
            EntityNotFoundError: If no entity exists with the given id
            RepositoryError: If a data access error occurs
        """
        pass
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save an entity to the data store.
        
        If the entity already exists, it will be updated,
        otherwise it will be created.
        
        Args:
            entity: The entity to save, must not be None
            
        Returns:
            The saved entity with any generated values populated
            
        Raises:
            ValidationError: If the entity fails validation
            RepositoryError: If a data access error occurs
        """
        pass
    
    @abstractmethod
    def delete(self, id: ID) -> None:
        """
        Delete an entity from the data store.
        
        Args:
            id: The entity identifier, must not be None
            
        Raises:
            EntityNotFoundError: If no entity exists with the given id
            RepositoryError: If a data access error occurs
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Retrieve all entities.
        
        Returns:
            A list of all entities, empty list if none exist
            
        Raises:
            RepositoryError: If a data access error occurs
        """
        pass
```

## Interface Contract Documentation

### Essential Components

1. **Method Purpose**
   - Clear statement of what the method does
   - Context in which the method should be called
   - Relationship to other methods (if applicable)

2. **Parameter Specifications**
   - Type, format, and valid range of each parameter
   - Required vs. optional parameters
   - Default values and their implications
   - Validation rules that will be applied

3. **Return Value Specification**
   - Type and format of the return value
   - Special return values (null, empty collections, etc.)
   - State changes resulting from the method call

4. **Exception Behavior**
   - Expected exceptions and when they will be thrown
   - Error recovery recommendations
   - State guarantees after exceptions

5. **Threading Model**
   - Thread-safety guarantees
   - Synchronization requirements
   - Reentrance capabilities

6. **Performance Expectations**
   - Time complexity (Big O notation)
   - Resource usage patterns
   - Expected response times

### Documentation Example

```typescript
/**
 * Payment processing service for handling financial transactions.
 * 
 * Thread-safety: All methods are thread-safe.
 * Performance: Methods should respond within 2 seconds under normal conditions.
 * State: This interface is stateless; implementations should not maintain session state.
 */
interface PaymentService {
  /**
   * Processes a payment transaction.
   * 
   * Validates the payment request, authorizes the payment with the financial provider,
   * and records the transaction. If successful, the customer's payment method will be charged.
   * 
   * Idempotency: This method is idempotent when supplied with the same requestId.
   * Repeated calls with the same requestId will return the same result without
   * processing duplicate payments.
   * 
   * @param request - The payment details including amount, currency, payment method, etc.
   *                 Must contain a valid requestId which should be unique for new requests.
   * @returns PaymentResult - Contains transaction ID, status, and receipt information.
   *                         Status will never be "PROCESSING" when the method returns.
   * 
   * @throws ValidationError - If the payment request fails validation (invalid amount, currency, etc.)
   * @throws PaymentDeclinedError - If the payment was declined by the financial provider
   * @throws PaymentProviderError - If communication with the payment provider fails
   * 
   * Time complexity: O(1)
   * Resource usage: Makes 1-2 external API calls to payment provider
   */
  processPayment(request: PaymentRequest): PaymentResult;
  
  /**
   * Refunds a previously processed payment.
   * 
   * Partial refunds are supported by specifying an amount less than the original payment.
   * Multiple partial refunds are allowed up to the original payment amount.
   * 
   * @param transactionId - ID of the original payment transaction
   * @param amount - Amount to refund, must be > 0 and <= original payment amount
   * @param reason - Optional reason for the refund
   * @returns RefundResult - Contains refund transaction ID and status
   * 
   * @throws InvalidTransactionError - If the transaction ID doesn't exist or wasn't successful
   * @throws InvalidAmountError - If the amount exceeds the refundable amount
   * @throws RefundFailedError - If the refund was rejected by the payment provider
   */
  refundPayment(transactionId: string, amount: number, reason?: string): RefundResult;
}
```

## Interface Evolution Best Practices

### 1. Versioning Interfaces

When evolving interfaces, consider these strategies:

#### Explicit Versioning

```typescript
interface UserServiceV1 {
  findUser(id: number): User;
  createUser(data: UserData): User;
}

interface UserServiceV2 extends UserServiceV1 {
  findUserByEmail(email: string): User;
  // Enhanced version of an existing method
  createUser(data: EnhancedUserData): User;
}
```

#### Package-Based Versioning

```java
// In package com.example.api.v1
public interface PaymentService {
    TransactionResult processPayment(PaymentRequest request);
}

// In package com.example.api.v2
public interface PaymentService {
    TransactionResult processPayment(PaymentRequest request);
    TransactionResult processCryptoPayment(CryptoPaymentRequest request);
}
```

### 2. Backward Compatibility Guidelines

1. **Never remove methods** from an existing interface
2. **Never change method signatures** in incompatible ways:
   - Don't change return types (except to subtypes)
   - Don't add required parameters
   - Don't change parameter types (except to supertypes)
3. **Never strengthen preconditions** or weaken postconditions
4. **Never add checked exceptions** in Java interfaces

### 3. Forward Compatibility Techniques

1. **Use extension interfaces** for new functionality
2. **Provide default implementations** when available in the language
3. **Add optional parameters** with default values when possible
4. **Use builder pattern** for complex parameter sets

```typescript
// Original interface
interface MessageService {
  sendMessage(message: Message): void;
}

// Extension interface
interface EnhancedMessageService extends MessageService {
  // New functionality
  scheduleMessage(message: Message, deliveryTime: Date): void;
}

// Forward-compatible implementation technique
class MessageServiceImpl implements EnhancedMessageService {
  sendMessage(message: Message): void {
    // Implementation
  }
  
  scheduleMessage(message: Message, deliveryTime: Date): void {
    // Implementation
  }
}
```

## Testing Interface Contracts

### 1. Contract Test Suites

Create shared test suites that verify all implementations comply with the contract:

```java
/**
 * Abstract test class that validates the Repository contract.
 * Any Repository implementation should extend this test.
 */
public abstract class RepositoryContractTest<T, ID> {
    
    // Each implementation provides these
    protected abstract Repository<T, ID> getRepository();
    protected abstract T createValidEntity();
    protected abstract ID getNonExistentId();
    
    @Test
    public void shouldFindEntityById() {
        // Arrange
        T entity = createValidEntity();
        T savedEntity = getRepository().save(entity);
        
        // Act
        T foundEntity = getRepository().findById(getId(savedEntity));
        
        // Assert
        assertThat(foundEntity).isEqualTo(savedEntity);
    }
    
    @Test
    public void shouldThrowExceptionWhenEntityNotFound() {
        // Arrange
        ID nonExistentId = getNonExistentId();
        
        // Act & Assert
        assertThrows(NotFoundException.class, () -> {
            getRepository().findById(nonExistentId);
        });
    }
    
    // More contract tests...
}

// Implementation-specific test
public class JpaUserRepositoryTest extends RepositoryContractTest<User, Long> {
    @Autowired
    private JpaUserRepository repository;
    
    @Override
    protected Repository<User, Long> getRepository() {
        return repository;
    }
    
    @Override
    protected User createValidEntity() {
        return new User("test@example.com", "Test User");
    }
    
    @Override
    protected Long getNonExistentId() {
        return 999L;
    }
    
    // Additional implementation-specific tests...
}
```

### 2. Property-Based Testing

Use property-based testing to verify interface invariants:

```java
@Property
void validInputAlwaysProducesValidOutput(
    @ForAll @Valid UserData userData) {
    
    // Arrange
    UserService service = getUserService();
    
    // Act
    User user = service.createUser(userData);
    
    // Assert - verifying contract invariants
    assertThat(user.getId()).isNotNull();
    assertThat(user.getEmail()).isEqualTo(userData.getEmail());
    assertThat(user.getCreatedAt()).isNotNull();
}
```

### 3. Behavior Verification

Test the interface behaviors rather than implementation details:

```typescript
describe('PaymentService contract', () => {
  it('should prevent duplicate payments with the same requestId', async () => {
    // Arrange
    const paymentService = getPaymentService();
    const request = createValidPaymentRequest();
    
    // Act
    const result1 = await paymentService.processPayment(request);
    const result2 = await paymentService.processPayment(request); // Same request ID
    
    // Assert - verifying contract behavior
    expect(result1.transactionId).toBe(result2.transactionId);
    expect(result1.status).toBe(result2.status);
  });
  
  it('should throw ValidationError for invalid payment amount', async () => {
    // Arrange
    const paymentService = getPaymentService();
    const invalidRequest = createPaymentRequestWithInvalidAmount();
    
    // Act & Assert
    await expect(
      paymentService.processPayment(invalidRequest)
    ).rejects.toThrow(ValidationError);
  });
});
```

## Common Anti-Patterns to Avoid

### 1. Fat Interfaces

**Bad**:
```java
// Too many unrelated methods in one interface
interface SystemService {
    User authenticateUser(String username, String password);
    void logEvent(String eventType, String details);
    Report generateReport(ReportType type, Date start, Date end);
    void sendEmail(String to, String subject, String body);
    void backupDatabase();
    // And more unrelated operations...
}
```

**Good**:
```java
// Segregated interfaces
interface AuthenticationService {
    User authenticateUser(String username, String password);
}

interface LoggingService {
    void logEvent(String eventType, String details);
}

interface ReportingService {
    Report generateReport(ReportType type, Date start, Date end);
}

interface EmailService {
    void sendEmail(String to, String subject, String body);
}
```

### 2. Leaky Abstractions

**Bad**:
```typescript
// Leaking implementation details in the interface
interface UserRepository {
  findById(id: number): User;
  
  // These expose database details
  executeRawSql(sql: string): any[];
  getConnection(): DatabaseConnection;
}
```

**Good**:
```typescript
// Clean abstraction
interface UserRepository {
  findById(id: number): User;
  findByEmail(email: string): User;
  save(user: User): User;
  delete(id: number): void;
}
```

### 3. Ambiguous Contracts

**Bad**:
```java
/**
 * Process data somehow.
 */
public interface DataProcessor {
    /**
     * Process the data.
     */
    void process(Object data);
}
```

**Good**:
```java
/**
 * Processes input data by applying transformation rules
 * and validation checks.
 */
public interface DataProcessor {
    /**
     * Processes the provided data by:
     * 1. Validating against schema rules
     * 2. Applying transformation rules
     * 3. Normalizing values
     *
     * @param data Raw data to process, must not be null
     * @throws ValidationException if data fails validation
     * @throws ProcessingException if transformation fails
     * @return Processed data in standardized format
     */
    ProcessedData process(RawData data) throws ValidationException, ProcessingException;
}
```

## Conclusion

Well-designed interface contracts form the foundation of robust, maintainable software systems. By following these guidelines, you can create interfaces that:

1. **Clearly communicate expectations** to implementers and users
2. **Support evolution** without breaking existing code
3. **Facilitate testing** at the contract level
4. **Improve separation of concerns** through focused, cohesive interfaces

Remember that interfaces define the "what" without specifying the "how." A good interface should hide implementation details while clearly documenting the contract between components. 