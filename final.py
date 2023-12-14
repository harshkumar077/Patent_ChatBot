from flask import Flask, render_template, request
import re

app = Flask(__name__)
app.static_folder = 'static'

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import fitz  # PyMuPDF
import os

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

file_path = r"C:\Users\prath\Downloads\CODING\HACKAPHASIA\sodapdf-converted (1).pdf"

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    if not os.path.exists(file_path):
        return "File not found.", False
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    print("text is done")    
    return text, True

def generate_answer(question, context):
    input_text = f"Context: {context[:1024]}\nQuestion: {question}\nAnswer:"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Generate a response with a maximum length
    output = model.generate(input_ids, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2,
                             pad_token_id=tokenizer.eos_token_id)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    text_array = answer.split()

    # Find the index of "Question:" in the array
    try:
        question_index = text_array.index("Answer:")
    except ValueError:
        question_index = -1

    # Print the remaining answer if "Question:" is found in the array
    if question_index != -1 and question_index < len(text_array) - 1:
        answer_part = ' '.join(text_array[question_index:]).strip()
        print(answer_part)
    else:
        answer_part="No output after the question."


   
     
    
    return answer_part

# Flask routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_answer():
    user_question = request.args.get("msg")  # Change to "msg" as per the URL parameters


    if file_path and user_question:
        text, success = extract_text_from_pdf(file_path)
        if not success:
            return "Error extracting text from PDF."

        result = generate_answer(user_question, text)

        question_index = result.find("Question:")

        # Print the text after "Question:" if it exists
        if question_index != -1:
            print(result[question_index + len("Question:"):])
        else:
            print("No output after the question.") 

        return result
    

    else:
        
        return "Please enter a valid question."

if __name__ == "__main__":
    app.run()

