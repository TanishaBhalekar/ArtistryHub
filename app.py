from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, current_user
from config import Config
from models import db, User, Artwork
from services.analytics import get_user_analytics
from routes.auth import auth as auth_blueprint
from routes.portfolio import portfolio as portfolio_blueprint
from routes.commissions import commissions as commissions_blueprint
from routes.ai import ai as ai_blueprint

def create_app(config_class=Config):
    """Application factory for ArtistryHub."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(portfolio_blueprint)
    app.register_blueprint(commissions_blueprint)
    app.register_blueprint(ai_blueprint)

    # Core routes
    @app.route('/')
    def index():
        return render_template('landing/index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        artworks = Artwork.query.order_by(Artwork.created_at.desc()).all()
        analytics = get_user_analytics(current_user.id)
        return render_template('dashboard/index.html', artworks=artworks, analytics=analytics)

    @app.route('/ai-studio')
    @login_required
    def ai_studio():
        return redirect(url_for('ai.hub'))

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            bio = request.form.get('bio', '').strip()
            if name:
                current_user.name = name
            if bio is not None:
                current_user.bio = bio
            try:
                db.session.commit()
                flash('Profile updated successfully!', 'success')
            except Exception:
                db.session.rollback()
                flash('Failed to update profile.', 'danger')
            return redirect(url_for('profile'))
        return render_template('account/profile.html')

    @app.route('/settings', methods=['GET', 'POST'])
    @login_required
    def settings():
        if request.method == 'POST':
            flash('Settings preferences saved!', 'success')
            return redirect(url_for('settings'))
        return render_template('account/settings.html')

    # Global Error Handlers for Presentation Stability
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Server Error: {e}")
        return render_template('errors/500.html'), 500

    # Create database tables automatically for dev environment
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
