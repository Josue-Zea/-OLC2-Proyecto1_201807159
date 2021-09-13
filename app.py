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

class MyForm1(FlaskForm):
    source_code = CodeMirrorField(language='julia', config={'lineNumbers': 'true', 'smartIndent': 'true'})
    submit = SubmitField('Submit')
    
@app.route('/', methods = ['GET', 'POST'])
def index():
    form = MyForm1()
    salida = ""
    text = form.source_code.data
    if text == None or text == "":
        salida = ""
    else:
        salida = executeCode(text)
    return render_template('index.html',form=form, salida=salida)

if __name__ == "__main__":
    app.run(debug=True)