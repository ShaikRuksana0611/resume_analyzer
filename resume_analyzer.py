import re
import nltk
import PyPDF2
import docx
import sys
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from tkinter import filedialog, Tk, scrolledtext, Button, Label

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Predefined skill set
COMMON_SKILLS = {"python", "java", "c++", "machine learning", "nlp", "sql", "excel", "tensorflow", "pandas", "django"}

# Function to extract text from different file formats
def extract_text_from_file(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".pdf"):
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    return ""

# Function to extract skills using NLTK
def extract_skills(text):
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum()]  # Remove punctuation
    words = [word for word in words if word not in stopwords.words('english')]  # Remove stopwords
    skills = set(words).intersection(COMMON_SKILLS)  # Match with predefined skills
    return skills

# Function to match skills with job description using TF-IDF
def match_skills(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    matched_skills = resume_skills.intersection(job_skills)
    match_percentage = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0
    return matched_skills, match_percentage

# GUI Mode
def analyze_resume_gui():
    resume_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Word files", "*.docx"), ("PDF files", "*.pdf")])
    if not resume_path:
        return
    job_description = job_text.get("1.0", "end")
    resume_text = extract_text_from_file(resume_path)
    matched_skills, match_percentage = match_skills(resume_text, job_description)

    result_text.delete("1.0", "end")
    result_text.insert("end", f"Matched Skills: {', '.join(matched_skills)}\n")
    result_text.insert("end", f"Match Percentage: {match_percentage:.2f}%")

# Function to exit GUI
def exit_gui():
    root.quit()
    root.destroy()

# GUI Creation
def create_gui():
    global root, job_text, result_text
    root = Tk()
    root.title("Resume Analyzer")

    Label(root, text="Paste Job Description:").pack()
    job_text = scrolledtext.ScrolledText(root, height=10, width=50)
    job_text.pack()

    Button(root, text="Analyze Resume", command=analyze_resume_gui).pack()
    Button(root, text="Exit", command=exit_gui).pack()  
    
    result_text = scrolledtext.ScrolledText(root, height=5, width=50)
    result_text.pack()

    root.mainloop()

# Console Mode
def analyze_resume_console():
    while True:
        resume_path = input("\nEnter the path of the resume file (or type 'exit' to quit): ")
        if resume_path.lower() == "exit":
            print("Exiting the program. Goodbye!")
            return

        job_desc_path = input("Enter the path of the job description file: ")
        if job_desc_path.lower() == "exit":
            print("Exiting the program. Goodbye!")
            return

        try:
            with open(job_desc_path, "r", encoding="utf-8") as job_file:
                job_description = job_file.read()
            resume_text = extract_text_from_file(resume_path)
            matched_skills, match_percentage = match_skills(resume_text, job_description)

            print("\n Matched Skills:", ", ".join(matched_skills))
            print(f" Match Percentage: {match_percentage:.2f}%")
        except Exception as e:
            print(f"Error: {e}")

# Function to handle user mode selection using a switch-case-like dictionary
def main_menu():
    options = {
        "1": create_gui,
        "2": analyze_resume_console,
        "3": sys.exit
    }

    while True:
        print("\n Resume Analyzer Menu")
        print("1️⃣ GUI Mode")
        print("2️⃣ Console Mode")
        print("3️⃣ Exit")

        choice = input("\nEnter your choice (1/2/3): ")
        action = options.get(choice, None)

        if action:
            action()
        else:
            print(" Invalid choice. Please enter 1, 2, or 3.")

# Run the program
if __name__ == "__main__":
    main_menu()
