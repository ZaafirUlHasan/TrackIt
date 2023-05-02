from flask import Flask
from views import views
from roblox import roblox
from Mojang import Mojang
from Steam import Steam
from LeagueOfLegends import LeagueOfLegends
from Apex import Apex

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.register_blueprint(roblox, url_prefix="/")
app.register_blueprint(Mojang, url_prefix="/")
app.register_blueprint(Steam, url_prefix="/")
app.register_blueprint(LeagueOfLegends, url_prefix="/")
app.register_blueprint(Apex, url_prefix="/")

if __name__=='__main__':
    app.run(debug=True)
