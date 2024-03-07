from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QPushButton,QRadioButton,QTextEdit,QSpinBox
from PyQt5.QtCore import QTimer
from PyQt5 import uic
import sys, random, json
 
class Game(QMainWindow):
    def __init__(self):
        super(Game,self).__init__()
        uic.loadUi("page1.ui",self)

        self.setWindowTitle("ROCK PAPER SCISSOR GAME")

        self.start_button = self.findChild(QPushButton, "start")
       
        self.start_button.setStyleSheet(
            "QPushButton {"
                "background-color: rgb(98, 98, 98);"
                "color:white;"
            "}"
            "QPushButton:hover {"
            " background-color: rgb(253, 0, 4);"
            "}"
        )
        
        self.start_button.clicked.connect(self.open_info_window)
        self.show()

    def open_info_window(self):
        self.first_half_window = Info()
        self.first_half_window.show()
        self.close()

class Info(QMainWindow):
    def __init__(self):
        super(Info,self).__init__()
        uic.loadUi("page1_5.ui",self)
        
        self.continue_2 = self.findChild(QPushButton, "continue_2")
        self.name = self.findChild(QTextEdit, "name")
        self.age = self.findChild(QSpinBox, "age")
        self.male = self.findChild(QRadioButton, "male")
        self.female = self.findChild(QRadioButton, "female")
        self.other = self.findChild(QRadioButton, "other")


        self.continue_2.setStyleSheet(
            "QPushButton {"
                "background-color: rgb(98, 98, 98);"
                "color:white;"
            "}"
            "QPushButton:hover {"
            " background-color: rgb(253, 0, 4);"
            "}"
        )

        self.continue_2.setEnabled(False)

        self.name.textChanged.connect(self.update_button_state)
        self.age.valueChanged.connect(self.update_button_state)
        self.male.toggled.connect(self.update_button_state)
        self.female.toggled.connect(self.update_button_state)
        self.other.toggled.connect(self.update_button_state)

        self.update_button_state()

        self.continue_2.clicked.connect(self.open_second_window)
        self.show()

    def update_button_state(self):
        self.name_text = self.name.toPlainText().strip()
        self.age_text = self.age.value()
        self.gender_selected = self.male.isChecked() or self.female.isChecked() or self.other.isChecked()

        self.continue_2.setEnabled(bool(self.name_text) and bool(self.age_text) and self.gender_selected)
          
    def open_second_window(self):
        self.second_window = Start(self.name_text)
        self.second_window.show()
        self.close()

class Start(QMainWindow):
    def __init__(self,name_text):
        super(Start,self).__init__()
        uic.loadUi("page2.ui",self)

        self.setWindowTitle("GAME")

        self.player_name = name_text.upper()
        self.player.setText(f"{self.player_name}")

        self.player = self.findChild(QLabel, "player")
        self.computer = self.findChild(QLabel, "computer")
        self.display = self.findChild(QLabel, "display")
        self.p_score = self.findChild(QLabel, "p_score")
        self.c_score = self.findChild(QLabel, "c_score")
        self.rock = self.findChild(QPushButton, "rock")
        self.paper = self.findChild(QPushButton, "paper")
        self.scissor = self.findChild(QPushButton, "scissor")

        buttons_style = """
            QPushButton {
                color:white;
                background-color: rgb(131, 131, 131);
            }
            QPushButton:hover {
                background-color: rgb(36, 120, 156);
            }
        """
        self.rock.setStyleSheet(buttons_style)
        self.paper.setStyleSheet(buttons_style)
        self.scissor.setStyleSheet(buttons_style)

        self.rock.clicked.connect(lambda: self.player_choice("ROCK"))
        self.paper.clicked.connect(lambda: self.player_choice("PAPER"))
        self.scissor.clicked.connect(lambda: self.player_choice("SCISSOR"))

        self.player_score = 0
        self.comp_score = 0
        self.rounds = 5
        self.display.setText(f"{self.player_name}, select your choice")  
      
        self.delay_timer = QTimer(self)
        self.delay_timer.timeout.connect(self.play_round) 
        self.delay_timer.setSingleShot(True)

        self.end_timer = QTimer(self)
        self.end_timer.timeout.connect(self.open_third_window)
        self.end_timer.setSingleShot(True)

        self.show()

    def player_choice(self, ans):
        self.answer = ans
        self.player.setText(self.answer)
        
        self.list = ["ROCK", "PAPER", "SCISSOR"]
        self.c_answer = random.choice(self.list)
        self.computer.setText(self.c_answer)

        if (self.answer == "ROCK" and self.c_answer == "PAPER") or (self.answer == "PAPER" and self.c_answer == "SCISSOR") or (self.answer == "SCISSOR" and self.c_answer == "ROCK"):
            self.display.setText("10 points to Computer")
            self.comp_score+=10
            self.c_score.setText(f"Score: {self.comp_score}")
            self.rounds-=1
        elif self.answer == self.c_answer:
            self.display.setText("Draw")
            if (self.comp_score and self.player_score)>0:
                self.comp_score-=5
                self.player_score-=5
                self.p_score.setText(f"Score: {self.player_score}")
                self.c_score.setText(f"Score: {self.comp_score}")
        else:
            self.display.setText(f"10 points to {self.player_name}")
            self.player_score+=10
            self.p_score.setText(f"Score: {self.player_score}")
            self.rounds-=1

        self.rock.setEnabled(False)
        self.paper.setEnabled(False)
        self.scissor.setEnabled(False)

        self.delay_timer.start(2000)
         
    def play_round(self):
        if self.rounds > 0:
            self.display.setText(f"{self.player_name}, select your choice")
            self.player.setText(f"{self.player_name}")
            self.computer.setText("Computer")

            self.rock.setEnabled(True)
            self.paper.setEnabled(True)
            self.scissor.setEnabled(True)
        else:
            self.display.setText("Game Over!")
            self.rock.setEnabled(False)
            self.paper.setEnabled(False)
            self.scissor.setEnabled(False)

            self.end_timer.start(2000)         

    def open_third_window(self):
        self.third_window = Result(self)
        self.third_window.show()
        self.close()

