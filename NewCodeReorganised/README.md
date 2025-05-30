# Math Day Score Keeper (Reorganized)

This project is a Python 3 application for managing and tracking scores for Math Day events. The codebase has been reorganized for clarity, maintainability, and best practices.

## Project Structure

```
NewCodeReorganised/
├── src/
│   ├── core/         # Core data structures and logic
│   ├── gui/          # GUI components (Tkinter windows, menus, dialogs)
│   ├── utils/        # Utility functions
│   ├── generators/   # Data and score generators
│   └── main.py       # Main application entry point
├── data/             # Data files (CSV, etc.)
├── tests/            # (Placeholder for future tests)
├── docs/             # (Placeholder for documentation)
└── README.md         # This file
```

## Getting Started

1. Ensure you have Python 3.8+ installed.
2. Install dependencies using the provided requirements.yml file (see below).
3. Run the application:

```bash
python src/main.py
```

## Dependencies
See `requirements.yml` for a list of required packages.

## Notes
- All code is now organized by function: core logic, GUI, utilities, and generators.
- Data files are separated from code.
- For any new development, add tests in the `tests/` directory. 