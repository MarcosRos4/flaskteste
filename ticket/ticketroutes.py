from flask import jsonify, request, Blueprint
from supabaseinfo import supabase

# Blueprint Configuration
ticket_bp = Blueprint(
    'ticket_bp', __name__
)

# criar ticket
@ticket_bp.route('/ticket/create',methods=['POST'])
def create_ticket():
    ticketinfo= request.get_json()
    try:
        [ticket] =supabase.table("ticket").insert({"user_id":ticketinfo["user_id"],
                                    "description": ticketinfo["description"],
                                    "image_link":ticketinfo["image_link"]}).execute().data
    except KeyError:
        return "KeyError: missing variable definition"
    else:
        return "ticket:{} created at {}".format(ticket["ticket_id"], ticket["created_at"])

# deletar ticket baseado em ticket_id
@ticket_bp.route('/ticket/delete-by-id/<ticket_id>',methods=['DELETE'])
def delete_ticket_by_ticket_id(ticket_id):
    try:
        [ticket] = supabase.table('ticket').delete().eq("ticket_id",ticket_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. ticket_id not found"
    else:
        return "ticket deleted: {}".format(ticket["ticket_id"])

# deletar ticket baseado em user_id
@ticket_bp.route('/ticket/delete-by-user_id/<user_id>',methods=['DELETE'])
def delete_ticket_by_user_id(user_id):
    try:
        ticket = supabase.table('ticket').delete().eq("user_id",user_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. user_id not found"
    else:
        return jsonify(ticket)

# acessar ticket baseado em user_id
@ticket_bp.route('/ticket/get-by-user_id/<user_id>',methods=['GET'])
def get_ticket_by_user_id(user_id):
    try:
        ticket = supabase.table('ticket').select("*").eq("user_id",user_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. user_id not found"
    else:
        return jsonify(ticket)

# acessar ticket baseado em ticket_id
@ticket_bp.route('/ticket/get-by-ticket_id/<ticket_id>',methods=['GET'])
def get_ticket_by_ticket_id(ticket_id):
    try:
        [ticket] = supabase.table('ticket').select("*").eq("ticket_id",ticket_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. ticket_id not found"
    else:
        return jsonify(ticket)

# acessar todos os tickets
@ticket_bp.route('/ticket/get-all',methods=['GET'])
def get_ticket_all():
    ticket = supabase.table('ticket').select("*").execute().data
    
    return jsonify(ticket)
