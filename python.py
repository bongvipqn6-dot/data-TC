import streamlit as st
import google.generativeai as genai

# ------------------------- KHUNG CHAT TƯƠNG TÁC VỚI GEMINI -------------------------
st.markdown("---")
st.subheader("💬 Trò chuyện trực tiếp với Gemini AI")

# --- 1. Quản lý Session State và Cấu hình API ---

# Khởi tạo session_state để lưu lịch sử hội thoại (giao diện)
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
    
# Khởi tạo đối tượng CHAT SESSION để Gemini ghi nhớ lịch sử (KEY FIX)
if "gemini_chat_session" not in st.session_state:
    st.session_state.gemini_chat_session = None

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Không tìm thấy khóa API Gemini. Vui lòng cấu hình 'GEMINI_API_KEY' trong `.streamlit/secrets.toml`.")
else:
    # Cấu hình và khởi tạo phiên chat chỉ chạy MỘT LẦN (giúp app chạy mượt hơn)
    if st.session_state.gemini_chat_session is None:
        try:
            genai.configure(api_key=api_key)
            chat_model = genai.GenerativeModel('gemini-pro')
            # Sử dụng start_chat để tạo đối tượng Chat có khả năng lưu history
            st.session_state.gemini_chat_session = chat_model.start_chat(history=[])
        except Exception as e:
            st.error(f"Lỗi cấu hình Gemini: {e}. Vui lòng kiểm tra lại API Key.")
            st.stop()
    
    chat_session = st.session_state.gemini_chat_session

    # --- 2. Hiển thị Lịch sử Trò chuyện ---
    
    # Hiển thị lịch sử đã lưu
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- 3. Xử lý Input và Phản hồi ---

    prompt = st.chat_input("Bạn muốn hỏi gì Gemini?")

    if prompt:
        # a) Hiển thị câu hỏi người dùng và lưu vào lịch sử giao diện
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # b) Gửi câu hỏi đến Gemini
        with st.chat_message("assistant"):
            with st.spinner("🤖 Gemini đang suy nghĩ..."):
                try:
                    # Gửi tin nhắn qua CHAT SESSION để duy trì bối cảnh.
                    # Dùng stream=True và st.write_stream() để hiển thị phản hồi dần dần (tối ưu UX).
                    response_stream = chat_session.send_message(prompt, stream=True)
                    full_reply = st.write_stream(response_stream)
                    
                except Exception as e:
                    full_reply = f"❌ Lỗi từ Gemini: {e}"
                    st.markdown(full_reply)
            
        # c) Lưu phản hồi đầy đủ vào lịch sử chat của Streamlit
        st.session_state.chat_messages.append({"role": "assistant", "content": full_reply})

# ----------------------------------------------------------------------------------import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG BAN ĐẦU ---
st.set_page_config(
    page_title="Streamlit Gemini Chat App",
    page_icon="✨",
    layout="wide"
)

# ------------------------- KHUNG CHAT TƯƠNG TÁC VỚI GEMINI -------------------------
st.markdown("---")
st.subheader("💬 Trò chuyện trực tiếp với Gemini AI")

# --- 1. Quản lý Session State và Cấu hình API ---

# Khởi tạo session_state để lưu lịch sử hội thoại (dùng cho hiển thị giao diện)
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
# Khởi tạo đối tượng chat (dùng để lưu lịch sử hội thoại Gemini)
if "gemini_chat_session" not in st.session_state:
    st.session_state.gemini_chat_session = None

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Không tìm thấy khóa API Gemini. Vui lòng cấu hình 'GEMINI_API_KEY' trong `.streamlit/secrets.toml`.")
else:
    # Cấu hình và khởi tạo phiên chat chỉ chạy một lần
    if st.session_state.gemini_chat_session is None:
        try:
            # 1a. Cấu hình API
            genai.configure(api_key=api_key)
            
            # 1b. Khởi tạo mô hình và phiên chat duy trì lịch sử (gemini-pro)
            # Dùng start_chat với history=[] để đảm bảo phiên chat mới hoàn toàn
            chat_model = genai.GenerativeModel('gemini-pro')
            st.session_state.gemini_chat_session = chat_model.start_chat(history=[])
        except Exception as e:
            st.error(f"Lỗi cấu hình Gemini: {e}. Vui lòng kiểm tra lại API Key.")
            st.stop() # Dừng script nếu cấu hình thất bại
    
    # Lấy phiên chat đã khởi tạo
    chat_session = st.session_state.gemini_chat_session

    # --- 2. Hiển thị Lịch sử Trò chuyện ---
    
    # Lặp qua lịch sử đã lưu trong session_state.chat_messages để hiển thị lại
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- 3. Xử lý Input và Phản hồi ---

    # Nhập câu hỏi từ người dùng
    prompt = st.chat_input("Bạn muốn hỏi gì Gemini?")

    if prompt:
        # 3a. Hiển thị câu hỏi người dùng và lưu vào lịch sử giao diện
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # 3b. Gửi câu hỏi đến Gemini và nhận phản hồi
        with st.chat_message("assistant"):
            # Sử dụng spinner để cải thiện trải nghiệm người dùng (UX)
            with st.spinner("🤖 Gemini đang suy nghĩ..."):
                try:
                    # Gửi tin nhắn qua đối tượng chat session để duy trì bối cảnh
                    # Sử dụng stream=True để phản hồi hiển thị dần dần
                    response_stream = chat_session.send_message(prompt, stream=True)
                    
                    # st.write_stream hiển thị phản hồi từng phần và trả về nội dung đầy đủ
                    full_reply = st.write_stream(response_stream)
                    
                except Exception as e:
                    # Xử lý lỗi nếu có
                    full_reply = f"❌ Lỗi từ Gemini: {e}"
                    st.markdown(full_reply)
            
        # 3c. Lưu phản hồi đầy đủ vào lịch sử chat của Streamlit
        # Biến full_reply đã chứa toàn bộ nội dung sau khi streaming kết thúc
        st.session_state.chat_messages.append({"role": "assistant", "content": full_reply})

