import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io

st.set_page_config(page_title="Smart Care", page_icon="🎤")
st.title("🎤 Smart Care - Voice Assistance for Seniors")

st.write("""
مرحبًا بك في تطبيق **Smart Care** ❤️  
هذا التطبيق يساعد كبار السن في إرسال نداء استغاثة صوتي عند الحاجة.
""")

audio_data = mic_recorder(start_prompt="🎙️ ابدأ التسجيل", stop_prompt="⏹️ إيقاف التسجيل", just_once=True)

if audio_data:
    st.success("✅ تم التسجيل بنجاح! جاري تحليل الصوت...")
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(audio_data["bytes"])) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="ar-SA")
            st.success(f"✅ تم التعرف على الصوت: {text}")
            if "مساعدة" in text or "النجدة" in text:
                st.warning("🚨 تم اكتشاف نداء استغاثة!")
            else:
                st.info("📢 لم يتم اكتشاف نداء استغاثة.")
    except sr.UnknownValueError:
        st.error("❌ لم يتم التعرف على الصوت")
    except sr.RequestError:
        st.error("⚠️ خطأ في الاتصال بخدمة Google")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
