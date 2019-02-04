from nltk.chat.util import Chat, reflections
import re
import random
import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta

# === This is the extension code for the NLTK library ===

class ContextChat(Chat):
    def respond(self, str):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response

                if callable(resp):
                    resp = resp(match.groups())
                
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num + 1)) + \
                response[pos+2:]
            pos = response.find('%')
        return response

    def converse(self, quit="quit"):
        user_input = ""
        user_speech = []
        user_speech.append(user_input)
        while user_input != quit:
            user_input = quit
            try: user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.": user_input = user_input[:-1]    
                print(self.respond(user_input))

# === Your code should go here ===

school_bus_time = ["3:45", "4:30", "5:30"]

lunchtime = {
    "not wednesday": ["11:00", "11:40"], 
    "wednesday": ["13:35", "14:20"]
    }

teacher_rooms = {
    "Jonica Asteros":"H214b" ,
    "Michael Barrett":"M123" ,
    "Carl Beach":"H005" ,
    "Kathryn Bechdolt":"AA104" ,
    "David Berntson":"M019" ,
    "Laura Berntson":"H004" ,
    "Cathy Beyers":"H101" ,
    "Gosia Gebert-Bielska": "M001" ,
    "Adam Campbell":"C154" ,
    "Chris Celinski":"AA103" ,
    "Cecelia Cienska":"A004" ,
    "Brent Chisholm":"AA007b" ,
    "Shayne Cokerdem":"C106" ,
    "Diane Cokerdem-DePriest":"H113" ,
    "Gina Cuthbert":"H007b" ,
    "Jason Cuthbert":"A003" ,
    "Angela Dachpian":"H214b" ,
    "David Dachpian":"H015" ,
    "Patricia Deo":"M012" ,
    "Suzanne Doering":"H013" ,
    "Janice Doiron":"M013" ,
    "Marilyn Dypczynski":"E045" ,
    "Tamara Fernandez": "AA118" ,
    "Joanna Galek":"C152" ,
    "Adam Gasiejewski":"H122" ,
    "Mark Gaspersich":"M112" ,
    "Kevin Hanners":"M122" ,
    "Nickie Hansen":"H111" ,
    "Tiffany Hay":"M116" ,
    "Ruth Hemerka":"M111" ,
    "Erin Herold":"M115" ,
    "Patricia Hermes":"H014" ,
    "Lee Hodin":"H211, H212, H112",
    "Malgorzata Hydzik": "H015",
    "Alan James":"C105",
    "Joanna Jaroslawska-Luft":"C102",
    "Carol Jordan":"A002",
    "Jenn Jordan":"AA119",
    "Doug Julien":"C161",
    "Agnieszka Kielcz":"H213",
    "Agata Kielczewska":"M002" ,
    "Caroline Kililea":"M115" ,
    "Betsy Kirkpatrick": "H211" ,
    "Aleksandra Kucinska": "M003" ,
    "Hania Kula": "M003" ,
    "Bart Kryger": "M004" ,
    "Wiola Leszczynska": "M003" ,
    "Samantha Linehan": "M022" ,
    "Melissa Lyons": "AA003" ,
    "Julie MacKay": "AA007D" ,
    "Bill MacKenty": "H121" ,
    "Richard Martens": "M121" ,
    "Lada Martens-Bensova": "C161" ,
    "Jaime Martinez": "H115" ,
    "Stewart Merritt": "H212" ,
    "Thomas Merritt": "AA1005" ,
    "Stephen Miele": "C153" ,
    "Anna Milewska": "H002" ,
    "Maria Milewska": "H007" ,
    "Tim Munnerlyn": "H007c" ,
    "Valerie Navarro": "AA107" ,
    "Michael Nieman": "A002" ,
    "Joanna Olczak": "H202" ,
    "Nicolas Pavlos": "C105" ,
    "Lucy Pawlik": "M115" ,
    "Jon Pitale": "H124" ,
    "Laura Pitale": "H114" ,                   
    "Pawel Ptak": "AA007b" ,
    "Tami Ranado": "H023" ,
    "Amber Russel": "M023, C154" ,
    "Benjamin Schlief": "AA007b and all gyms" ,
    "Lourdes Segurado": "M011" ,
    "Irene Sendra": "C122" ,
    "Solomon Senrick": "M114" ,
    "Michael Sheehan": "H002" ,
    "Kristin Sheehan": "M014" ,
    "Joey Shousky": "H112" ,                   
    "Stephen Sidaway": "A003" ,
    "Noel Simon": "H214a" ,                   
    "Rachella Simon": "C123" , 
    "Josh Skjold": "H021" ,
    "Iza Skoczylas": "M005" , 
    "Marcin Skoczylas": "H214a" ,
    "Ewa Smutek-Rusek": "C162" ,
    "Carla Staffa": "C122" ,
    "David Stein": "C107" ,
    "Katie Stein": "AA106" ,
    "David Stutz": "M021" ,
    "Christopher Taylor": "H024" ,                   
    "Elizabeth Swanson": "H101" ,
    "Bolek Szuter": "E048-2" ,
    "Monika Wieczorkiewicz": "H112" ,                   
    "Kasia Wodnicka": "H002" ,
    "Steven Wood": "C161" ,
    "James Wyatt": "H022"                    
} #source: Ms.Gosia from MS office

