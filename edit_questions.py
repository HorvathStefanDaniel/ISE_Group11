import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database filename
DATABASE = 'quiz_game.db'

class TopicDialog(tk.Toplevel):
    def __init__(self, parent, title, topic_id=None):
        super().__init__(parent)
        self.title(title)
        self.topic_id = topic_id
        self.result = None

        tk.Label(self, text="Topic Name:").grid(row=0, column=0, padx=10, pady=10)
        self.topic_name_var = tk.StringVar()
        self.topic_entry = tk.Entry(self, textvariable=self.topic_name_var)
        self.topic_entry.grid(row=0, column=1, padx=10, pady=10)

        save_button = tk.Button(self, text="Save", command=self.on_save)
        save_button.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

        if topic_id:
            # Load the topic name from the database
            topic_data = execute_db_query("SELECT topic_name FROM Topics WHERE topic_id=?", (topic_id,), fetch=True)
            if topic_data:
                self.topic_name_var.set(topic_data[0][0])

        self.topic_entry.focus_set()

    def on_save(self):
        topic_name = self.topic_name_var.get().strip()
        if topic_name:
            if self.topic_id:
                # Update existing topic
                execute_db_query("UPDATE Topics SET topic_name=? WHERE topic_id=?", (topic_name, self.topic_id))
            else:
                # Insert new topic
                execute_db_query("INSERT INTO Topics (topic_name) VALUES (?)", (topic_name,))
            self.result = topic_name
            self.destroy()
        else:
            messagebox.showwarning("Warning", "The topic name cannot be empty.", parent=self)


class QuestionDialog(tk.Toplevel):
    def __init__(self, parent, title, topic_id, question_id=None):
        super().__init__(parent)
        self.title(title)
        self.question_id = question_id
        self.topic_id = topic_id
        self.result = None

        tk.Label(self, text="Question Text:").grid(row=0, column=0, padx=10, pady=10)
        self.question_text_var = tk.StringVar()
        self.question_entry = tk.Entry(self, textvariable=self.question_text_var)
        self.question_entry.grid(row=0, column=1, padx=10, pady=10)

        save_button = tk.Button(self, text="Save", command=self.on_save)
        save_button.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

        if question_id:
            # Load the question text from the database
            question_data = execute_db_query("SELECT question_text FROM Questions WHERE question_id=?", (question_id,), fetch=True)
            if question_data:
                self.question_text_var.set(question_data[0][0])

        self.question_entry.focus_set()

    def on_save(self):
        question_text = self.question_text_var.get().strip()
        if question_text:
            if self.question_id:
                # Update existing question
                execute_db_query("UPDATE Questions SET question_text=? WHERE question_id=?", (question_text, self.question_id))
            else:
                # Insert new question
                execute_db_query("INSERT INTO Questions (topic_id, question_text) VALUES (?, ?)", (self.topic_id, question_text))
            self.result = question_text
            self.destroy()
        else:
            messagebox.showwarning("Warning", "The question text cannot be empty.", parent=self)

