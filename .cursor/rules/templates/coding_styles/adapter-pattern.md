# Adapter Pattern Implementation Guide

## Core Principles

The Adapter pattern converts the interface of a class into another interface clients expect. It lets classes work together that couldn't otherwise because of incompatible interfaces.

### Key Components

1. **Target Interface** - The interface that clients use (what we're adapting to)
2. **Adaptee** - The class with an incompatible interface (what we're adapting from)
3. **Adapter** - The class that makes Adaptee compatible with Target

## Implementation Guidelines

### TypeScript Implementation

```typescript
// Target Interface
interface Target {
  request(): string;
}

// Adaptee (incompatible interface)
class Adaptee {
  specificRequest(): string {
    return 'Specific behavior';
  }
}

// Object Adapter (uses composition)
class Adapter implements Target {
  private adaptee: Adaptee;
  
  constructor(adaptee: Adaptee) {
    this.adaptee = adaptee;
  }
  
  request(): string {
    return `Adapter: (TRANSLATED) ${this.adaptee.specificRequest()}`;
  }
}

// Client code
function clientCode(target: Target) {
  console.log(target.request());
}

// Usage
const adaptee = new Adaptee();
const adapter = new Adapter(adaptee);
clientCode(adapter);
```

### Java Implementation

```java
// Target Interface
interface Target {
    String request();
}

// Adaptee (incompatible interface)
class Adaptee {
    public String specificRequest() {
        return "Specific behavior";
    }
}

// Object Adapter using composition
class Adapter implements Target {
    private Adaptee adaptee;
    
    public Adapter(Adaptee adaptee) {
        this.adaptee = adaptee;
    }
    
    @Override
    public String request() {
        return "Adapter: (TRANSLATED) " + adaptee.specificRequest();
    }
}

// Client code
class Client {
    public static void clientCode(Target target) {
        System.out.println(target.request());
    }
    
    public static void main(String[] args) {
        Adaptee adaptee = new Adaptee();
        Target adapter = new Adapter(adaptee);
        clientCode(adapter);
    }
}
```

### Python Implementation

```python
# Target Interface (using ABC for explicitness)
from abc import ABC, abstractmethod

class Target(ABC):
    @abstractmethod
    def request(self) -> str:
        pass

# Adaptee (incompatible interface)
class Adaptee:
    def specific_request(self) -> str:
        return "Specific behavior"

# Adapter
class Adapter(Target):
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee
        
    def request(self) -> str:
        return f"Adapter: (TRANSLATED) {self._adaptee.specific_request()}"

# Client code
def client_code(target: Target) -> None:
    print(target.request())

# Usage
adaptee = Adaptee()
adapter = Adapter(adaptee)
client_code(adapter)
```

## Best Practices

### 1. Prefer Composition Over Inheritance

Always prefer object adapters (using composition) over class adapters (using inheritance) for:
- Improved maintainability
- Lower coupling
- Better testability
- Supporting multiple adaptees

```typescript
// RECOMMENDED: Object Adapter (composition)
class Adapter implements Target {
  private adaptee: Adaptee;
  
  constructor(adaptee: Adaptee) {
    this.adaptee = adaptee;
  }
  
  request(): string {
    return this.adaptee.specificRequest();
  }
}

// AVOID: Class Adapter (multiple inheritance - not possible in some languages)
class Adapter extends Adaptee implements Target {
  request(): string {
    return this.specificRequest();
  }
}
```

### 2. Complete Interface Implementation

Ensure adapters implement the entire target interface, not just the parts currently needed:

```typescript
// CORRECT: Full implementation of target interface
interface DataProvider {
  fetchData(): Promise<Data>;
  saveData(data: Data): Promise<void>;
  deleteData(id: string): Promise<void>;
}

class LegacyDataProviderAdapter implements DataProvider {
  constructor(private legacyProvider: LegacyProvider) {}
  
  fetchData(): Promise<Data> {
    return this.legacyProvider.getData()
      .then(legacyData => this.convertData(legacyData));
  }
  
  saveData(data: Data): Promise<void> {
    const legacyData = this.convertToLegacyFormat(data);
    return this.legacyProvider.updateData(legacyData);
  }
  
  deleteData(id: string): Promise<void> {
    return this.legacyProvider.removeRecord(id);
  }
  
  private convertData(legacyData: LegacyData): Data {
    // Conversion logic
  }
  
  private convertToLegacyFormat(data: Data): LegacyData {
    // Conversion logic
  }
}
```

### 3. Proper Error Translation

Always translate exceptions/errors from the adaptee to match the target interface contract:

```java
// CORRECT: Error translation
public class DatabaseAdapter implements DataStorage {
  private LegacyDatabase legacyDb;
  
  @Override
  public Data fetch(String id) throws NotFoundException {
    try {
      return legacyDb.retrieve(id);
    } catch (LegacyDbException e) {
      if (e.getErrorCode() == 404) {
        throw new NotFoundException("Item not found: " + id, e);
      }
      throw new StorageException("Database error: " + e.getMessage(), e);
    }
  }
}
```

### 4. Keep Adapters Focused

An adapter should focus on:
- Interface translation
- Type conversion
- Protocol adaptation

It should NOT:
- Add new business logic
- Filter or modify data beyond what's needed for conversion
- Cache or optimize (unless that's part of the interface contract)

```python
# CORRECT: Focused adapter
class PaymentServiceAdapter(PaymentProvider):
    def __init__(self, legacy_payment_service):
        self.service = legacy_payment_service
        
    def process_payment(self, payment: Payment) -> PaymentResult:
        # Only focuses on conversion and delegation
        legacy_payment = self._convert_to_legacy_format(payment)
        legacy_result = self.service.make_payment(legacy_payment)
        return self._convert_to_new_format(legacy_result)
    
    def _convert_to_legacy_format(self, payment):
        # Conversion logic only
        return LegacyPayment(
            amount=payment.amount,
            currency=payment.currency,
            card_token=payment.payment_method.token
        )
    
    def _convert_to_new_format(self, legacy_result):
        # Conversion logic only
        return PaymentResult(
            success=legacy_result.status == "OK",
            transaction_id=legacy_result.id,
            timestamp=datetime.fromisoformat(legacy_result.timestamp)
        )
```

### 5. Two-Way Adapters When Needed

If both interfaces need to interact, consider implementing two-way adapters:

```typescript
// Two-way adapter example
class MessageFormatAdapter {
  // Convert from new format to legacy format
  static toExternalFormat(internalMessage: InternalMessage): ExternalMessage {
    return {
      msgId: internalMessage.id,
      content: internalMessage.body,
      sender: internalMessage.fromUser,
      timestamp: internalMessage.sentAt.toISOString()
    };
  }
  
  // Convert from legacy format to new format
  static toInternalFormat(externalMessage: ExternalMessage): InternalMessage {
    return {
      id: externalMessage.msgId,
      body: externalMessage.content,
      fromUser: externalMessage.sender,
      sentAt: new Date(externalMessage.timestamp)
    };
  }
}
```

## Common Variants

### 1. Service Adapter

Adapts service interfaces, often used in API integrations:

```typescript
// Service adapter for payment gateway
class StripePaymentAdapter implements PaymentGateway {
  constructor(private stripeClient: Stripe) {}
  
  async processPayment(payment: PaymentRequest): Promise<PaymentResult> {
    try {
      const stripeResponse = await this.stripeClient.charges.create({
        amount: payment.amount * 100, // Convert to cents
        currency: payment.currency.toLowerCase(),
        source: payment.token,
        description: payment.description
      });
      
      return {
        success: true,
        transactionId: stripeResponse.id,
        amount: stripeResponse.amount / 100,
        timestamp: new Date(stripeResponse.created * 1000)
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        errorCode: this.mapErrorCode(error.code)
      };
    }
  }
  
  private mapErrorCode(stripeCode: string): string {
    // Map Stripe-specific error codes to our unified codes
    const errorMap: Record<string, string> = {
      'card_declined': 'PAYMENT_DECLINED',
      'incorrect_cvc': 'INVALID_CARD_DETAILS',
      // ...more mappings
    };
    
    return errorMap[stripeCode] || 'UNKNOWN_ERROR';
  }
}
```

### 2. Data Format Adapter

Converts between different data representations:

```java
// Data format adapter
public class JsonToXmlAdapter implements DataFormat {
    private JsonParser jsonParser;
    private XmlGenerator xmlGenerator;
    
    @Override
    public String convert(String input) {
        JsonNode jsonNode = jsonParser.parse(input);
        return xmlGenerator.generateFromJson(jsonNode);
    }
}
```

### 3. Bidirectional Adapter

Maintains both interfaces:

```typescript
class BidirectionalAdapter implements NewInterface, LegacyInterface {
  constructor(
    private newComponent: NewComponent | null = null,
    private legacyComponent: LegacyComponent | null = null
  ) {
    // One of the components must be provided
    if (!newComponent && !legacyComponent) {
      throw new Error("At least one component must be provided");
    }
  }
  
  // Implement NewInterface methods
  newMethod(): Result {
    if (this.newComponent) {
      return this.newComponent.newMethod();
    } else {
      // Adapt legacy method to match new interface
      const legacyResult = this.legacyComponent!.oldMethod();
      return this.convertToNewResult(legacyResult);
    }
  }
  
  // Implement LegacyInterface methods
  oldMethod(): OldResult {
    if (this.legacyComponent) {
      return this.legacyComponent.oldMethod();
    } else {
      // Adapt new method to match legacy interface
      const newResult = this.newComponent!.newMethod();
      return this.convertToOldResult(newResult);
    }
  }
  
  private convertToNewResult(oldResult: OldResult): Result {
    // Conversion logic
  }
  
  private convertToOldResult(newResult: Result): OldResult {
    // Conversion logic
  }
}
```

## Testing Adapters

### 1. Contract Compliance

Test that adapters properly implement the target interface:

```typescript
describe('PaymentGatewayAdapter', () => {
  it('should implement the full PaymentGateway interface', () => {
    const adapter = new StripePaymentAdapter(mockStripeClient);
    
    // Verify all interface methods exist and are callable
    expect(typeof adapter.processPayment).toBe('function');
    expect(typeof adapter.refundPayment).toBe('function');
    expect(typeof adapter.getTransaction).toBe('function');
  });
});
```

### 2. Conversion Verification

Test that data is properly converted between formats:

```typescript
test('should correctly convert adaptee data to target format', () => {
  const adaptee = new LegacyService();
  const adapter = new ServiceAdapter(adaptee);
  
  // Setup adaptee with test data
  jest.spyOn(adaptee, 'getLegacyData').mockReturnValue({
    old_id: '123',
    old_name: 'Test',
    old_values: [1, 2, 3]
  });
  
  // Call adapter method
  const result = adapter.getData();
  
  // Verify proper conversion
  expect(result).toEqual({
    id: '123',
    name: 'Test',
    values: [1, 2, 3]
  });
});
```

### 3. Error Handling

Test proper error translation:

```java
@Test
public void shouldTranslateAdapteeExceptionsToTargetExceptions() {
  // Create mock adaptee that throws exception
  LegacyService mockAdaptee = mock(LegacyService.class);
  when(mockAdaptee.fetchData()).thenThrow(new LegacyDataException("Not found", 404));
  
  ServiceAdapter adapter = new ServiceAdapter(mockAdaptee);
  
  // Verify exception is translated
  assertThrows(ResourceNotFoundException.class, () -> {
    adapter.getData();
  });
}
```

## Anti-Patterns to Avoid

### 1. Incomplete Interface Implementation

```typescript
// INCORRECT: Incomplete implementation
interface DataService {
  getData(): Promise<Data[]>;
  saveData(data: Data): Promise<void>;
  deleteData(id: string): Promise<void>;
}

class LegacyAdapter implements DataService {
  // Only implements part of the interface
  getData(): Promise<Data[]> {
    // Implementation
    return Promise.resolve([]);
  }
  
  // Missing methods:
  // - saveData
  // - deleteData
}
```

### 2. Leaky Abstraction

```java
// INCORRECT: Leaky abstraction
public class LeakyAdapter implements TargetInterface {
  private Adaptee adaptee;
  
  // BAD: Exposing the adaptee directly
  public Adaptee getAdaptee() {
    return adaptee;
  }
  
  // BAD: Requiring client to understand adaptee's error types
  public Result operation() throws AdapteeSpecificException {
    try {
      return convert(adaptee.specificOperation());
    } catch (AdapteeSpecificException e) {
      // Just passing through the adaptee's exception type
      throw e;
    }
  }
}
```

### 3. Overloaded Responsibility

```python
# INCORRECT: Adding business logic to adapter
class OverloadedAdapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee
        
    def request(self):
        # BAD: Adding business logic in the adapter
        if not self.is_authorized():
            raise PermissionError("Not authorized")
            
        # BAD: Doing data filtering/processing beyond conversion
        result = self.adaptee.specific_request()
        filtered_data = self.apply_business_rules(result)
        return filtered_data
        
    def is_authorized(self):
        # Authorization logic that doesn't belong in an adapter
        return True
        
    def apply_business_rules(self, data):
        # Business rules that don't belong in an adapter
        return filtered_data
``` 