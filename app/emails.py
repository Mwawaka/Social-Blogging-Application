from flask_mailing import Message
from flask import current_app, jsonify, render_template
from app import mail


        
async def send_email(to,subject,template,**kwargs):
    app=current_app._get_current_object()
    msg=Message(str(app.config['FLASKY_MAIL_SUBJECT_PREFIX'])+' '+subject,sender=app.config['MAIL_FROM'],recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template +'.html',**kwargs)
    
    await mail.send_message(msg)
    return jsonify(status_code=200,content={"message":"Email has been sent."})
    