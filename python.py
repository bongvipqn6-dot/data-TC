# ------------------------- KHUNG CHAT TƯƠNG TÁC VỚI GEMINI -------------------------
st.markdown("---")
st.subheader("💬 Trò chuyện trực tiếp với Gemini AI")

# Khởi tạo session_state để lưu lịch sử hội thoại
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Kiểm tra API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.warning("⚠️ Không tìm thấy khóa API Gemini. Hãy cấu hình 'GEMINI_API_KEY' trong `.streamlit/secrets.toml`.")
else:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    chat_model = genai.GenerativeModel('gemini-pro')

    # Hiển thị lịch sử trò chuyện
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Nhập câu hỏi từ người dùng
    prompt = st.chat_input("Bạn muốn hỏi gì Gemini?")

    if prompt:
        # Hiển thị câu hỏi người dùng
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        try:
            response = chat_model.generate_content(prompt)
            reply = response.text
        except Exception as e:
            reply = f"❌ Lỗi từ Gemini: {e}"

        # Hiển thị phản hồi từ Gemini
        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
