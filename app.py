# 📦 All Imports
import os
import streamlit as st
import json
from datetime import datetime, timedelta
import calendar
from gtts import gTTS
from dotenv import load_dotenv
import google.generativeai as genai
import random
from fpdf import FPDF
import base64

# 🌐 Load env variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Dark mode CSS with improved colors
dark_mode_css = """
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    [data-testid="stHeader"] {
        background-color: #1E1E1E;
    }
    [data-testid="stSidebar"] {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    .st-bq, .st-cx, .st-cd {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stToolbar"], div[data-testid="stMarkdown"] {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    .stTextInput>div>div>input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        background-color: #3B3B3B !important;
        color: white !important;
        border: 1px solid #555555 !important;
    }
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #BBBBBB !important;
    }
    .stSelectbox>div>div>div {
        background-color: #3B3B3B !important;
        color: white !important;
    }
    div[role="radiogroup"] label {
        color: white !important;
    }
    .st-emotion-cache-bkyxgn,
    .st-emotion-cache-1uixxvy {
        background-color: #FF5733 !important;
    }
    .stProgress>div>div>div {
        background-color: #FF5733 !important;
    }
    .st-emotion-cache-edgvbvh {
        border-color: #FF5733 !important;
    }
    .calendar-container {
        background-color: #2D2D2D;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #555555;
    }
    .calendar-container th {
        color: #FFFFFF;
    }
    [data-testid="stExpander"] {
        background-color: #2D2D2D;
        border: 1px solid #555555;
        color: #FFFFFF;
    }
    .notification-dropdown {
        position: relative;
        display: inline-block;
    }
    .notification-icon {
        cursor: pointer;
        padding: 5px 10px;
        background-color: #3B3B3B;
        border-radius: 5px;
        color: white;
        border: 1px solid #FF5733;
    }
    .notification-content {
        display: none;
        position: absolute;
        right: 0;
        background-color: #2D2D2D;
        min-width: 300px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
        border-radius: 5px;
        max-height: 400px;
        overflow-y: auto;
        color: white;
    }
    .show {
        display: block;
    }
</style>
"""


# Light mode CSS (default styles or minor adjustments)
light_mode_css = """
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stProgress>div>div>div {
        background-color: #FF5733;
    }
    /* Title bar styling for light mode */
    .title-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 20px;
        border: 1px solid #FF5733;
    }
    .title-container img {
        height: 40px;
    }
    .reward-points {
        background-color: #f8f9fa;
        padding: 5px 10px;
        border-radius: 10px;
        font-weight: bold;
        color: #000000;
        border: 1px solid #FF5733;
    }
    /* Calendar styling */
    .calendar-container {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    /* Notification styling */
    .notification-dropdown {
        position: relative;
        display: inline-block;
    }
    .notification-icon {
        cursor: pointer;
        padding: 5px 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        color: #333;
        border: 1px solid #FF5733;
    }
    .notification-content {
        display: none;
        position: absolute;
        right: 0;
        background-color: #ffffff;
        min-width: 300px;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        z-index: 1;
        border-radius: 5px;
        max-height: 400px;
        overflow-y: auto;
    }
    .show {
        display: block;
    }
</style>
"""

# 🎨 Set Streamlit config
st.set_page_config(page_title="AI Guru - Kuku FM", layout="centered")

# 📜 Quotes
quotes = [
    "Believe in yourself and all that you are.",
    "Every day is a new beginning.",
    "The secret of getting ahead is getting started.",
    "You are capable of amazing things.",
    "Progress is progress, no matter how small."
]

# 📂 Data load/save
try:
    with open('data/sample_episodes.json') as f:
        episodes = json.load(f)
except:
    episodes = {}

leaderboard_path = "data/leaderboard.json"
try:
    with open(leaderboard_path) as f:
        leaderboard = json.load(f)
except:
    leaderboard = {}

