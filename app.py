import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import fitz  # PyMuPDF
import os

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    if not os.path.exists(file_path):
        return "File not found.", False
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text, True

def generate_answer(question, context):
    input_text = f"Context: {context[:1024]}\nQuestion: {question}\nAnswer:"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Generate a response with a maximum length
    output = model.generate(input_ids, max_length=300, num_return_sequences=1, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    return answer

# Streamlit app
def main():
    st.title("Patent ChatBot")

    # Set background color to black
    st.markdown("""
        <style>
        body {
            background-color: black;
            color: white;
        }
        </style>
         """ ,
        unsafe_allow_html=True,

    )

    file_path="sodapdf-converted (1).pdf"
    question = st.text_input("Enter your question")

    if st.button("Answer"):
        if file_path and question:
            # Extract text from the PDF
            text, file_exists = extract_text_from_pdf(file_path)

            if not file_exists:
                st.write("Error: File not found.")
            else:
                # Generate an answer
                answer = generate_answer(question, text)
                # Extracting just the question and answer from the provided text
                question_answer_text = re.search(r"Answer:\s*(.*)", answer, re.DOTALL)


                # Extracted question and answer
                # question = question_answer_text.group(1) if question_answer_text else "No question found"
                answer = question_answer_text.group(1) if question_answer_text else "No answer found"

                st.write("Answer:", answer)
        else:
            st.write("Please enter a valid file path and a question.")

if __name__ == '__main__':
    main()
