# pronounce_text.py

import azure.cognitiveservices.speech as speechsdk
from speech_translator import authWithBearer
from dotenv import load_dotenv

load_dotenv()

def pronounce_text(text):
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = authWithBearer()
    service_region = os.getenv('REGION')
    speech_config = speechsdk.SpeechConfig(auth_token=speech_key, region=service_region)

    # Set the voice name, refer to https://aka.ms/speech/voices/neural for the full list.
    speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesizes the received text to speech.
    result = speech_synthesizer.speak_text_async(text).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")

# Example usage
if __name__ == "__main__":
    example_text = "Hello, this is an example text to be pronounced."
    pronounce_text(example_text)