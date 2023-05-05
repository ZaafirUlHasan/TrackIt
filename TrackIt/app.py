from flask import Flask, render_template
from views import views
from roblox import roblox
from Mojang import Mojang
from Steam import Steam
from LeagueOfLegends import LeagueOfLegends

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.register_blueprint(roblox, url_prefix="/")
app.register_blueprint(Mojang, url_prefix="/")
app.register_blueprint(Steam, url_prefix="/")
app.register_blueprint(LeagueOfLegends, url_prefix="/")

@app.route("/")
def index():
    return render_template("index.html")
    
if __name__=='__main__':
    app.run(debug=True)
