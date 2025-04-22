# Import the necessary modules for the application
from app.core.run_app import run_xtrium  # Function to initialize and run the Xtrium application

def main():
    """
    Main entry point for the Xtrium app.

    This function is responsible for:
    1. Initializing the application's core settings and configurations using `run_xtrium`.
    2. Serving as the central point of execution when the application is launched.

    The function encapsulates the setup and initialization logic to ensure the app starts
    with all necessary components and configurations.
    """
    # Initialize and run the Xtrium application
    run_xtrium()

# Ensure that the `main` function is executed only when the script is run directly
# This safeguard prevents unintended execution if the script is imported as a module.
if __name__ == "__main__":
    main()