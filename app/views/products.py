from flask.blueprints import Blueprint
from flask import request
from uuid import uuid4
from flask import send_file
from app.models import Product,User,Depts
from app import API_PREFIX, db, qcode
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_wtf import FlaskForm
from wtforms import StringField,SelectMultipleField,FileField
from wtforms.validators import DataRequired
from flask import jsonify
from app import logger
from datetime import datetime
import base64

products_bp = Blueprint("products",__name__,url_prefix=API_PREFIX+"/products")

class AddProductForm(FlaskForm):
    notes = StringField(validators=[DataRequired()])
    verifier_depts = SelectMultipleField(choices=[Depts.LEVEL_1,Depts.LEVEL_2,Depts.LEVEL_3])

class VerificationForm(FlaskForm):
    image = FileField(validators=[DataRequired()])


@products_bp.post("/")
@jwt_required()
def add_product():
    form = AddProductForm(data=request.json)
    if not form.validate():
        return jsonify(form.errors),422


    id:str = str(uuid4().hex)
    current_user = get_jwt_identity()
    user:User = User.query.filter_by(username=current_user)

    baseImage = qcode.generate(id)
    baseImage.save(f"../assets/{id}.png")

    product = Product()
    product.id = id
    product.notes = form.notes.data
    product.created_by = user.id
    product.verifier_depts = ",".join(form.verifier_depts.data)

    db.session.add(product)
    db.session.commit()

    return send_file(baseImage,mimetype="image/png")
    


@products_bp.post("<id>/verification")
@jwt_required
def check_code(id:str):
    
    form = VerificationForm(data=request.form)
    if not form.validate():
        return jsonify(form.errors),422
    
    product:Product = Product.query.find(id)
    username = get_jwt_identity()
    user:User = User.query.filter_by(username=username)

    if product is None:
        # record incident
        logger.recordProductMissing(id)
        return "No such product",404

    
    if product.verified_by is not None:
        # record incident
        product_copy = base64.b64encode(request.files.get('image').read())
        logger.recordDuplicateProduct(product.id,product_copy)
        return "Product already verified",409

    if user.dept not in product.verifier_depts.split(","):
        # record incident
        logger.recordProductViolation(product.id,user.id)
        return "This user cannot verify product",403
    

    product.verified_by = user.id
    product.verified_at = datetime.now()
    product.verifier_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 
    db.session.commit()

    return f"Product {id} verification successful"

    
    