# ----------------------------------------------------------------------------------import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG BAN ĐẦU (có thể giữ nguyên hoặc tùy chỉnh) ---
st.set_page_config(
    page_title="Streamlit Gemini Chat App",
    page_icon="✨",
    layout="wide"
)

# ------------------------- KHUNG CHAT TƯƠNG TÁC VỚI GEMINI -------------------------
st.markdown("---")
st.subheader("💬 Trò chuyện trực tiếp với Gemini AI")

# --- 1. Quản lý Session State và Cấu hình API ---

# Khởi tạo session_state để lưu lịch sử hội thoại (dùng cho hiển thị giao diện)
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
# Khởi tạo đối tượng chat (dùng để lưu lịch sử hội thoại Gemini)
if "gemini_chat_session" not in st.session_state:
    st.session_state.gemini_chat_session = None

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Không tìm thấy khóa API Gemini. Vui lòng cấu hình 'GEMINI_API_KEY' trong `.streamlit/secrets.toml`.")
else:
    # Cấu hình và khởi tạo phiên chat chỉ chạy một lần
    if st.session_state.gemini_chat_session is None:
        try:
            # 1a. Cấu hình API
            genai.configure(api_key=api_key)
            
            # 1b. Khởi tạo mô hình và phiên chat duy trì lịch sử (gemini-pro)
            chat_model = genai.GenerativeModel('gemini-pro')
            st.session_state.gemini_chat_session = chat_model.start_chat(history=[])
        except Exception as e:
            st.error(f"Lỗi cấu hình Gemini: {e}. Vui lòng kiểm tra lại API Key.")
            # Dừng script để tránh lỗi gọi API tiếp theo
            st.stop()
    
    # Lấy phiên chat đã khởi tạo
    chat_session = st.session_state.gemini_chat_session

    # --- 2. Hiển thị Lịch sử Trò chuyện ---
    
    # Lặp qua lịch sử đã lưu để hiển thị lại
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- 3. Xử lý Input và Phản hồi ---

    # Nhập câu hỏi từ người dùng
    prompt = st.chat_input("Bạn muốn hỏi gì Gemini?")

    if prompt:
        # 3a. Hiển thị câu hỏi người dùng và lưu vào lịch sử giao diện
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # 3b. Gửi câu hỏi đến Gemini và nhận phản hồi
        with st.chat_message("assistant"):
            # Sử dụng spinner để cải thiện UX
            with st.spinner("🤖 Gemini đang suy nghĩ..."):
                try:
                    # Gửi tin nhắn qua đối tượng chat session để duy trì bối cảnh (context)
                    response = chat_session.send_message(prompt, stream=True)
                    
                    # Tối ưu: Sử dụng stream để phản hồi hiển thị dần dần
                    reply = st.write_stream(response)
                    
                except Exception as e:
                    # Xử lý lỗi nếu có
                    reply = f"❌ Lỗi từ Gemini: {e}"
                    st.markdown(reply)
            
        # 3c. Lưu phản hồi cuối cùng vào lịch sử chat của Streamlit
        # Lấy nội dung đầy đủ từ phản hồi Stream (nếu dùng stream=True)
        # Note: Nếu không dùng stream, 'reply' đã là response.text
        if isinstance(reply, str):
            final_reply_content = reply
        else:
            final_reply_content = "".join(response.text for response in chat_session.get_history()[-1].parts)
            
        st.session_state.chat_messages.append({"role": "assistant", "content": final_reply_content})

# ----------------------------------------------------------------------------------import streamlit as st

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
