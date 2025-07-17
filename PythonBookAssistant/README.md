1. Clone or extract the PythonBookAssistant project folder.

2. Navigate to the project directory.

3. Create and activate a Python virtual environment.

4. Run `pip install -r requirements.txt` to install dependencies.

5. Open `.env` and replace the placeholder values with your own Azure OpenAI and Azure Speech resource keys.

6. Place your PDF(s) inside the `assistant/docs/` folder.

7. Navigate to the `assistant/` directory in the terminal.

8. Run `python main.py` to load, embed, and store the PDF chunks into the vector database. A cache file will be saved inside `assistant/cache/`.

9. After embedding is complete, you can ask questions directly in the terminal using the assistant. Type "exit" to exit.

10. To launch the web interface, run `python assistant.py` inside the `assistant/` folder.

11. In a new terminal window, activate the virtual environment again.

12. Navigate to the `avatar/` folder.

13. Run `python app.py` to start the Azure 3D avatar service.

14. Go to (`http://localhost:5001`), type a question related to the embedded PDF.

15. The assistant will answer and the avatar will speak the response aloud automatically.

16. To stop the assistant, press `Ctrl + C` in both running terminals.

17. You can replace or add more PDFs in the `docs/` folder and rerun `main.py` to update the embeddings.
