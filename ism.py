import os
import re
import subprocess
from influxdb import InfluxDBClient
import json
import time

taghost = os.environ["TAGHOST"]
influxhost = os.environ["INFLUXHOST"]
influxport = os.environ["INFLUXPORT"]
influxuser = os.environ["INFLUXUSER"]
influxpass = os.environ["INFLUXPASS"]
influxdatabasename = os.environ["INFLUXDATABASENAME"]
sleeptime = int(os.environ["INTERVAL"])
server_id = int(os.environ["SERVER_ID"])

while True:

  command = 'speedtest --accept-license --accept-gdpr -f json'
  if server_id > 0:
    command += ' -s '
    command += str(server_id)

  response = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
  data = json.loads(response)

  speed_data = [
          {
              "measurement" : "internet_speed",
              "tags" : {
                  "host": taghost
                  },
              "fields" : {
                  "download" : float(data['download']['bandwidth']) * 8,
                  "upload" : float(data['upload']['bandwidth']) * 8,
                  "ping" : float(data['ping']['latency']),
                  "jitter" : float(data['ping']['jitter'])
                  }
              }
          ]

  print(json.dumps(data, indent = 1))
  print(json.dumps(speed_data, indent = 1))

  client = InfluxDBClient(influxhost, influxport, influxuser, influxpass, influxdatabasename)

  client.write_points(speed_data)
  time.sleep(sleeptime)
