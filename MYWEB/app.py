from flask import Flask, request, render_template, redirect, url_for,flash
import csv
import os
import smtplib
from email.message import EmailMessage
import requests
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    if request.method == 'POST':
        Name = request.form['NAME']
        User_Name = request.form['USER_NAME']
        Address = request.form['ADDRESS']
        Mobile = request.form['MOBILE']
        Email = request.form['E-MAIL']
        City = request.form['CITY']
        password = request.form['PASSWORD']
        Account='user'
        
        # Get the current date and time
        date=str(datetime.now().date())
        time=str(datetime.now().time()) 
        
        # Save to CSV
        file_exists = os.path.isfile('registrations.csv')
        print('hello')
        if file_exists:
            with open('registrations.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    existing_user_name = row[1]  # Assuming the username is the second column
                    existing_password = row[2]  # Assuming the password is the third column
                    existing_email = row[5]
                    if User_Name == existing_user_name:
                        return "Username already taken. Please choose a different username."
                    if password == existing_password:
                        return "Password already in use. Please choose a different password."
                    if Email  == existing_email:
                        return "email already in use. Please choose a different email."

           
        with open('registrations.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            
            if not file_exists:
                writer.writerow(['Name', 'User_Name', 'Password', 'Address', 'Mobile', 'Email', 'City','date','time','Account'])
            writer.writerow([Name, User_Name, password, Address, Mobile, Email, City,date,time,Account])
        
    return redirect(url_for('login'))

@app.route('/login.html')
def login():
    return render_template('login.html')



@app.route('/login', methods=['POST', 'GET'])
def go_in():
    if request.method == 'POST':
        u_name = request.form.get('User_Name')
        pass_word = request.form.get('Password')
        date = str(datetime.now().date())
        time = str(datetime.now().time())

        # Check if the registration file exists
        if not os.path.isfile('registrations.csv'):
            return "Registration file does not exist.", 404

        user_found = False
        Name = User_Name = pass_wor = address = Email = Account = ""

        with open('registrations.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == u_name and row[2] == pass_word:
                    user_found = True
                    Name = row[0]
                    User_Name = row[1]
                    pass_wor = row[2]
                    address = row[3]
                    Email = row[5]
                    Account = row[9]
                    break

        if not user_found:
            return "Invalid username or password.", 403

        # Log user login
        log_file_exists = os.path.isfile('logins.csv')
        with open('logins.csv', 'a', newline='') as log_file:
            log_writer = csv.writer(log_file)
            if not log_file_exists:
                log_writer.writerow(['Name', 'User_Name', 'Time', 'Date'])
            log_writer.writerow([Name, User_Name, time, date])

        # Calculate today's sales and identify the highest-selling product
        today_date = datetime.now().date()
        total_sales = {}
        highest_product = None
        highest_sales = 0
        
        if os.path.isfile('payment.csv'):
            with open('payment.csv', 'r') as payment_file:
                payment_reader = csv.reader(payment_file)
                next(payment_reader)  # Skip header if present

                for row in payment_reader:
                    try:
                        product = row[1]  # Product name
                        amount = float(row[2])  # Sales amount
                        sale_date = datetime.strptime(row[3], '%Y-%m-%d').date()  # Date
                    except (IndexError, ValueError):
                        continue  # Skip rows with missing or invalid data

                    if sale_date == today_date:
                        if product not in total_sales:
                            total_sales[product] = 0
                        total_sales[product] += amount

            # Determine the highest-selling product for today
            if total_sales:
                highest_product = max(total_sales, key=total_sales.get)
                highest_sales = total_sales[highest_product]

        total_sales_amount = sum(total_sales.values()) if total_sales else 0

        # Render account page with sales data
        return render_template('account.html', 
                               name=Name, 
                               Address=address, 
                               Email=Email, 
                               User_Name=User_Name, 
                               account=Account, 
                               sale=total_sales_amount, 
                               highest=highest_product, 
                               higher=highest_sales)
 
    return render_template('login.html')

@app.route('/account.html')
def account():
    return render_template('account.html')
@app.route('/account.js')
def accountjs():
    return render_template('account.js')

@app.route('/tobuy.html')
def tobuy():
    return render_template('tobuy.html')

@app.route('/trailer.html')
def trailer():
    return render_template('trailer.html')

@app.route('/payment.html')
def pay():
    return render_template('payment.html')





@app.route('/pay', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            courseid=request.form.get['course']
            Email=request.form['Your_Email']
            amount = int(1500)
            currency = request.form['currency']
            card_number = request.form['card_number']
            exp_month = request.form['exp_month']
            exp_year = request.form['exp_year']
            cvc = request.form['cvc']
            date = str(datetime.now().date())
            time=str(datetime.now().time())
            file_exists1 = os.path.isfile('payment.csv')
            

            def send():
                # Email sender and receiver
                sender_email = "unknownlion001@example.com"
                receiver_email = Email
                password = "Thilo@01"
                # Create the email content using the EmailMessage class
                msg = EmailMessage()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = "payment by you"
                msg.set_content(f"Thankyou for buy our course at  and study well.")
                # Send the email using smtplib
                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use the appropriate SMTP server and port
                        server.starttls()  # Enable TLS for security
                        server.login(sender_email, password)  # Log in to your email account
                        server.send_message(msg)  # Send the email
                        print("Email sent successfully!")
                except Exception as e:
                    print(f"Failed to send email: {e}")
                with open('payment.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
            
            
                    if not file_exists1:
                        writer.writerow(['course', 'amount', 'cardnum', 'expmonth', 'expyear', 'cvc','email','date','time'])
                    writer.writerow([courseid, amount, card_number/6 , exp_month, exp_year,cvc*3,Email,date,time])
            
            
            with open('registrations.csv', 'r', newline='') as file:
                reader=csv.reader(file)
                for row in reader:
                    if row[5]==Email:
                        name1=row[0]
                        name2=row[1]
                        phone=row[4]
                        address=row[3]
                        city=row[6]



            payload = {
    'merchant_id': '1228195',  # Replace with your actual Merchant ID
    'return_url': 'https://wuzoon.com/course',
    'cancel_url': 'https://wuzoon.com/cancel',
    'notify_url': 'https://wuzoon.com/notify',
    'order_id': '12345',
    'items': courseid,
    'currency': currency,
    'amount': amount,
    'first_name': name1,
    'last_name': name2,
    'email': Email,
    'phone': phone,
    'address': address,
    'city': city,
    'country': 'Sri Lanka',
    'payment_method': 'VISA'
}


            headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer your_api_key'  # Include your API key here
}

            response = requests.post('https://sandbox.payhere.lk/pay/checkout', data=payload, headers=headers)

            if response.status_code == 200:
                print("Payment processed successfully")
                send()
                if courseid=='pyadvance':
                    courses='<embed src="/static/pybasic.mp4" id="pybasic" height="500px" width="1000px"><br><span>{{nocourses | safe}}</span>'
                return render_template('course.html',no_courses=courses)
            else:
                print("Payment failed")
                return render_template('payment.html')
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for('payment'))
    return render_template('payment.html')



@app.route('/cancel')
def cancel():
    return "Payment was canceled."



@app.route('/course.html')
def course():
    return render_template('course.html')


            


@app.route('/report.html')
def report():
    return render_template('report.html')

@app.route('/supperadmin.html')
def sadmin():
    return render_template('supperadmin.html')

@app.route('/admin.html')
def admin():
    return render_template('admin.html')
    
@app.route('/user.html')
def user():
    return render_template('user.html')

@app.route('/registration', methods=['GET'])
def registration():
    # Path to your CSV file
    csv_file_path = 'registrations.csv'
    
    # Start the HTML table
    table_html = '<table><thead><tr>'
    
    # Read the CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        
        # Read the header (first row) and create table headers
        headers = next(reader, None)
        if headers:
            table_html += ''.join(f'<th>{header}</th>' for header in headers)
            table_html += '</tr></thead><tbody>'
            
            # Read the rest of the rows and create table rows
            for row in reader:
                table_html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    
    # Close the table
    table_html += '</tbody></table>'
    
    return table_html, 200, {'Content-Type': 'text/html'}

@app.route('/payment', methods=['GET'])
def payment():

    return '<h2>Payment Details</h2><p>Here are your payment options.</p>', 200, {'Content-Type': 'text/html'}

@app.route('/log_in', methods=['GET'])
def log_in():
    csv_file_path = 'logins.csv'
    
    # Start the HTML table
    table_html = '<table><thead><tr>'
    
    # Read the CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        
        # Read the header (first row) and create table headers
        headers = next(reader, None)
        if headers:
            table_html += ''.join(f'<th>{header}</th>' for header in headers)
            table_html += '</tr></thead><tbody>'
            
            # Read the rest of the rows and create table rows
            for row in reader:
                table_html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    
    # Close the table
    table_html += '</tbody></table>'
    
    return table_html, 200, {'Content-Type': 'text/html'}

@app.route('/highersales', methods=['GET'])
def highersales():
    counts = {}  # Dictionary to store counts of each value
    
    file_exists1 = os.path.isfile('logins.csv')
    if file_exists1:
        with open('logins.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue  # Skip empty rows
                
                value = row[0]  # Get the value from the first column
                
                # Count occurrences of each value
                if value in counts:
                    counts[value] += 1
                else:
                    counts[value] = 1

    # Sort counts in descending order by count value
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    
    # Prepare results for HTML
    results = [f'{item[0]} {item[1]}' for item in sorted_counts[:5]]
    
    # Ensure there are exactly 5 entries for consistent display
    while len(results) < 5:
        results.append('--------')

    # Generate HTML response
    html_content = f"""
    <div>
        <span><h3>{results[0]}</h3></span><br>
        <span><h3>{results[1]}</h3></span><br>
        <span><h3>{results[2]}</h3></span><br>
        <span><h3>{results[3]}</h3></span><br>
        <span><h3>{results[4]}</h3></span>
    </div>
    """
    return html_content

@app.route('/show', methods=['GET'])
def show():
    file_exists1 = os.path.isfile('deatails.csv')
    with open('payment.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            course=row[0]
            email=row[6]
            with open('registrations.csv','r') as file:
                reader1=csv.reader(file)
                for row1 in reader1:
                    if email==row1[5]:
                        user=row1[1]
                        city=row1[6]
            user1=user
            city1=city
            time=row[7]
        with open('payment1.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists1:
                writer.writerow(['course','user','email','city','time'])
            writer.writerow([course,user1,email,city1,time ])

    # Start the HTML table
    table_html = '<table><thead><tr>'
    
    # Read the CSV file
    with open('payment1', 'r') as file:
        reader = csv.reader(file)
        
        # Read the header (first row) and create table headers
        headers = next(reader, None)
        if headers:
            table_html += ''.join(f'<th>{header}</th>' for header in headers)
            table_html += '</tr></thead><tbody>'
            
            # Read the rest of the rows and create table rows
            for row in reader:
                table_html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    
    # Close the table
    table_html += '</tbody></table>'
    
    return table_html, 200, {'Content-Type': 'text/html'}


    

@app.route('/mypayment', methods=['GET'])
def mypayment():
    return '<h2>My Payment Details</h2><p>Details about your payments.</p>', 200, {'Content-Type': 'text/html'}

@app.route('/bought', methods=['GET'])
def bought():
    return '<h2>Bought Items</h2><p>Details about items you have bought.</p>', 200, {'Content-Type': 'text/html'}
    

if __name__ == "__main__":
    app.run(debug=True)
