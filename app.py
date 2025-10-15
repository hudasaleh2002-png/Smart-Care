import streamlit as st
import speech_recognition as sr

st.title("🎤 Smart Care - Voice Assistance for Seniors")

st.write("""
مرحبًا بك في تطبيق **Smart Care** ❤️  
هذا التطبيق يساعد كبار السن في إرسال نداء استغاثة صوتي عند الحاجة.
""")

if st.button("ابدأ التسجيل 🎙️"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎧 جاري الاستماع... تفضل بالتحدث")
        audio = r.listen(source)
        st.write("⏳ جاري تحليل الصوت...")
        try:
            text = r.recognize_google(audio, language="ar-AR")
            st.success(f"✅ تم التعرف على الصوت: {text}")
            if "مساعدة" in text or "النجدة" in text:
                st.warning("🚨 تنبيه! تم اكتشاف نداء استغاثة!")
            else:
                st.info("📢 لم يتم اكتشاف نداء استغاثة.")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