class AnswerDialog(tk.Toplevel):
    def __init__(self, parent, title, question_id, answer_id=None):
        super().__init__(parent)
        self.title(title)
        self.answer_id = answer_id
        self.question_id = question_id
        self.result = None

        tk.Label(self, text="Answer Text:").grid(row=0, column=0, padx=10, pady=10)
        self.answer_text_var = tk.StringVar()
        self.answer_entry = tk.Entry(self, textvariable=self.answer_text_var)
        self.answer_entry.grid(row=0, column=1, padx=10, pady=10)

        self.is_correct_var = tk.BooleanVar()
        self.is_correct_check = tk.Checkbutton(self, text="Correct answer?", variable=self.is_correct_var)
        self.is_correct_check.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

        save_button = tk.Button(self, text="Save", command=self.on_save)
        save_button.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)

        if answer_id:
            # Load the answer text and correctness from the database
            answer_data = execute_db_query("SELECT answer_text, is_correct FROM Answers WHERE answer_id=?", (answer_id,), fetch=True)
            if answer_data:
                self.answer_text_var.set(answer_data[0][0])
                self.is_correct_var.set(answer_data[0][1])

        self.answer_entry.focus_set()

    def on_save(self):
        answer_text = self.answer_text_var.get().strip()
        is_correct = self.is_correct_var.get()
        if answer_text:
            if self.answer_id:
                # Update existing answer
                execute_db_query("UPDATE Answers SET answer_text=?, is_correct=? WHERE answer_id=?", (answer_text, is_correct, self.answer_id))
            else:
                # Insert new answer
                execute_db_query("INSERT INTO Answers (question_id, answer_text, is_correct) VALUES (?, ?, ?)", (self.question_id, answer_text, is_correct))
            self.result = (answer_text, is_correct)
            self.destroy()
        else:
            messagebox.showwarning("Warning", "The answer text cannot be empty.", parent=self)


