import os
import sqlite3
import torch
from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Flask app setup
app = Flask(__name__)

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "generated_code.db")

# Debugging outputs to check paths
print(f"BASE_DIR: {BASE_DIR}")
print(f"DB_FILE: {DB_FILE}")

# Ensure the parent directory exists and the database file exists
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS code_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            generated_code TEXT
        )
    """)
    conn.commit()
    conn.close()

# Model setup
MODEL_NAME = "gpt2"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model once when the server starts
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME).to(device)
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)

@app.route("/generate", methods=["POST"])
def generate_code():
    """
    Generate code based on a user-provided prompt and save it to a database.
    """
    data = request.get_json()
    if "prompt" not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data["prompt"]
    max_length = data.get("max_length", 150)
    temperature = data.get("temperature", 0.7)

    try:
        # Generate code
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
        
        # Avoid large tensor memory issue by generating in a controlled manner
        with torch.no_grad():
            output = model.generate(input_ids, max_length=max_length, temperature=temperature, pad_token_id=tokenizer.eos_token_id)
        
        generated_code = tokenizer.decode(output[0], skip_special_tokens=True)

        # Save to SQLite database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO code_data (prompt, generated_code) VALUES (?, ?)", (prompt, generated_code))
        conn.commit()
        conn.close()

        return jsonify({"generated_code": generated_code})
    
    except Exception as e:
        app.logger.error(f"Error during code generation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print(f"Database file path: {DB_FILE}")
    app.run(host="127.0.0.1", port=5000)
