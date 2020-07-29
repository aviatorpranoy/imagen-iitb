from flask import Flask, render_template, url_for, request, jsonify, make_response
import render

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
	if request.method == "POST":
		clicked=request.form['data']
    	# sum=render.add(a,b,c)
		print(clicked)
		return json.dumps({options})

if __name__ == "__main__":
    app.run(debug=True)