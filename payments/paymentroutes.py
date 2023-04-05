from flask import jsonify, request, Blueprint
from supabaseinfo import supabase


# Blueprint Configuration
payments_bp = Blueprint(
    'payments_bp', __name__
)

# criar payment
@payments_bp.route('/payments/create',methods=['POST'])
def create_payment():
    paymentinfo= request.get_json()
    try:
        [payment] =supabase.table("payments").insert({"user_id":paymentinfo["user_id"]}).execute().data
    except KeyError:
        return "KeyError: missing variable definition"
    else:
        return "payment:{} created at {}".format(payment["payment_id"], payment["created_at"])

# deletar payment baseado em payment_id
@payments_bp.route('/payments/delete-by-payment_id/<payment_id>',methods=['DELETE'])
def delete_payment_by_id(payment_id):
    try:
        [payment] = supabase.table('payments').delete().eq("payment_id",payment_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. payment_id not found"
    return "payment deleted: {}".format(payment["payment_id"])

# deletar payment baseado em user_id
@payments_bp.route('/payments/delete-by-user_id/<user_id>',methods=['DELETE'])
def delete_payment_by_user_id(user_id):
    try:
        payment = supabase.table('payments').delete().eq("user_id",user_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. user_id not found"
    else:
        payments_deleted = "Payments Deleted: "
        for id in payment:
            payments_deleted += id["payment_id"] +", "
        return jsonify(payment)

# acessar payment baseado em payment_id
@payments_bp.route('/payments/get-by-payment_id/<payment_id>',methods=['GET'])
def get_payment_by_payment_id(payment_id):
    try:
        [payment] = supabase.table('payments').select("*").eq("payment_id",payment_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. payment_id not found"
    else:
        return jsonify(payment)

# acessar payment baseado em user_id
@payments_bp.route('/payments/get-by-user_id/<user_id>',methods=['GET'])
def get_payment_by_user_id(user_id):
    try:
        payment = supabase.table('payments').select("*").eq("user_id",user_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. user_id not found"
    else:
        return jsonify(payment)

# acessar todos os payments
@payments_bp.route('/payments/get-all',methods=['GET'])
def get_payment_all():
    payment = supabase.table('payments').select("*").execute().data
    
    return jsonify(payment)
