import os
import azure.cognitiveservices.speech as speechsdk
import requests,json
from dotenv import load_dotenv

load_dotenv()

def authWithBearer():
    resourceID = os.getenv("RESOURCE_ID")
    url = os.getenv('LOGIN_URL')
    
    payload = f"{'grant_type=client_credentials&client_id='}{os.getenv('clientID')}{'&client_secret='}{os.getenv('secret')}{'&resource=https%3A%2F%2Fcognitiveservices.%azure.com%2F'}"
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
    iason = json.loads(response.text)
    bearer = iason["access_token"]
    
    return 'aad#' + resourceID + '#' + bearer

def recognize_from_microphone(source_language, target_language):
    SPEECH_KEY = authWithBearer()
    resourceRegion = os.getenv("REGION")  # Change this to match your Azure Speech Service region
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(auth_token=SPEECH_KEY, region=resourceRegion)
    speech_translation_config.speech_recognition_language = source_language

    if not target_language:
        print("Please provide a target language.")
        return None

    speech_translation_config.add_target_language(target_language)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

    print("Speak into your microphone.")
    try:
        translation_recognition_result = translation_recognizer.recognize_once_async().get()

        if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
            print("Recognized: {}".format(translation_recognition_result.text))
            print("""Translated into '{}': {}""".format(
                target_language,
                translation_recognition_result.translations[target_language]))

            return translation_recognition_result.text, translation_recognition_result.translations[target_language]

        elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
        elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = translation_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
                print("Language details: source={}, target={}".format(source_language, target_language))
                print("Azure Region: {}".format(resourceRegion))
        else:
            print("Recognition failed with reason: {}".format(translation_recognition_result.reason))
            print("Language details: source={}, target={}".format(source_language, target_language))
            print("Azure Region: {}".format(resourceRegion))

    except Exception as e:
        print("An error occurred:", str(e))

    return None

if __name__ == "__main__":
    # Example usage
    source_language = "ro-RO"  # Romanian
    target_language = "it"
    result = recognize_from_microphone(source_language, target_language)

    if result is None:
        print("Recognition failed.")