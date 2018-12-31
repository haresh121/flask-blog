import bloggy

app = bloggy.create_app()
with app.app_context():
    bloggy.db.init_app(app)
    bloggy.mail.init_app(app)
    bloggy.bcrypt.init_app(app)
    bloggy.log_mngr.init_app(app)
if __name__ == "__main__":
    app.run(host = "192.168.31.182", port=8081)
