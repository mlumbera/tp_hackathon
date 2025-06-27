import pyttsx3
import threading
import time
from typing import Optional, Dict, Any

class ScreenReader:
	"""
	Provides screen reader compatibility for LLM responses
	Handles text-to-speech with configurable voice settings
	"""
	
	def __init__(self, voice_rate: int = 150, voice_volume: float = 0.9):
		"""
		Initialize the screen reader with voice settings
		
		Args:
			voice_rate: Speech rate (words per minute)
			voice_volume: Volume level (0.0 to 1.0)
		"""
		self.engine = pyttsx3.init()
		self.voice_rate = voice_rate
		self.voice_volume = voice_volume
		self.is_speaking = False
		self.current_thread = None
		
		# Configure voice settings
		self._configure_voice()
	
	def _configure_voice(self):
		"""Configure the text-to-speech engine with optimal settings"""
		self.engine.setProperty('rate', self.voice_rate)
		self.engine.setProperty('volume', self.voice_volume)
		
		voices = self.engine.getProperty('voices')
		self.engine.setProperty('voice', 'com.apple.eloquence.en-US.Reed')
	
	def speak_response(self, text: str, interrupt: bool = True) -> None:
		"""
		Speak the LLM response using text-to-speech
		
		Args:
			text: The text response to speak
			interrupt: Whether to interrupt current speech
		"""
		if not text or text.strip() == "":
			return
		
		# Stop current speech if interrupting
		if interrupt and self.is_speaking:
			self.stop_speaking()
		
		# Speak in a separate thread to avoid blocking
		self.current_thread = threading.Thread(target=self._speak_text, args=(text,))
		self.current_thread.daemon = True
		self.current_thread.start()
	
	def _speak_text(self, text: str) -> None:
		"""
		Internal method to speak text (runs in separate thread)
		
		Args:
			text: The text to speak
		"""
		try:
			self.is_speaking = True
			self.engine.say(text)
			self.engine.runAndWait()
		except Exception as e:
			print(f"Screen reader error: {e}")
		finally:
			self.is_speaking = False
	
	def stop_speaking(self) -> None:
		"""Stop current speech playback"""
		if self.is_speaking:
			self.engine.stop()
			self.is_speaking = False
	
	def pause_speaking(self) -> None:
		"""Pause current speech (if supported by engine)"""
		# Note: pyttsx3 doesn't support pause/resume directly
		# This is a placeholder for future implementation
		pass
	
	def resume_speaking(self) -> None:
		"""Resume paused speech (if supported by engine)"""
		# Note: pyttsx3 doesn't support pause/resume directly
		# This is a placeholder for future implementation
		pass
	
	def change_voice_settings(self, rate: Optional[int] = None, volume: Optional[float] = None) -> None:
		"""
		Change voice settings dynamically
		
		Args:
			rate: New speech rate (words per minute)
			volume: New volume level (0.0 to 1.0)
		"""
		if rate is not None:
			self.voice_rate = rate
			self.engine.setProperty('rate', rate)
		
		if volume is not None:
			self.voice_volume = volume
			self.engine.setProperty('volume', volume)
	
	def get_available_voices(self) -> list:
		"""
		Get list of available voices
		
		Returns:
			List of voice information dictionaries
		"""
		voices = self.engine.getProperty('voices')
		voice_info = []
		
		for voice in voices:
			voice_info.append({
				'id': voice.id,
				'name': voice.name,
				'languages': voice.languages,
				'gender': voice.gender,
				'age': voice.age
			})
		
		return voice_info
	
	def set_voice(self, voice_id: str) -> bool:
		"""
		Set a specific voice by ID
		
		Args:
			voice_id: The voice ID to set
			
		Returns:
			True if voice was set successfully, False otherwise
		"""
		try:
			self.engine.setProperty('voice', voice_id)
			return True
		except Exception as e:
			print(f"Error setting voice: {e}")
			return False
	
	def speak_llm_response(self, response: str, announce_type: str = "Recipe Response") -> None:
		"""
		Speak LLM response with accessibility announcement
		
		Args:
			response: The LLM response text
			announce_type: Type of response for context
		"""
		# Add context for screen reader users
		announcement = f"{announce_type}. {response}"
		self.speak_response(announcement)
	
	def cleanup(self) -> None:
		"""Clean up resources when done"""
		self.stop_speaking()
		if hasattr(self.engine, 'destroy'):
			self.engine.destroy()


# Example usage and integration functions
def create_screen_reader() -> ScreenReader:
	"""
	Create and configure a screen reader instance
	
	Returns:
		Configured ScreenReader instance
	"""
	return ScreenReader(voice_rate=150, voice_volume=0.9)


def speak_recipe_response(response: str, screen_reader: Optional[ScreenReader] = None) -> None:
	"""
	Speak a recipe response with proper accessibility
	
	Args:
		response: The recipe response from LLM
		screen_reader: Optional ScreenReader instance, creates new one if None
	"""
	if screen_reader is None:
		screen_reader = create_screen_reader()
	
	screen_reader.speak_llm_response(response, "Recipe Response")


# Integration example for chatgpt.py
def integrate_with_llm_response(llm_response: str) -> None:
	"""
	Example integration function to be called after LLM responds
	
	Args:
		llm_response: The response from the LLM
	"""
	screen_reader = create_screen_reader()
	speak_recipe_response(llm_response, screen_reader)


if __name__ == "__main__":
	# Test the screen reader functionality
	screen_reader = create_screen_reader()
	
	# Test with sample recipe response
	test_response = "Here's a delicious Indiana-inspired corn and tomato chicken recipe. You'll need 2 cups of fresh corn, 4 ripe tomatoes, and 2 chicken breasts. First, season the chicken with salt and pepper. Then, grill the chicken for 6 minutes per side. Next, sauté the corn and tomatoes in olive oil for 5 minutes. Finally, serve the chicken with the corn and tomato mixture on top."
	
	print("Testing screen reader functionality...")
	print("Available voices:")
	for voice in screen_reader.get_available_voices():
		print(f"  - {voice['name']} ({voice['id']})")
	
	print(f"\nSpeaking test response...")
	screen_reader.speak_llm_response(test_response, "Test Recipe")
	
	# Wait for speech to complete
	time.sleep(2)
	screen_reader.cleanup()
	print("Screen reader test completed.") 