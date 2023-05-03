from app import create_app

if __name__ == '__main__':
    app=create_app('development')
    # app=create_app('production')
    app.run(port=5001,debug=True)
