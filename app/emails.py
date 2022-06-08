from flask_mailing import Message
from flask import current_app, jsonify
from app import mail


async def send_email(to, subject, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        subject=str(app.config['FLASKY_MAIL_SUBJECT_PREFIX'])+' '+subject,
        recipients=[to],
        template_body={
            'new_user': kwargs.get('new_user.username')
        }

    )

    await mail.send_message(msg, template_name='auth/email.html')
    return jsonify(status_code=200, content={"message": "Email has been sent."})
