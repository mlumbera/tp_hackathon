import speech_recognition as sr

def voice_input():
	"""
	Captures voice input from microphone and converts to text
	Returns the transcribed text or None if failed
	"""
	recognizer = sr.Recognizer()
	
	# Use default microphone
	with sr.Microphone() as source:
		print("Listening... Speak now!")
		
		# Adjust for ambient noise
		recognizer.adjust_for_ambient_noise(source, duration=0.5)
		
		try:
			# Listen for audio input
			audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
			print("Processing speech...")
			
			# Convert speech to text using Google's speech recognition
			text = recognizer.recognize_google(audio)
			print(f"You said: {text}")
			return text
			
		except sr.WaitTimeoutError:
			print("No speech detected within timeout period")
			return None
		except sr.UnknownValueError:
			print("Could not understand the audio")
			return None
		except sr.RequestError as e:
			print(f"Could not request results; {e}")
			return None 