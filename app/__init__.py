from .app import app
from .routes import main_bp

app.register_blueprint(main_bp)
