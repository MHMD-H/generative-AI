import streamlit as st
from llm import call_messages

st.title("🏋️ AI Fitness Coach")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if "image" in message:
            st.image(message["image"], width=300)

image = st.file_uploader(
    "Upload media here",
    type=["png", "jpg", "jpeg"]
)

prompt = st.chat_input("Can I help You today?")

if prompt:

    # حفظ رسالة المستخدم
    user_message = {
        "role": "user",
        "content": prompt
    }

    if image:
        user_message["image"] = image

    st.session_state.messages.append(user_message)

    # الحصول على الرد
    answer = call_messages(prompt, image)

    # حفظ رد المساعد
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # إعادة تشغيل الصفحة لعرض المحادثة من session_state
    st.rerun()