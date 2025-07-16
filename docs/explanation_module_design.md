# Award Explanation Module Design

## Overview
This document outlines the design for the explanation module that will accompany award recommendations in the Coast Guard Award Writing Tool. The module will generate clear, detailed explanations for why a particular award was recommended based on the information provided and the objective criteria from the Coast Guard manuals.

## Purpose
The explanation module serves to:
1. Provide transparency in the award recommendation process
2. Educate users on the objective criteria for different award levels
3. Demonstrate how the nominee's accomplishments align with specific award criteria
4. Reduce subjectivity and rank-based bias in award decisions
5. Generate well-structured justification text that can be used in award submissions

## Explanation Components

### 1. Award Selection Rationale
- Summary of why the specific award was selected
- Comparison to alternative award levels (higher and lower)
- Key differentiating factors that determined the recommendation

### 2. Criteria Alignment
- Explicit mapping of accomplishments to manual criteria
- Citation of specific manual sections and requirements
- Explanation of how thresholds were met or exceeded

### 3. Evidence Summary
- Recap of the strongest quantitative evidence
- Highlight of most impactful actions and results
- Contextual information about challenges or circumstances

### 4. Rank Neutrality Assurance
- Explanation of how the recommendation would apply regardless of rank
- Comparison to standard expectations for the position
- Focus on accomplishment rather than position or authority

## Output Format

### Explanation Structure
1. **Introduction**: Brief overview of the recommendation and basis
2. **Evidence Analysis**: Detailed breakdown of key evidence points
3. **Criteria Mapping**: Explicit connection to manual requirements
4. **Comparative Assessment**: Why this award level vs. others
5. **Conclusion**: Summary reinforcement of the recommendation

### Presentation Elements
- Bullet points for key evidence
- Direct quotes from the manual where applicable
- Visual indicators (e.g., checkmarks) for met criteria
- Confidence level indicator for the recommendation

## Implementation Approach

### Template-Based Generation
- Create base templates for each award type
- Populate with specific evidence and criteria references
- Customize based on strength of evidence and unique factors

### Natural Language Generation
- Convert structured data into natural, flowing text
- Vary sentence structure for readability
- Maintain formal, professional tone appropriate for military context

### Contextual Adaptation
- Adjust explanation depth based on evidence strength
- Provide more detailed justification for edge cases
- Address potential questions or concerns proactively

## Integration with Award Algorithm

### Data Flow
1. Award algorithm provides recommendation with scoring details
2. Explanation module receives structured data and scores
3. Module selects appropriate template and generation approach
4. Customized explanation is generated and returned to interface

### Feedback Loop
- User feedback on explanations can improve future generations
- Track which explanations lead to accepted awards
- Refine templates and language based on effectiveness

## Example Explanation Output

```
AWARD RECOMMENDATION: Coast Guard Commendation Medal

RATIONALE:
Based on the quantitative achievements and impact described, a Coast Guard Commendation Medal is recommended. The nominee's actions exceed the threshold for an Achievement Medal but do not meet all criteria for a Meritorious Service Medal.

EVIDENCE ANALYSIS:
• Led emergency response operation saving 12 lives during Hurricane [Name]
• Developed new maintenance procedure reducing downtime by 35%
• Coordinated interagency effort involving 5 federal partners
• Initiative resulted in $250,000 cost savings over 6-month period

CRITERIA ALIGNMENT:
The Coast Guard Medals and Awards Manual (COMDTINST M1650.25E) states that the Commendation Medal is appropriate when an individual:
✓ "Demonstrates exceptional professional ability" (evidenced by new procedure development)
✓ "Achieves significant operational impact" (evidenced by lives saved)
✓ "Shows superior initiative beyond normal expectations" (evidenced by interagency coordination)

COMPARATIVE ASSESSMENT:
While the Achievement Medal recognizes notable accomplishments, the scope and impact of these actions exceed that level. The interagency coordination and significant cost savings demonstrate performance well above standard expectations.

The actions do not fully meet Meritorious Service Medal criteria, which requires broader organizational impact or sustained performance over a longer period.

CONCLUSION:
The Coast Guard Commendation Medal appropriately recognizes these significant accomplishments based on objective criteria from the manual, independent of the nominee's rank or position.
```

## Next Steps
1. Develop template library for each award type
2. Implement natural language generation functions
3. Create criteria reference database from manuals
4. Build integration with award algorithm
5. Test with sample scenarios and refine language
