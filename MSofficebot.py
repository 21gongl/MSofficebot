from nltk.chat.util import Chat, reflections
import re
import random

# === This is the extension code for the NLTK library ===
#        === You dont have to understand it ===

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

    def converse(self, quit="bye"):
        user_input = ""
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

lunch_time = {
    "not wednesday": ["11:00", "11:40"], 
    "wednesday": ["13:35", "14:20"]
    }

teachers_room_number = {
    "Mr. Barrett":[],
    "Ms. Bechdolt":[],
    "Mr. Berntson":[],
    "Ms. Beyers":[],
    "Mr. Campbell":[],
    "Mr. Celinski":[],
    "Mr. Chisholm":[],
    "Mr. Dachpian":[],
    "Ms. Deo":[],
    "Ms. Doering":[],
    "Ms. Doiron":[],
    "Ms. Galek":[],
    "Mr. Gaspersich":[],
    "Mr. Hanners":[],
    "Ms. Hay":[],
    "Ms. Hemerka":[],
    "Mr. Hodin":[],
    "Ms. Jordan":[],
    "Mr. Julien":[],
    "Ms. Kielczewska":[],
    "Ms. Kililea":[],
    "Mr. Kryger":[],
    "Ms. Linehan":[],
    "Ms. Lyons":[],
    

}
pairs = [
    [
        r'(.*)(add|put)( )(.*)( )(on|to)(.*)', 
        [lambda matches: 'Noted!' if add_to_list(matches[3]) else '%3 is already on the list!']
    ],
    [
        r'What is on the list?',
        [lambda matches: ','.join(shopping_list)],
    ],
  	[
      	r'(.*)(when|what time)(.*)(schoolbus|bus)(leave)?',
      	['Buses leave at {0}.'.format(school_bus_time)]
    ],
  	[
      	r'(.*)(where)(.*)(MS Lost and Found)?',
      	['MS Lost and Found is next to the MS Office.']
    ],
  	[
      	r"(.*)(why can't I use my phone)",
      	["You can't use your phone because it may distract you from learning."]
    ],
    [
        r'(.*)(when|what time)(.*)(lunch)(.*)(monday|tuesday|thursday|friday)', 
        ['Lunch is between {0}.'.format(lunch_time["not wednesday"])]
    ],
    [
        r'(.*)(when|what time)(.*)(lunch)(.*)(wednesday)', 
        ['Lunch is between {0} on Wednesdays.'.format(lunch_time["wednesday"])]
    ],
  	[
      	r"(.*)(when|what time)(.*)(lunch)",
      	['Lunch is between {0}.'.format(lunch_time["not wednesday"])]
    ],
    [
        r'(.*)(how)(.*)(quit)(.*)',
        ["To quit, you simply enter the word 'bye'."]
    ],
    [
        r'(.*)(thanks|thank you|thx)',
        ["You're welcome!"]
    ],
  	[
        r'(.*)',
        ["Okay. "],
    ]
]

if __name__ == "__main__":
    name = "MSofficeBot"
    print("Hi, I am {0}.".format(name))
    username = input("What's your name?")
    print("Okay, so your name is {0}.".format(username))
    print("{0}, what questions do you have?".format(username))
    chat = ContextChat(pairs, reflections)
    chat.converse()
