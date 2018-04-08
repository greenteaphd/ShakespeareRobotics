# Andy Han, Joweina Hsiao, and Nikhil Smith

charactersFull = ["Claudius","Hamlet","Polonius","Horatio","Laertes","Voltemand","Cornelius","Rosencrantz",
                  "Guildenstern","Osric","Gentleman","Priest","Marcellus","Bernardo","Francisco","Reynaldo",
                  "Players", "Two Clowns", "Fortinbras", "Norwegian Captain", "English Ambassador", "Gertrude",
                  "Ophelia","Ghost of Hamlet's Father","Lord","Lady","Officer","Solider","Sailor","Messenger","Attendant"]

charactersShort = ["King","Ham.","Pol.","Hor.","Laer.","Volt.","Cor.","Ros.","Guil.","Osr.","Gent.","Priest.",
                   "Mar.","Ber.","Fran.","Rey.","1. Play.", "Clown.", "Fort.","Capt.","Ambassador.","Queen.","Oph.",
                   "Ghost.","Lord.","","","","Sailor.","Mess.","Servant."]

def countLineNumbers(fileName):
    with open(fileName) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

totalLineNumbers = countLineNumbers("Hamlet.txt")

def respond(inputText, character):
    if len(inputText) == 0:
        return "" #say nothing
    else:
        file = open("Hamlet.txt", "r")
        oneLine = file.readline()
        print (oneLine)

#respond("a", "character")

count = 0
file = open("Hamlet.txt", "r")
prevLine = 0
for line in file:
    count += 1
    if "Who's there?" in line:
        prevLine = count
    if (prevLine != 0) and ((prevLine + 1) == count):
        print(line)
        break