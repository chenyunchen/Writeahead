#-*- coding: utf8 -*-
import flask, json
import os
import time
import urllib2
import GetSuggestion as AAN
app = flask.Flask(__name__)

app.secret_key = 'gina'

@app.route('/_show_words')
def add_numbers():
    text = flask.request.args.get('text')
    return flask.jsonify(result=text)

@app.route("/aangetSuggestion")
def aangetSuggestion():
    '''獲得輸入的字串, 回傳建議字'''
    text = flask.request.args['text'].strip()
    text = text.split()
    if len(text) > 1:
        # print text[-2]
        if text[-2][-1] == ',' or text[-2][-1] == '.' or text[-2][-1] == '!' or text[-2][-1] == '?':
            text[-2] = text[-2][-1]
        # print "I get the query:",' '.join(text[-2:])
        result = AAN.getWordSuggestion(' '.join(text[-2:]))
        # print result
        return json.dumps(result)
    else:
        return ''

@app.route("/lexgetSuggestion")
def lexgetSuggestion():
    '''獲得輸入的字串, 回傳建議字'''
    text = flask.request.args['text'].strip()
    text = text.split()
    textarray = []
    if len(text) > 1:
        # print text[-2]
        if text[-2][-1] == ',' or text[-2][-1] == '.' or text[-2][-1] == '!' or text[-2][-1] == '?':
            text[-2] = text[-2][-1]
        # print "I get the query:",' '.join(text[-2:])
        result = AAN.getPhraseSuggestion(' '.join(text[-2:]))
        for textjson in result:
          if textjson == 'a':
            textarray.append({"name": ' a'})
          else:
            textarray.append({"name": textjson})
        print textarray
        if not textarray:
          return json.dumps([{"name": "no recommendation :("}])
        else:
          return json.dumps(textarray)
    else:
      return json.dumps([{"name": "no recommendation :("}])

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/request', methods=['POST'])
def jsonreq():
    member = ''.join(json.loads(flask.request.data)["id"])
    data = json.loads(urllib2.urlopen("https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token="+member).read())["id"]
    if os.path.exists("documents/"+data+".txt"):
      article = ''
      with open("documents/"+data+".txt") as the_file:
        for line in the_file.readlines():
           article += line
      article = article.split("===")
      articlejson = {
          "time": article[0],
          "firstparagraph": article[1],
          "secondparagraph": article[2],
          "thirdparagraph": article[3],
          "clickevent1": article[4],
          "clickevent2": article[5],
          "clickevent3": article[6]
      }
      return json.dumps(articlejson)
    else:
      with open("documents/"+data+".txt","w") as the_file:
        the_file.write("")
      return ''

@app.route('/articlesave', methods=['POST'])
def articlesave():
  articles = json.loads(flask.request.data)
  accessagree = ''.join(articles["accessagree"])
  if accessagree:
    data = json.loads(urllib2.urlopen("https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token="+accessagree).read())["id"]
    firstparagraph = ''.join(articles["firstparagraph"])
    secondparagraph = ''.join(articles["secondparagraph"])
    thirdparagraph = ''.join(articles["thirdparagraph"])
    clickevent1 = ''.join(articles["clickevent1"])
    clickevent2 = ''.join(articles["clickevent2"])
    clickevent3 = ''.join(articles["clickevent3"])
    t = time.time()
    tt = time.strftime('%Y-%m-%d', time.localtime(t))
    fcontent = tt + "===" + firstparagraph + "===" + secondparagraph + "===" + thirdparagraph + "===" + clickevent1 + "===" + clickevent2 + "===" + clickevent3
    if os.path.exists("documents/"+data+".txt"):
      with open("documents/"+data+".txt","w") as the_file:
        the_file.write(fcontent.encode("utf8"))
  else:
    pass
  return ''

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument(
        "-d", "--debug", action="store_true", dest="debug_mode",
        help="run in debug mode", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=7878)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port, 'host':'127.0.0.1'}

    if cmd_args.debug_mode == False:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False
        app_options["host"] = "127.0.0.1"

    app.run(**app_options)
