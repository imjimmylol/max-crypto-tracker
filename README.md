# Crypto Signal Tracker

A Python application to monitor, parse, and analyze Telegram trading signals.

## Features

-   Real-time monitoring of new messages in a specified Telegram chat.
-   Utility to fetch historical messages from a chat for a given period.
-   Utility to list all your Telegram chats and find their IDs.
-   Configurable through environment variables.

## Setup

### Prerequisites

-   Python 3.10+
-   [Conda](https://docs.conda.io/en/latest/miniconda.html) for environment management.

### Installation

1.  **Clone the repository (optional):**
    ```bash
    git clone <repository-url>
    cd crypto-signal-tracker
    ```

2.  **Create Conda Environment:**
    The project is configured to run within a Conda environment named `crypto-signal-tracker`. You should have this environment already. If not, you would create and activate it:
    ```bash
    conda create -n crypto-signal-tracker python=3.10
    conda activate crypto-signal-tracker
    ```

3.  **Install Dependencies:**
    Install the required Python packages.
    ```bash
    # From the root of the project
    pip install -e .
    ```
    This command installs the project in "editable" mode and pulls in the dependencies from `pyproject.toml`.

4.  **Configure Environment Variables:**
    You need to provide your Telegram API credentials. Copy the example `.env` file:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file and fill in your `API_ID` and `API_HASH`. You can get these from [my.telegram.org](https://my.telegram.org).
    ```
    API_ID=1234567
    API_HASH=your_api_hash_here
    SESSION_NAME=crypto-signal-tracker
    ```

## Usage

Make sure your `crypto-signal-tracker` conda environment is activated before running any scripts.

### 1. Find Your Chat ID (`get_chat_id.py`)

Before you can monitor a chat or fetch its history, you need to know its ID.

Run the `get_chat_id.py` script:
```bash
conda run -n crypto-signal-tracker python get_chat_id.py
```
This will print a list of all your chats and their corresponding IDs. Find your target chat (it's usually a negative number for groups and channels) and copy the ID.

The first time you run this, you will be prompted to enter your phone number, a login code from Telegram, and your 2FA password if you have one.

### 2. Fetch Historical Messages (`fetch_history.py`)

This script allows you to download messages from a specific chat for a defined number of past days. The messages are saved to `messages.json`.

1.  **Set the Chat ID:** Open `fetch_history.py` and replace the `TARGET_CHAT_ID` with the ID you found in the previous step.

2.  **Run the script:**
    ```bash
    # Fetch history from the last 7 days (default)
    conda run -n crypto-signal-tracker python fetch_history.py

    # Fetch history from the last 30 days
    conda run -n crypto-signal-tracker python fetch_history.py --past-days 30
    ```

### 3. Monitor for New Messages (`main.py`)

This is the main application script that listens for new messages in real-time.

1.  **Set the Chat ID:** Open `src/crypto_signal_tracker/main.py` and find the following line. Replace the placeholder ID with your target chat ID.
    ```python
    @client.on(events.NewMessage(chats=[-1002430013497])) # <--- IMPORTANT: REPLACE WITH YOUR CHAT ID
    ```

2.  **Run the script:**
    ```bash
    conda run -n crypto-signal-tracker python src/crypto_signal_tracker/main.py
    ```
    The application will now be running and will print any new messages from your target chat to the console. Press `Ctrl+C` to stop it.

## Development

This project uses `pre-commit` hooks to maintain code quality. To set it up for development, install the dev dependencies and the hooks:

```bash
pip install -e ".[dev]"
pre-commit install
```
