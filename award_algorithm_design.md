# Award Recommendation Algorithm Design

## Overview
This document outlines the design for the award recommendation algorithm that will be used in the Coast Guard Award Writing Tool. The algorithm will analyze the information gathered through the chat interface and recommend appropriate awards based on objective criteria from the Coast Guard manuals.

## Core Principles
1. **Rank Neutrality**: Award recommendations must be based solely on accomplishments and impact, not on the nominee's rank
2. **Evidence-Based**: All recommendations must be supported by specific, quantifiable evidence
3. **Manual Alignment**: Criteria must directly align with the Coast Guard Military Medals and Awards Manual and Civilian Awards Manual
4. **Transparency**: The reasoning behind each recommendation must be clear and traceable

## Data Processing Flow

### 1. Information Categorization
- Parse chat responses into structured data categories:
  - Basic information (rank, name, position, time period)
  - Quantitative achievements (metrics, statistics, scope)
  - Actions (specific behaviors, initiatives, leadership)
  - Impact (direct effects, challenges overcome)
  - Results (measurable outcomes, improvements)

### 2. Criteria Matching
- Map structured data to specific award criteria
- Assign weighted scores to each criteria match
- Identify threshold requirements for each award level

### 3. Award Scoring
- Calculate composite scores for each potential award
- Apply minimum threshold requirements
- Rank potential awards by score
- Select primary and alternative recommendations

### 4. Justification Generation
- Identify strongest evidence points for recommended award
- Map evidence to specific manual criteria
- Generate explanation text with direct references to manual

## Scoring System

### Quantitative Metrics
- **Scope of Impact**:
  - Individual/Small Team (1 point)
  - Unit/Department (2 points)
  - Coast Guard-wide (3 points)
  - Interagency/National (4 points)
  - International (5 points)

- **Duration/Sustainability**:
  - Single instance (1 point)
  - Short-term project (2 points)
  - Sustained effort (3-5 points, based on duration)

- **Resource Efficiency**:
  - Within expected resources (1 point)
  - Significant resource savings (2-3 points)
  - Exceptional efficiency (4-5 points)

### Qualitative Factors
- **Initiative Level**:
  - Expected performance (1 point)
  - Above expected (2-3 points)
  - Exceptional initiative (4-5 points)

- **Technical Complexity**:
  - Routine (1 point)
  - Moderately complex (2-3 points)
  - Highly complex (4-5 points)

- **Risk/Danger**:
  - Minimal risk (0 points)
  - Moderate risk (1-3 points)
  - Significant personal risk (4-5 points)

### Award Thresholds
Each award type will have minimum threshold requirements and scoring ranges:

- **Achievement Medal**: 10-15 points
- **Commendation Medal**: 16-25 points
- **Meritorious Service Medal**: 26-35 points
- **Legion of Merit**: 36-45 points
- **Distinguished Service Medal**: 46+ points

*Note: These are examples; actual thresholds will be calibrated based on manual criteria*

## Special Considerations

### Heroism Awards
- Separate scoring pathway for acts involving heroism
- Higher weighting for risk, danger, and lives saved
- Special threshold requirements from manual

### Unit Awards
- Aggregate impact scoring
- Team contribution assessment
- Organizational improvement metrics

### Career Achievement
- Cumulative impact assessment
- Sustained performance evaluation
- Progressive responsibility consideration

## Implementation Approach

### NLP Processing
- Extract key metrics and achievements from narrative text
- Identify action verbs and impact statements
- Recognize quantitative values and comparatives

### Rule-Based Scoring
- Apply scoring rules based on extracted data points
- Calculate composite scores across categories
- Apply threshold requirements

### Machine Learning Enhancement
- Train on sample award citations (when provided)
- Improve pattern recognition for achievement types
- Refine scoring weights based on historical awards

## Explanation Generation
The algorithm will generate explanations that:
1. Cite specific accomplishments from the input data
2. Reference relevant criteria from the awards manual
3. Explain how the accomplishments meet or exceed criteria
4. Compare to standard expectations for clarity
5. Provide justification for the award level recommendation

## Next Steps
1. Implement data extraction from chat responses
2. Develop scoring functions for each criteria category
3. Create award threshold mapping from manual
4. Build explanation generation module
5. Test with sample scenarios and refine
