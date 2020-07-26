from flask import Flask, render_template, url_for
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
    return render_template('home.html', posts=posts)

@app.route("/data")
def data():
    return render_template('data.html', title='Data')

@app.route("/about")
def about():
    return render_template('about.html', title='Team')

if __name__ == '__main__':
    app.run(debug=True)
