# Source Verification Template

## Purpose
This template provides a standardized structure for verifying and documenting information sources used in project documentation, following the MECE principle (Mutually Exclusive, Collectively Exhaustive).

## Structure

### Metadata
```
---
title: [Document Title]
date: [YYYY-MM-DD]
author: [Author or Team]
status: [Draft/In Review/Completed]
version: [X.Y]
last_sources_verification_date: [YYYY-MM-DD]
---
```

### References Section
At the end of each document containing statistical data, market figures, or statements based on external sources, include a References section with the following format:

```
## References

### [Category 1 - e.g. Market Size and Growth]
1. [Author/Organization]. (Year). [Document/Report Title]. Retrieved from [URL]
   - [Key data point 1 extracted from this source]
   - [Key data point 2 extracted from this source]
   - [Key data point 3 extracted from this source]

### [Category 2 - e.g. User Statistics]
1. [Author/Organization]. (Year). [Document/Report Title]. Retrieved from [URL]
   - [Key data point 1 extracted from this source]
   - [Key data point 2 extracted from this source]

### Last sources verification date: [YYYY-MM-DD]
```

## Verification Criteria (MECE)

### Currency
- **Maximum age**: 1-2 years for market data and statistics
- **Publication date**: Clearly identified
- **Version or edition**: Specified when relevant

### Credibility
- **Source type**: Prioritize primary sources over secondary ones
- **Authority**: Recognized organizations, respected researchers, peer-reviewed publications
- **Methodology**: Transparent and solid for studies or surveys

### Relevance
- **Thematic relevance**: Directly related to the topic being addressed
- **Geographic scope**: Appropriate for the project context
- **Market segment**: Specific to the relevant industry or technology

### Consistency
- **Triangulation**: Data cross-checked between multiple sources when possible
- **Internal coherence**: No contradictions between different parts of the document
- **External coherence**: Alignment with other reliable sources

## Verification Process

1. **Identification of key claims**: Mark all claims that require source backing
2. **Search for primary sources**: Locate the original source of each data point or statistic
3. **Evaluation according to criteria**: Apply verification criteria to each source
4. **Documentation**: Record verified sources in the References section
5. **Cross-review**: Verify that all key claims have their corresponding reference
6. **Metadata update**: Include verification date in document metadata

## Footnotes

For specific figures within the text, use the footnote format:

```
According to recent studies, 78% of developers report quality issues with AI-generated code[1].

[1] Stack Overflow. (2024). 2024 Stack Overflow Developer Survey.
```

## Centralized References Document

Keep the centralized references document (`docs/[type]/[name]/references.md`) updated with all sources used in the project, organized by categories.

## Next Review

Schedule the next sources review for 3-6 months after the current verification date.

---

This template follows MECE principles by organizing verification criteria into mutually exclusive and collectively exhaustive categories, covering all relevant aspects to ensure the quality and reliability of the sources used. 