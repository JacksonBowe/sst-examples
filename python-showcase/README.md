# Python Monorepo with UV Dependency Manager

This project is a monorepo that utilizes Python UV as the dependency manager, handling multiple Python Lambda functions. It is designed to work seamlessly in both **local development** and **deployed environments**.

### Key Features

-   **Monorepo** architecture with multiple Python Lambda functions
-   Uses **Python UV** for managing dependencies across functions
-   **Lambda Layers** are used for external libraries, as the default bundling behavior is disabled for Python functions
-   Works for both **local development** and **deployed environments**

### Disclaimer

This template disables the default bundling behavior on Python functions. When external libraries are needed, **Lambda Layers** are utilized to package dependencies.

---

## Getting Started

### Prerequsites

-   Node.js
-   Python 3.12
-   Python UV

### How to run the project

1. **Clone the repository**: You can clone or copy this folder however you prefer
2. **Sync dependencies using UV**: Run the following command to sync the dependencies and set up the virtual environment:

    ```sh
    uv sync
    ```

    You should see a `.venv`folder appear after this step 3.

3. **Activate the vitual environment**:

    - Windows

        ```sh
        .venv\Scripts\activate
        ```

    - Linux/MacOS

        ```sh
        source .venv\bin\activate
        ```

4. **Prepare the development environment**: After activating the virtual environment, you'll need to use the appropriate command to start development. To better understand which scripts are available, you can open the `package.json`file and take a look at the `scripts` section:

    ```json
    "scripts": {
        "auth": "aws sso login --profile sandbox",
        "dev": "sst dev --profile sandbox",
        "build": "sst build --profile sandbox",
        "deploy": "sst deploy --stage prod --profile sandbox",
        "remove:local": "sst remove --profile sandbox",
        "remove:prod": "sst remove --stage prod --profile sandbox",
        "console": "sst console",
        "typecheck": "tsc --noEmit"
    }
    ```

    These scripts are predefined commands for common tasks live development, building, deploying, and removing the infrastructure

    - **Notice**: Each command contains the `--profile sandbox` flag. This specifies the AWS profile to use for authentication and operations.
    - **Notice**: The `deploy`and `remove:prod` commands use the `--stage prod` flag. Customize this as needed

5. **Start the development environment**:

    ```sh
    npm run dev
    ```

6. **Testing**: This project has `pytest` pre-installed. Run it with

    ```sh
    pytest
    ```

7. **Deploy to production**:

    ```sh
    npm run deploy
    ```

8. **Cleanup**:

    ```sh
    npm run remove:local
    npm run remove:prod
    ```
