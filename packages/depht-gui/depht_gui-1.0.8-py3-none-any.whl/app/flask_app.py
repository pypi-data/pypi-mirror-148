"""Flask app for DEPhT."""
from pathlib import Path
from flask import Flask

from importlib_resources import files

# import app
from app.views import depht, train, models, documentation
from app import config
from app import templates, static
# from app import static, templates

PKG = "depht_gui"

# templates_module = import_module("templates")
# static_module = import_module("static")


def create_app(name=PKG, **kwargs):
    """
    Create the Flask app.

    :param name: name of the app
    :type name: str
    """
    app = Flask(name, instance_relative_config=True,
                template_folder=files(templates),
                static_folder=files(static))

    # app = Flask(name)
    app.config.from_object(config)

    path = Path(app.instance_path)

    if not path.is_dir():
        path.mkdir(parents=True)

    app.register_blueprint(depht.bp)
    app.register_blueprint(train.bp)
    app.register_blueprint(models.bp)
    app.register_blueprint(documentation.bp)

    return app
