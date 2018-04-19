# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 8th, 2019

# Import statements
import socket
import speech_recognition as sr


def google_speech():
    """ Function that handles the transcription of audio into text via Google Speech API """
    # Reading in the Google API key
    with open("api-key-andy.json") as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something!")
        audio = r.listen(source)

    human_input = ""

    # Speech recognition using Google Speech Recognition
    try:
        human_input = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print("You said: " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if len(human_input) > 0:
        pass
    else:
        human_input = "Try again"

    print("The API picked up: " + human_input)
    return human_input


def client_main(server_address):
    """ This method takes in a server address in order to send data to the server. """
    data = google_speech()
    data = data.encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, 7000))
    s.sendall(data)
    print("SUCCESS! HOUSTON, WE HAVE CONTACT.")
    s.close()
    return

if __name__ == "__main__":
    client_main("169.254.85.238")
