
from app import appl,API_PREFIX
from app.views.register import register
from app.views.login import login

appl.add_url_rule(API_PREFIX+"/users",methods=['POST'],view_func=register)
appl.add_url_rule(API_PREFIX+"/login",methods=['POST'],view_func=login)

from app.views.products import products_bp

appl.register_blueprint(products_bp)


if __name__ == '__main__':
    appl.run(host='0.0.0.0',port=4545)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
