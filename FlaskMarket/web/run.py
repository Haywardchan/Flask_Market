from market import app
import os
#  run this command to run the application in Debug mode
# docker run -p 5000:5000 -e DEBUG=1 flask_app_dev <imae-name>
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('DEBUG')=='1') 
    # IP=0.0.0.0 for all internet connections