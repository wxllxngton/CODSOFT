from flask import Flask, redirect,request,render_template, url_for
from flask_bootstrap import Bootstrap
from db_config import TaskToday, TaskNTS, TaskForever, database_tnts


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# --------------------------- DATABASE CONFIG ----------------------------------#
# Create tables
database_tnts.connect()
database_tnts.create_tables([TaskToday, TaskNTS, TaskForever], safe=True)
database_tnts.close()
#--------------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list', methods=['GET','POST'])
def list():
    query = TaskToday.select()
    return render_template('list.html', query=query)


@app.route('/complete/<int:id>')
def complete(id):
    if TaskToday.get(TaskToday.id == id):
        query = TaskToday.get(TaskToday.id == id)
        query.delete_instance()
        return redirect(url_for('list'))
    return render_template('list.html')


@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        query = TaskToday(task=request.form["task_name"])
        query.save()  # save() returns the number of rows modified.
        return redirect(url_for('list'))
    return render_template('list.html')

#------------------------------------------------------------------------------#

#----------------------------- NON-TIME-SENSITIVE ------------------------------#

@app.route('/list_nts', methods=['GET','POST'])
def list_nts():
    query = TaskNTS.select()
    return render_template('list_nts.html', query=query)


@app.route('/complete_nts/<int:id>')
def complete_nts(id):
    if TaskNTS.get(TaskNTS.id == id):
        query = TaskNTS.get(TaskNTS.id == id)
        query.delete_instance()
        return redirect(url_for('list_nts'))
    return render_template('list_nts.html')


@app.route('/add_nts', methods=['GET','POST'])
def add_nts():
    if request.method == 'POST':
        query = TaskNTS(task=request.form["task_name"])
        query.save()  # save() returns the number of rows modified.
        return redirect(url_for('list_nts'))
    return render_template('list_nts.html')

#------------------------------------------------------------------------------#

#----------------------------------- FOREVER ----------------------------------#

@app.route('/list_forever', methods=['GET','POST'])
def list_forever():
    query = TaskForever.select()
    return render_template('list_forever.html', query=query)


@app.route('/complete_forever/<int:id>')
def complete_forever(id):
    if TaskForever.get(TaskForever.id == id):
        query = TaskForever.get(TaskForever.id == id)
        query.delete_instance()
        return redirect(url_for('list_forever'))
    return render_template('list_forever.html')


@app.route('/add_forever', methods=['GET','POST'])
def add_forever():
    if request.method == 'POST':
        query = TaskForever(task=request.form["task_name"])
        query.save()  # save() returns the number of rows modified.
        return redirect(url_for('list_forever'))
    return render_template('list_forever.html')

#------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=True)
