# Changelog
All notable changes to PAELLADOC will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-08-01

### Breaking Changes
- Complete restructuring for Cursor 0.47 compatibility
- New `.cursorrules` architecture for dynamic rule loading
- Changed template organization structure
- Modified AI interaction patterns
- Updated for Cursor's new MDC format

### Added
- Dynamic rule loading system with priorities
- Timestamp management system with multiple formats
- AI operation modes (autonomous, collaborative, advisory)
- Template hooks system for automation
- Enhanced memory system with better categorization
- Comprehensive template organization in `.cursor/rules/templates/`
- New documentation validation system
- Support for Cursor 0.47 features
- Automatic deep research system for market research documents
- Comprehensive market validation with cross-referencing
- New `FORCE_RESEARCH` command for mandatory automatic document research
- Architecture Decision Record (ADR) lifecycle management
- `UPDATE_ADR` command for architectural decision tracking
- Proper timestamping system for all generated documents
- Frontmatter YAML management with metadata standardization
- Template variable substitution with context-aware values
- Confidence scoring system for research reliability
- Deep validation system with multiple verification levels
- Global priorities configuration for research automation
- Document settings with standardized formatting rules
- Automatic MDC generation from completed documentation
- `GENERATE_MDC` command for creating development MDC files
- Documentation completeness tracking and reporting
- Seamless transition from documentation to development
- Automatic extraction of development rules from docs
- Improved MDC generation system with true orchestrator architecture
- Dedicated MDC template focusing on referencing documentation
- Enhanced MDC structure with explicit source references for each rule
- Clear separation between documentation and MDC orchestration
- File pattern-based rules mapping to specific documentation files

### Changed
- Moved to new Cursor 0.47 rules architecture
- Improved command structure with more specific arguments
- Enhanced template system organization
- Updated priorities system with descriptions
- Improved documentation structure validation
- Enhanced security review system
- Optimized for Cursor 0.47 performance
- Enhanced the CONTINUE workflow with automatic research detection
- Modified document generation to include academic references
- Updated market research process to validate all claims with 3+ sources
- Improved document templates with proper YAML frontmatter
- Enhanced research workflow to prevent hallucinations
- Optimized command structure for professional use cases
- Modified CONTINUE to check documentation completeness
- Added auto-detection of documentation completeness
- Enhanced workflow to offer MDC generation when ready
- Changed MDC file extension to .mdc.example for clarity on required renaming
- Improved CONTINUE workflow to automatically generate MDC when user indicates documentation is complete
- Added explicit "MARK DOCUMENTATION AS COMPLETE" option to trigger immediate MDC generation
- Redesigned MDC generation to act as a true orchestrator that references documentation instead of duplicating it
- Updated messages to clearly explain the orchestrator role of the MDC file

### Fixed
- Timestamp generation in document frontmatter
- Template variable substitution during document creation
- Research workflow to prioritize automatic data gathering
- Documentation structure validation for market research
- MDC file generation path to store files in the project's directory instead of a fixed location
- Instructions for using generated MDC file and documentation in the actual development project
- MDC structure to properly reference documentation files instead of duplicating content

### Removed
- Old Cursor integration methods
- Legacy template structure
- Deprecated command formats
- Support for Cursor versions below 0.47

## [1.0.0] - 2024-03-11

### Added
- Initial release of PAELLADOC
- Basic MECE documentation system
- Core commands (PAELLA, CONTINUE, ACHIEVEMENT, ISSUE, DECISION, MEMORY, VERIFY)
- Basic template system
- Documentation structure
- Memory system
- Project directives 