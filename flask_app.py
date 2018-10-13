from flask import Flask, render_template, request
from feature_estimate import formulate_query, fetch_data, crunch_stats

app = Flask(__name__)


DEFAULT_QUALIFIERS = {
    'state':'closed',
    'is': 'merged',
    'type': 'pr',
    'review': 'approved'
}
API_URL="https://api.github.com/search/issues"
access_token = '17d68145f02692b64c08b2067c1e59a65c940604'
authentication = {'Authorization':'token'+' '+access_token}


@app.route('/')
def query():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      query_requested = request.form.get('query_string')
      query_term =query_requested.replace(" ", "+")
      query_string = formulate_query(str(query_term), **DEFAULT_QUALIFIERS)
      pagination = "&per_page=100"

      final_url = API_URL+query_string+pagination
      data = fetch_data(final_url, authentication)
      stats = crunch_stats(data)
      stats.update({"feature":query_requested})

      return render_template("result.html",
                             result = stats)

if __name__ == '__main__':
   app.run(debug = True)
