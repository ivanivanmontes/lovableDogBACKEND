from init import app
from routes.pin_routes import *
from routes.db_routes import *
from routes.user_routes import *

if __name__ == '__main__':
    app.run(port=3000)

