import os
from gtts import gTTS
from dotenv import load_dotenv
from tqdm import tqdm
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model only once
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Enhanced prompt for better quality
def generate_motivation(goal, day, name):
    prompt = f"""
You are a motivational AI coach and storyteller. Write an engaging and emotionally supportive audio script for **Day {day}** of a **10-day motivational journey**.

### Context:
- The user's goal is: "{goal}"
- The user's name is: {name}
- Your tone should be inspiring, personal, and positive.
- If Day > 1, reference the previous day's progress with a brief recap.
- End with a teaser or motivation to look forward to Day {day + 1}.
- Include an actionable tip or mindset shift.

### Constraints:
- Length: Around 100–150 words.
- Use simple, conversational English.
- Do not repeat the same lines across days.
"""
    try:
        response = model.generate_content(prompt, generation_config={"temperature": 0.9})
        return response.text.strip()
    except Exception as e:
        print(f"❌ Error generating text for Day {day}: {e}")
        return "Hi! I'm sorry, something went wrong with generating your message today."

# Convert text to voice
def convert_to_voice(text, filename):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
    except Exception as e:
        print(f"❌ Error generating audio for {filename}: {e}")

# Generate motivational journey
def generate_10_day_journey(goal, name):
    os.makedirs("motivation_audio", exist_ok=True)
    log_file = open("motivation_audio/generated_scripts.txt", "w", encoding="utf-8")

    for day in tqdm(range(1, 11), desc="Generating Journey", ncols=100):
        time.sleep(1)  # gentle delay to avoid API rate issues
        print(f"\n🎧 Generating content for Day {day}...")
        text = generate_motivation(goal, day, name)
        
        log_file.write(f"\n--- Day {day} ---\n{text}\n")
        
        voice_path = f"motivation_audio/day{day}_motivational.mp3"
        convert_to_voice(text, voice_path)
        print(f"✅ Saved: {voice_path}")

    log_file.close()
    print("\n🎉 All 10 motivational audios are generated!")

# Entry point
if __name__ == "__main__":
    user_goal = input("💡 Enter your goal: ")
    user_name = input("🙋 Enter your name: ")
    generate_10_day_journey(user_goal.strip(), user_name.strip())
