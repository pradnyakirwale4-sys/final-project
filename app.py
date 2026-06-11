from flask import Flask, render_template,request
app = Flask(__name__)
import json

class BlogPost:
   def __init__(self,id,title,desc,hero):
     
    self.id = id
    self.title = title
    self.desc = desc
    self.hero = hero
   def to_dict(self):
      return {"id":self.id, 
              "title":self.title, 
              "desc":self.desc,
              "hero":self.hero
              }
def get_all_blogs():
      with open("db.json","r") as file:
         return json.load(file)
    
def create_new_blog(data):
      with open("db.json","w") as file:
         json.dump(data,file)
      
      

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/posts" , methods=["GET"])
def get_posts():
    return get_all_blogs()["posts"]
@app.route("/posts",methods=["POST"])
def create_post():
    body = request.json #{in body it is an dictionary like "title":"","desc":""..etc}
    all_blogs = get_all_blogs() #{post:[]}
    id = len(all_blogs["posts"]) + 1
    new_blog = BlogPost(id,body["title"],body["desc"],body["hero"])
    all_blogs["posts"].append(new_blog.to_dict())
    create_new_blog(all_blogs)
    return{"message":"blog create success"}

@app.route("/posts/<int:bid>", methods=["DELETE"])
def remove_blog(bid):
    all_blogs = get_all_blogs() #{posts[]}
    result = []
    for item in get_all_blogs()["posts"]: #in posts in all list
        if item["id"] != bid:
            result.append(item) # []
    all_blogs["posts"] = result 
    create_new_blog(all_blogs)
    return{"message":"blog remove success"}


if __name__ == "__main__":
    app.run(debug=True)