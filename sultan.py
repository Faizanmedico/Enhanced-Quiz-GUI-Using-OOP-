import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import os

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Python Quiz")
        self.root.geometry("600x500")
        
        # Quiz data (text + image questions)
        self.questions = [
            {
                "question": "What is the output of print(type(3.14))?",
                "image": "1.png",  # Image path
                "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>"],
                "answer": "<class 'float'>"
            },
            {
                "question": "Which keyword defines a function in Python?",
                "image": "1.png",  # Image path
                "options": ["def", "function", "lambda"],
                "answer": "def"
            },


            {
                "options": ["3", "4", "5"],
                "image": "1.png",  # Hypothetical image
                "question": "What is the output of 2 + 2?",
                "answer": "4"
            },
            {
                "question": "Which of these is a mutable data type in Python?",
                "image": "1.png",  # Hypothetical image
                "options": ["tuple", "string", "list"],
                "answer": "list"
            },
            {
                "question": "What does the 'len()' function do?",
                "image": "1.png",  # Hypothetical image
                "options": ["Returns the largest element", "Returns the length of a sequence", "Returns the smallest element"],
                "answer": "Returns the length of a sequence"
            },
            {
                "question": "Which operator is used for exponentiation in Python?",
                "image": "1.png",  # Hypothetical image
                "options": ["^", "**", "*"],
                "answer": "**"
            },
            {
                "question": "What will print('Hello'[1]) output?",
                "image": "1.png",  # Hypothetical image
                "options": ["H", "e", "l"],
                "answer": "e"
            },
            {
                "question": "Which of the following is a boolean value?",
                "image": "1.png",  # Hypothetical image
                "options": ["'True'", "True", "false"],
                "answer": "True"
            },
            {
                "question": "What type of loop is 'for i in range(5):'?",
                "image": "1.png",  # Hypothetical image
                "options": ["while loop", "do-while loop", "for loop"],
                "answer": "for loop"
            },
            {
                "question": "How do you write a single-line comment in Python?",
                "image": "1.png",  # Hypothetical image
                "options": ["// This is a comment", "# This is a comment", "/* This is a comment */"],
                "answer": "# This is a comment"
            },
            {
                "question": "What is the output of bool(0)?",
                "image": "1.png",  # Hypothetical image
                "options": ["True", "False", "Error"],
                "answer": "False"
            },
            {
                "question": "Which method is used to add an element to the end of a list?",
                "image": "1.png",  # Hypothetical image
                "options": ["insert()", "add()", "append()"],
                "answer": "append()"
            },


                 ]
        random.shuffle(self.questions)
        
        self.current_question = 0
        self.score = 0
        self.time_left = 10
        
        # GUI Setup
        self.question_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.question_label.pack(pady=10)
        
        self.image_label = tk.Label(root)  # For images
        self.image_label.pack(pady=10)
        
        self.radio_var = tk.StringVar()
        self.option_buttons = []
        for i in range(3):
            btn = tk.Radiobutton(
                root, text="", variable=self.radio_var, value="",
                font=("Arial", 12), anchor="w"
            )
            self.option_buttons.append(btn)
            btn.pack(fill="x", padx=50)
        
        # Timer and Progress Bar
        self.timer_label = tk.Label(root, text="", font=("Arial", 12))
        self.timer_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)
        
        # Navigation Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)
        
        self.prev_button = tk.Button(
            self.button_frame, text="← Previous", command=self.prev_question,
            state="disabled", font=("Arial", 12)
        )
        self.prev_button.pack(side="left", padx=20)
        
        self.next_button = tk.Button(
            self.button_frame, text="Next →", command=self.check_answer,
            font=("Arial", 12)
        )
        self.next_button.pack(side="right", padx=20)
        
        self.load_question()
    
    def load_question(self):
        # Reset UI for new question
        q = self.questions[self.current_question]
        self.question_label.config(text=q["question"])
        
        # Load image if available
        if "image" in q and os.path.exists(q["image"]):
            try:
                pil_img = Image.open(q["image"])
                pil_img = pil_img.resize((300, 200), Image.LANCZOS)
                img = ImageTk.PhotoImage(pil_img)
                self.image_label.config(image=img)
                self.image_label.image = img  # Keep reference
            except Exception as e:
                self.image_label.config(text=f"[Image Error: {e}]")
        else:
            self.image_label.config(image="")
        
        # Load options
        for i, option in enumerate(q["options"]):
            self.option_buttons[i].config(text=option, value=option)
        self.radio_var.set("")
        
        # Update navigation buttons
        self.prev_button.config(state="normal" if self.current_question > 0 else "disabled")
        
        # Start timer
        self.time_left = 10
        self.update_timer()
    
    def update_timer(self):
        if self.time_left > 0:
            # Update progress bar and color
            self.progress_bar["value"] = (self.time_left / 10) * 100
            color = "red" if self.time_left <= 5 else "green"
            self.timer_label.config(text=f"⏱️ Time left: {self.time_left}s", fg=color)
            self.time_left -= 1
            self.root.after(5000, self.update_timer)
        else:
            self.check_answer(auto_submit=True)
    
    def check_answer(self, auto_submit=False):
        # Check if answer is correct
        user_answer = self.radio_var.get()
        correct_answer = self.questions[self.current_question]["answer"]
        
        if user_answer == correct_answer:
            self.score += 1
        
        # Move to next question or end quiz
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_result()
    
    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.load_question()
    
    def show_result(self):
        messagebox.showinfo(
            "Quiz Finished!",
            f"🎉 Your score: {self.score}/{len(self.questions)}\n"
            f"Accuracy: {round(self.score/len(self.questions)*100)}%"
        )
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

