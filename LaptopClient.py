# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 26th, 2018

# Import statements
import socket
import speech_recognition as sr
import string


###
# Global static variables needed for LaptopClient's main to function properly
#   FILE_NAME is a string representing the name of play
###
FILE_NAME1 = "Hamlet.txt"
FILE_NAME2 = "WorkProblems.txt"

###
# PLEASE SET UP THE CORRESPONDING STATIC VARIABLES ACCORDING TO WHATEVER PLAY YOU WANT TO WORK WITH!!
#TODO: could make this based on user input to make it prettier
###

FILE_NAME = FILE_NAME2



###
# Helper functions used to recognize and process human speech data
###

def recognizeSpeechWithAPI():
    """ Function that handles the transcription of audio into text via Google Speech API """
    # Reading in the Google API key
    with open("api-key-andy.json") as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something!")
        audio = r.listen(source)

    humanInput = ""

    # Speech recognition using Google Speech Recognition
    try:
        humanInput = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print("You said: " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # An attempt to bulletproof work done with the API
    if len(humanInput) > 0:
        pass
    else:
        humanInput = "Try again"

    return humanInput

def maxAndMinLines(fileName):
    """ maxAndMinLines() determines the maximum and minimum lengths of lines in the play overall.
    These numbers will assist processHumanSpeech() cut down the human input into something that
    the robot's respond() function can work with. """
    file = open(fileName, "r")
    lengths = []
    for currentLine in file:
        if len(currentLine) > 1:
            length = len(currentLine)
            lengths.append(length)
    maxLength = max(lengths)
    minLength = min(lengths)
    file.close()
    return maxLength, minLength

def processHumanSpeech(speech, maxLength, minLength):
    """ processHumanSpeech() cuts down the human input string if it is too long. It cuts it down
     based on the minimum length line of the play and pairs down the input to that minimum length
     from the end of the string. The lengths are different depending on the play. Additionally,
     processHumanSpeech() also gets rid of the ending whitespace that sometimes tags along with
     output from the Google Speech API."""
    processedSpeech = speech
    if len(speech) >= maxLength/2:
        if FILE_NAME == "Hamlet.txt":
            processedSpeech = speech[-(minLength + 10):]
        else:
            processedSpeech = speech[-minLength:]
    if speech[-1:] == " ":
        processedSpeech = speech[0:len(speech) - 1]
    return processedSpeech

def postProcessHumanSpeech(speech):
    """ postProcessHumanSpeech() gets rid of punctuation in the human input string. Mostly, this comes into
     play when there are contractions like "don't" in the human speech input. Otherwise, this does nothing. """
#TODO: fix this so that it only does it if it has an apostrophe in the line
    postProcessed = ""
    for char in speech:
        if char not in string.punctuation:
            postProcessed += char
    return postProcessed

###
# The following functions detail what LaptopClient as a class does. It is responsible
# for working with the Google Speech API to recognize speech, process it, and then
# send it to the robot to interpret/respond.
#
# We've established the relationship between the robot and the laptop as a server-client model.
# The robot is charge of listening to the laptop and whatever data it sends over,
# while the laptop is in charge of sending and processing that data to the robot.
###

def client_main(server_address):
    """ This method takes in a server address in order to send data to the server. """
    maxLength, minLength = maxAndMinLines(FILE_NAME)
    humanInput = recognizeSpeechWithAPI()
    processed = processHumanSpeech(humanInput, maxLength, minLength)
    postProcessed = postProcessHumanSpeech(processed)
    data = postProcessed.encode()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, 7000))
    s.sendall(data)
    print("SUCCESS! HOUSTON, WE HAVE CONTACT.")
    s.close()
    return

if __name__ == "__main__":
    client_main("169.254.85.238")


