# Smart-Care 
# 🚨 Smart Care – AI Emergency Detection System  
**نظام المساعدة الذكية Smart Care**

Smart Care هو مشروع تخرّج يهدف إلى دعم كبار السن وذوي الاحتياجات الخاصة باستخدام الذكاء الاصطناعي والتعرف الصوتي للكشف عن حالات الطوارئ.

Smart Care is an AI-powered voice recognition system designed to help elderly or disabled individuals in emergency situations.  
It continuously listens for help calls, analyzes audio signals, and automatically triggers alerts if an emergency is detected.

---

## 🎯 Main Features | المميزات الرئيسية
- مراقبة صوتية لحظية باستخدام **PyAudio**  
- التعرف التلقائي على الأصوات وكلمات المساعدة  
- واجهة سهلة الاستخدام مبنية باستخدام **Streamlit**  
- تحليل ذكي للكلام عبر **OpenAI API**  
- إمكانية تخصيص حساسية الصوت وتشغيل الميكروفون المباشر  

---

## 🧠 How It Works | آلية العمل
1. يبدأ النظام في وضع الاستماع الدائم.  
2. عند رصد صوت يتجاوز مستوى محدد، يتم تسجيله تلقائيًا.  
3. يُحلَّل الصوت باستخدام الذكاء الاصطناعي.  
4. في حال اكتشاف حالة طوارئ، يتم إرسال تنبيه فوري (محاكاة).  

---

## 🛠️ Technologies Used | التقنيات المستخدمة
- Python 3.13  
- Streamlit  
- PyAudio  
- NumPy  
- OpenAI API  
- dotenv  

---

## 📦 Installation | طريقة التشغيل
```bash
git clone https://github.com/HudaUsername/Smart_Care.git
cd Smart_Care
pip install -r requirements.txt
streamlit run main.py

📱 Future Development | التطوير المستقبلي

تحويل المشروع إلى تطبيق جوال (Android / iOS)

إضافة تحديد موقع المستخدم أثناء الطوارئ

دعم التعرف على أصوات محددة لكل مستخدم

إرسال التنبيهات إلى السحابة

👩‍💻 Author | المطوّرة

Huda Saleh
Graduation Project – TM471, Arab Open University
2025