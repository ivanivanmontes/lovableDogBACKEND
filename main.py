from init import app
from routes.pin_routes import *
from routes.db_routes import *
from routes.user_routes import *
from routes.s3_routes import *

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3000, ssl_context='adhoc')
    app.run(port=3000)


