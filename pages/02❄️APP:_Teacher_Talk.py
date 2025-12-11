import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="Classroom English Trainer", layout="wide")


def tts_bytes(text: str, lang: str = "en"):
    """Generate TTS audio bytes from text using gTTS."""
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp


# -------- Classroom English Scripts -------- #

lesson_focus_options = [
    "Vocabulary",
    "Grammar",
    "Speaking",
    "Listening",
    "Reading",
    "Writing",
]

scripts_by_category = {
    "1) Starting the class": [
        "Okay everyone, let’s get started. Please settle down and face the front. Today we’re going to work together on some English, so get your books and notebooks ready. Take a deep breath, clear your mind, and let’s begin our class.",
        "Good morning, everyone. How are you today? I hope you’re ready to learn and to use some English. Please put away your phones, open your notebooks, and get your pens ready. Let’s start our lesson now.",
        "All right, class, let’s focus. Today we’ll continue from where we left off last time. Please open your books to today’s lesson page, and make sure you have something to write with. When you’re ready, look up at me so we can begin.",
        "Hello, everyone. Welcome back to English class. Before we start, please sit in your seats and check that you have your textbook and notebook. Today we’ll do some activities together, so try to use as much English as you can.",
        "Okay, class, let’s begin. Today we’ll review what we studied last time and then try something new. Please get your materials ready and clear your desks of anything you don’t need. When you’re ready, give me your full attention.",
        "Good afternoon, everyone. Let’s get started with today’s English lesson. Please turn to the correct page in your book and take out your notebook. I’d like you to keep an open mind, ask questions, and try to participate actively today.",
        "All right, students, it’s time to start. Please finish your conversations and look this way. Today, we’ll practice using English step by step, so don’t worry if it feels difficult at first. Just relax, listen carefully, and do your best.",
        "Welcome, everyone. Thank you for coming on time today. In this lesson, we’ll build on what you already know and try to use English more confidently. Please prepare your pens and notebooks, and let’s begin working together.",
        "Okay class, let’s begin today’s session. First, I’d like you to sit comfortably and get your materials ready. We’ll warm up with a simple review and then move into new activities. Try to stay focused and enjoy using English.",
        "Good morning, class. Let’s start our English lesson now. Please check that you have your textbook, notebook, and something to write with. Today I’d like you to listen carefully, think in English as much as possible, and share your ideas with the class."
    ],
    "2) Asking for opinions or answers": [
        "Now, I’d like to hear from you. What do you think about this point? Take a moment to think, and then raise your hand if you’d like to share your idea. There’s no perfect answer, so just try to explain your thoughts in English.",
        "Can anyone tell me what this means in your own words? Don’t worry about being perfect. Just give it a try and use the key words we learned today. Who would like to go first and share an answer with the class?",
        "Let’s hear your opinion. How would you explain this idea to a friend? Think of a simple example and try to say it in English. If you’re not sure, you can start and I’ll help you finish your sentence.",
        "I’ll ask a question, and I want you to think carefully before you answer. Why do you think this is important in English? Try to give one short reason and, if you can, an example. Who can share their answer with us?",
        "Turn to this sentence and tell me what you notice. What pattern do you see here? Take a few seconds to think, and then try to explain it in English. Even if you’re not completely sure, it’s good practice to try.",
        "I’d like to check your understanding. Can someone summarize what we just learned? Try to use your own words, not the exact sentence from the book. Raise your hand when you’re ready to share your summary.",
        "Let’s make this more interactive. How would you use this expression in a real situation? Imagine you are talking to a friend or a classmate. Try to create a short example sentence and share it with the class.",
        "Now, I want to hear some different ideas. Do you agree or disagree with this example? Why or why not? Try to give a short explanation in English. Remember, it’s okay to make mistakes as long as you are trying.",
        "Take a moment to think quietly. Then, when you’re ready, tell us your answer. You can start with a simple phrase like ‘I think…’ or ‘In my opinion…’. Use that as a starting point, and then add your idea.",
        "Before we move on, let’s check together. How would you answer this question? Try to say at least one sentence in English. If you get stuck, I can give you a prompt, and you can finish the sentence."
    ],
    "3) Giving positive feedback to students": [
        "That was a great attempt. I can see that you really tried to use the new expression we learned today. Even if it wasn’t perfect, your idea was clear, and that’s what matters most. Keep going like this and you’ll improve a lot.",
        "Nice job, thank you for sharing. Your sentence was easy to understand, and you used good intonation as well. If you keep practicing like this, your English will sound more and more natural. Well done.",
        "I really like how you explained that. You spoke clearly and didn’t give up even when it was difficult. That kind of effort is very important in language learning. Please keep using English with that same confidence.",
        "Excellent work. You chose a very good example and connected it well to what we learned today. Even if there were a few small mistakes, your communication was successful. That is exactly what I want to see in this class.",
        "Thank you, that was a very thoughtful answer. You showed that you understood the main idea, and you expressed it in your own words. That’s a big step in learning a language. You should feel proud of yourself.",
        "Great effort there. I could hear that you were trying to pronounce the words carefully and use the correct structure. Don’t worry too much about small errors; what matters is that you are improving with each try.",
        "I appreciate your willingness to answer. It’s not easy to speak in front of the whole class, but you did it well. The more you practice speaking like this, the more natural your English will become. Keep it up.",
        "Very good. You used the key vocabulary from today’s lesson in a natural way. This shows that you’re really paying attention and trying to apply what you learn. That kind of attitude will help you grow quickly.",
        "That was a clear and confident answer. I could follow your explanation without any problem. If you keep giving answers like that, your speaking skills will continue to develop. Thank you for your contribution.",
        "I’m happy to see you trying so hard. Your answer might not be perfect yet, but it’s getting better each time you speak. Remember, progress is more important than perfection. Please continue to challenge yourself."
    ],
    "4) Wrapping up the class": [
        "All right, everyone, we need to finish here for today. Before we end, take a moment to think about one thing you learned in this lesson. Try to remember it clearly so you can use it next time. Thank you for your hard work.",
        "Okay, let’s wrap up today’s class. We reviewed some important points and practiced using them in English. I’d like you to think about which part was easiest and which part was hardest for you. We’ll build on this again in our next lesson.",
        "We’re out of time for today, so we’ll stop here. Please look back at your notes and underline any expressions you want to remember. If you have questions, write them down and bring them to the next class. You did a nice job today.",
        "That brings us to the end of our lesson. We practiced using English in different ways, and I could see good effort from many of you. Try to review for a few minutes at home so that you don’t forget. Thank you, and see you next time.",
        "Let’s finish up now. Today we focused on using English actively, and I appreciate your participation. Before you leave, quickly check your notebook and make sure you’ve written down anything important. Great work today, everyone.",
        "Time is almost up, so we’ll stop here. I’d like you to think of one expression from today that you can use outside this classroom. Try using it with a friend or family member if you can. Thank you for your effort today.",
        "We’ll end our class at this point. You all did well, even when the tasks were a bit challenging. Please review the key ideas at home, and come back ready to build on them in our next lesson. Have a good rest of the day.",
        "That’s all for today’s English lesson. I was happy to see you trying to speak and share your ideas. Remember, small, regular practice is the best way to improve. Take care, and I’ll see you in the next class.",
        "Okay, everyone, let’s stop here for today. Before you go, think about how you felt using English in this class. Were you more confident than before? I hope you keep that feeling and continue to practice. Great job today.",
        "We’ve reached the end of our time together today. Thank you for listening, participating, and trying your best. Please keep your notes safe and look at them again before the next lesson. See you next time, and keep using English."
    ],
}

