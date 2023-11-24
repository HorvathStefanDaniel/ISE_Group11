import tkinter as tk
from tkinter import messagebox
import sqlite3

DATABASE = 'quiz_game.db'

def execute_db_query(query, parameters=(), fetchall=False, commit=False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        if commit:
            conn.commit()
        if fetchall:
            return cursor.fetchall()
        return cursor.fetchone()
    
class GameSetup:
    def __init__(self, root, on_game_start, on_main_menu):
        self.root = root
        self.on_game_start = on_game_start
        self.on_main_menu = on_main_menu
        self.selected_topics = []
        self.number_of_players = 1

        # Setup UI elements
        self.setup_frame = tk.Frame(self.root)
        self.setup_frame.pack(pady=20)

        self.topic_label = tk.Label(self.setup_frame, text="Select Topics:")
        self.topic_label.grid(row=0, column=0, padx=10, pady=10)

        self.topic_listbox = tk.Listbox(self.setup_frame, selectmode="multiple")
        self.topic_listbox.grid(row=0, column=1, padx=10, pady=10)
        self.load_topics()

        self.player_number_label = tk.Label(self.setup_frame, text="Number of Players:")
        self.player_number_label.grid(row=1, column=0, padx=10, pady=10)

        self.player_number_spinbox = tk.Spinbox(self.setup_frame, from_=1, to=4)
        self.player_number_spinbox.grid(row=1, column=1, padx=10, pady=10)

        self.start_button = tk.Button(self.setup_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=2, column=1, padx=10, pady=10)

        self.back_button = tk.Button(self.setup_frame, text="Back to Main Menu", command=self.on_main_menu)
        self.back_button.grid(row=2, column=0, padx=10, pady=10)

    def load_topics(self):
        # Fetch topics from the database
        topics_data = execute_db_query("SELECT topic_id, topic_name FROM Topics", fetchall=True)
        for topic in topics_data:
            self.topic_listbox.insert(tk.END, topic[1])

    def start_game(self):
        # Get selected topics
        selected_indices = self.topic_listbox.curselection()
        self.selected_topics = [self.topic_listbox.get(i) for i in selected_indices]
        # Get number of players
        self.number_of_players = int(self.player_number_spinbox.get())
        # Start the game with the selected options
        self.setup_frame.destroy()
        self.on_game_start(self.selected_topics, self.number_of_players)

class Game:
    
    def __init__(self, root, on_main_menu, topics, number_of_players):
        self.topics = topics
        self.number_of_players = number_of_players
        self.root = root
        self.on_main_menu = on_main_menu
        self.score = 0
        self.current_question_index = 0
        self.questions = self.load_questions()

        # UI elements setup
        self.question_label = tk.Label(self.root, text="", font=('Helvetica', 18))
        self.question_label.pack(pady=20)

        self.answer_frame = tk.Frame(self.root)
        self.answer_frame.pack(pady=20)

        # Start the game
        self.display_next_question()

    def load_questions(self):
        # Fetch valid questions and their answers from the database
        questions_data = execute_db_query(
            "SELECT Q.question_id, Q.question_text "
            "FROM Questions Q "
            "WHERE EXISTS ("
            "SELECT 1 FROM Answers A WHERE A.question_id = Q.question_id AND A.is_correct = 1) "
            "AND ("
            "SELECT COUNT(*) FROM Answers A WHERE A.question_id = Q.question_id) >= 2 "
            "ORDER BY RANDOM()", 
            fetchall=True
        )
        
        questions = []
        for question in questions_data:
            question_id, question_text = question
            answers_data = execute_db_query(
                "SELECT answer_text, is_correct FROM Answers WHERE question_id=?",
                (question_id,), fetchall=True
            )
            
            # Filter out questions with less than 2 answers or no correct answer
            if len(answers_data) < 2 or not any(answer[1] for answer in answers_data):
                continue

            answers = [answer[0] for answer in answers_data]
            correct = next(i for i, answer in enumerate(answers_data) if answer[1])
            questions.append({"question": question_text, "answers": answers, "correct": correct})
        return questions

    def display_next_question(self):
        if self.current_question_index < len(self.questions):
            # Clear previous answers
            for widget in self.answer_frame.winfo_children():
                widget.destroy()

            question_info = self.questions[self.current_question_index]
            self.question_label.config(text=question_info["question"])

            # Display answer buttons
            for i, answer in enumerate(question_info["answers"]):
                answer_button = tk.Button(self.answer_frame, text=answer, command=lambda i=i: self.select_answer(i))
                answer_button.pack(side=tk.LEFT)
        else:
            # No more questions, end the game
            self.end_game()

    def select_answer(self, answer_index):
        correct_answer = self.questions[self.current_question_index]["correct"]
        if answer_index == correct_answer:
            # Increase score if the answer is correct
            self.score += 1
        self.current_question_index += 1
        self.display_next_question()

    def end_game(self):
        # Display the user's score and end the game
        messagebox.showinfo("Game Over", f"Your score is {self.score}")
        self.on_main_menu()  # Call the passed in function to show the main menu

def play_game_window(root, on_main_menu):
    # This will create a new instance of the game setup
    game_setup = GameSetup(root, on_game_start=lambda topics, players: Game(root, on_main_menu, topics, players), on_main_menu=on_main_menu)
