from app import create_app

app = create_app()

if __name__ == "__main__":
    # Dev runner
    app.run(host=app.config_manager.get("app", {}).get("host", "127.0.0.1"),
            port=int(app.config_manager.get("app", {}).get("port", 8000)),
            debug=True)

