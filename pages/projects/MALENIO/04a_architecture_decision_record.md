---
layout: project-layout
title: "Architecture Decision Record (ADR)"
description: "This document records significant architectural decisions made during the development of MALENIO, providing a historical record of the options considered, decisions made, and their justifications. Its purpose is to create transparency in the decision-making process, document architectural commitments, and serve as a reference for future team members and stakeholders."
project: "MALENIO"
date: 2025-03-15
order: 04
---


## Executive Summary

This document records significant architectural decisions made during the development of MALENIO, providing a historical record of the options considered, decisions made, and their justifications. Its purpose is to create transparency in the decision-making process, document architectural commitments, and serve as a reference for future team members and stakeholders.

Architectural decisions represent choices with significant impact on the structure, performance, maintainability, or functionality of the MALENIO system. Each decision has been made after careful analysis of alternatives and trade-offs.

## Decision Record Format

Each entry in this record follows a consistent format:

```
# ADR-[number]: [Decision Title]

## Status
[Accepted/Superseded/Replaced by ADR-XXX/Proposed]

## Date
YYYY-MM-DD

## Context
[Description of the problem or situation that motivates this decision]

## Options Considered
[List of evaluated alternatives]

## Decision
[Selected option with justification]

## Consequences
[Positive and negative impacts of this decision]

## References
[Documents, research, or sources consulted]
```

---

# ADR-001: Local vs. Cloud AI Processing

## Status
Accepted

## Date
2025-04-10

## Context
A central component of MALENIO is the capability for intelligent email analysis. We had to decide whether this processing should occur on remote cloud servers or locally on the user's machine. Emails contain potentially sensitive and confidential information, making privacy a critical consideration.

## Options Considered

1. **Cloud processing**
   - Advantages: Access to larger and more powerful models, no local hardware restrictions, faster processing, centralized updates.
   - Disadvantages: Privacy risks, dependency on internet connection, cloud infrastructure costs, complex regulatory compliance.

2. **Hybrid processing**
   - Advantages: Flexibility to choose which data is processed locally vs. in the cloud, balance between power and privacy.
   - Disadvantages: Additional technical complexity, potential confusion for users about which data is sent to remote servers.

3. **Completely local processing**
   - Advantages: Maximum privacy and security, no transmission of sensitive data, simplified regulatory compliance, offline operation, complete user control.
   - Disadvantages: Local hardware limitations, potentially less powerful models, more complex updates, variable performance depending on user hardware.

## Decision
Implement completely local processing through integration with Ollama to run AI models directly on the user's machine.

This decision aligns with our fundamental commitment to privacy and establishes a key differentiation from competitors who send data to remote servers. Advances in small but powerful AI models, along with the growing capability of consumer hardware, make this approach viable without significantly compromising processing quality.

## Consequences

**Positive**:
- Distinctive value proposition centered on extreme privacy
- Elimination of cloud infrastructure costs and scaling concerns
- Simplified compliance with privacy regulations such as GDPR, CCPA
- Possible offline operation for key functionalities
- Greater user trust by not extracting data from their communications

**Negative**:
- Limitation to models that can run on consumer hardware
- Potentially inconsistent experience depending on user hardware
- Additional complexity in initial installation and configuration
- Potential overload of the user's system with intensive processes
- More complex and bandwidth-consuming model updates

