# Coast Guard Award Writing Tool - Chat Interface Design

## Overview
This document outlines the design for the chat interface of the Coast Guard Award Writing Tool. The interface will use a conversational AI approach to gather comprehensive information about a service member's accomplishments, then use this data to recommend appropriate awards based on objective criteria from the Coast Guard Military Medals and Awards Manual (COMDTINST M1650.25E) and the Coast Guard Civilian Awards Manual (COMDTINST M12451.1C).

## GUI Layout

### Main Window
- **Title Bar**: "Coast Guard Award Writing Assistant"
- **Left Panel**: Navigation and status
  - Home/Dashboard
  - New Award Recommendation
  - Saved Recommendations
  - Settings
  - Help/Documentation
- **Center Panel**: Chat interface and award display
  - Chat message area (scrollable)
  - Text input area (with text wrapping)
  - Send button
- **Right Panel**: Award information and criteria reference
  - Currently selected award details
  - Criteria checklist
  - Export/Save options

### Chat Interface Components
1. **Message Bubbles**:
   - AI messages (left-aligned, distinct color)
   - User messages (right-aligned, distinct color)
   - System notifications (centered, neutral color)

2. **Input Area**:
   - Multi-line text box with wrapping
   - Character counter
   - Attachment option for supporting documents
   - Send button

3. **Award Display Area**:
   - Award recommendation card
   - Justification text
   - Edit/Refine button
   - Export options (PDF, Word, plain text)

## Conversation Flow

### Initial Setup Phase
1. Welcome message and purpose explanation
2. Request basic information:
   - Is the nominee military or civilian?
   - Nominee's rank/grade
   - Nominee's name
   - Nominee's unit/position
   - Time period covered by the award

### Data Collection Phase
The chat will systematically gather information in these key areas:

1. **Quantitative Achievements**:
   - "What specific metrics or numbers demonstrate the nominee's performance?"
   - "How does this compare to standard expectations for their position?"
   - "What was the scope of impact? (individual, unit, Coast Guard-wide, interagency)"

2. **Actions Taken**:
   - "What specific actions did the nominee take?"
   - "What initiative did they demonstrate?"
   - "What leadership qualities were exhibited?"
   - "What technical skills were utilized?"

3. **Impact Assessment**:
   - "What was the direct impact of these actions?"
   - "Were there any unusual circumstances or challenges?"
   - "How did these actions benefit the Coast Guard or its mission?"

4. **Results Documentation**:
   - "What were the measurable outcomes of these actions?"
   - "How did these results exceed normal expectations?"
   - "Were there any long-term benefits or improvements?"

### Clarification and Refinement
- The AI will ask follow-up questions based on responses
- Prompts for additional details when answers lack specificity
- Suggestions for quantifying qualitative statements
- Requests for clarification on technical terms or acronyms

### Award Recommendation Phase
- Presentation of recommended award(s)
- Detailed explanation of why the award was selected
- Comparison to award criteria from the manual
- Option to refine or adjust the recommendation

## OpenAI API Integration

### API Configuration
- Model: GPT-4 or equivalent
- Temperature: 0.7 (balanced between creativity and accuracy)
- Max tokens: Sufficient for detailed responses
- System prompt: Includes award criteria and evaluation guidelines

### Conversation Management
- Maintain conversation history for context
- Track collected data points
- Identify missing information
- Guide user through structured data collection

### Award Recommendation Logic
- Map collected data to award criteria
- Weight factors based on manual guidelines
- Consider rank-appropriate expectations
- Generate objective justification

## User Experience Considerations

### Accessibility
- High contrast text options
- Keyboard navigation support
- Screen reader compatibility

### Usability
- Clear progress indicators
- Save/resume functionality
- Undo/edit previous responses
- Help tooltips for unfamiliar terms

### Privacy and Security
- Local data storage option
- No PII transmission without consent
- Session timeout and data clearing

## Implementation Notes
- Use Python with a modern GUI framework (PyQt, Tkinter with custom styling)
- Implement responsive design for various screen sizes
- Ensure text wrapping in all input and display areas
- Design for both keyboard and mouse interaction
- Include loading indicators for API calls

## Next Steps
1. Create wireframe mockups of the interface
2. Develop conversation flow diagrams
3. Draft system prompts for the OpenAI API
4. Implement prototype of the chat interface
5. Test with sample award scenarios
