from server import app

# Vercel需要这个变量名
handler = app

if __name__ == "__main__":
    app.run() 