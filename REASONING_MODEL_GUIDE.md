# Switching to OpenAI Reasoning Models (O1)

## Quick Setup

To switch to a reasoning model like `o1-mini`, simply set the environment variable:

```bash
export OPENAI_MODEL="o1-mini"
```

Or in your `.env` file:
```
OPENAI_MODEL=o1-mini
```

## Supported Reasoning Models

- `o1-mini` - Faster, more cost-effective reasoning model
- `o1-preview` - More capable but slower reasoning model

## What Changes When Using Reasoning Models

### Automatic Adaptations
The OpenAI client now automatically handles:

1. **System Message Conversion** - System messages are merged into user messages since O1 models don't support them
2. **Parameter Removal** - Temperature and max_tokens are not sent to O1 models
3. **Message Formatting** - System instructions are prepended to user messages

### Performance Differences

- **Longer Response Times** - O1 models "think" before responding, taking 10-30+ seconds
- **Better Analysis** - More thorough document analysis and achievement extraction
- **Improved Reasoning** - Better at understanding context and making award recommendations

### Cost Considerations

O1 models are more expensive than GPT-4:
- `o1-mini`: ~3-4x more expensive than `gpt-4o-mini`
- `o1-preview`: ~10-15x more expensive than `gpt-4o-mini`

## Testing the Change

1. Set the environment variable
2. Restart the application
3. Upload a document or describe achievements
4. The model will automatically use reasoning capabilities

## Reverting to Standard Model

To switch back to the standard model:
```bash
export OPENAI_MODEL="gpt-4o-mini-2024-07-18"
```

## Note on Model Names

If you mentioned `o4-mini-2025-04-16`, this appears to be a future model. Current reasoning models are:
- `o1-mini` (recommended for this use case)
- `o1-preview` (more expensive, marginally better)