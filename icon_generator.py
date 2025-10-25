"""
Multi-agent icon generator using agent delegation pattern.

This application demonstrates pydantic-ai's agent delegation pattern by creating
custom 128x128 icons. The parent agent (Icon Creator) delegates to a specialist
agent (Style Expert) to refine prompts before generating the final icon.
"""

import asyncio
import re
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import httpx
from openai import AsyncOpenAI
from PIL import Image
from pydantic_ai import Agent, RunContext


@dataclass
class IconRequest:
    """Dependencies shared between agents."""

    art_style: str
    description: str
    openai_client: AsyncOpenAI


# Delegate Agent: Style Expert
# Specializes in different art styles and creates optimized prompts
style_expert = Agent(
    "openai:gpt-4o",
    system_prompt=(
        """
You are an expert in visual art styles and icon design.
When given an art style and description, you create detailed, optimized prompts for generating high-quality icons.
Focus on: composition, color palettes, visual elements, and style-specific techniques.
Keep prompts concise but detailed, suitable for 128x128 icon generation.
    """
    ),
    deps_type=IconRequest,
)


@style_expert.tool
async def refine_prompt(ctx: RunContext[IconRequest]) -> str:
    """
    Refine the icon description based on the specified art style.

    Returns a detailed prompt optimized for icon generation.
    """
    style = ctx.deps.art_style
    description = ctx.deps.description

    # Style Expert creates an optimized prompt
    prompt = f"""
Create a detailed prompt for a 128x128 pixel icon in {style} art style.
The icon should depict: {description}.
Include specific details about composition, colors, and visual elements
that best represent this style.
"""
    return prompt


# Parent Agent: Icon Creator
# Orchestrates the icon generation process using delegation
icon_creator = Agent(
    "openai:gpt-4o",
    system_prompt=(
        "You are an icon creator that generates custom 128x128 icons. "
        "Your workflow is: "
        "1. First, call consult_style_expert to get a refined prompt. "
        "2. Then, IMMEDIATELY call generate_icon_image with the refined prompt to create the actual icon file. "
        "You must ALWAYS generate the actual image - never just describe it."
    ),
    deps_type=IconRequest,
)


@icon_creator.tool
async def consult_style_expert(ctx: RunContext[IconRequest], prompt: str) -> str:
    """
    Delegate to the Style Expert agent to refine the icon prompt.

    This demonstrates the agent delegation pattern where the parent agent
    calls a specialized delegate agent through a tool.
    """
    # Delegate to style expert, passing usage context and dependencies
    result = await style_expert.run(
        f"Please refine this icon prompt: {prompt}",
        deps=ctx.deps,
        usage=ctx.usage,
    )

    print(f"[DEBUG]{result.output}")

    return f"Style expert's refined prompt: {result.output}"


@icon_creator.tool
async def generate_icon_image(ctx: RunContext[IconRequest], refined_prompt: str) -> str:
    """
    Generate the actual icon image using OpenAI's DALL-E API.

    Downloads the generated image, resizes it to 128x128, and saves it to disk.
    """
    client = ctx.deps.openai_client
    art_style = ctx.deps.art_style
    description = ctx.deps.description

    # Extract the actual prompt from the refined_prompt string if it contains extra text
    # The refined_prompt might have "Style expert's refined prompt: " prefix
    actual_prompt = refined_prompt
    if "Style expert's refined prompt:" in refined_prompt:
        actual_prompt = refined_prompt.split("Style expert's refined prompt:")[
            -1
        ].strip()

    print(f"  Generating image with DALL-E...")
    response = await client.images.generate(
        model="dall-e-3",
        prompt=actual_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    # Download the image
    print(f"  Downloading image...")
    async with httpx.AsyncClient() as http_client:
        img_response = await http_client.get(image_url)
        img_response.raise_for_status()
        image_data = img_response.content

    # Resize to 128x128
    print(f"  Resizing to 128x128...")
    image = Image.open(BytesIO(image_data))
    image = image.resize((128, 128), Image.Resampling.LANCZOS)

    # Create a safe filename
    safe_style = re.sub(r"[^\w\s-]", "", art_style).strip().replace(" ", "_")
    safe_desc = re.sub(r"[^\w\s-]", "", description)[:30].strip().replace(" ", "_")
    filename = f"icon_{safe_style}_{safe_desc}.png"
    filepath = Path.cwd() / filename

    # Save the image
    image.save(filepath, "PNG")
    print(f"  ✓ Saved to {filepath}")

    return f"Icon generated and saved to: {filename}"


async def create_icon(
    art_style: str, description: str, openai_client: AsyncOpenAI
) -> str:
    """
    Create a custom icon using agent delegation.

    Args:
        art_style: The artistic style for the icon (e.g., "minimalist", "pixel art", "watercolor")
        description: Single sentence describing what the icon should depict
        openai_client: AsyncOpenAI client instance

    Returns:
        Result message with icon details
    """
    deps = IconRequest(
        art_style=art_style, description=description, openai_client=openai_client
    )

    result = await icon_creator.run(
        f"Create a {art_style} style icon: {description}",
        deps=deps,
    )

    return result.output


async def main():
    """Example usage of the icon generator."""
    print("🎨 Multi-Agent Icon Generator (using Agent Delegation)\n")

    # Initialize OpenAI client
    client = AsyncOpenAI()

    print("=" * 60)
    print("1. Minimalist coffee cup")
    print("=" * 60)
    result1 = await create_icon(
        art_style="minimalist", description="a hot cup of coffee", openai_client=client
    )
    print(f"{result1}\n")

    print("=" * 60)
    print("2. Pixel art rocket")
    print("=" * 60)
    result2 = await create_icon(
        art_style="pixel art",
        description="a retro rocket ship launching into space",
        openai_client=client,
    )
    print(f"{result2}\n")

    print("=" * 60)
    print("3. Watercolor flower")
    print("=" * 60)
    result3 = await create_icon(
        art_style="watercolor",
        description="a blooming sunflower with a bee",
        openai_client=client,
    )
    print(f"{result3}\n")


if __name__ == "__main__":
    asyncio.run(main())
