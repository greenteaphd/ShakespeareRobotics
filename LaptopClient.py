# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 8th, 2018

# Import statements
import socket
import speech_recognition as sr
import string

FILE_NAME = "WorkProblems.txt"
#FILE_NAME = "Hamlet.txt"


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

# TO DO: add comment
def maxAndMinLines(fileName):
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

# TO DO: add comment
def processHumanSpeech(speech, maxLength, minLength):
    processedSpeech = speech
    if len(speech) >= maxLength/2:
        if FILE_NAME == "Hamlet.txt":
            processedSpeech = speech[-(minLength + 10):]
        else:
            processedSpeech = speech[-minLength:]
    if speech[-1:] == " ":
        processedSpeech = speech[0:len(speech) - 1]
    return processedSpeech

# TO DO: add comment
def postProcessHumanSpeech(speech):
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
# while the laptop is in charge of sending that data to the robot.
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


