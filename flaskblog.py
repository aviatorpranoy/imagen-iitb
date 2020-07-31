from flask import Flask, render_template, url_for, request, jsonify, make_response
import render, json

app = Flask(__name__)

posts = [
	{
		'author': 'Alankar',
		'title': 'Blog Post 1',
		'content': 'First Post Content. Lorem Ipsum.',
		'date_posted': 'July 24, 2020'
	},
	{
		'author': 'Pranoy',
		'title': 'Blog Post 2',
		'content': 'Second Post Content. Lorem Ipsum.',
		'date_posted': 'July 25, 2020'
	}
]
sums=0

@app.route("/")
@app.route("/home")
def home():
	#return pt.main()
    return render_template('data.html')

@app.route("/blog")
def blog():
    return render_template('home.html', posts=posts, title='Blog')

@app.route("/about")
def about():
    return render_template('about.html', title='Team')

@app.route("/test")
def test():
    return render_template('test.html', title='Test')

@app.route("/process", methods=["POST"])
def process():
	print("process is called")
	if request.method == "POST":
		clicked=request.form['data']
    	# sum=render.add(a,b,c)
		#print(clicked)
		#print(type(clicked))
		first = clicked.split(";")[0]
		
		a=int(first)

		sums = a
		print(type(sums))
		#print(type(sums))
		#def display(sums):
		print(sums)
		return json.dumps({"sum" : sums})

@app.route("/process1", methods=["POST"])
def process1():
	print("process1 is called")
	if request.method == "POST":
		clicked=request.form['data']
    	# sum=render.add(a,b,c)
		#print(clicked)
		#print(type(clicked))

		second = clicked.split(";")[1]
		b=int(second)
		copya=sums
		
		sums = render.execute2(copya, b)
		print(type(sums))
		#print(type(sums))
		#def display(sums):
		print(sums)
		return json.dumps({"sum" : sums})

@app.route("/process2", methods=["POST"])
def process2():
	print("process2 is called")
	if request.method == "POST":
		clicked=request.form['data']
    	# sum=render.add(a,b,c)
		#print(clicked)
		#print(type(clicked))
		#first = clicked.split(";")[0]
		#second = clicked.split(";")[1]
		third = clicked.split(";")[2]
		print(type(third))
		c=int(third)
		print(type(c))
		d=sums

		sums = render.execute3(c,d)
		print(type(sums))
		print(sums)
		#console.log(sums)
		print(sums)
		return json.dumps({"sum" : sums})

if __name__ == "__main__":
    app.run(debug=True)