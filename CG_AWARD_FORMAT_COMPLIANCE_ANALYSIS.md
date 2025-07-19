# Coast Guard Award Formatting Compliance Analysis

## Executive Summary

The current Award Generator uses a **report card style** presentation that **does NOT comply** with official Coast Guard award formatting requirements. The application generates analytical reports with scored criteria rather than properly formatted award citations.

### Compliance Status: ❌ **NON-COMPLIANT**

---

## Critical Formatting Violations

### 1. Citation Format Structure ❌

**Official Requirement:**
- Opening sentence with standard phrase, duty assignment, dates
- Statement of heroic acts/accomplishments (recipient in CAPS)
- Standard closing sentence specific to award level

**Current Implementation:**
- Generates free-form narrative without required structure
- No standardized opening/closing phrases
- Recipient name not in CAPS format
- Missing duty assignment in proper format

### 2. Document Layout ❌

**Official Requirement:**
- **Orientation**: Landscape (personal awards)
- **Paper**: Award stationery
- **Margins**: 1" sides, 1" top, 2" bottom
- **Font**: Times New Roman, 11pt, Bold
- **Line Limits**: 12-16 lines (varies by award)

**Current Implementation:**
- Portrait orientation
- Standard paper
- Default margins
- Variable fonts
- No line limit enforcement

### 3. "Report Card" Style Issues ❌

The application currently generates:

```
IV. ACHIEVEMENT SUMMARY
A. Key Achievements
   1. Led search and rescue operation
   2. Managed team of 15 personnel
   
B. Measurable Impact
   • Saved 3 lives
   • Zero safety incidents
   
C. Leadership Demonstrated
   • Team management
   • Training delivery

V. SCORING ANALYSIS
Overall Score: 53.6/100
- Leadership: 3.5/5.0
- Impact: 4.0/5.0
- Innovation: 2.1/5.0
```

**This violates CG requirements** which mandate a single, flowing narrative citation without sections, scores, or bullet points.

### 4. Missing Required Elements ❌

**Not Implemented:**
- Award stationery formatting
- 2-inch seal placement (lower left)
- Proper spacing (double space default, single for exceptions)
- Operational/Valor device formatting
- Line count validation
- Standard opening/closing phrases

---

## Required Citation Format Example

### Official Format (Meritorious Service Medal):
```
FOR SERVICE AS SET FORTH IN THE FOLLOWING CITATION:

PETTY OFFICER FIRST CLASS JOHN A. SMITH, UNITED STATES COAST GUARD,
while serving as Boatswain's Mate, Coast Guard Station Miami, Florida,
from 1 January 2025 to 30 June 2025, distinguished himself by exceptionally
meritorious service. PETTY OFFICER SMITH demonstrated exceptional leadership
during Hurricane response operations, personally leading the rescue of three
civilians from life-threatening conditions. His innovative maintenance tracking
system reduced equipment downtime by 40 percent, significantly enhancing
operational readiness. Additionally, PETTY OFFICER SMITH trained 25 new
recruits in advanced navigation techniques, directly contributing to unit
mission success. Petty Officer Smith's devotion to duty is most heartily
commended and is in keeping with the highest traditions of the United States
Coast Guard.
```

### Current Generator Output:
```
COAST GUARD ACHIEVEMENT MEDAL

Citation:
Based on the achievements provided, Petty Officer First Class John Smith 
demonstrated exceptional service through multiple accomplishments including
search and rescue operations, team leadership, and process improvements...

Achievement Summary:
- Led search and rescue operation
- Managed 15 personnel
- Implemented tracking system
- Trained 25 recruits

Scoring Breakdown:
Leadership: 3.5/5
Impact: 4.0/5
Innovation: 2.1/5
Overall: 53.6/100
```

---

## Specific Formatting Requirements by Award Level

### Meritorious Service Medal and Below:
- **Max Lines**: 12 (14 with operational device)
- **Devices Allowed**: Operational "O", Valor "V"
- **Spacing**: Double (with exceptions)
- **Acronyms**: Not authorized

### Above Meritorious Service Medal:
- **Max Lines**: 16 (18 with valor device)
- **Devices Allowed**: Valor "V" only
- **No operational device** for these awards

---

## Required Changes for Compliance

### 1. Complete Citation Reformat
- Remove all section headers
- Eliminate scoring/grading elements
- Implement single narrative flow
- Add standard opening/closing phrases

### 2. Implement Format Validation
```python
def validate_citation_format(citation_text, award_level):
    """Validate citation meets CG formatting requirements"""
    lines = citation_text.split('\n')
    
    # Check line limits
    if award_level in ['MSM', 'below']:
        max_lines = 14 if has_device else 12
    else:
        max_lines = 18 if has_valor else 16
    
    # Validate opening phrase
    required_openings = {
        'Achievement Medal': 'while serving as',
        'Commendation Medal': 'distinguished himself/herself by',
        'MSM': 'distinguished himself/herself by exceptionally meritorious'
    }
    
    # Check recipient name in CAPS
    # Validate closing phrase
    # Count lines and characters
```

### 3. Document Generation Updates
```python
def generate_award_document(citation_data):
    """Generate properly formatted award document"""
    doc = Document()
    
    # Set landscape orientation
    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11)
    section.page_height = Inches(8.5)
    
    # Set margins
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(2)
    
    # Add citation in Times New Roman 11pt Bold
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    style.font.bold = True
    
    # Add formatted citation text
    doc.add_paragraph(citation_text)
```

### 4. Update OpenAI Prompts
Include specific formatting requirements in the prompt:
```python
prompt = f"""
Generate a Coast Guard {award} citation following EXACT formatting requirements:

1. Opening: "FOR SERVICE AS SET FORTH IN THE FOLLOWING CITATION:"
2. Start with: "{rank} {NAME IN CAPS}, UNITED STATES COAST GUARD,"
3. Continue: "while serving as {position}, {unit}, from {start_date} to {end_date},"
4. Body: One flowing paragraph describing accomplishments
5. Use recipient's name in CAPS when referencing specific actions
6. Close with: "{closing_phrase}"
7. MUST be exactly {max_lines} lines or less
8. NO bullet points, sections, or scores

Standard closings:
- Achievement Medal: "Petty Officer/Seaman {Last Name}'s initiative, perseverance, and devotion to duty are most heartily commended and are in keeping with the highest traditions of the United States Coast Guard."
- Commendation Medal: "Commander/Lieutenant/Petty Officer {Last Name}'s achievement/performance reflects great credit upon himself/herself and is in keeping with the highest traditions of the United States Coast Guard."
"""
```

### 5. Remove Report Card Elements
- Eliminate all scoring displays
- Remove achievement summaries with bullets
- Remove section headers
- Focus on single citation narrative

---

## Implementation Priority

1. **CRITICAL**: Remove scoring/grading from citation output
2. **HIGH**: Implement proper citation narrative format
3. **HIGH**: Add standard opening/closing phrases
4. **MEDIUM**: Implement line count validation
5. **MEDIUM**: Add landscape orientation for documents
6. **LOW**: Add seal placement formatting

---

## Conclusion

The current Award Generator fundamentally misunderstands Coast Guard award formatting by treating citations as analytical reports rather than formal military citations. A complete redesign of the citation generation process is required to meet official standards.

The "report card" approach with scores and bullet points must be entirely removed in favor of properly formatted narrative citations that follow strict military formatting guidelines.