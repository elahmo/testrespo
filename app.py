from webapp import app
import schedule
import time
from webapp.core.views import update, news_update


if __name__ == '__main__':
    app.run(debug=True)
