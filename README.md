# Multi-Agent Icon Generator

A demonstration of pydantic-ai's **agent delegation pattern** for creating custom 128x128 icons.

## Architecture

This application uses two agents in a delegation pattern:

### Icon Creator Agent (Parent)
- **Role**: Orchestrator of the icon generation process
- **Responsibility**: Delegates to Style Expert, then generates the final icon
- **Model**: GPT-4o

### Style Expert Agent (Delegate)
- **Role**: Specialist in art styles and visual design
- **Responsibility**: Refines user descriptions into detailed, style-specific prompts
- **Model**: GPT-4o

### Image Generation (Tool)
- **Role**: Image generation engine
- **Responsibility**: Generates the actual icon image based on the refined prompt
- **Model**: DALL-E-3

## Usage

```bash
python icon_generator.py --style "minimalist" --description "a dancing baby shark" --count 3
```

## Example Styles

- **minimalist**: Clean, simple designs with essential elements
- **pixel art**: Retro, 8-bit inspired graphics
- **watercolor**: Soft, flowing artistic style
- **flat**: Modern, 2D with solid colors
- **isometric**: 3D perspective with geometric precision
- **line art**: Simple outlines and contours
- **gradient**: Smooth color transitions
- **woodcut**: Textured, engraved appearance
- **cartoon**: Exaggerated, playful designs
- **sketch**: Hand-drawn, rough style
- **vector**: Scalable graphics with clean lines
- **surrealist**: Dream-like, abstract imagery
- **cyberpunk**: Futuristic, neon-lit aesthetics
- **steampunk**: Victorian-era mechanical designs
- **gothic**: Dark, ornate style with intricate details
- **pop art**: Bold, vibrant colors with a comic book feel
- **art deco**: Geometric shapes with luxurious details
- **impressionist**: Light and color-focused, with visible brush strokes
- **cubist**: Abstract, fragmented forms and perspectives
- **expressionist**: Emotional, distorted representations with vivid colors
- **realistic**: Life-like, detailed imagery
- **fantasy**: Magical, otherworldly themes and elements
- **sci-fi**: Futuristic, space-themed designs
- **vintage**: Nostalgic, old-fashioned aesthetics
- **modern**: Sleek, contemporary designs with clean lines


## Dependencies

This project is managed with `uv`. To install dependencies, run:

```bash
uv sync
. .venv/bin/activate
```

## How It Works

1. **User Input**: Provides art style + description
2. **Delegation**: Icon Creator delegates to Style Expert
3. **Refinement**: Style Expert creates optimized prompt with style-specific details
4. **Generation**: Icon Creator uses refined prompt to generate concept
5. **Output**: Returns icon details and outputs actual image to `output/icon.png`

