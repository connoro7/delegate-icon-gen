# Multi-Agent Icon Generator

A demonstration of pydantic-ai's **agent delegation pattern** for creating custom 128x128 icons.

## Architecture

This application uses two agents in a delegation pattern:

### <¨ Style Expert Agent (Delegate)
- **Role**: Specialist in art styles and visual design
- **Responsibility**: Refines user descriptions into detailed, style-specific prompts
- **Model**: GPT-4o

### =¼ Icon Creator Agent (Parent)
- **Role**: Orchestrator of the icon generation process
- **Responsibility**: Delegates to Style Expert, then generates the final icon
- **Model**: GPT-4o

## Agent Delegation Pattern

The implementation follows pydantic-ai's delegation pattern:

```python
# Parent agent delegates through a tool
@icon_creator.tool
async def consult_style_expert(ctx: RunContext[IconRequest]) -> str:
    result = await style_expert.run(
        'Please refine this icon prompt.',
        deps=ctx.deps,      # Share dependencies
        usage=ctx.usage,    # Track combined usage
    )
    return result.data
```

**Key features:**
- Usage tracking across both agents (`usage=ctx.usage`)
- Shared dependencies (`deps=ctx.deps`)
- Parent maintains control and resumes after delegation
- Tools as delegation mechanism

## Usage

```bash
python icon_generator.py
```

### Programmatic Usage

```python
from icon_generator import create_icon

# Create a minimalist icon
result = await create_icon(
    art_style="minimalist",
    description="a steaming cup of coffee on a saucer"
)
print(result)
```

## Example Styles

- **minimalist**: Clean, simple designs with essential elements
- **pixel art**: Retro, 8-bit inspired graphics
- **watercolor**: Soft, flowing artistic style
- **flat design**: Modern, 2D with solid colors
- **isometric**: 3D perspective with geometric precision
- **line art**: Simple outlines and contours
- **gradient**: Smooth color transitions

## Extending to Real Image Generation

To generate actual images, integrate an image generation API:

```python
@icon_creator.tool
async def generate_icon_concept(ctx: RunContext[IconRequest], refined_prompt: str) -> str:
    # Option 1: OpenAI DALL-E
    from openai import AsyncOpenAI
    client = AsyncOpenAI()

    response = await client.images.generate(
        model="dall-e-3",
        prompt=refined_prompt,
        size="1024x1024",  # Then resize to 128x128
        quality="standard",
    )

    # Save and resize image
    image_url = response.data[0].url
    # Download, resize to 128x128, save...

    return f"Icon saved to: icon.png"
```

## Dependencies

```bash
pip install pydantic-ai
```

For actual image generation, add:
```bash
pip install openai pillow  # For DALL-E + image processing
# OR
pip install replicate pillow  # For Stable Diffusion
```

## How It Works

1. **User Input**: Provides art style + description
2. **Delegation**: Icon Creator delegates to Style Expert
3. **Refinement**: Style Expert creates optimized prompt with style-specific details
4. **Generation**: Icon Creator uses refined prompt to generate concept
5. **Output**: Returns icon details (or actual image in production)

## Benefits of This Pattern

- **Separation of Concerns**: Each agent has a specific expertise
- **Reusability**: Style Expert can be used by other agents
- **Resource Tracking**: Combined usage tracking across all agents
- **Maintainability**: Easy to add new specialist agents
- **Flexibility**: Can mix different models for different tasks
