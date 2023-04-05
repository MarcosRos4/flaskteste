from flask import jsonify, request, Blueprint
from supabaseinfo import supabase

# Blueprint Configuration
templates_bp = Blueprint(
    'templates_bp', __name__
)

# criar template
@templates_bp.route('/templates/create',methods=['POST'])
def create_template():
    templateinfo= request.get_json()
    try:
        [template] =supabase.table("templates").insert({"name":templateinfo["name"],
                                    "file_link": templateinfo["file_link"],
                                    "image_link":templateinfo["image_link"],
                                    "video_link":templateinfo["video_link"]}).execute().data
    except KeyError:
        return "KeyError: missing variable definition"
    else:
        return "template:{} created at {}".format(template["template_id"], template["created_at"])

# atualizar template baseado em template_id
@templates_bp.route('/templates/update/<template_id>', methods=['PUT'])
def update_template_by_id(template_id):
    templateinfo= request.get_json()
    try:
        [template] =supabase.table("templates").update({"name":templateinfo["name"],
                                    "video_link": templateinfo["video_link"],
                                    "image_link":templateinfo["image_link"],
                                    "file_link":templateinfo["file_link"]}).eq("template_id", template_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. template_id not found"
    else:
        return "template:{} Id:{} updated".format(template["name"], template["template_id"])

# deletar template baseado em template_id
@templates_bp.route('/templates/delete-by-id/<template_id>',methods=['DELETE'])
def delete_template_by_id(template_id):
    try:
        [template] = supabase.table('templates').delete().eq("template_id",template_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. template_id not found"
    else:
        return "template deleted: {}".format(template["template_id"])

# acessar template baseado em template_id
@templates_bp.route('/templates/get-by-template_id/<template_id>',methods=['GET'])
def get_template_by_template_id(template_id):
    try:
        [template] = supabase.table('templates').select("*").eq("template_id",template_id).execute().data
    except ValueError:
        return "ValueError: not enough values to unpack (expected 1, got 0) e.g. template_id not found"
    else:
        return jsonify(template)

# acessar todos os templates
@templates_bp.route('/templates/get-all',methods=['GET'])
def get_template_all():
    template = supabase.table('templates').select("*").execute().data
    
    return jsonify(template)

