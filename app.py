from Gramatica import executeCode
from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField
from flask_codemirror import CodeMirror
SECRET_KEY = 'secret!'
CODEMIRROR_LANGUAGES = ['julia']
CODEMIRROR_THEME = 'isotope'
CODEMIRROR_ADDONS = (
     ('display','placeholder'),
)
app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)
CodigoReporte = ""

class MyForm1(FlaskForm):
    source_code = CodeMirrorField(language='julia', config={'lineNumbers': 'true', 'smartIndent': 'true'})
    submit = SubmitField('Submit')
    
@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/compiler', methods = ['GET', 'POST'])
def compiler():
    global CodigoReporte
    form = MyForm1()
    salida = ["","",""]
    text = form.source_code.data
    if text == None or text == "":
        salida[0] = ""
    else:
        salida = executeCode(text)
        CodigoReporte = salida[3]
    return render_template('compiler.html',form=form, salida=salida[0], fails=salida[1], tabla = salida[2])

@app.route('/report', methods = ['GET', 'POST'])
def report():
    global CodigoReporte
    code = CodigoReporte.pipe().decode("utf-8")
    return render_template('report.html', codigo=code)

if __name__ == "__main__":
    app.run(debug=True)