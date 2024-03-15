# Hardware_Store

Hardware Store Project: A management system for hardware store.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.11.1
- pip

### Setting Up a Virtual Environment

To isolate the project dependencies, create and activate a virtual environment within the project directory. Use the following commands:

1. Create a virtual environment
```bash
python -m venv venv
```

2. Activate the virtual environment 

(Windows)
```bash
venv\Scripts\activate
```

(Unix/Linux/macOS)
```bash
source venv/bin/activate
```

### Installing Dependencies

Once your virtual environment is active, you can install the required dependencies.

Run the following command:

```bash
pip install flask cx_Oracle
```

This will install Flask and the Oracle database driver (cx_Oracle) within your virtual environment.

### Setting Up a New Python Environment from requirements.txt

To quickly establish a Python environment for the project with all the necessary dependencies, follow these steps:

1. **Create a Virtual Environment (optional but recommended)**

   It's a best practice to create a virtual environment to isolate your project's dependencies. You can use the `venv` module or a tool like `virtualenv`. After creating the virtual environment, activate it by following the commands outlined in the "Setting Up a Virtual Environment" section.

2. **Install Dependencies from requirements.txt**

   Run the following command to install the required packages and their specified versions from the "requirements.txt" file. Ensure that you are in the project directory and, if you created a virtual environment, it should be activated.

```bash
pip install -r requirements.txt
```

3. **You're all set!**

   Your Python environment is now configured with the necessary packages to run this project.

### Configuration

Before running the application, make sure to add a `config.py` file. This file may contain configuration settings specific to your project, such as database credentials, API keys, or other environment-specific variables.

## Running the Application

To run the application, use the following command:

```bash
python setup.py
```

This will start the application, and you should be able to access it in your web browser.

## Author

- David Gómez Venegas
- Franciny Aguero Siles
- Daniel Espinoza Castro
- Luis Diego Coto Jiménez

## License

This project is licensed under the MIT License. See the LICENSE.md file for details.