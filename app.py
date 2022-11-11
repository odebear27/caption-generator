import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_session import Session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from tempfile import mkdtemp

# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# UPLOAD_FOLDER = 'D:/Odelia Tan/Online_courses/edX/3. HarvardX CS50x/week 10_emoji/uploads/'
UPLOAD_FOLDER = './uploads/'
# GENERATED_FOLDER = 'D:/Odelia Tan/Online_courses/edX/3. HarvardX CS50x/week 10_emoji/generated/'
GENERATED_FOLDER = './generated/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def check_path_exists(path):
    isExist = os.path.exists(path)
    return isExist

def make_path(path):
    try: 
        os.mkdir(path)
    except OSError as error: 
        print(error)

if check_path_exists(UPLOAD_FOLDER) == False:
    make_path(UPLOAD_FOLDER)

if check_path_exists(GENERATED_FOLDER) == False:
    make_path(GENERATED_FOLDER)


# Configure application
app = Flask(__name__)

# Create an upload folder to store uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create a generated folder to store generated images
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER

# Connect to MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mydb'
app.config['MYSQL_DB'] = 'cs50file'
mysql = MySQL(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("upload.html")
    
    elif request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filelocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filelocation)
            # return redirect(url_for('download_file', name=filename))

            #Creating a connection cursor
            cursor = mysql.connection.cursor()
            
            #Executing SQL Statements
            cursor.execute("CREATE TABLE IF NOT EXISTS file(fileid int AUTO_INCREMENT, filename varchar (20) NOT NULL, filelocation VARCHAR (100) NOT NULL, generatedlocation VARCHAR (100), PRIMARY KEY (fileid))")
            record = [filename, filelocation, '']
            cursor.execute("INSERT INTO file (filename, filelocation, generatedlocation) VALUES(%s,%s,%s)", record)
            
            #Saving the Actions performed on the DB
            mysql.connection.commit()
            
            #Closing the cursor
            cursor.close()

            return render_template("generatecaption.html")

@app.route("/generatecaption", methods=["GET", "POST"])
def generate_caption():
    """Enter caption to generate"""
    if request.method == "GET":
        return render_template("generatecaption.html")

    elif request.method == "POST":
        # Get input from user
        font = request.form.get("font")
        print(font)
        top_caption = request.form.get("topcaption")
        bottom_caption = request.form.get("bottomcaption")

        # Read file name from file path
        # img_path = 'D:/Odelia Tan/Online_courses/edX/3. HarvardX CS50x/week 10_emoji/uploads/pic1.png'

         #Creating a connection cursor
        cursor = mysql.connection.cursor()
        
        #Executing SQL Statements
        # cursor.execute("SELECT filelocation FROM file WHERE fileid=1")
        cursor.execute("SELECT filelocation FROM file ORDER BY fileid DESC LIMIT 1")
        print("executed")
        
        img_paths = cursor.fetchall()
        for img_path in img_paths:
            print(img_path)

        # Open an Image
        img = Image.open(img_path[0]) # Index 0 since img_path is a tuple

        # Get Image size
        width, height = img.size
        
        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img)
        
        # Custom font style and font size
        # myFont = ImageFont.truetype('cookie-monster.ttf', 65)
        myFont = ImageFont.truetype(font, 65)
        
        # Add Top Caption to image
        I1.text((50, 20), top_caption, font=myFont, fill =(255, 0, 0))

        # Add Bottom Caption to image
        # I1.text((600, 500), bottom_caption, font=myFont, fill =(255, 0, 0))
        I1.text((width-400, height-100), bottom_caption, font=myFont, fill =(255, 0, 0))
        
        # Display edited image
        img.show()
        
        #Executing SQL Statements
        # cursor.execute("SELECT filename FROM file WHERE fileid=1")
        cursor.execute("SELECT filename FROM file ORDER BY fileid DESC LIMIT 1")
        print("executed")

        filenames = cursor.fetchall()
        for filename in filenames:
            print(filename)

        generatedlocation = os.path.join(app.config['GENERATED_FOLDER'], filename[0])
        
        # Save the edited image
        # img.save("D:/Odelia Tan/Online_courses/edX/3. HarvardX CS50x/week 10_emoji/generated/pic1.png")
        img.save(generatedlocation)

        # Update generatedlocation in table in MySQL
        # record = [generatedlocation]
        record = [generatedlocation, filename]
        # cursor.execute("UPDATE file SET generatedlocation = %s WHERE fileid=1", record)
        cursor.execute("UPDATE file SET generatedlocation = %s WHERE filename=%s", record)
        
        #Saving the Actions performed on the DB
        mysql.connection.commit()

        #Closing the cursor
        cursor.close()

        return redirect("/")

if __name__ == "__main__":
    app.run()