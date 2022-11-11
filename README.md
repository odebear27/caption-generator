# Caption Generator
## My Final Project for Harvard's CS50x Introduction to Computer Science
#### Video Demo: https://youtu.be/C4anVtuN54k
#### Features
*** [Flask](https://flask.palletsprojects.com/en/2.2.x/)
*** [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/)
*** [Flask-MySQLdb](https://flask-mysqldb.readthedocs.io/en/latest/)
*** [Jinja2](https://svn.python.org/projects/external/Jinja-2.1.1/docs/_build/html/index.html)
*** [Pillow](https://pillow.readthedocs.io/en/stable/)
#### Description:
This web application helps users to add captions to images ('png', 'jpg', 'jpeg', 'gif').  
This web application runs on Flask and is connected to MySQL database via MySQL Connector and Flask-MySQLdb. The file details are stored in cs50file.db.  
Jinja2 is used to extend layout.html to all html pages.  
Pillow is used to generate captions on the image and to save the generated image to the directory.
#### Walkthrough:
The user starts off with the Landing Page asking him to choose a file to upload.  
![landing_page](https://user-images.githubusercontent.com/101394672/201252524-75402df8-5c3f-4e34-8820-9c3ef8733d76.png)

Upon pressing the `Upload` button, the file will be saved to the `Uploads` folder in the directory and the user will be directed to the Generate Caption page.  
![generatecaption_page](https://user-images.githubusercontent.com/101394672/201252699-08d57438-cb4d-4f43-995d-2dfb53a74a15.png)

The user can choose the font and input the words for `Top Caption` and `Bottom Caption` respectively, before pressing the `Generate` button.  
![choosefont_input](https://user-images.githubusercontent.com/101394672/201252820-316625f1-8c11-4688-a8ff-1aa7fa8487bd.png)

Upon pressing the `Generate` button, a temp image will appear with the captions generated on the image with the user's chosen font. The user will be redirected to the Landing Page.  
![generatedimage](https://user-images.githubusercontent.com/101394672/201253144-9a1f4866-9344-4155-85b1-b6812b004ffc.png)

The generated image can be found in the `generated` folder in the directory.  
![generated_folder](https://user-images.githubusercontent.com/101394672/201253275-763b368c-d84c-48d8-a224-bb204f929e5f.png)

The details of the file (fileid, filename, filelocation, generatedlocation) will be saved in cs50file database in MySQL.  
![mysql](https://user-images.githubusercontent.com/101394672/201253406-e69b5e7f-dec8-4a1e-b9f5-4d477aef83d1.png)

#### Improvements in the Future:
The user could be given the opton to choose what colour and the exact position where he wants the caption to be.
