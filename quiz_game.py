# quiz_game.py
# Main quiz game implementation

import json
import os
from datetime import datetime
from quiz_data import quiz_questions


class QuizGame:
    def __init__(self):
        self.questions = quiz_questions
        self.score = 0
        self.total_questions = len(self.questions)
        self.player_name = ""
        self.answers_history = []
        
    def welcome(self):
        """Display welcome message and get player name"""
        print("=" * 50)
        print("        WELCOME TO THE QUIZ GAME!")
        print("=" * 50)
        print("\nTest your knowledge with our exciting quiz!\n")
        
        self.player_name = input("Please enter your name: ").strip()
        if not self.player_name:
            self.player_name = "Player"
        
        print(f"\nHello {self.player_name}! Let's begin the quiz.\n")
        print(f"You will be asked {self.total_questions} questions.")
        print("Each question has 4 options (A, B, C, D).")
        print("Type the letter of your answer.\n")
        input("Press Enter to start...")
        print("\n" + "=" * 50 + "\n")
    
    def ask_question(self, question_data, question_num):
        """Ask a single question and return if answer is correct"""
        print(f"Question {question_num}/{self.total_questions}")
        print("-" * 40)
        print(question_data["question"])
        print()
        
        for option in question_data["options"]:
            print(option)
        print()
        
        # Get user answer with validation
        while True:
            user_answer = input("Your answer (A/B/C/D): ").strip().upper()
            if user_answer in ['A', 'B', 'C', 'D']:
                break
            print("Invalid input! Please enter A, B, C, or D.")
        
        # Check if answer is correct
        is_correct = user_answer == question_data["answer"]
        
        # Store answer history
        self.answers_history.append({
            "question": question_data["question"],
            "user_answer": user_answer,
            "correct_answer": question_data["answer"],
            "is_correct": is_correct
        })
        
        # Update score
        if is_correct:
            self.score += 1
            print("\n✅ Correct! Well done!\n")
        else:
            print(f"\n❌ Wrong! The correct answer was {question_data['answer']}.\n")
        
        return is_correct
    
    def run_quiz(self):
        """Run the complete quiz"""
        self.welcome()
        
        for i, question in enumerate(self.questions, 1):
            self.ask_question(question, i)
            if i < self.total_questions:
                print("-" * 40 + "\n")
        
        self.show_results()
        self.save_results()
    
    def show_results(self):
        """Display final results"""
        print("\n" + "=" * 50)
        print("              QUIZ COMPLETE!")
        print("=" * 50)
        print(f"\nPlayer: {self.player_name}")
        print(f"Score: {self.score}/{self.total_questions}")
        
        percentage = (self.score / self.total_questions) * 100
        print(f"Percentage: {percentage:.1f}%")
        
        # Grade evaluation
        if percentage >= 90:
            grade = "A+ (Excellent!)"
        elif percentage >= 80:
            grade = "A (Great Job!)"
        elif percentage >= 70:
            grade = "B (Good Work!)"
        elif percentage >= 60:
            grade = "C (Not Bad!)"
        elif percentage >= 50:
            grade = "D (Keep Practicing!)"
        else:
            grade = "F (Better Luck Next Time!)"
        
        print(f"Grade: {grade}")
        print("\n" + "=" * 50)
        
        # Show detailed review
        print("\n📋 DETAILED REVIEW:")
        print("-" * 50)
        for i, entry in enumerate(self.answers_history, 1):
            status = "✅" if entry["is_correct"] else "❌"
            print(f"{i}. {status} {entry['question']}")
            print(f"   Your answer: {entry['user_answer']} | Correct: {entry['correct_answer']}\n")
    
    def save_results(self):
        """Save quiz results to a file"""
        # Create results directory if it doesn't exist
        if not os.path.exists("results"):
            os.makedirs("results")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/quiz_result_{self.player_name}_{timestamp}.json"
        
        result_data = {
            "player_name": self.player_name,
            "score": self.score,
            "total_questions": self.total_questions,
            "percentage": (self.score / self.total_questions) * 100,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "answers_history": self.answers_history
        }
        
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=4)
        
        print(f"\n💾 Results saved to: {filename}")
    
    def load_previous_results(self):
        """Load and display previous results"""
        if not os.path.exists("results"):
            print("\nNo previous results found.")
            return
        
        result_files = [f for f in os.listdir("results") if f.endswith('.json')]
        
        if not result_files:
            print("\nNo previous results found.")
            return
        
        print("\n📊 PREVIOUS RESULTS:")
        print("-" * 50)
        
        for filename in sorted(result_files, reverse=True)[:10]:  # Show last 10
            filepath = os.path.join("results", filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                print(f"Player: {data['player_name']}")
                print(f"Score: {data['score']}/{data['total_questions']}")
                print(f"Percentage: {data['percentage']:.1f}%")
                print(f"Date: {data['date']}")
                print("-" * 50)


def main():
    """Main program entry point"""
    while True:
        print("\n" + "=" * 50)
        print("        QUIZ GAME MENU")
        print("=" * 50)
        print("1. Start New Quiz")
        print("2. View Previous Results")
        print("3. Exit")
        print("=" * 50)
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            game = QuizGame()
            game.run_quiz()
        elif choice == '2':
            game = QuizGame()
            game.load_previous_results()
            input("\nPress Enter to continue...")
        elif choice == '3':
            print("\nThank you for playing! Goodbye! 👋")
            break
        else:
            print("\nInvalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
