from fabric.api import env
from flask import render_template,Flask,request,redirect



app = Flask(__name__,static_url_path='')

@app.route("/login.html",methods=['POST','GET'])
 
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin123': 
                error= "sorry"
        else:
            return redirect(url_for('index'))
    return render_template('login.html',error=error)
 
 
@app.route("/index.html")
def index():
    return render_template('index.html')

@app.route("/tables.html")
def tables():
   	return render_template('tables.html')

@app.route("/form-compiled.html")
def form_compiled():
	return render_template('form-compiled.html')

@app.route("/form-interpreted.html")
def form_interpreted():
	return render_template('form-interpreted.html')

@app.route("/form-common.html")
def form_common():
	return render_template('form-common.html')

@app.route("/form-validation.html")
def form_validation():
	return render_template('form-validation.html')

@app.route("/form-wizard.html")
def form_wizard():
	return render_template('form-wizard.html')

@app.route("/buttons.html")
def buttons():
	return render_template('buttons.html')

@app.route("/interface.html")
def interface():
	return render_template('interface.html')

@app.route("/grid.html")
def grid():
	return render_template('grid.html')

@app.route("/invoice.html")
def invoice():
	return render_template('invoice.html')

@app.route("/chat.html")
def chat():
	return render_template('chat.html')

@app.route('/calendar.html')
def calendar():
	return render_template('calendar.html')

@app.route('/gallery.html')
def gallery():
	return render_template('gallery.html')

@app.route('/charts.html')
def charts():
	return render_template('charts.html')

@app.route('/widgets.html')
def widgets():
	return render_template('widgets.html')


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=80, 
        debug=True)
