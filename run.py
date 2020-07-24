from pathlib import Path

from app.wsgi import the_app


if __name__ == "__main__":
    """ Run the local development server """

    files_to_watch = [str(path) for path in Path.cwd().glob("app/**/*.yaml")]
    
    the_app.run(
        debug=True,
        host="0.0.0.0",
        port=5000,
        extra_files=files_to_watch,
    )