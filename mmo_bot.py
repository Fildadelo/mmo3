#!/usr/bin/env python
import os
import time
import random
import json
import openai
import click
from rich.console import Console
from rich.prompt import Prompt

# Initialize a Rich console for pretty output
console = Console()

# Set your OpenAI API key from environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

# ---------------------------------------------------------------------------
# Define tool functions that simulate in-game actions for the MMO bot.
# ---------------------------------------------------------------------------
def scan_for_enemies():
    """Simulate scanning the area for enemies; returns a list of enemy positions."""
    num_enemies = random.randint(0, 3)
    enemies = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_enemies)]
    console.log(f"[bold green]Action:[/bold green] Scanned enemies: {enemies}")
    return enemies

def attack_enemy(enemy_position):
    """Simulate attacking an enemy at a given (x, y) coordinate."""
    console.log(f"[bold green]Action:[/bold green] Attacking enemy at {enemy_position}...")
    result = random.choice(["attack successful", "attack missed"])
    return result

def explore_area():
    """Simulate exploring a new area; returns a new position."""
    new_position = (random.randint(0, 100), random.randint(0, 100))
    console.log(f"[bold green]Action:[/bold green] Exploring area; moved to {new_position}")
    return new_position

# ---------------------------------------------------------------------------
# Define function calling specifications to tell the API what tools are available.
# ---------------------------------------------------------------------------
function_definitions = [
    {
        "name": "scan_for_enemies",
        "description": "Scan the current area for enemies.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "attack_enemy",
        "description": "Attack an enemy at a specified position.",
        "parameters": {
            "type": "object",
            "properties": {
                "enemy_position": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Coordinates [x, y] of the enemy to attack."
                }
            },
            "required": ["enemy_position"]
        }
    },
    {
        "name": "explore_area",
        "description": "Explore a new area to find enemies or resources.",
        "parameters": {"type": "object", "properties": {}}
    }
]

# Map function names to the actual Python functions.
function_map = {
    "scan_for_enemies": scan_for_enemies,
    "attack_enemy": attack_enemy,
    "explore_area": explore_area,
}

# ---------------------------------------------------------------------------
# The interactive bot loop.
# This function sends a conversation (with a system prompt and iterative user queries)
# to the OpenAI API and processes function call instructions.
# ---------------------------------------------------------------------------
def bot_loop(model_choice: str, reasoning_effort: str):
    console.rule(f"[bold blue]Starting MMO Bot (Model: {model_choice}, Reasoning: {reasoning_effort})")
    # Initialize the conversation with a system message instructing the model.
    conversation = [
        {
            "role": "system",
            "content": (
                "You are an AI MMO game bot controlling a character in an online game. "
                "Decide which action to perform: scan_for_enemies, attack_enemy, or explore_area. "
                "Return a function call directive when appropriate."
            )
        }
    ]
    
    # Interactive loop – type 'exit' to quit.
    while True:
        user_input = Prompt.ask("\n[bold yellow]Enter a command ('next' for next action, 'exit' to quit)[/bold yellow]")
        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold red]Exiting bot loop.[/bold red]")
            break

        # Here we always ask: "What should I do next?"
        conversation.append({"role": "user", "content": "What should I do next?"})
        
        try:
            response = openai.ChatCompletion.create(
                model=model_choice,
                messages=conversation,
                functions=function_definitions,
                function_call="auto",
                max_tokens=100,
                # Some providers let you specify additional options like reasoning_effort:
                # You might need to wrap these in provider_options if supported:
                provider_options={"reasoningEffort": reasoning_effort}
            )
        except openai.error.OpenAIError as e:
            console.print(f"[bold red]API Error:[/bold red] {e}")
            break

        message = response.choices[0].message

        # Process the response: if the model wants to call a function…
        if message.get("function_call"):
            func_call = message["function_call"]
            func_name = func_call.get("name")
            arguments_str = func_call.get("arguments", "{}")
            try:
                arguments = json.loads(arguments_str)
            except json.JSONDecodeError as e:
                console.print(f"[bold red]Failed to parse arguments:[/bold red] {e}")
                arguments = {}
            console.print(f"[bold cyan]Model requested function:[/bold cyan] {func_name} with arguments {arguments}")

            if func_name in function_map:
                # Execute the tool function.
                result = function_map[func_name](**arguments)
                # Append the function call result to the conversation.
                conversation.append({
                    "role": "function",
                    "name": func_name,
                    "content": json.dumps(result)
                })
            else:
                console.print(f"[bold red]Warning:[/bold red] Unknown function '{func_name}'.")
        else:
            # Otherwise, simply print the model's text output.
            content = message.get("content", "")
            console.print(f"[bold magenta]Model says:[/bold magenta] {content}")
            # Optionally, append the text message to the conversation.
            conversation.append({"role": "assistant", "content": content})

        # Pause a bit before the next round.
        time.sleep(1)

# ---------------------------------------------------------------------------
# CLI using Click.
# ---------------------------------------------------------------------------
@click.command()
@click.option("--model", default="o3-mini", help="Model to use (e.g. o3-mini, gpt-4).")
@click.option("--reasoning", default="medium", type=click.Choice(["low", "medium", "high"], case_sensitive=False), help="Reasoning effort level.")
def main(model, reasoning):
    """
    This script uses the OpenAI API (with function calling) to run an MMO game bot.
    It continuously queries the model for the next action and executes tool functions accordingly.
    Use 'exit' at the prompt to quit.
    """
    console.print(f"[bold green]Using model:[/bold green] {model} with reasoning effort set to [bold green]{reasoning}[/bold green].")
    try:
        bot_loop(model_choice=model, reasoning_effort=reasoning)
    except KeyboardInterrupt:
        console.print("\n[bold red]Bot loop terminated by user.[/bold red]")

if __name__ == "__main__":
    main()
