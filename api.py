from flask import Flask
from flask_mail import Mail, Message 
import os

app=Flask(__name__)
mail = Mail(app) # instantiate the mail class 
   
# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'user@gmail.com'  # update valid mail id
app.config['MAIL_PASSWORD'] = '********'   # add password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/health")
def index():
    return 'Health Monitoring Tool'

@app.route("/health/device_status/<host>", methods=['GET'])
def device_status_api(host=None):
	try:
		if host:
			device_status = os.system(f"ping -n 1 {host}")
			if device_status:
				raise Exception(f"Device {host} is down")
			return "Status: OK"
	except Exception as error_msg:
		send_email(str(error_msg), host)
		return "Status: Down. Email sent"

def send_email(error_msg, host): 
   mail_user = f'{app.config.get("MAIL_USERNAME")}'
   msg = Message( 
                f'Health_Report - {host}', 
                sender = mail_user, 
                recipients = [mail_user,] 
               )
   msg.body = error_msg
   mail.send(msg)


if __name__ == "__main__":
	app.run(debug = True)
