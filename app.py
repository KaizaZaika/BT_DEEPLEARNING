import streamlit as st
import ollama
import time

# --- 1. CẤU HÌNH ---
# Thay DeepSeek bằng Yi-Coder (thông minh hơn)
MODELS = [
    'yi-coder:1.5b', 
    'qwen2.5-coder:1.5b', 
    'llama3.2:1b'
]

st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")
st.title("🤖 Phân tích mã lập trình bằng LLM")

# --- 2. HÀM TẠO PROMPT (KHỚP YÊU CẦU ĐỀ BÀI) ---
def make_strict_prompt(code_input):
    # Dùng biến backtick để tránh lỗi hiển thị khi copy code
    bt = "`" * 3
    
    # Prompt song ngữ: Hướng dẫn bằng Tiếng Anh (để model hiểu) 
    # nhưng yêu cầu Output Tiêu đề Tiếng Việt.
    prompt = f"""
You are a Senior Code Reviewer. Analyze the code below.
You MUST reply using EXACTLY the following structure with these specific headers in Vietnamese:

### 1. Tóm tắt code
(Summarize what the code does in 1-2 sentences in Vietnamese)

### 2. Danh sách lỗi hoặc nguy cơ bug
(List logic errors, syntax errors, or security issues using bullet points in Vietnamese)
- Lỗi 1: ...
- Lỗi 2: ...

### 3. Gợi ý tối ưu
(Provide the full fixed and optimized code inside a Python code block)
{bt}python
# Code đã sửa
{bt}

---
CODE TO ANALYZE:
{bt}python
{code_input}
{bt}
"""
    return prompt

# --- 3. HÀM XỬ LÝ CHÍNH ---
def process_input(content, is_file=False):
    # Hiển thị tin nhắn người dùng (xử lý chuỗi an toàn)
    display_text = content
    if is_file:
        display_text = f"📄 **Đã gửi file code:**\n```python\n{content}\n```"
    
    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
        st.markdown(display_text)

    # TẠO PROMPT
    strict_prompt = make_strict_prompt(content)
    
    with st.chat_message("assistant"):
        st.write("🔍 Đang phân tích lần lượt từng model...")
        
        outputs = [] 
        
        # Chạy vòng lặp qua từng model
        for i, model_name in enumerate(MODELS):
            st.markdown(f"### 🤖 Model: **{model_name}**")
            status_box = st.empty()
            status_box.info(f"⏳ {model_name} đang chạy...")
            
            try:
                start_time = time.time()
                # Gọi Ollama (keep_alive=0 để xả RAM ngay)
                response = ollama.chat(model=model_name, keep_alive=0, messages=[
                    {'role': 'system', 'content': "You strictly follow the requested format."},
                    {'role': 'user', 'content': strict_prompt},
                ])
                duration = round(time.time() - start_time, 2)
                result_text = response['message']['content']
                
                # Hiển thị kết quả
                status_box.empty()
                st.success(f"⏱️ Xong trong {duration}s")
                st.markdown(result_text)
                
                outputs.append(result_text)
                
            except Exception as e:
                st.error(f"Lỗi: {e} (Bạn đã 'ollama pull {model_name}' chưa?)")
                outputs.append(str(e))
            
            # Kẻ đường gạch ngang phân cách
            st.divider()
            
            # Nghỉ 0.5s để xả RAM
            time.sleep(0.5)

        # Lưu kết quả vào lịch sử
        st.session_state.messages.append({
            "role": "assistant", 
            "content": outputs, 
            "type": "vertical" 
        })

# --- 4. GIAO DIỆN CHÍNH ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("type") == "vertical":
            for i, content in enumerate(message["content"]):
                if i < len(MODELS): 
                    st.markdown(f"### 🤖 Model: **{MODELS[i]}**")
                    st.markdown(content)
                    st.divider()
        elif message.get("type") == "comparison": 
             cols = st.columns(3)
             for i, content in enumerate(message["content"]):
                with cols[i]:
                    st.markdown(f"**{MODELS[i]}**")
                    st.markdown(content)
        else:
            st.markdown(message["content"])

st.write("---") 

# --- 5. KHU VỰC NHẬP LIỆU ---
with st.expander("📎 Đính kèm File Code (Click để mở)", expanded=False):
    uploaded_file = st.file_uploader("Chọn file code (.py, .txt...)", label_visibility="collapsed")
    if uploaded_file and st.button("⬆️ Gửi File này"):
        file_content = uploaded_file.getvalue().decode("utf-8")
        process_input(file_content, is_file=True)
        st.rerun()

# Ô Chat Input
if prompt := st.chat_input("Nhập code hoặc câu hỏi vào đây..."):
    process_input(prompt, is_file=False)