## References
- [Performance benchmarks of local AI models](https://example.com/local-ai-benchmark)
- Internal study on privacy concerns of Gmail users
- Proof of concept with Ollama on standard consumer hardware
- GDPR and CCPA regulations on personal data processing

---

# ADR-002: Local AI Model Selection

## Status
Accepted

## Date
2025-05-15

## Context
Having decided to use completely local AI processing, we needed to select which specific models to offer. This decision must balance capabilities, performance, and hardware requirements to provide the best possible experience on a variety of user devices.

## Options Considered

1. **Llama 2/3 Models**
   - Advantages: Well documented, widely compatible, good general performance.
   - Disadvantages: Larger sizes in some variants, Meta license.

2. **Mistral**
   - Advantages: Good performance in specific tasks, efficiency.
   - Disadvantages: Less optimized for email analysis, fewer available distillations.

3. **Phi-2/Phi-3**
   - Advantages: Extremely compact, surprising performance for its size.
   - Disadvantages: More limited capabilities, less specialized in extensive text analysis.

4. **DeepSeek R1 (various sizes)**
   - Advantages: Competitive performance, multiple distilled variants, good size/performance ratio, MIT license.
   - Disadvantages: Relatively newer, less extensively tested.

5. **Single default model approach**
   - Advantages: Simplification for the user, optimized installation, consistent quality.
   - Disadvantages: Not adaptable to different hardware capabilities, single experience.

6. **Flexible multi-model system**
   - Advantages: Adaptable to different devices, user choice, future support for new models.
   - Disadvantages: Additional complexity, more testing needed, possible user confusion.

## Decision
Implement a flexible multi-model system with pre-selected options in different power/requirement ranges:

- **DeepSeek-R1-Distill-Qwen-1.5B**: Lightweight option for systems with limited resources (1.1GB, ~6GB VRAM)
- **DeepSeek-R1-Distill-Qwen-7B**: Balanced option (requires ~12GB VRAM)
- **DeepSeek-R1-Distill-Llama-8B**: Llama-based alternative (requires ~14GB VRAM)
- **Llama 3.1 (8B)**: High-quality option (requires ~16GB VRAM)

With automatic hardware detection to suggest the optimal model and ease of switching between models at any time.

## Consequences

**Positive**:
- Accessibility to users with different hardware capabilities
- Flexibility to choose between performance and efficiency
- Ability to incorporate new models as they become available
- Better user experience tailored to their specific resources
- Future support for models specialized in specific tasks

**Negative**:
- Greater complexity in testing and maintenance
- Need to maintain compatibility with multiple models
- Possible user confusion about which model to choose
- Increased disk space usage for users who install multiple models
- Additional complexity in the installation system

## References
- Internal benchmarks comparing model performance in email analysis
- [Ollama model repository](https://ollama.com/library)
- Typical hardware statistics for Chrome extension users
- User tests on model selection understanding

---

# ADR-003: Chrome Extension Architecture

## Status
Accepted

## Date
2025-04-25

## Context
MALENIO requires deep integration with Gmail, access to email content, and the ability to modify the user interface. We needed to determine the architectural approach for the browser extension that best supports these requirements while maintaining compliance with Chrome extension policies.

## Options Considered

1. **MV2 Architecture (Manifest V2 - Obsolete)**
   - Advantages: More permissive APIs, more direct DOM access, better support for persistent background scripts.
   - Disadvantages: Being discontinued by Google, limited future, longer review times.

2. **MV3 Architecture with Service Worker**
   - Advantages: Approved for long-term future, better performance, increased security, faster review times.
   - Disadvantages: Limitations for persistent background scripts, more restrictive permissions model.

3. **Progressive Web Application (PWA)**
   - Advantages: Browser independence, fewer restrictions, simpler updates.
   - Disadvantages: Limited integration with Gmail, separate experience, restricted access to email data.

4. **Hybrid Solution (Extension + Desktop Application)**
   - Advantages: Ability to split responsibilities, process locally outside the browser, fewer limitations.
   - Disadvantages: More complex installation, two components to maintain, potential communication issues.

## Decision
Adopt an **MV3 (Manifest V3) architecture with communication to a local application** that combines:

1. **Chrome MV3 Extension** for Gmail integration, UI, and data access
2. **Local component (integrated with Ollama)** for AI processing and storage

This architecture complies with current Chrome guidelines, ensures long-term support, and allows powerful local processing while maintaining an integrated experience with Gmail.

## Consequences

**Positive**:
- Long-term compatibility with Chrome and possibly other Chromium-based browsers
- Simple distribution through the Chrome Web Store
- Clear separation of responsibilities between components
- Better performance and security than MV2
- Ability to access system resources through the local component

**Negative**:
- Additional complexity in communication between components
- More complex installation (two components)
- Limitations of the Service Worker lifecycle for background operations
- Potential synchronization issues between extension and local application
- Greater effort to stay updated with changes in MV3

## References
- [Chrome Extensions Manifest V3 Documentation](https://developer.chrome.com/docs/extensions/mv3/intro)
- Study of extension architectures for local processing
- Analysis of Chrome API limitations for Gmail access
- Proof of concept for communication between extensions and local applications

---

# ADR-004: Ollama Integration

## Status
Accepted

## Date
2025-05-20

## Context
To implement local AI capability, we needed a system that would allow efficient execution of language models on the user's device in an accessible way with minimal configuration. Integration with this system must be robust, efficient, and easy to use.

## Options Considered

1. **Custom implementation with low-level libraries**
   - Advantages: Complete control, specific optimizations, independence.
   - Disadvantages: Significant complexity, costly maintenance, steep development curve.

2. **LlamaIndex/LangChain with custom backend**
   - Advantages: Structured frameworks, pre-designed advanced functionalities.
   - Disadvantages: Additional overhead, complex dependencies, heavier installation.

3. **Ollama**
   - Advantages: Simple packaging, clear REST API, built-in model management, cross-platform.
   - Disadvantages: Dependency on external project, limitations in deep customization.

4. **LocalAI**
   - Advantages: Very flexible, support for multiple backends, compatible with OpenAI API.
   - Disadvantages: More complex to configure, less optimized for end users.

5. **Browser-based solution (WebGPU/WebGL)**
   - Advantages: No additional installation required, fully integrated.
   - Disadvantages: Significantly inferior performance, inconsistent support between browsers/hardware.

## Decision
Adopt **Ollama** as the AI model execution system, with a custom installer that simplifies its configuration and direct communication from the extension.

Ollama offers the best balance between ease of use and power, with a clear and consistent API, good model management, and a packaging system that minimizes friction for the end user. Its growing ecosystem and community support also ensure its long-term viability.

## Consequences

**Positive**:
- Significant simplification of development by using established APIs
- Robust model management with built-in update system
- Cross-platform compatibility (Windows, macOS, Linux)
- Active community and continuous development
- Easy expansion to new models as they become available

**Negative**:
- Dependency on an external project and its roadmap
- Need to adapt to changes in the Ollama API
- Limitations in specific optimizations for our use case
- Potential overhead from unused functionalities
- Need to encapsulate the installation for a smooth experience

## References
- [Official Ollama Documentation](https://ollama.com/docs)
- Comparative performance tests between different runtimes
- Analysis of ease of installation for end users
- Feasibility study of all-in-one installers

---

# ADR-005: Advanced Search and Batch Operations Strategy

## Status
Accepted

## Date
2025-06-01

## Context
A key functionality of MALENIO is the ability to search emails with complex criteria and perform group actions on the results. This capability requires an approach that balances search power, performance, and compatibility with the Gmail API.

## Options Considered

1. **100% local search**
   - Advantages: Complete control, possibility of full semantic search, independence from API limitations.
   - Disadvantages: Requires local indexing of all emails, high resource utilization, potential inconsistencies.

2. **Complete delegation to Gmail API**
   - Advantages: No data duplication, guaranteed consistency, better performance for large volumes.
   - Disadvantages: Limited to Gmail search capabilities, no advanced semantic search.

3. **Hybrid approach with delegated predicates**
   - Advantages: Combines the best of both worlds, performance optimization, lower local load.
   - Disadvantages: Complexity in coordination, need to maintain both capabilities.

4. **Intelligent cache system with local enrichment**
   - Advantages: Optimized performance, advanced search on filtered results, better user experience.
   - Disadvantages: Need for cache management, possible temporary inconsistencies.

## Decision
Implement a **hybrid search and batch action system** that:

1. Uses the Gmail API (`messages.list` with `q` parameter) for initial structured searches
2. Applies additional semantic filtering and enrichment locally as needed
3. Uses Gmail API's `batchModify` for efficient batch operations (up to 1000 messages)
4. Implements operations like archiving/moving to trash through system label manipulation (INBOX, TRASH)
5. Maintains intelligent cache of frequent results for better performance

This approach maximizes efficiency by leveraging the strengths of the Gmail API while extending its capabilities with local processing.

## Consequences

**Positive**:
- Efficient operations on large batches of up to 1000 messages
- Optimized performance by delegating initial searches to Gmail
- Extended capabilities beyond the API's limitations
- Lower resource consumption by processing only relevant subsets
- Full compatibility with other tools/clients that access Gmail

**Negative**:
- Greater complexity in implementation and maintenance
- Need to handle failures in partial operations
- Inherited limitations from the Gmail API (e.g., no thread-level search)
- Potential performance challenges in very complex searches
- Additional handling for synchronization of local and remote state

## References
- [Gmail API filtering documentation](https://developers.google.com/gmail/api/guides/filtering)
- [batchModify reference](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/batchModify)
- Search performance tests on large email volumes
- Analysis of common search and action patterns in Gmail users

---

# ADR-006: Installation and Configuration Strategy

## Status
Accepted

## Date
2025-06-10

## Context
MALENIO's adoption significantly depends on a smooth installation experience, especially considering the added complexity of configuring a local AI engine. We needed to define a strategy that minimizes entry friction while implementing technically complex components.

## Options Considered

1. **Manual installation of separate components**
   - Advantages: Complete transparency, granular control for the user.
   - Disadvantages: Significant friction, high abandonment rate, complexity for non-technical users.

2. **Chrome Extension + Instructions for Ollama**
   - Advantages: Simplicity for the extension, shared responsibility.
   - Disadvantages: Fragmented experience, multiple friction points, dependence on correct installation by the user.

3. **All-in-one installer with wizard**
   - Advantages: Unified experience, maximum simplicity for the user, control over the environment.
   - Disadvantages: Development complexity, potential permission issues, maintenance of multiple installers.

4. **Chrome Extension with automatic on-demand download**
   - Advantages: Lighter initial installation, components downloaded only when needed.
   - Disadvantages: Potential surprises for the user, fragmented experience, potential failures in secondary downloads.

## Decision
Implement an **all-in-one installer with guided wizard** that:

1. Installs the Chrome extension directly from the installer
2. Configures Ollama with zero command line interaction
3. Evaluates the user's hardware and recommends appropriate models
4. Downloads selected models in the background
5. Verifies and configures system requirements automatically
6. Completes all configuration in a maximum of 5 clicks
7. Provides a visually attractive experience with clear progress indicators

This strategy prioritizes friction reduction and a cohesive user experience above the technical separation of components.

## Consequences

**Positive**:
- Dramatic reduction in the entry barrier
- Professional and smooth experience for the user
- Control over the execution environment and compatibility
- Higher rate of complete successful installations
- Improved perception of product quality

**Negative**:
- Greater complexity in development and maintenance
- Need to maintain platform-specific installers
- Potential challenges with system permissions
- Larger initial download size
- More complex updates for packaged components

## References
- Usability studies on software installation
- Analysis of abandonment cases in multi-stage processes
- Benchmarks of all-in-one installers in complex applications
- User tests on different platforms

---

# ADR-007: Monetization Strategy

## Status
Accepted

## Date
2025-06-15

## Context
To ensure the sustainability of the MALENIO project, we needed to define a monetization model that generates sufficient revenue while maintaining the commitment to privacy and local processing, without alienating potential users.

## Options Considered

1. **Completely free model**
   - Advantages: Maximum adoption, no barriers, aligned with privacy philosophy.
   - Disadvantages: No direct revenue, dependence on external funding, questionable sustainability.

2. **Freemium model (free basic functions, paid premium)**
   - Advantages: Low entry barrier, clear monetization path, flexibility for users.
   - Disadvantages: Need to balance free vs. paid value, greater product complexity.

3. **Pure subscription (all paid after trial period)**
   - Advantages: Predictable revenue model, simplicity of single product.
   - Disadvantages: Higher entry barrier, potential negative perception for privacy tool.

4. **One-time purchase + optional updates**
   - Advantages: No recurring costs for users, psychology of ownership.
   - Disadvantages: Non-recurring revenue, challenges to fund continuous development.

5. **Monetization through complementary services**
   - Advantages: Main product can be free, indirect revenue models.
   - Disadvantages: Potential misalignment with core values, dependence on additional services.

## Decision
Implement a **freemium model with service tiers** that includes:

1. **Free Tier**:
   - Basic organization and search functionality
   - Reasonable limits on processing volume
   - Access to lighter AI models
   - Complete privacy and local processing functionality

2. **Premium Tier** (monthly/annual subscription):
   - Advanced features (complete analysis, assisted responses)
   - No processing limits
   - Access to all AI models
   - Priority support
   - Advanced customization

3. **Enterprise Option** (per user/year):
   - Functions specific to business environments
   - Centralized administration
   - Additional integrations
   - Dedicated support
   - Customizable deployment

This model allows any user to benefit from the basic privacy-centered capabilities while offering a clear path for sustainable monetization.

## Consequences

**Positive**:
- Wide accessibility to basic functionalities
- Sustainable revenue stream for continuous development
- Incentive to deliver more value in premium tiers
- Clear value proposition for different segments
- Possibility to adjust the balance between free/premium over time

**Negative**:
- Additional complexity in development and maintenance of multiple tiers
- Challenge of correctly balancing free vs. premium value
- Potential negative perception for "withholding" features
- Need for subscription and payment management platform
- Additional fiscal and legal implications

## References
- Analysis of business models in premium Chrome extensions
- Studies on willingness to pay in productivity tools
- Freemium conversion benchmarks in privacy applications
- Surveys of potential users on monetization preferences

---

# ADR-008: Web Management Platform

## Status
Accepted

## Date
2025-06-20

## Context
The management of accounts, subscriptions, and advanced configuration of MALENIO required a more robust solution than what a browser extension can natively provide. We needed to define the architecture of a complementary component for these functions.

## Options Considered

1. **No web platform (everything in the extension)**
   - Advantages: Simplicity, less infrastructure, consistency with local processing.
   - Disadvantages: Severe limitations for account/subscription management, restricted user experience.

2. **Minimal web platform only for subscriptions**
   - Advantages: Focus on essentials, lower development cost, smaller attack surface.
   - Disadvantages: Fragmented experience, limited capabilities, restricted growth.

3. **Complete web platform with dashboard**
   - Advantages: Rich experience, advanced management capabilities, potential for community and support.
   - Disadvantages: Higher development and maintenance cost, need for cloud infrastructure.

4. **Integration with existing platforms (GitHub, Discord, etc.)**
   - Advantages: Faster development, existing infrastructure, established communities.
   - Disadvantages: Less control, fragmented experience, dependency on third parties.

## Decision
Implement a **complete web platform with user dashboard** that:

1. Manages user accounts and subscriptions
2. Provides configuration synchronization between devices
3. Offers privacy-preserving usage statistics
4. Hosts support resources and documentation
5. Facilitates a user community
6. Allows advanced preference management

The platform will maintain a clear separation between account/subscription data and email content, which will never be transmitted outside the user's device.

## Consequences

**Positive**:
- Professional and complete user experience
- Robust management of accounts and subscriptions
- Ability to develop a user community
- Potential for additional web-based features
- Better support and onboarding experience

**Negative**:
- Need for backend infrastructure and maintenance
- Additional development and operation costs
- Potential confusion about the privacy model
- Larger surface for security attacks
- Challenges of consistency between web and extension experience

## References
- Analysis of web platforms for similar SaaS products
- Evaluation of infrastructure and development costs
- Studies of user expectations for account management
- Architecture models that preserve privacy while offering web services

---

# ADR-009: Security and Audit Strategy

## Status
Accepted

## Date
2025-06-25

## Context
Given the sensitive nature of the data processed by MALENIO (emails), and our central commitment to privacy, we needed to establish a security and audit strategy that ensures the integrity of the system and user trust.

## Options Considered

1. **Reactive approach based on reports**
   - Advantages: Lower initial cost, operational simplicity.
   - Disadvantages: Potential undetected vulnerabilities, reputational damage in case of incident.

2. **Periodic internal review**
   - Advantages: Process control, moderate costs, flexibility.
   - Disadvantages: Potential lack of objectivity, possible blind spots, lower external credibility.

3. **External audit and partial open source**
   - Advantages: Greater credibility, problem detection by multiple parties, balance between transparency and ownership.
   - Disadvantages: Moderate to high costs, management of partial exposure, complexity.

4. **Completely open source project**
   - Advantages: Maximum transparency, potential for external contributions, high credibility.
   - Disadvantages: Monetization challenges, potential for forks, exposure of intellectual property.

## Decision
Implement an **external audit and partial open source strategy** that includes:

1. Security audits by independent third parties before each major release
2. Publication of critical privacy components as open source for review
3. Vulnerability detection reward program (bug bounty)
4. Detailed documentation of the security model and data flow
5. Formal incident response processes
6. No collection of telemetry that compromises privacy

This approach provides a balance between transparency and commercial sustainability, prioritizing the verifiability of privacy-related aspects.

## Consequences

**Positive**:
- Greater user trust in privacy guarantees
- Early detection of potential vulnerabilities
- Market differentiation as a verifiably secure solution
- Potential contributions and improvements from the community
- Better resistance to attacks and vulnerabilities

**Negative**:
- Additional costs for audits and bug bounty program
- Complexity in managing open vs. proprietary components
- Need for more rigorous security documentation and processes
- Potential delays in releases due to audit cycles
- Careful management of public security findings

## References
- OWASP standards for web application security
- Partial open source models in commercial privacy products
- Cost-benefit analysis of bug bounty programs
- Surveys on trust factors in privacy tools

---

# ADR-010: Testing and Quality Strategy

## Status
Accepted

## Date
2025-07-01

## Context
The complex nature of MALENIO, which combines browser extension, local AI processing, and email manipulation, presents significant challenges for ensuring product quality and reliability. We needed to establish a testing strategy that addresses these complexities.

## Options Considered

1. **Primarily manual testing**
   - Advantages: Flexibility, lower initial investment, adaptability to rapid changes.
   - Disadvantages: Not scalable, inconsistent, limited coverage, undetected regressions.

2. **End-to-end automation with real data**
   - Advantages: Realistic tests, high confidence, validation of complete flows.
   - Disadvantages: Privacy challenges, technical complexity, test fragility, costly maintenance.

3. **Layered approach with simulation**
   - Advantages: Balance between coverage and feasibility, component isolation, better maintainability.
   - Disadvantages: Potential gaps between simulation and reality, greater initial effort.

4. **Testing in production with gradual channels**
   - Advantages: Validation in real environments, early detection of environment-specific problems.
   - Disadvantages: Risks for users, infrastructure complexity, potential reputational impact.

## Decision
Implement a **layered testing strategy with gradual release channels** that includes:

1. **Unit tests** for isolated components with high coverage
2. **Integration tests** between subsystems with simulated APIs
3. **Sandbox environment** with Gmail simulation for complete flow testing
4. **Performance tests** specific to intensive operations
5. **Compatibility tests** across platforms and devices
6. **Gradual release channels**:
   - Alpha channel for internal testing
   - Beta channel for voluntary early users
   - Stable channel for all users

This approach provides a balance between reliability, feasibility, and protection of user data.

## Consequences

**Positive**:
- Early detection of issues in critical components
- Ability to test complete flows without compromising real data
- Feedback from real users before general releases
- Greater confidence in product quality
- Ability to test complex hardware/software combinations

**Negative**:
- Significant investment in testing infrastructure
- Additional complexity in the development process
- Need to keep simulation environments updated
- Potential differences between simulated and real environment
- Management of multiple release channels

## References
- Testing practices in high-profile browser extensions
- Simulation strategies for external APIs
- Gradual release models in complex software
- Analysis of production failure costs vs. testing investment

---

## Revision History

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-03-12 | 1.0 | Initial document with ADRs 001-010 | MALENIO Architecture Team | 