"""
Account Service Routes
"""
from flask import Flask, request, abort
from service.models import Account, db
from service import status


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register routes
    register_routes(app)

    return app


def register_routes(app):
    """Register all routes with the Flask app"""
    _register_account_routes(app)
    _register_utility_routes(app)


def _register_account_routes(app):
    """Register account-related routes"""
    @app.route("/accounts", methods=["POST"])
    def create_accounts():
        """Create an Account"""
        app.logger.info("Request to create an Account")
        account = Account()
        account.deserialize(request.get_json())
        account.save()
        app.logger.info("Account with ID [%s] saved.", account.id)
        return account.serialize(), status.HTTP_201_CREATED

    @app.route("/accounts", methods=["GET"])
    def list_accounts():
        """Returns all of the Accounts"""
        app.logger.info("Request to list Accounts")
        accounts = Account.all()
        results = [account.serialize() for account in accounts]
        app.logger.info("Returning %d accounts", len(results))
        return results, status.HTTP_200_OK

    @app.route("/accounts/<int:account_id>", methods=["GET"])
    def get_accounts(account_id):
        """Retrieve a single Account"""
        app.logger.info("Request to retrieve Account with id: %s", account_id)
        account = Account.find(account_id)
        if not account:
            abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
        app.logger.info("Returning account: %s", account.name)
        return account.serialize(), status.HTTP_200_OK

    @app.route("/accounts/<int:account_id>", methods=["PUT"])
    def update_accounts(account_id):
        """Update an Account"""
        app.logger.info("Request to update Account with id: %s", account_id)
        account = Account.find(account_id)
        if not account:
            abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
        account.deserialize(request.get_json())
        account.id = account_id
        account.save()
        app.logger.info("Account with ID [%s] updated.", account.id)
        return account.serialize(), status.HTTP_200_OK

    @app.route("/accounts/<int:account_id>", methods=["DELETE"])
    def delete_accounts(account_id):
        """Delete an Account"""
        app.logger.info("Request to delete Account with id: %s", account_id)
        account = Account.find(account_id)
        if account:
            account.delete()
            app.logger.info("Account with ID [%s] delete complete.", account_id)
        return "", status.HTTP_204_NO_CONTENT


def _register_utility_routes(app):
    """Register utility routes"""
    @app.route("/")
    def index():
        """Root endpoint"""
        return {"message": "Account Service"}, status.HTTP_200_OK

    @app.route("/health")
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}, status.HTTP_200_OK


# For backward compatibility, create app instance
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