class Result(QMainWindow):
    def __init__(self,second_win):
        super(Result,self).__init__()
        uic.loadUi("page3.ui",self)

        self.inherit_second_window = second_win  #composing the second class so that i can use its attritubes, as the inheritance is not accessable
        
        self.setWindowTitle("RESULT")

        self.win = self.findChild(QLabel, "win")
        self.win_score = self.findChild(QLabel, "win_score")
        self.play_again = self.findChild(QPushButton, "play_again")
        self.highscore_button = self.findChild(QPushButton, "highscore_button")
        self.exit = self.findChild(QPushButton, "exit")

        style = """  
            QPushButton {
                background-color: rgb(98, 98, 98);
                color:white;
            }
            QPushButton:hover {
             background-color: rgb(253, 0, 4);
            }
        """
        self.play_again.setStyleSheet(style)
        self.highscore_button.setStyleSheet(style)
        self.exit.setStyleSheet(style)
        
        self.high_scores = {}

        if self.inherit_second_window.comp_score > self.inherit_second_window.player_score:
            self.win.setText("Computer Wins")
            self.win_score.setText(f"Total Score: {self.inherit_second_window.comp_score}")
        else:
            self.win.setText(f"{self.inherit_second_window.player_name} Wins")
            self.win_score.setText(f"Total Score: {self.inherit_second_window.player_score}")

        self.add_high_score()

        self.play_again.clicked.connect(self.back_to_game)
        self.highscore_button.clicked.connect(self.open_highscore_window)
        self.exit.clicked.connect(self.exit_game)

        self.show()

    def back_to_game(self):
        self.first_half_window = Info()
        self.first_half_window.show()
        self.close()
    
    def open_highscore_window(self):
        self.load_high_scores()
        self.highscore_window = High(self.high_scores)
        self.highscore_window.show()

    def exit_game(self):
        self.close()
        
    def load_high_scores(self):
        try:
            with open("high_scores.json", 'r') as file:
                self.high_scores = json.load(file)
        except FileNotFoundError:
            # Handle file not found error
            print("High scores file not found. Creating a new one.")
            self.high_scores = {}

    def save_high_scores(self):
        with open("high_scores.json", 'w') as file:
            json.dump(self.high_scores, file, indent=4)

    def add_high_score(self):
        self.load_high_scores()
        self.high_scores[self.inherit_second_window.player_name] = self.inherit_second_window.player_score
        self.save_high_scores()
    
class High(QMainWindow):
    def __init__(self, high_scores):
        super(High,self).__init__()
        uic.loadUi("top5_highscore.ui",self)
 
        self.exitt = self.findChild(QPushButton, "exit")
        self.score_labels = [
            self.findChild(QLabel, f"score_{i+1}") for i in range(5)
        ]
        
        self.exitt.setStyleSheet(
            "QPushButton {"
                "background-color: rgb(98, 98, 98);"
                "color:white;"
            "}"
            "QPushButton:hover {"
            " background-color: rgb(253, 0, 4);"
            "}"
        )

        self.exitt.clicked.connect(self.exit_game)
       
        self.high_scores = high_scores
        self.update_scores()
        self.show()

    def update_scores(self):
        top_scores = self.get_top_5_scores()
        for label, (name, score) in zip(self.score_labels, top_scores):
            label.setText(f"{name}: {score}")

    def get_top_5_scores(self):
        sorted_scores = sorted(self.high_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:5]

    def exit_game(self):
        self.close()

app = QApplication(sys.argv)
window = Game()
app.exec_()