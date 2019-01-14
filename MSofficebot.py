from nltk.chat.util import Chat, reflections
import re
import random
from teacher_room_number import teacher_room_number

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

    def converse(self, quit="quit"):
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

pairs = [
  	[
      	r'(when)(.*)(schoolbus|bus)(leave)?',
      	['Buses leave at {0}.'.format(school_bus_time)]
    ],
    [
        r'(when)(.*)(lunch)(.*)(monday|tuesday|thursday|friday)?', 
        ['Lunch is between {0}.'.format(lunch_time["not wednesday"])]
    ],
    [
        r'(when)(.*)(lunch)(.*)(wednesday)?', 
        ['Lunch is between {0} on Wednesdays.'.format(lunch_time["wednesday"])]
    ],
  	[
      	r'(when)(.*)(lunch)?',
      	['Lunch is between {0} on most days.'.format(lunch_time["not wednesday"])]
    ],
    [
        r'(how)(.*)(quit)(.*)?',
        ["To quit, you simply enter the word 'quit'."]
    ],
    [
        r'(where)(.*)( )(room)?',
        ["They are in {0}.".format(teacher_room_number.get("something"))] #instead of "something", we need to insert the teacher's name that the student inputed before "room" in their question
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
        r'(.*)(thanks|thank you|thx)(.*)',
        ["You're welcome!"]
    ],
  	[
        r'(.*)',
        ["Maybe you should try to rephrase your question."],
        ["I don't know, but Ms. Gosia may be able to answer that."]
    ],
]

if __name__ == "__main__":
    name = "MSofficeBot"
    print("Hi, I am {0}.".format(name))
    username = input("What's your name?")
    print("Okay, so your name is {0}.".format(username))
    print("{0}, what questions do you have?".format(username))
    chat = ContextChat(pairs, reflections)
    chat.converse()
