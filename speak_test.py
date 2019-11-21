from subprocess import call
file = open('Audio.txt', 'r')
text = file.read().strip()
file.close()
speech = text
print(speech)
call(["espeak \"Hello Wolrd World\" --stdout |aplay"])

