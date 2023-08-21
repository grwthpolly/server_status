import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import requests
from datetime import datetime
import time
import schedule

# Fetch the service account key JSON file contents
SECRET_KEY = os.environ["SECRET_KEY"]
cred = credentials.Certificate(SECRET_KEY)
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://grwth-63006-default-rtdb.firebaseio.com/"
})

ref = db.reference('/Status')

url = 'https://app.grwth.hk/status/grwth_stat2.html'


def task():
    r = requests.get(url)
    # json_data = r.json()
    json_data = r.text
    # json_pretty = json.dumps(json_data, sort_keys=True, indent=4)

    time_now = datetime.now()
    current_time = time_now.strftime("%Y-%m-%d %H:%M:%S")

    ref.update({"data": json_data})
    ref.update({"timestamp": current_time})
    print(ref.get())

    error_pos = json_data.find("count") + 9

    if json_data[error_pos:error_pos+1] != "0":
        filename = "error_" + time_now.strftime("%Y%m%d%H%M%S")
        with open(filename + ".json", "w", encoding='utf-8') as f:
            f.write(json_data)


schedule.every().minute.do(task) # Run every minute

while True:
    schedule.run_pending()
    time.sleep(1)
