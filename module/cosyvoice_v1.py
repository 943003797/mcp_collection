import os
import dashscope
from dotenv import load_dotenv
from dashscope.audio.tts_v2 import VoiceEnrollmentService, SpeechSynthesizer
from dashscope.audio.tts_v2.speech_synthesizer import json
load_dotenv()

class Cosyvoice:
    
    @staticmethod
    def generate_audio(text: str, out_path) -> str:
        dashscope.api_key = os.getenv("ALI_KEY")
        target_model = "cosyvoice-v1"
        voice_id = "cosyvoice-prefix-4eec46a3b5d8499a8c29c46766452a63"
        synthesizer = SpeechSynthesizer(model=target_model, voice=voice_id)
        audio_result = synthesizer.call(str(text))
        try:
            with open(out_path, "wb") as f:
                if audio_result is not None:
                    f.write(audio_result)
                else:
                    raise Exception("Geneal audio faild")
            return "Success"
        except Exception as e:
            return "Failed"