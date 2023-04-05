from flask import jsonify, request, Blueprint
from supabaseinfo import supabase


# Blueprint Configuration
users_bp = Blueprint(
    'users_bp', __name__
)

# retornar todos os usuarios da tabela usuarios: nome, telefone, email, templates
@users_bp.route('/users/get-all',methods=['GET'])
def get_user_all():
    user = supabase.table('users').select("*").execute()
    print("AQUI: " + user)
    return jsonify(user)

# retornar informações da tabela usuarios: nome, telefone, email, templates
@users_bp.route('/users/get-by-id/<user_id>',methods=['GET'])
def get_user_by_id(user_id):
    try:
        [user] = supabase.table('users').select("*").eq("user_id",user_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. user_id not found"
    else:
        return jsonify(user)

# deletar usuario baseado em seu user_id
@users_bp.route('/users/delete-by-id/<user_id>',methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        [user] = supabase.table('users').delete().eq("user_id",user_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. user_id not found"
    else:
        return "User:{} User_Id:{} deleted".format(user["user_name"], user["user_id"])

# atualizar usuario 
@users_bp.route('/users/update/<user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    userinfo= request.get_json()
    try:
        [user] =supabase.table("users").update({"user_name":userinfo["user_name"],
                                    "cellphone": userinfo["cellphone"],
                                    "email":userinfo["email"],
                                    "templates":userinfo["templates"]}).eq("user_id", user_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. user_id not found"
    else:
        return "User:{} Id:{} updated".format(user["user_name"], user["user_id"])


# criar usuario
@users_bp.route('/users/create',methods=['POST'])
def create_user():
    userinfo= request.get_json()
    try:
        [user] =supabase.table("users").insert({"user_name":userinfo["user_name"],
                                    "cellphone": userinfo["cellphone"],
                                    "email":userinfo["email"],
                                    "templates":userinfo["templates"]}).execute().data
    except KeyError:
        return "KeyError: missing variable definition"
    else:
        return "User:{} User_Id: {} created ".format(user["user_name"], user["user_id"])
