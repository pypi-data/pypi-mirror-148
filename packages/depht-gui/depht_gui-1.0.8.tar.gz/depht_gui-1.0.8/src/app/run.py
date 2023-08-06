"""Run the app."""
import shutil
import sys

from signal import signal, SIGINT

from app.flask_app import create_app

app = create_app()
instance_path = app.instance_path

print(instance_path)


def exit_handle(sig, frame):
    """Exit when CTRL+C is pressed."""
    shutil.rmtree(instance_path)
    sys.exit(0)


def main():
    """Run the app."""
    signal(SIGINT, exit_handle)

    app.run(debug=False, port=50000)


if __name__ == "__main__":
    main()
