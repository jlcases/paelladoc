---
title: "Ruby on Rails - Style Guide and Best Practices"
date: 2025-03-22
author: "PAELLADOC"
version: 1.0
status: "Active"
tags: ["Ruby", "Rails", "backend", "MVC", "web"]
---

# Ruby on Rails - Style Guide and Best Practices

## Project Structure
- Follow the "Convention over Configuration" principle
- Maintain clear separation of MVC architecture
- Use namespaces to organize related code
- Group complex functionality into engines when needed
- Place complex logic in services, not in controllers or models

## Naming Conventions
- **Models**: Singular, CamelCase (e.g., `User`, `BlogPost`)
- **Controllers**: Plural, CamelCase (e.g., `UsersController`)
- **Tables**: Plural, snake_case (e.g., `users`, `blog_posts`)
- **Methods and variables**: snake_case (e.g., `find_by_email`)
- **Service classes**: Verb + noun (e.g., `AuthenticateUser`)
- **Workers and Jobs**: Suffix with `Worker` or `Job` (e.g., `EmailNotificationWorker`)

## Models
- Use Active Record validations to ensure data integrity
- Implement callbacks with moderation and for simple logic
- Extract complex business logic to services or modules
- Use concerns to share functionality between models
- Keep relationship definitions at the top of the model
- Use scopes for frequent and complex queries
- Implement thin models and avoid "fat models"

## Controllers
- Follow RESTful pattern (7 main actions)
- Keep controllers lightweight without business logic
- Use `before_action` for repetitive logic
- Allow only necessary parameters with `strong_parameters`
- Handle responses in multiple formats (HTML, JSON, etc.) consistently
- Implement consistent API design for API controllers

## Views
- Use partials for reusable elements
- Keep presentation logic in helpers or view objects
- Implement hierarchically structured layouts
- Avoid complex logic in views
- Limit database calls in views
- Use I18n for text and messages

## Active Record
- Use migrations for all schema changes
- Prefer scopes over class methods for queries
- Use includes/eager_loading to avoid N+1 queries
- Implement indexes on frequently queried columns
- Use transactions for operations that must be atomic
- Keep migrations idempotent and reversible

## Security
- Validate and sanitize all user inputs
- Protect against CSRF using Rails' built-in protection
- Implement authorization with gems like Pundit or CanCanCan
- Prevent SQL injection using ActiveRecord's secure query methods
- Protect against XSS using appropriate escape helpers
- Follow OWASP guidelines for web security

## Testing
- Implement unit tests for models and services
- Write integration tests for important flows
- Use factories instead of fixtures (with FactoryBot)
- Apply TDD/BDD when appropriate
- Maintain a complete and fast test suite
- Test edge cases and validations

## Performance
- Use caching effectively (fragment, Russian doll, etc.)
- Implement background jobs for heavy tasks (using Sidekiq or similar)
- Optimize N+1 queries with eager loading
- Apply pagination for large collections
- Use Turbo/Hotwire for partial page updates
- Monitor and optimize slow queries

## Dependency Management
- Keep Gemfile organized by purpose
- Specify gem versions explicitly
- Document the purpose of each non-standard gem
- Evaluate maintenance and security of gems before including them
- Regularly update gems for security and features

## Deployment
- Use staging environments that mirror production
- Implement CI/CD for automated testing before deployment
- Use zero-downtime migrations when possible
- Implement code reviews before deployment
- Maintain automated and consistent deployment scripts
- Follow containerization best practices if using Docker

## Advanced Code Organization
- **Services**: `app/services` for complex business logic
- **Queries**: `app/queries` for complex queries
- **Presenters**: `app/presenters` for presentation logic
- **Values**: `app/values` for immutable value objects
- **Policies**: `app/policies` for authorization rules
- **Decorators**: `app/decorators` for extending models with presentation logic

## Recommended Tools
- **Linting**: RuboCop for enforcing style guide
- **Testing**: RSpec, Capybara, FactoryBot
- **Debugging**: Pry, Byebug
- **Documentation**: YARD or RDoc
- **Analysis**: Brakeman for security, Bullet for N+1 queries
- **Monitoring**: New Relic, Skylight, or Scout 