# ----------------- UI Layout ----------------- #

st.title("Classroom English Streamlit App 🎓")

tab1, tab2, tab3 = st.tabs(
    ["Classroom English Practice", "Tab 2 (Coming Soon)", "Tab 3 (Coming Soon)"]
)

with tab1:
    st.header("English Expressions for EFL Classrooms")

    # Lesson focus selection (for teacher awareness; phrases remain generic)
    focus = st.selectbox("Lesson focus (for this class):", lesson_focus_options)
    st.info(f"Current lesson focus: **{focus}**. The expressions below are generic and can be used with any content type.")

    category = st.selectbox(
        "Choose a classroom situation:",
        list(scripts_by_category.keys()),
    )

    st.markdown("### Expressions")
    st.write("Open a script below, read it, and click **Play** to listen to the audio.")

    for idx, script in enumerate(scripts_by_category[category], start=1):
        with st.expander(f"{category} – Script {idx}"):
            st.write(script)
            if st.button(f"▶️ Play audio for Script {idx}", key=f"{category}_{idx}"):
                audio_data = tts_bytes(script)
                st.audio(audio_data, format="audio/mp3")

with tab2:
    st.header("Tab 2")
    st.write("This tab is reserved for future activities (e.g., role-plays, quizzes, or recording practice).")

with tab3:
    st.header("Tab 3")
    st.write("This tab is reserved for future expansions, such as saving favorite expressions or creating custom scripts.")
