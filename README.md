# BetonBot

BetonBot is a Python project designed to automate and streamline tasks related to concrete (beton) management.
It integrates various functionalities such as weather updates, Telegram bot interactions, and data processing to enhance the efficiency of concrete delivery operations.

## Features

- Automated workflows for concrete management
- Easy integration and setup
- Customizable modules
- User-friendly command-line interface
- Logging and error handling for robust operation

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/nafanius/beton_bot.git
cd betonBot
pip install -r requirements.txt
```

## Configuration

create a file named `auth_data.py` in the `src` directory and fill in your tokens and credentials:

```python

token_bot = 'TokenTelegramBot'
token_weather = 'TOkenWeather'
token_chat_gpt = "TokenChatGPT"
cod_wit = 'COD_WIT'
```

## Usage

Run the main script:

```bash
python main.py
```

## Documentation

Detailed documentation is available in the [docs](docs/) folder. Refer to it for advanced configuration, module development, and troubleshooting.

## Contributing

Contributions are welcome! Please open issues or submit pull requests. Make sure to follow the contribution guidelines in `CONTRIBUTING.md`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