def find_teacher_room(teacher):
    return teacher_rooms[teacher]

today = datetime.now()
today_date = today.strftime('%Y-%m-%d %A')
str_today_date = str(today_date)

def find_lunchtime(today):
    today_weekday = today.strftime('%A')
    if today_weekday == "Wednesday":
        today_lunchtime = lunchtime.get("wednesday")
    else:
        today_lunchtime = lunchtime.get("not wednesday")
    return today_lunchtime

def find_rotation_day(date):
    start = datetime.strptime('2018-01-28', '%Y-%m-%d')
    end = today
    daydiff = end.weekday() - start.weekday()
    days = ((end-start).days - daydiff) / 7 * 5 + min(daydiff,5) - (max(end.weekday() - 4, 0) % 5) #source: StockOverflow
    if days % 4 == 0:
        rotation_day = "Day C"
    elif days % 4 == 1:
        rotation_day = "Day D"
    elif days % 4 == 2:
        rotation_day = "Day A"
    elif days % 4 == 3:
        rotation_day = "Day B"
    today_day = str_today_date + " " + rotation_day + "."
    return today_day

if __name__ == "__main__":
    name = "MSofficeBot"
    print("Hi, I am {0}.".format(name))
    username = input("What's your name? ")
    print("Okay, so your name is {0}.".format(username))
    
    user_feeling = input("How are you today? ")
    if user_feeling == "good":
        print("I'm glad.")
    elif user_feeling == "great":
        print("Cool!")
    elif user_feeling == "bad":
        event = input("That's not good! What happened? ")
        print("That's very unfortunate, I hope it gets better!")
    else:
        print("Well, I hope you'll have a great day.")

    print("So {0}, what questions do you have?".format(username))

    pairs = [
    [
      	r'(when)(.*)(schoolbus|bus)(leave)?',
      	['Buses leave at {0}.'.format(school_bus_time)]
    ],
    [
        r'(when)(.*)(lunch)(.*)(monday|tuesday|thursday|friday?)', 
        ['Lunch is between {0}.'.format(lunchtime["not wednesday"])]
    ],
    [
        r'(when)(.*)(lunch)(.*)(wednesday?)', 
        ['Lunch is between {0} on Wednesdays.'.format(lunchtime["wednesday"])]
    ],
    [
      	r'(when)(.*)(lunch?)',
        [lambda matches: "Lunch is between " + str(find_lunchtime(today))]
    ],
    [
        r'(where is)(.*)(room?)',
        [lambda matches: "It is in " + str( find_teacher_room(matches[1].strip()) )] #credits: Michał
    ],
    [
        r'(what day is it?)',
        [lambda matches: "Today is " + str(find_rotation_day(today))]
    ],
    [
      	r'(where is MS Lost and Found?)',
      	['MS Lost and Found is next to the MS Office.']
    ],
    [
      	r"(why can't I use my phone?)",
      	["You can't use your phone because it may distract you from learning."]
    ],
    [
        r'(how do I quit?)',
        ["To quit, you simply enter the word 'quit'."]
    ],
    [
        r'(how are you?)',
        ["Fine, thank you! And I know you are feeling {0}.".format(user_feeling)]
    ],
    [
        r'(hi)',
        ["Hi!"]
    ],
    [
        r'(hello)',
        ["Hello."]
    ],
    [
        r'(.*)(thanks|thank you|thx)(.*)',
        ["You're welcome, {0}.".format(username)]
    ],
    [
        r'(quit)',
        ["Bye!"]
    ],
  	[
        r'(.*)',
        ["Maybe you should try to rephrase your question."],
    ]
]
    chat = ContextChat(pairs, reflections)
    chat.converse()
