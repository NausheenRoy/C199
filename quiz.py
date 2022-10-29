import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []

questions = [
    'What is the Italian word for PIE? \n a.Mozeralla\n b.Pastry\n c.Patty\n d.Pizza',
    'Water boils at 212 units at which scale? \n a.Fahrenheit\n b.Celcius\n c.Rankine\n d.Kelvin'
]
answers = ['d', 'a']

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer


def clientthread(conn):
    score = 0
    conn.send('Welcome to this quiz game!'.encode('utf-8'))
    conn.send('You will receive a question and you have to answer it from a,b,c,d'.encode('utf-8'))
    conn.send('Good luck\n\n'.encode('utf-8'))
    index, question, answers = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answers:
                    score+=1
                    conn.send(f'Bravo! Your score is {score}\n\n'.encode('utf-8'))
                else:
                    conn.send('Incorrect answer!Better luck next time\n\n'.encode('utf-8'))
                remove_question(index)
                index, question, answers = get_random_question_answer
            else:
                remove(conn)
        except:
            continue

def remove_question(index):
    questions.pop(index)
    answers.pop(index)
