# 3D Snake Game

A 3D implementation of the classic Snake game, built with Python and the Ursina engine.

## Prerequisites

*   Python 3 (tested with Python 3.7+)
*   pip (Python package installer)

## Installation

1.  **Clone the repository (or download the source code):**
    ```bash
    # Replace <repository_url> and <repository_directory> with actual values if known
    # For now, this is a general instruction.
    git clone <repository_url>
    cd <repository_directory>
    ```
    (If you downloaded the code as a zip file, extract it and open your terminal/command prompt in the extracted directory.)

2.  **Set up a virtual environment (recommended):**
    Open your terminal or command prompt in the project's root directory.
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    With your virtual environment active, install Ursina:
    ```bash
    pip install ursina
    ```

## Running the Game

Once the prerequisites are met and dependencies are installed (and your virtual environment is active, if you used one):

1.  Navigate to the project's root directory in your terminal.
2.  Run the game using the following command:
    ```bash
    python src/snake_game_3d.py
    ```

## Controls

*   **Arrow Keys (Up, Down, Left, Right):** Control snake movement in the X (left/right) and Y (up/down) plane relative to the current view.
*   **W Key:** Move the snake "forward" along its current Z-axis.
*   **S Key:** Move the snake "backward" along its current Z-axis.
*   **Enter Key:** Start the game from the main menu.
*   **R Key:** Restart the game if you are on the "Game Over" screen.

Enjoy the game!
