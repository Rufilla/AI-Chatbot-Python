import os
import openai
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox
from openai import ChatCompletion
from dotenv import load_dotenv
import json
import time


# Define the chatbot application class
class ChatbotApp:
    # Initialise the chatbot application
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Joe's AI Chatbot V2")

        # Initialise the font
        self.chat_font = tkFont.Font(size=14, family="monospace")

        # Initialize conversation history
        self.conversation_history = ""

        # Initialize OpenAI API
        # Load OpenAI API key from .env file
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")

        # Load system prompt from a file
        with open("system_prompt_default.txt", "r") as file:
            system_prompt = file.read().strip()

        # Initialize message history with a system message
        self.message_history = [{"role": "system", "content": system_prompt}]
        
        # Set up GUI
        self.setup_gui()

        # Move focus to the message entry field
        self.entry_field.focus()


    # Set up the GUI
    def setup_gui(self):
        # Create chat display area
        self.chat_display = tk.Text(self.window, height=30, width=130, wrap=tk.WORD, font=self.chat_font, yscrollcommand=True)
        self.chat_display.pack()

        # Create message entry field
        self.entry_field = tk.Text(self.window, height=5, width=130, wrap=tk.WORD, font=self.chat_font, yscrollcommand=True)
        self.entry_field.bind("<Control-Return>", self.send_message)  # Use Ctrl+Enter to send message
        self.entry_field.pack()

        # Create send button
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack()

        # Create some colour tags
        self.chat_display.tag_configure("system", foreground="black")
        self.chat_display.tag_configure("user", foreground="blue")
        self.chat_display.tag_configure("assistant", foreground="green")


    # Send a message to the chatbot
    def send_message(self, event=None):
        # Get the message from the entry field
        message = self.entry_field.get("1.0", "end-1c")  # "1.0" means that the input should be read from line one, character zero
        # Delete the contents of the entry field
        self.entry_field.delete("1.0", tk.END)
        
        # Ignore empty messages
        if not message:
            return 'break'  # This stops the event propagation

        # Update the chat display and message history
        self.conversation_history += f"User: {message}\n"
        self.chat_display.insert(tk.END, f"User: {message}\n", "user")

        # Check if the message is a command
        if message.startswith("/"):
            self.process_command(message[1:])
        else:
            self.chat_with_openai(message)

        # Set cursor back to the top left of the input box
        self.entry_field.focus_set()  # Set focus back to the entry field
        self.entry_field.mark_set("insert", "1.0")

        return 'break'  # This stops the event propagation


    # ============================================================
    # Command processing
    # ============================================================
    # Process a command
    def process_command(self, command):
        # Split the command into words
        words = command.split()

        # If it's not a command, send it to the OpenAI API
        if not words:
            return

        # Process known commands
        if words[0] == "help":
            self.show_help()
        elif words[0] == "quit":
            self.window.quit()
        elif words[0] == "save":
            self.save_conversation()
        elif words[0] == "load":
            self.load_conversation()
        elif words[0] == "clear":
            self.clear_conversation()
        elif words[0] == "loadprompt":
            self.load_system_prompt()


    # Command: Show help message
    def show_help(self):
            help_message = """
/help: Show this help message
/quit: Exit the program
/save: Save the conversation
/load: Load a saved conversation
/clear: Clear the conversation
/loadprompt: Load system prompt from a file
"""
            self.conversation_history += f"System: {help_message}\n"
            self.chat_display.insert(tk.END, f"System: {help_message}\n", "system")
            self.chat_display.see(tk.END)  # Scroll to the end of the text in the chat display


    # Command: Save the conversation
    def save_conversation(self):
        # Save the message history to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.message_history, file)


    # Command: Load conversation from a file
    def load_conversation(self):
        # Load the message history from a file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                self.message_history = json.load(file)
                # Reset the conversation history
                self.conversation_history = ""
                for message in self.message_history:
                    # Add each message to the conversation history
                    role = "User" if message["role"] == "user" else "Bot"
                    self.conversation_history += f"{role}: {message['content']}\n"
                # Update the chat display with the loaded conversation
                self.chat_display.delete(1.0, tk.END)
                self.chat_display.insert(tk.END, self.conversation_history, "system")


    # Command: Clear the conversation
    def clear_conversation(self):
        # Clear the message history and reset the conversation history
        self.message_history = [{"role": "system", "content": "You are a helpful assistant."}]
        self.conversation_history = ""
        # Clear the chat display
        self.chat_display.delete(1.0, tk.END)


    # Command: Load system prompt from a file
    def load_system_prompt(self):
        # Load the system prompt from a file
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                system_prompt = file.read().strip()
                self.message_history = [{"role": "system", "content": system_prompt}]


    # ============================================================
    # OpenAI API
    # ============================================================
    # Chat with the OpenAI API
    def chat_with_openai(self, message):
        start_time = time.time()
        delay_time = 0.01 # DELAY TIME BETWEEN EACH EVENT
        answer = '' # ANSWER TO BE PRINTED
        max_tokens = 500 # MAX TOKENS PER REQUEST

        # Add the new user message to the message history
        self.message_history.append({"role": "user", "content": message})

        # Send the message history to the OpenAI API
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.message_history,
            stream=True,
            max_tokens=max_tokens,
        )

        self.conversation_history += "Bot:"
        self.chat_display.insert(tk.END, "Bot:", "assistant")

        for event in response: 
            # STREAM THE ANSWER
            #print(answer, end='', flush=True) # Print the response
            # RETRIEVE THE TEXT FROM THE RESPONSE
            event_time = time.time() - start_time  # CALCULATE TIME DELAY BY THE EVENT
            event_text = event['choices'][0]['delta'] # EVENT DELTA RESPONSE
            answer = event_text.get('content', '') # RETRIEVE CONTENT
            time.sleep(delay_time)
            self.conversation_history += answer
            self.chat_display.insert(tk.END, answer, "assistant")
            self.chat_display.see(tk.END)  # Scroll to the end of the text in the chat display
            self.window.update_idletasks()  # Needed to make the changes appear immediately

        # Add a newline after the response
        self.conversation_history += "\n"
        self.chat_display.insert(tk.END, "\n", "assistant")

        # Add the bot's response to the message history
        self.message_history.append({"role": "assistant", "content": answer})

    # ============================================================

    # Run the chatbot application
    def run(self):
        # Start the Tkinter event loop
        tk.mainloop()


if __name__ == "__main__":
    # Create a new instance of the chatbot application and run it
    app = ChatbotApp()
    app.run()
