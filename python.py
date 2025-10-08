import streamlit as st

# ------------------------- KHUNG CHAT TƯƠNG TÁC VỚI GEMINI -------------------------
st.markdown("---")
st.subheader("💬 Trò chuyện trực tiếp với Gemini AI")

# Khởi tạo session_state để lưu lịch sử hội thoại và đối tượng chat
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
# Khởi tạo đối tượng chat (lưu trữ lịch sử)
if "gemini_chat_session" not in st.session_state:
    st.session_state.gemini_chat_session = None

# Kiểm tra API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.warning("⚠️ Không tìm thấy khóa API Gemini. Hãy cấu hình 'GEMINI_API_KEY' trong `.streamlit/secrets.toml`.")
else:
    # Chỉ import và cấu hình khi có API Key
    import google.generativeai as genai 
    
    # Cấu hình chỉ chạy một lần
    if st.session_state.gemini_chat_session is None:
        try:
            genai.configure(api_key=api_key)
            # Khởi tạo mô hình và phiên chat
            chat_model = genai.GenerativeModel('gemini-pro')
            st.session_state.gemini_chat_session = chat_model.start_chat(history=[])
        except Exception as e:
            st.error(f"Lỗi cấu hình Gemini: {e}")
            st.stop()

    chat_session = st.session_state.gemini_chat_session

    # Hiển thị lịch sử trò chuyện đã lưu trong session_state.chat_messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Nhập câu hỏi từ người dùng
    prompt = st.chat_input("Bạn muốn hỏi gì Gemini?")

    if prompt:
        # 1. Hiển thị câu hỏi người dùng
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # 2. Gửi câu hỏi đến Gemini và nhận phản hồi
        with st.chat_message("assistant"):
            # Sử dụng một spinner để thể hiện quá trình đang xử lý
            with st.spinner("🤖 Gemini đang suy nghĩ..."):
                try:
                    # Gửi tin nhắn qua đối tượng chat session để duy trì lịch sử
                    response = chat_session.send_message(prompt)
                    reply = response.text
                except Exception as e:
                    # Xử lý lỗi nếu có
                    reply = f"❌ Lỗi từ Gemini: {e}"
            
            # 3. Hiển thị phản hồi từ Gemini
            st.markdown(reply)
            
        # 4. Lưu phản hồi vào lịch sử chat của Streamlit
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})

# ----------------------------------------------------------------------------------
