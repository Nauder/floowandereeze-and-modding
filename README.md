# Floowandereeze & Modding

<p align="center">
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
</p>

This is a pure Python tool that is able to replace card sleeves, deluxe sleeves, card arts, icons, home arts and
most fields in the Yu-Gi-Oh! Master Duel game with a user-given image, making the process of creating custom
assets trivial. It's also able to swap mates and field assets. 

- [Downloading](#Downloading)
- [Usage](#Usage)
- [Building](#Building)
    - [Prerequisites](#Prerequisites)
    - [Cloning the Repository](#Cloning-the-Repository)
    - [Setting up a Virtual Environment](#Setting-up-a-Virtual-Environment)
    - [Installing Dependencies](#Installing-Dependencies)
    - [Running the App](#Running-the-App)
    - [Creating an Executable](#Creating-an-Executable)
 
## Downloading

Download the app from the "releases" tab. Releases prior to v2.1.0 are available on 
[Nexus Mods](https://www.nexusmods.com/yugiohmasterduel/mods/372).

## Usage

Refer to the [usage](./docs/USAGE.md) guide.

## Building

The following section details the standard process to build the app manually; end user releases are available in the
"releases" tab.

### Prerequisites

Before you start, ensure that you have the following software installed on your machine:

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [GitHub account](https://github.com/)

### Cloning the Repository

1. Open your terminal.

2. Clone the GitHub repository to your local machine using the following command:
   ```bash
   git clone https://github.com/Nauder/floowandereeze-and-modding
   ```

### Setting up a Virtual Environment

1. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```

2. Create a virtual environment (recommended to isolate project dependencies):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
    - On Windows:
   ```bash
   venv\Scripts\activate
   ```
    - On Linux:
   ```bash
   source venv/bin/activate
   ```

### Installing Dependencies

1. Ensure you are in the project directory with the activated virtual environment.

2. Install project dependencies from the requirements.txt file:
    ```bash
   pip install -r requirements.txt
    ```

### Running the App

1. Start the app:
    ```bash
   python MasterApp.py
    ```

2. Follow the [usage](./docs/USAGE.md) guide to test functionalities.

### Creating an Executable

1. Run the build script (Windows only):
    ```bash
   .\build.ps1
    ```

2. Check the resulting exe in the folder informed by the build script.

## License

This project is licensed under the [GNU General Public License](LICENSE).
   
