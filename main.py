from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import logging

# Flask 앱 초기화
app = Flask(__name__)

# 로깅 설정
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')
app.logger.setLevel(logging.ERROR)

# CORS 활성화
CORS(app)

# 이메일 설정
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'winwalking1106@dneuro.ai'  # Gmail 계정
app.config['MAIL_PASSWORD'] = 'wxyeqzazyidmjxqh'  # 앱 비밀번호

# Mail 초기화
mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        # 클라이언트 요청에서 데이터 가져오기
        data = request.json
        name = data.get("name")  # 작성자 이름
        email = data.get("email")  # 작성자 이메일
        company = data.get("company")  # 회사 이름
        message_body = data.get("message")  # 메시지 내용

        # 이메일 메시지 생성
        msg = Message(
            subject=f"[문의] {name} ({company})",
            sender=email,  # 작성자 이메일을 발신자로 설정
            recipients=['winwalking1106@dneuro.ai'],  # 고정된 수신자 이메일
            body=f"""
안녕하세요,

아래는 사용자로부터 접수된 문의 내용입니다:

이름: {name}
이메일: {email}
회사명: {company}

메시지:
{message_body}

감사합니다.
"""
        )

        # 이메일 전송
        mail.send(msg)
        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({"message": "Failed to send email", "error": str(e)}), 500

if __name__ == "__main__":
    app.run("0.0.0.0")