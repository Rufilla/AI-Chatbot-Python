# AI-Chatbot-Python
# Open AI Chatbot

This is a simple chatbot for Open AI GPT4, written in Python.
To correctly use it, you will need to create a file called .env from the template file and add in your Open AI key to that file. Then, run it using python3 command with chat.py as an argument.

## Dependencies

The program requires several Python dependencies. Here is a list of them:

- `os`
- `openai`
- `tkinter`
- `tkinter.font`
- `filedialog` (from tkinter)
- `messagebox` (from tkinter)
- `ChatCompletion` (from openai)
- `dotenv`
- `json`
- `time`

## Setup

1. Clone this repository.
2. Install the required Python libraries listed in the "Dependencies" section. You can typically install these with pip by running `pip install <library-name>`.
3. Rename the `dotenv_template` file to `.env`.
4. Open the `.env` file with any text editor, and provide your Open AI key. It should look something like this:

```
OPENAI_KEY=your-key-goes-here
```

Replace "your-key-goes-here" with your actual Open AI key.

## How to run 

Run the chatbot script with python3:

```bash
python3 chat.py
```

That's it! The chatbot program should now be up and running.

## Contribution

Feel free to fork this project and make your contribution.

## License

This project is licensed under the MIT License.

## Disclaimer

This is a basic chatbot for OpenAI and does not include any sophisticated error handling or complex features. Please use at your own discretion.

## Developer Contact 

For any suggestions or feedback or if you would like to report any bugs, please contact me at: joe@rufilla.com
