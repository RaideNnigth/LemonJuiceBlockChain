from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        return render_template(url_for('index'))
        
    else: 
        return render_template('home.html')
    
if __name__ == '__main__':
    app.run(debug=True)
    
    