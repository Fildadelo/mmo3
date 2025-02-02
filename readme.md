hi,

# MMO Bot with OpenAI o3-mini API

This is an interactive MMO bot script that uses the OpenAI API (with the o3-mini model) to decide in‑game actions via function calling. It simulates a game bot that can scan for enemies, attack a target, or explore a new area. A beautiful command‑line interface (CLI) is provided using [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/).

## Features

- **Advanced Reasoning:** Uses OpenAI’s o3-mini model optimized for STEM, coding, and logical tasks.
- **Function Calling:** The bot calls pre‑defined functions (tools) such as scanning for enemies, attacking, and exploring.
- **Interactive CLI:** Provides a user-friendly interface for interacting with the bot.
- **Customizable Reasoning Effort:** Adjust the reasoning effort (low, medium, high) via CLI options.

## Requirements

- Python 3.8 or later
- [openai](https://pypi.org/project/openai/) (Install with `pip install openai`)
- [Click](https://pypi.org/project/click/) (Install with `pip install click`)
- [Rich](https://pypi.org/project/rich/) (Install with `pip install rich`)

## Setup

1. **Clone or Download the Repository**

   Clone this repository or download the `mmo_bot.py` script to your local machine.

2. **Set Your OpenAI API Key**

   Make sure you have an API key from OpenAI. Set it as an environment variable. For example, in your terminal (on Unix-like systems):

   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

   On Windows, you can set the environment variable using:

   ```cmd
   set OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Install Dependencies**

   Install the required Python packages using pip:

   ```bash
   pip install openai click rich
   ```

## Usage

The script provides a command-line interface with options to select the model and adjust the reasoning effort level.

### Running the Script

Run the script using Python from the terminal:

```bash
python mmo_bot.py
```

By default, the script uses the `o3-mini` model with a "medium" reasoning effort.

### Command-Line Options

- `--model`: Specify the model to use (e.g., `o3-mini` or `gpt-4`).
- `--reasoning`: Choose the reasoning effort level. Valid choices are `low`, `medium`, or `high`.

#### Examples:

- **Run with the default o3-mini model (medium reasoning):**

  ```bash
  python mmo_bot.py
  ```

- **Run with high reasoning effort:**

  ```bash
  python mmo_bot.py --reasoning high
  ```

- **Run with a different model (if available):**

  ```bash
  python mmo_bot.py --model gpt-4 --reasoning medium
  ```

## How It Works

1. **Tool Functions:**  
   The script defines three in‑game actions:
   - `scan_for_enemies()`: Simulates scanning for enemy positions.
   - `attack_enemy(enemy_position)`: Simulates attacking an enemy at a given position.
   - `explore_area()`: Simulates exploring a new area.

2. **Function Calling:**  
   The script sets up function calling definitions and maps them to the corresponding Python functions. The OpenAI API is then used to ask the question, "What should I do next?" If the model returns a function call directive, the script parses the arguments, executes the corresponding function, and appends the result back into the conversation.

3. **Interactive CLI:**  
   The CLI built with Click and Rich prompts the user for input. Type `next` (or any text) to request the next action from the model, or type `exit` to quit the bot loop.

## Troubleshooting

- **API Errors:**  
  If you encounter API errors, ensure that your `OPENAI_API_KEY` is set correctly and that you have the appropriate access tier for the o3-mini model.

- **Installation Issues:**  
  Verify that all required packages are installed and that you are using Python 3.8 or later.

## License

This project is provided for educational purposes. Please refer to the LICENSE file for more details.

## References

- [OpenAI o3-mini Official Announcement](https://openai.com/index/openai-o3-mini/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