# 🚀 Session state init
for key in ["goal", "day", "streak", "logged_in", "username", "dark_mode", "mood", "voice", "notes", 
            "reward_points", "notifications", "last_checkin_date", "checkin_history"]:
    if key not in st.session_state:
        if key == "day":
            st.session_state[key] = 1
        elif key == "streak":
            st.session_state[key] = 0
        elif key == "dark_mode":
            st.session_state[key] = False
        elif key == "reward_points":
            st.session_state[key] = 0
        elif key == "notes":
            st.session_state[key] = []
        elif key == "notifications":
            st.session_state[key] = []
        elif key == "last_checkin_date":
            st.session_state[key] = None
        elif key == "checkin_history":
            st.session_state[key] = {}
        else:
            st.session_state[key] = None

# Display title bar with logo and rewards
def display_title_bar():
    # Determine background and text colors based on dark mode
    title_bg_color = "#2D2D2D" if st.session_state.dark_mode else "#f0f2f6"
    points_bg_color = "#3B3B3B" if st.session_state.dark_mode else "#f8f9fa"
    points_text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"
    border_color = "#FF5733"
    
    # Calculate reward points if logged in
    reward_points_display = ""
    if st.session_state.logged_in:
        # Calculate reward points
        reward_points = st.session_state.day - 1  # Day 1 has 0 points
        if reward_points < 0:
            reward_points = 0
            
        # Add bonus points if stored in session state
        if "reward_points" in st.session_state:
            reward_points += st.session_state.reward_points
            
        reward_points_display = f'<div class="reward-points">🔥 {reward_points} Points</div>'
    
    # Logo selection
    logo_html = ""
    if os.path.exists("kukufm_logo.png"):
        # We'll use a Base64 encoded image to avoid file path issues
        try:
            with open("kukufm_logo.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{encoded_string}" alt="KukuFM Logo">'
        except:
            # Fallback to text logo if file can't be read
            logo_html = '<div style="color: #FF5733; font-size: 24px; font-weight: bold;">KUKU<span style="background-color: #FF5733; color: white; padding: 2px 5px; border-radius: 4px;">FM</span></div>'
    else:
        # Fallback to text logo if file doesn't exist
        logo_html = '<div style="color: #FF5733; font-size: 24px; font-weight: bold;">KUKU<span style="background-color: #FF5733; color: white; padding: 2px 5px; border-radius: 4px;">FM</span></div>'
    
    # Title bar with variables for colors
    custom_css = f"""
    <style>
        .title-container {{
            --title-bg-color: {title_bg_color};
            --points-bg-color: {points_bg_color};
            --points-text-color: {points_text_color};
            border: 1px solid {border_color};
        }}
        .reward-points {{
            border: 1px solid {border_color};
        }}
    </style>
    """    
    title_bar_html = f"""
    {custom_css}
    <div class="title-container">
        {logo_html}
        {reward_points_display}
    </div>
    """
    
    st.markdown(title_bar_html, unsafe_allow_html=True)

# Function to display notifications
def display_notifications():
    if not st.session_state.notifications:
        return "<div style='padding: 10px; text-align: center; color: #999;'>No notifications yet</div>"
    
    notifications_html = "<div style='max-height: 200px; overflow-y: auto;'>"
    
    # Sort notifications with unread first, then by date/time (newest first)
    sorted_notifications = sorted(
        st.session_state.notifications, 
        key=lambda x: (x.get("read", True), x.get("date", ""), x.get("time", "")), 
        reverse=True
    )
    
    for i, notif in enumerate(sorted_notifications):
        bg_color = "#2D2D2D" if st.session_state.dark_mode else "#f8f9fa"
        border_color = "#FF5733" if not notif.get("read", True) else "#555"
        text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"
        
        notifications_html += f"""
        <div id="notif-{i}" style="
            margin-bottom: 10px; 
            padding: 10px; 
            border-left: 3px solid {border_color}; 
            background-color: {bg_color};
            color: {text_color};
        ">
            <div style="display: flex; justify-content: space-between;">
                <strong>{notif.get("message", "")}</strong>
                <small>{notif.get("time", "")}</small>
            </div>
            <div style="font-size: 0.8em; color: #999; margin-top: 5px;">
                {notif.get("date", "")}
            </div>
        </div>
        """
        
        # Mark as read after displaying
        notif["read"] = True
    
    notifications_html += "</div>"
    return notifications_html

# Add notification section
def add_notification_section():
    # Count unread notifications
    unread_count = sum(1 for n in st.session_state.notifications if not n.get("read", True))
    
    notification_html = f"""
<div style="position: relative; text-align: right; margin: 10px 0;">
    <div class="notification-dropdown">
        <span class="notification-icon" id="notif-icon">
            🔔 {f"({unread_count})" if unread_count > 0 else ""}
        </span>
        <div id="notification-content" class="notification-content">
            <h4 style="margin-top: 0; padding: 10px; border-bottom: 1px solid #555;">Notifications</h4>
            {display_notifications()}
        </div>
    </div>
</div>
<script>
    // Toggle dropdown when clicking the icon
    document.getElementById('notif-icon').addEventListener('click', function(event) {{
        document.getElementById('notification-content').classList.toggle('show');
        event.stopPropagation();
    }});
    
    // Close the dropdown when clicking outside
    document.addEventListener('click', function(event) {{
        if (!event.target.matches('.notification-icon')) {{
            var dropdowns = document.getElementsByClassName("notification-content");
            for (var i = 0; i < dropdowns.length; i++) {{
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {{
                    openDropdown.classList.remove('show');
                }}
            }}
        }}
    }});
</script>
"""
    
    st.markdown(notification_html, unsafe_allow_html=True)

# Function to display a calendar with check-in status
def display_calendar():
    # Get current month calendar
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    month_name = calendar.month_name[now.month]
    
    # Start calendar HTML
    cal_html = f"""
    <div class="calendar-container" style="margin: 20px 0;">
        <h3 style="text-align: center; margin-bottom: 10px;">{month_name} {now.year}</h3>
        <table style="width: 100%; border-collapse: collapse; text-align: center;">
            <tr>
                <th style="padding: 8px; border: 1px solid #555;">Mon</th>
                <th style="padding: 8px; border: 1px solid #555;">Tue</th>
                <th style="padding: 8px; border: 1px solid #555;">Wed</th>
                <th style="padding: 8px; border: 1px solid #555;">Thu</th>
                <th style="padding: 8px; border: 1px solid #555;">Fri</th>
                <th style="padding: 8px; border: 1px solid #555;">Sat</th>
                <th style="padding: 8px; border: 1px solid #555;">Sun</th>
            </tr>
    """
    
    # Add rows for each week
    for week in cal:
        cal_html += "<tr>"
        for day in week:
            if day == 0:
                # Empty cell for days not in this month
                cal_html += f'<td style="padding: 8px; border: 1px solid #555;"></td>'
            else:
                # Format the date string to match our history keys
                date_str = f"{now.year}-{now.month:02d}-{day:02d}"
                
                # Check if user checked in on this day
                checked_in = date_str in st.session_state.checkin_history
                
                # Highlight today's date
                is_today = (day == now.day)
                
                # Set cell styling based on check-in status and if it's today
                if checked_in:
                    # Checked in - show with checkmark and green background
                    cell_style = 'background-color: #4CAF50; color: white;'
                    day_display = f'{day} ✓'
                elif is_today:
                    # Today but not checked in - highlight
                    cell_style = 'background-color: #FF5733; color: white;'
                    day_display = day
                else:
                    # Regular day
                    cell_style = ''
                    day_display = day
                
                cal_html += f'<td style="padding: 8px; border: 1px solid #555; {cell_style}">{day_display}</td>'
        cal_html += "</tr>"
    
    cal_html += """
        </table>
    </div>
    """
    
    return cal_html

# Function to handle daily check-in
def process_daily_checkin():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if already checked in today
    if st.session_state.last_checkin_date != today:
        # Update last check-in date
        st.session_state.last_checkin_date = today
        
        # Record in history
        st.session_state.checkin_history[today] = True
        
        # Add reward point for checking in
        if "reward_points" not in st.session_state:
            st.session_state.reward_points = 0
        st.session_state.reward_points += 1
        
        # Add notification
        st.session_state.notifications.append({
            "message": f"🎯 Daily check-in complete! +1 point added.",
            "time": datetime.now().strftime("%H:%M"),
            "date": today,
            "read": False
        })
        
        return True
    
    return False

def day_navigation():
    day = st.session_state.day_index
    st.subheader(f"🌟 Day {day}")
    day_data = st.session_state.generated_data.get(day)

    if day_data:
        st.write(day_data["text"])
        audio_file_path = day_data["audio_file"]
        if audio_file_path:
            with open(audio_file_path, "rb") as audio:
                st.audio(audio.read(), format="audio/mp3")
                st.download_button(f"Download Day {day} Audio", data=open(audio_file_path, "rb"),
                                   file_name=f"day{day}_motivational.mp3")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅ Previous", key="prev") and st.session_state.day_index > 1:
            st.session_state.day_index -= 1
            st.experimental_rerun()
    with col3:
        if st.button("Next ➡", key="next") and st.session_state.day_index < len(st.session_state.generated_data):
            st.session_state.day_index += 1
            st.experimental_rerun()

# 🎓 Generate Certificate PDF
def generate_certificate(username, goal, badge):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 20, "Certificate of Completion", ln=True, align='C')

    pdf.set_font("Arial", '', 16)
    pdf.ln(10)
    pdf.cell(0, 10, f"Presented to: {username}", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(0, 10, f"For completing the 10-Day Goal: {goal}", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(0, 10, f"Badge Earned: {badge}", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%B %d, %Y')}", ln=True, align='R')

    os.makedirs("data", exist_ok=True)
    path = f"data/{username}_certificate.pdf"
    pdf.output(path)
    return path

# ✍ Generate motivation
def generate_motivation(goal, day, name, mood=None):
    if not mood:
        mood = "Motivated"
        
    prompt = f"""
You are a motivational coach. Write an engaging script for Day {day} of a 10-day motivational journey.
- Goal: {goal}
- Name: {name}
- Mood: {mood}
- Length: ~120 words
- Recap previous day briefly if Day > 1
- Tease Day {day + 1}
- Add 1 actionable tip or mindset
"""
    try:
        response = model.generate_content(prompt, generation_config={"temperature": 0.9})
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return "Something went wrong."

# 🔊 Convert text to voice
def convert_to_voice(text, filename):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Audio error: {e}")
        return None

# Process daily check-in when user logs in or refreshes the page
if st.session_state.logged_in:
    process_daily_checkin()

# --------- 🌙 DARK MODE TOGGLE ---------
with st.sidebar:
    st.title("⚙ Settings")
    st.session_state.dark_mode = st.toggle("Dark Mode 🌗", value=st.session_state.dark_mode)
    st.caption("Toggle visual mode")
    
    # Apply CSS based on dark mode state
    if st.session_state.dark_mode:
        st.markdown(dark_mode_css, unsafe_allow_html=True)
    else:
        st.markdown(light_mode_css, unsafe_allow_html=True)
    
    st.markdown("---")
    st.title("👤 Login")
    if not st.session_state.logged_in:
        username = st.text_input("Enter your name to start:")
        if st.button("Login"):
            if username:
                st.session_state.username = username
                st.session_state.logged_in = True
                st.session_state.reward_points = 0
                st.success(f"Welcome, {username}!")
    else:
        st.success(f"Hi, {st.session_state.username} 👋")
        if st.button("Logout"):
            for key in ["logged_in", "username", "goal", "day", "streak", "reward_points"]:
                if key == "day":
                    st.session_state[key] = 1
                elif key == "streak" or key == "reward_points":
                    st.session_state[key] = 0
                else:
                    st.session_state[key] = None
    
    st.markdown("💡 *Daily Reminder:* One episode a day keeps procrastination away!")

    # 🏅 Leaderboard
    st.markdown("---")
    st.title("🏅 Leaderboard")
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    for i, (user, streak) in enumerate(sorted_leaderboard[:5], 1):
        st.write(f"{i}. {user} - 🔥 {streak} Days")

    # 📒 Notes Section
    if hasattr(st.session_state, 'notes') and st.session_state.notes:
        st.markdown("---")
        st.title("📝 Saved Notes")
        for i, note in enumerate(st.session_state.notes, 1):
            st.write(f"*Day {note.get('day', '?')}:* {note.get('content', '')}")

# Display the title bar
display_title_bar()

# Add notification section
add_notification_section()

# --------- 🎯 APP BODY ---------
if st.session_state.logged_in:
    st.title("🎧 AI Guru: Personalized Audio Journey")
    
    if not st.session_state.goal:
        st.subheader("Choose Your Goal to Begin")
        
        # Use text input instead of selectbox
        goal = st.text_input(
            "🎯 What would you like to focus on?",
            placeholder="Type your goal here (e.g., Be More Confident, Improve Focus, etc.)"
        )
        
        # Optional: Add a suggestions section if you still want to provide ideas
        with st.expander("Need inspiration? Try these goals"):
            st.write("• Learn Public Speaking")
            st.write("• Be More Confident")
            st.write("• Improve Focus")
            st.write("• Build Gratitude")
        
        st.session_state.mood = st.radio("💬 How are you feeling?", ["Motivated", "Tired", "Curious", "Neutral"])
        st.session_state.voice = st.radio("🎙 Voice Style", ["Friendly", "Energetic", "Calm", "Professional"])
        
        # Modify button to check for non-empty input
        if st.button("🚀 Start My Journey"):
            if goal.strip():  # Check if goal is not empty after stripping whitespace
                st.session_state.goal = goal
                st.session_state.day = 1
                st.session_state.streak = 1
                st.success(f"You're now on Day 1 of your '{goal}' journey!")
                st.balloons()
            else:
                st.error("Please enter a goal to begin your journey.")
    else:
        st.markdown("---")
        st.header(f"📘 Day {st.session_state.day} - {st.session_state.goal}")
        st.markdown(f"🧠 Quote of the Day: {random.choice(quotes)}")
        
        # Get or generate episode content
        current_day_key = f"day_{st.session_state.day}"
        if st.session_state.goal in episodes and current_day_key in episodes[st.session_state.goal]:
            episode_text = episodes[st.session_state.goal][current_day_key]
        else:
            # Generate new content
            episode_text = generate_motivation(
                st.session_state.goal, 
                st.session_state.day, 
                st.session_state.username, 
                st.session_state.mood
            )
            
            # Save to episodes dictionary
            if st.session_state.goal not in episodes:
                episodes[st.session_state.goal] = {}
            episodes[st.session_state.goal][current_day_key] = episode_text
        
        # Create folder for audio files if it doesn't exist
        os.makedirs("motivation_audio", exist_ok=True)
        
        # Generate or retrieve audio
        voice_path = f"motivation_audio/{st.session_state.username}_day{st.session_state.day}_{st.session_state.goal.replace(' ', '_')}.mp3"
        
        # Check if audio file already exists
        if not os.path.exists(voice_path):
            audio_file = convert_to_voice(episode_text, voice_path)
        
        # Display audio and script
        if os.path.exists(voice_path):
            with open(voice_path, "rb") as audio:
                st.audio(audio.read(), format="audio/mp3")
        else:
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format='audio/mp3')
        
        st.markdown(f"📝 Script:\n\n{episode_text}")

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state.day > 1:
                if st.button("⬅ Previous Day"):
                    st.session_state.day -= 1
                    st.rerun()
        with col3:
            if st.session_state.day < 10:
                if st.button("Next Day ➡"):
                    st.session_state.day += 1
                    st.rerun()

        # 🧘 Journal
        with st.expander("✍ Reflection Journal"):
            journal_input = st.text_area("Write today's reflection or insight...")
            if st.button("Save Reflection"):
                if not hasattr(st.session_state, 'notes'):
                    st.session_state.notes = []
                st.session_state.notes.append({
                    "day": st.session_state.day,
                    "content": journal_input
                })
                st.success("Reflection saved!")
        
        # Display calendar
        st.markdown("<h3>📅 Check-in Calendar</h3>", unsafe_allow_html=True)
        st.markdown(display_calendar(), unsafe_allow_html=True)
        
        # Complete button
        if st.button("✅ Mark Episode Complete"):
            # Prepare next day's content
            next_day = st.session_state.day + 1
            if next_day <= 10:  # Only generate for 10 days
                next_day_text = generate_motivation(
                    st.session_state.goal, 
                    next_day, 
                    st.session_state.username,
                    st.session_state.mood
                )
                next_voice_path = f"motivation_audio/{st.session_state.username}_day{next_day}_{st.session_state.goal.replace(' ', '_')}.mp3"
                convert_to_voice(next_day_text, next_voice_path)
                
                # Save to episodes dictionary
                if st.session_state.goal not in episodes:
                    episodes[st.session_state.goal] = {}
                episodes[st.session_state.goal][f"day_{next_day}"] = next_day_text
            
            # Update session state
            st.session_state.day += 1
            st.session_state.streak += 1
            
            # Update leaderboard
            leaderboard[st.session_state.username] = st.session_state.streak
            
            # Add bonus points for milestones
            if st.session_state.day in [5, 10]:
                bonus_points = 5
                st.session_state.reward_points += bonus_points
                st.balloons()
                st.toast(f"🏆 You've hit Day {st.session_state.day - 1}! +{bonus_points} bonus points!", icon="🏅")
                
                # Add notification for milestone
                today = datetime.now().strftime("%Y-%m-%d")
                st.session_state.notifications.append({
                    "message": f"🏆 Milestone reached: Day {st.session_state.day-1}! +{bonus_points} bonus points!",
                    "time": datetime.now().strftime("%H:%M"),
                    "date": today,
                    "read": False
                })
            
            st.success("🎉 Great job! You're making progress.")
            
            # Save leaderboard
            os.makedirs("data", exist_ok=True)
            with open(leaderboard_path, 'w') as f:
                json.dump(leaderboard, f, indent=2)
            
            # Refresh the page to show next day's content
            st.rerun()
        
        # Progress indicators
        st.progress(min(st.session_state.day / 10, 1.0), text="Journey Progress")
        st.metric("🔥 Streak", f"{st.session_state.streak} Days")
        
        # Download button
        if os.path.exists(voice_path):
            with open(voice_path, "rb") as file:
                st.download_button(
                    label="📥 Download Today's Audio",
                    data=file,
                    file_name=f"Day{st.session_state.day}_{st.session_state.goal.replace(' ', '_')}.mp3",
                    mime="audio/mp3"
                )
        
        # 🎓 Certificate & Badge for journey completion
        if st.session_state.day > 10:
            st.markdown("🎉 You've completed your journey!")
            badge_name = random.choice(["💪 Confidence Master", "🎯 Focus Champ", "🔥 Motivation Hero"])
            st.success(f"🏅 Badge Earned: {badge_name}")

            # Generate certificate
            cert_path = generate_certificate(st.session_state.username, st.session_state.goal, badge_name)
            
            # Allow download of certificate
            if os.path.exists(cert_path):
                with open(cert_path, "rb") as f:
                    st.download_button(
                        "🎓 Download Certificate (PDF)", 
                        data=f,
                        file_name=f"{st.session_state.username}_certificate.pdf", 
                        mime="application/pdf"
                    )
            
            # Add notification for journey completion
            today = datetime.now().strftime("%Y-%m-%d")
            st.session_state.notifications.append({
                "message": f"🎓 Congratulations! You've completed your 10-day journey for '{st.session_state.goal}'!",
                "time": datetime.now().strftime("%H:%M"),
                "date": today,
                "read": False
            })
else:
    st.warning("🔐 Please log in using the sidebar to begin your personalized journey.")

# Try to save updated episodes
try:
    os.makedirs("data", exist_ok=True)
    with open('data/sample_episodes.json', 'w') as f:
        json.dump(episodes, f, indent=2)
except Exception as e:
    st.error(f"Could not save episode data: {e}")
