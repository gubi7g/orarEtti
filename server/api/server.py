from flask import Flask, request, jsonify
from os import path
import sys
projectRoot = path.abspath('./')
sys.path.append(projectRoot)
import config
import json
import re

# print(config.addresses['out'])

pattern_grupa = re.compile(r'4[1-4]{1}[1-5]{1}\w{1,2}')
Flask.debug = True

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello, World!'

@app.route('/<queryGroup>/<zi>')
def getOrarDay(queryGroup, zi):

  if not pattern_grupa.match(queryGroup):
    return {'error': 'This group doesn\'t exist'}

  print(queryGroup)
  an = int(queryGroup[1])

  with open(path.join(projectRoot, config.addresses['out'], f'orar_an{an}' + '.json')) as f:
    orar = json.load(f)
  for ind, group in enumerate(orar):
    if queryGroup in group['grupa']:
      if group['grupa'].lower() == queryGroup.lower() :
        orar = group
        break
      else:
        orar = [ orar[ind], orar[ind+1] ]
        break
  return jsonify(orar)

@app.route('/<queryGroup>')
def getOrarGroup(queryGroup):

  if not pattern_grupa.match(queryGroup):
    return {'error': 'This group doesn\'t exist'}
  an = int(queryGroup[1])

  with open(path.join(projectRoot, config.addresses['out'], f'orar_an{an}' + '.json')) as f:
    orar = json.load(f)
  
    if len(queryGroup) == 4:
      flagStream = 0
      semigrupe = []
      # vom returna toate semigrupele
      for group in orar:
        if group['grupa'].lower()[0:-1] == queryGroup.lower():
          print(group['grupa'].lower()[0:-1])
          flagStream += 1
          semigrupe.append(group)

        elif flagStream != 0:
          # am prins toate semigrupele
          break

      if semigrupe:
        return jsonify(semigrupe)
      else:
        return {'error': 'Group not found...'}

    if len(queryGroup) == 5:
      # semigrupa unica
      for group in orar:
        if group['grupa'].lower() == queryGroup.lower() :
          orar = group
          break
      else:
        return {'error': 'Group not found...'}
    
    
    return jsonify(orar)



if __name__ == "__main__":
  app.run()