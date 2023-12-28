from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__,template_folder='template')

# Database configuration
# ...

@app.route('/home1.html')
def index():
    return render_template('home1.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        password = request.form['pass']
        confirm_password = request.form['cpass']
        email = request.form['email']
        mobile_number = request.form['mobile_no']

        # Check if the entered passwords match
        if password != confirm_password:
            return "Passwords do not match!"

        # Insert data into the database
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='project_v'
            )

            if conn.is_connected():
                cursor = conn.cursor()

                # Check if the mobile number already exists in the database
                cursor.execute("SELECT * FROM register WHERE mobile_number = %s", (mobile_number,))
                if cursor.fetchone():
                    return "Mobile number already exists!"

                insert_query = "INSERT INTO register (firstName, lastName1,Email, MobileNumber,Password) VALUES (%s, %s, %s, %s, %s)"
                values = (firstname, lastname,  email, mobile_number,password)

                cursor.execute(insert_query, values)
                conn.commit()
                print("Data inserted successfully")

                cursor.close()

        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")

        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

        # Redirect to another page after successful registration
        # Replace 'success.html' with your success pag
        return redirect(url_for('login'))
    return render_template('register.html')




@app.route('/login1.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        # Verify if the email and password match an existing user
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='project_v'
            )

            if conn.is_connected():
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM register WHERE Email = %s AND Password = %s", (email, password))
                user_data = cursor.fetchone()

                if user_data:
                    user_type = user_data[6]  # Assuming user type is in the 7th column (change as per your schema)
                    if user_type == 'student':
                        return redirect(url_for('student_page'))
                    elif user_type == 'admin':
                        return redirect(url_for('admin_page'))
                    elif user_type == 'employee':
                        return redirect(url_for('employee_page'))

                cursor.close()

        except mysql.connector.Error as e:
            print(f"Error logging in: {e}")

        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    return render_template('login1.html')

# Define routes for different user types
@app.route('/student_page')
def student_page():
    # Logic for rendering student page
    return render_template('student.html')

@app.route('/admin_page')
def admin_page():
    # Logic for rendering admin page
    return render_template('admin.html')

@app.route('/employee_page')
def employee_page():
    # Logic for rendering employee page
    return render_template('employee.html')

if __name__ == '__main__':
    app.run(debug=True)