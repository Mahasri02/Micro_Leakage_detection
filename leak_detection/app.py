from flask import Flask, render_template, redirect, url_for, request
from flask_mail import Mail, Message
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Google OAuth setup
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google_bp = make_google_blueprint(
    client_id="YOUR_GOOGLE_CLIENT_ID",
    client_secret="YOUR_GOOGLE_CLIENT_SECRET",
    redirect_to="google_login"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        try:
            msg = Message(
                subject=f"New Message from {name}",
                recipients=['mahasri359@gmail.com'],
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            return render_template("contact.html", message="Your message has been sent successfully!")
        except Exception as e:
            return render_template("contact.html", message=f"Error sending message: {str(e)}")
    return render_template("contact.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Normally you'd send a reset email here
        return redirect(url_for('password_reset_sent'))
    return render_template('forgot_password.html')

@app.route('/password-reset-sent')
def password_reset_sent():
    return "A password reset link has been sent to your email."

@app.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()
    return f"Hello, {user_info['name']}! Welcome to the Smart Leak Detection System."

# ✅ NEW ROUTES for clickable cards
@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)
