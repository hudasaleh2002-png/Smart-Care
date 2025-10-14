import streamlit as st
import pyaudio
import numpy as np
import threading
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 500  # Sound threshold to activate listening

class EmergencyDetector:
    def __init__(self):
        self.is_listening = False
        self.is_recording = False
        self.audio_data = []
        self.p = pyaudio.PyAudio()
        
    def get_audio_level(self, data):
        """Calculate the audio level from raw audio data"""
        audio_array = np.frombuffer(data, dtype=np.int16)
        return np.abs(audio_array).mean()
    
    def listen_for_sound(self):
        """Continuously monitor for sound above threshold"""
        try:
            stream = self.p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            while self.is_listening:
                data = stream.read(CHUNK)
                audio_level = self.get_audio_level(data)
                
                if audio_level > THRESHOLD and not self.is_recording:
                    st.session_state.status = "🎤 Sound detected! Recording..."
                    self.start_recording()
                
                time.sleep(0.1)
                
        except Exception as e:
            st.error(f"Audio error: {e}")
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
    
    def start_recording(self):
        """Start recording audio for analysis"""
        self.is_recording = True
        self.audio_data = []
        
        # Record for 3 seconds
        threading.Thread(target=self.record_audio, daemon=True).start()
    
    def record_audio(self):
        """Record audio for analysis"""
        try:
            stream = self.p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            for _ in range(0, int(RATE / CHUNK * 3)):  # Record for 3 seconds
                data = stream.read(CHUNK)
                self.audio_data.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Analyze the recorded audio
            self.analyze_audio()
            
        except Exception as e:
            st.error(f"Recording error: {e}")
        finally:
            self.is_recording = False
    
    def analyze_audio(self):
        """Analyze audio using OpenAI API"""
        try:
            # Convert audio data to a format suitable for OpenAI
            # Note: This is a simplified version - you might need to save to file first
            st.session_state.status = "🤖 Analyzing audio..."
            
            # Simulate analysis (replace with actual OpenAI API call)
            time.sleep(2)
            
            # For demo purposes, randomly detect emergency
            import random
            is_emergency = random.choice([True, False])
            
            if is_emergency:
                st.session_state.status = (
        "🚨 **تم الكشف عن طارئ!**\n\n"
        "📞 **يرجى الاتصال برقم الطوارئ المناسب:**\n"
        "- الإسعاف: 997\n"
        "- الدفاع المدني: 998\n"
        "- الشرطة: 999\n"
        "- رقم الطوارئ الموحد: 911"
    )
                st.session_state.emergency_detected = True
                # Here you would implement actual emergency response
                time.sleep(3)
                st.session_state.status +=  "\n\n✅ تم الإبلاغ. الرجاء البقاء هادئاً حتى وصول المساعدة."

            else:
                st.session_state.status = "✅ No emergency detected. Resuming monitoring..."
                time.sleep(2)
                st.session_state.status = "👂 Listening for sounds..."
                
        except Exception as e:
            st.error(f"Analysis error: {e}")
            st.session_state.status = "❌ Analysis failed. Resuming monitoring..."

def main():
    st.set_page_config(
        page_title="Emergency Detection System",
        page_icon="🚨",
        layout="centered"
    )
    
    st.title("🚨 Emergency Detection System")
    st.markdown("*Listening for calls for help using AI*")
    
    # Initialize session state
    if 'detector' not in st.session_state:
        st.session_state.detector = EmergencyDetector()
        st.session_state.status = "🔴 System ready - Click Start to begin monitoring"
        st.session_state.emergency_detected = False
    
    # Status display
    status_container = st.container()
    with status_container:
        if st.session_state.emergency_detected:
            st.error(st.session_state.status)
        elif "Listening" in st.session_state.status:
            st.success(st.session_state.status)
        elif "Recording" in st.session_state.status or "Analyzing" in st.session_state.status:
            st.warning(st.session_state.status)
        else:
            st.info(st.session_state.status)
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Start Monitoring", disabled=st.session_state.detector.is_listening):
            st.session_state.detector.is_listening = True
            st.session_state.status = "👂 Listening for sounds..."
            st.session_state.emergency_detected = False
            
            # Start listening in background thread
            threading.Thread(
                target=st.session_state.detector.listen_for_sound, 
                daemon=True
            ).start()
            st.rerun()
    
    with col2:
        if st.button("🔴 Stop Monitoring", disabled=not st.session_state.detector.is_listening):
            st.session_state.detector.is_listening = False
            st.session_state.status = "🔴 Monitoring stopped"
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.detector.is_listening = False
            st.session_state.status = "🔴 System ready - Click Start to begin monitoring"
            st.session_state.emergency_detected = False
            st.rerun()
    
    # Settings
    with st.expander("⚙️ Settings"):
        st.slider("Sound Threshold", 100, 2000, THRESHOLD, key="threshold")
        st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        
        if st.button("Test Microphone"):
            st.info("Testing microphone access...")
            try:
                test_stream = st.session_state.detector.p.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK
                )
                data = test_stream.read(CHUNK)
                level = st.session_state.detector.get_audio_level(data)
                test_stream.close()
                st.success(f"✅ Microphone working! Current audio level: {level:.0f}")
            except Exception as e:
                st.error(f"❌ Microphone error: {e}")
    
    # Instructions
    with st.expander("📖 How to Use"):
        st.markdown("""
        1. **Set up your OpenAI API key** in the settings or create a `.env` file
        2. **Click "Start Monitoring"** to begin listening
        3. **The system will activate** when sound is detected above the threshold
        4. **AI will analyze** the audio for emergency keywords
        5. **If an emergency is detected**, the system will simulate calling authorities
        
        **Note**: This is a demo version. In production, you would:
        - Implement actual emergency contact system
        - Use proper audio file handling for OpenAI API
        - Add more sophisticated sound detection
        - Include privacy and security measures
        """)
    
    # Auto-refresh for real-time updates
    if st.session_state.detector.is_listening:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
