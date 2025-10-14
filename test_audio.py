import speech_recognition as sr

recognizer = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("🎤 قل شيئًا...")
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        print("✅ تم التعرف على النص:", text)
except sr.RequestError:
    print("❌ مشكلة في الاتصال بخدمة Google")
except sr.UnknownValueError:
    print("❌ لم يتم التعرف على الصوت")
except Exception as e:
    print(f"🚨 خطأ آخر: {e}")
