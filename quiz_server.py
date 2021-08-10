import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nickname= []

print("Server has started...")

questions = [
    "Who created the character Mowgli? \n a.Rudyard Kipling\n b.Charles Dickens\n c.Thomas Hardy",
    "The term Grand Slam is used in which sport? \n a.Golf\n b.Rugby\n c.Tennis",
    "What is the APJ in Dr.APJ Abdul Kalam's name? \n a.Avul Pakir Jainulabdin\n b.Ashraf Pakir Jainulabdin\n c.Aziruddin Pakir Jainulabdin",
    "Who invented gramaphone? \n a.Lee De Forest\n b.Thomas Alva Edison\n c.Alexanderson",
    "Who was the founder of The low of gravitation? \n a.Sir Issac Newton\n b.Galileo\n c.Charles Boyle",
    "What is the approximate playing time of our National Antem? \n a.52 seconds\n b.30 second\n c.2 minute",
    "When I say Wimbledon Trophy,I am talking of which sport? \n a.Golf\n b.Football\n c.Tennis",
    "Name the first woman Chief Minister of India? \n a.Sucheta Kriplani\n b.Indira Gandhi\n c.Sarojini Naidu",
]
answer = ['a','c','a','b','a','a','c','a']

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    message = "{} joined!".format(nickname)
    print(message)
    new_thread = Thread(target= clientthread,args=(conn, nickname))
    new_thread.start()

    def clientthread(conn):
     score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("you will recieve a question.the answer to that question should be a,b,c\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index,questions,answer = get_random_questions_answer(conn)
    while True:
      try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send("Bravo! that was the right answer,Your score is {score}\n\n".encode('utf-8'))
                else:
                     conn.send("Incorrect answer! Wish you Best Luck for next time\n\n".encode('utf-8'))
                remove_questions(index)
                index,questions,answer = get_random_questions_answer(conn)
            else:
                 remove(conn)
                 remove(nickname)
      except:
             continue

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

def remove_questions(index):
    questions.pop(index)
    answer.pop(index)

def get_random_questions_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_questions = questions[random_index]
    random_answers = answer[random_index]
    conn.send(random_questions.encode('utf-8'))
    return random_index, random_questions, random_answers