from flask import Flask, request, render_template
# import nltk
# nltk.download('stopwords')
from interception2 import intrsp
from stemmer2 import stemm_match
from word_vec2 import wrd_vec_match

app = Flask(__name__)


@app.route('/')
def indx():
    # return 'HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEELP!!'
    return render_template('main.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
    req = request.form['a']
    f = open('table.html', 'r')
    return """

    <!DOCTYPE html>
<html>
<body height="50em">
<div width="50%" style="width: 50%; float: left;">
<h2>find CV</h2>
<p>enter your request like, separating parts by coma, like: <b> Business-focused high-level process improvement, Adaptive foreground website</b> </p>
<p>you can choose several of characteristics from responsibility column</p>

<form action="/process" method="post" enctype="text">
  <input type="text" id="a" name="a"  style='width:50em' value='""" + req + """'>
  <br><br>

  <input type="submit">

<br><br>
  Direct matching: <br><br>
  <output name="x">""" + intrsp(req) + """</output>
  <br><br>
    Stem matching: <br><br>

  <output name="x1">""" + stemm_match(req) + """</output>
  <br><br>
      deep matching: <br><br>

  <output name="x2">""" + wrd_vec_match(req) + """</output>
  <br><br>
  <input type="submit">
</form>
</div>
<div style="width: 50%; float: left; height: 50em; overflow: scroll;">""" + f.read() + """
</div>

</body>
</html>
"""


if __name__ == '__main__':
    app.run()
