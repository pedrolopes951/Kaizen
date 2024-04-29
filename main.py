from Kaizen import KaizenApp


kaizen_app = KaizenApp()

# Decorator and makes index() funciton should be called whenm a request is made to the root URL '/' of the Flask
# I am telling Flask object that when a request comes in with a spcecified URL pattern like '/' index() is called
@kaizen_app.app.route('/')
def index():
    return "Welcome to Kaizen!" 

if __name__ == '__main__':
    kaizen_app.run()