def execute_db_query(query, parameters=(), fetch=False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        if fetch:
            return cursor.fetchall()
        conn.commit()

def load_topics_from_db():
    return execute_db_query("SELECT * FROM Topics", fetch=True)

def load_questions_from_db(topic_id):
    return execute_db_query("SELECT * FROM Questions WHERE topic_id=?", (topic_id,), fetch=True)

def load_answers_from_db(question_id):
    return execute_db_query("SELECT * FROM Answers WHERE question_id=?", (question_id,), fetch=True)

def edit_questions_window(main_root):
    # Function to refresh the tree view
    def refresh_tree():
        tree.delete(*tree.get_children())  # Clear the tree view
        for topic in load_topics_from_db():
            topic_id = topic[0]
            topic_title = topic[1]
            topic_node = tree.insert('', 'end', iid=f"topic_{topic_id}", values=(topic_id, topic_title, 'Topic'))
            
            for question in load_questions_from_db(topic_id):
                question_id = question[0]
                question_text = question[2]  # Adjust the index as needed
                # One indent and a ↳ for questions
                question_node = tree.insert(topic_node, 'end', iid=f"question_{question_id}", values=(question_id, '    ' + '↳ ' + question_text, 'Question'))
                
                for answer in load_answers_from_db(question_id):
                    answer_id = answer[0]
                    answer_text = answer[2]  # Adjust the index as needed
                    is_correct = answer[3]  # Adjust the index as needed
                    correct_text = "Correct" if is_correct else "Incorrect"
                    # Two indents and a ↳ for answers
                    tree.insert(question_node, 'end', iid=f"answer_{answer_id}", values=(answer_id, '       ' + '↳ ' + answer_text + ' (' + correct_text + ')', 'Answer'))

# ... (rest of the previous code remains unchanged)

    # Create a top-level window
    edit_window = tk.Toplevel(main_root)
    edit_window.title('Edit Questions')
    edit_window.state('zoomed')  # Fullscreen mode

    # Treeview widget
    tree = ttk.Treeview(edit_window, columns=('ID', 'Description', 'Type'), show='headings')
    tree.pack(expand=True, fill='both')
    # Define ID
    # When setting up the Treeview columns, set the ID column width and minwidth to 0
    tree.column('ID', width=0, minwidth=0, stretch=tk.NO)
    tree.heading('ID', text='ID', anchor=tk.CENTER)  # You can keep the heading configuration if needed for sorting or other operations

    # Define columns
    tree.column('Description', anchor=tk.W, width=800)
    tree.column('Type', anchor=tk.W, width=120)

    # Create headings
    tree.heading('Description', text='Description', anchor=tk.W)
    tree.heading('Type', text='Type', anchor=tk.W)

    # Buttons for managing data
    btn_frame = tk.Frame(edit_window)
    btn_frame.pack(fill='x')

    add_btn = tk.Button(btn_frame, text="Add")
    edit_btn = tk.Button(btn_frame, text="Edit")
    delete_btn = tk.Button(btn_frame, text="Delete")

    add_btn.pack(side=tk.LEFT, padx=10, pady=10)
    edit_btn.pack(side=tk.LEFT, padx=10, pady=10)
    delete_btn.pack(side=tk.LEFT, padx=10, pady=10)

    def get_selected_topic_or_question(tree):
    # Helper function to return the selected topic or question and its type
        selected_item = tree.selection()
        if selected_item:
            item_id, _, item_type = tree.item(selected_item, 'values')
            return item_id, item_type
        return None, None

    def add_item():
        selected_item = tree.selection()
        item_id, item_type = None, None
        
        # If there's a selected item, get its ID and type
        if selected_item:
            item_id, _, item_type = tree.item(selected_item, 'values')

        if item_type == 'Question':
            # Adding an answer to the selected question
            dialog = AnswerDialog(edit_window, "Add Answer", question_id=item_id)
        elif item_type == 'Topic':
            # Adding a question to the selected topic
            dialog = QuestionDialog(edit_window, "Add Question", topic_id=item_id)
        else:
            # If no item is selected or the item is not a question, default to adding a new topic
            dialog = TopicDialog(edit_window, "Add Topic")

        edit_window.wait_window(dialog)

        # After closing the dialog, refresh the tree if an item was added
        if dialog.result:
            refresh_tree()

    # You need to implement the edit_item function
    def edit_item():
        selected_item = tree.selection()
        if selected_item:
            item_id, _, item_type = tree.item(selected_item, 'values')
            if item_type == 'Topic':
                dialog = TopicDialog(edit_window, "Edit Topic", topic_id=item_id)
                edit_window.wait_window(dialog)
                if dialog.result:
                    refresh_tree()
            elif item_type == 'Question':
                # Retrieve the topic_id by finding the parent item in the tree
                parent_item = tree.parent(selected_item)
                topic_id = tree.item(parent_item, 'values')[0]
                dialog = QuestionDialog(edit_window, "Edit Question", topic_id, question_id=item_id)
                edit_window.wait_window(dialog)
                if dialog.result:
                    refresh_tree()
            elif item_type == 'Answer':
                # Retrieve the question_id by finding the parent item in the tree
                parent_item = tree.parent(selected_item)
                question_id = tree.item(parent_item, 'values')[0]
                dialog = AnswerDialog(edit_window, "Edit Answer", question_id, answer_id=item_id)
                edit_window.wait_window(dialog)
                if dialog.result:
                    refresh_tree()
            else:
                messagebox.showwarning("Warning", "Please select a valid item to edit.")
        else:
            messagebox.showwarning("Warning", "Please select an item to edit.")


    def delete_item():
        selected_item = tree.selection()
        if selected_item:
            item_id, item_description, item_type = tree.item(selected_item, 'values')
            response = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {item_type.lower()}:\n{item_description}?", parent=edit_window)
            if response:
                try:
                    if item_type == 'Topic':
                        execute_db_query("DELETE FROM Topics WHERE topic_id=?", (item_id,))
                    elif item_type == 'Question':
                        execute_db_query("DELETE FROM Questions WHERE question_id=?", (item_id,))
                    elif item_type == 'Answer':
                        execute_db_query("DELETE FROM Answers WHERE answer_id=?", (item_id,))
                    else:
                        messagebox.showerror("Error", "Unknown item type. Cannot delete.", parent=edit_window)
                        return
                    refresh_tree()  # Refresh the interface to reflect the deletion
                except sqlite3.IntegrityError as e:
                    messagebox.showerror("Error", "This item cannot be deleted because it is in use.", parent=edit_window)
        else:
            messagebox.showwarning("Warning", "Please select an item to delete.", parent=edit_window)


    # Bind buttons to event handlers
    add_btn.config(command=add_item)
    edit_btn.config(command=edit_item)
    delete_btn.config(command=delete_item)

    # Populate the tree with data
    refresh_tree()

    return edit_window
