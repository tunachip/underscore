# Move Maker

This script is a command-line tool for creating combat moves for a role-playing game. It allows you to define the properties of a move, such as its name, element, type, and effects, and then save it as a JSON file.

## How to Use

To use the move maker, simply run the `movemaker.py` script from your terminal:

```bash
python movemaker.py
```

The script will guide you through the process of creating a new move. You will be prompted to enter the following information:

*   **Move Name:** The name of the move.
*   **Element:** The elemental affinity of the move (e.g., water, fire, stone).
*   **Type:** The type of move (e.g., attack, utility).
*   **Target:** The target of the move (e.g., caster, opponent, declared).
*   **Base Damage:** The base damage of the move.
*   **Base Iterations:** The number of times the move will be executed.
*   **Effects:** The special effects of the move.

### Effects

Effects are special actions that occur when a move is used. They are defined by a host, a function, arguments, and return values.

*   **Host:** The object that the effect is applied to (e.g., `character`, `combat`).
*   **Function:** The action that the effect performs (e.g., `calculate_damage`, `gain_status`).
*   **Arguments:** The parameters that are passed to the function.
*   **Return Values:** The values that are returned by the function.

Effects can be added to one of three execution phases:

*   **pre-iter:** Executed before the main iterations of the move.
*   **iterable:** Executed during each iteration of the move.
*   **post-iter:** Executed after the main iterations of the move.

## Move Data Structure

The move data is stored in a JSON file with the following structure:

```json
{
    "name": "",
    "element": "",
    "type": "",
    "target": "",
    "description": "",
    "base_damage": 0,
    "base_iters": 1,
    "effects": {
        "pre-iter": [],
        "iterable": [],
        "post-iter": []
    }
}
```

## Files

*   `movemaker.py`: The main script for the move maker.
*   `move_template.json`: A template for the move data structure.
*   `moves/`: A directory where the move JSON files are saved.
