import whisper
import os
import ollama

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
model = whisper.load_model("small", device="cpu")
filename = "/home/raulpuscas/Downloads/test3.ogg";

def transcribe_audio(selected_file: str):
    result = model.transcribe(selected_file)
    return result['text']

def extract_medical_context(text: str):
    prompt = (
        "You are a medical scribe. Your task is to extract all medically relevant information from the transcript below.\n\n"
        "Focus on:\n"
        "- Diagnoses\n"
        "- Findings\n"
        "- Measurements\n"
        "- Clinical impressions\n"
        "- Anatomical references\n"
        "- Procedures\n\n"
        "Do not include any formatting, categories, or explanations. Simply list the extracted terms and phrases line by line, as plain text.\n"
        "Avoid any additional comments or reasoning.\n\n"
        f"Transcript:\n{text}\n\n"
        "Extracted medical content:"
    )

    response = ollama.chat(
        model='llama3-chatqa',
        messages=[{
            'role': 'user',
            'content': prompt
        }]
    )
    return response['message']['content']

def process_audio(selected_file: str):
    transcription = transcribe_audio(selected_file)
    medical_content = extract_medical_context(transcription)
    return medical_content

print(process_audio(filename));
