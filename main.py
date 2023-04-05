from flask import Flask

# create flask aplication

app = Flask(__name__)
    #app.config.from_object('config.Config')
@app.route("/")
def default_route():
    return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
with app.app_context():
        # import parts of the aplication firebucks
    from users.usersroutes import users_bp
    from ticket.ticketroutes import ticket_bp
    from template.templateroutes import templates_bp
    from payments.paymentroutes import payments_bp
    
    app.register_blueprint(users_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(payments_bp)
        
app.run(port=5000,host='localhost',debug=True)
