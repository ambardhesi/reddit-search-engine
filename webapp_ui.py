from flask import Flask, render_template, request, url_for, redirect, flash
from searcher import Searcher

app = Flask(__name__)
searcher = Searcher("indexes")

@app.route("/", methods = ["GET", "POST"])
def main():
    try:
        if request.method == "POST":
            search = request.form['search'] 
            return redirect(url_for("search_results", query = search))
       
    except Exception as e:
        flash(e)
    return render_template("main.html")

@app.route("/search_results/<query>")
def search_results(query): 
    try:
        pos_and_ids = searcher.find_docs(query.split(" ")) 
        urls = []
        for pos,id in pos_and_ids[0]:
            if searcher.get_url(id) not in urls:
                urls.append(searcher.get_url(id))  
        return render_template("search_results.html", query = query, urls = urls)
    except Exception as e:
        print "Not found! Redirecting to homepage", e
        return redirect(url_for("item_not_found", e))

@app.errorhandler(500)
def item_not_found(e):
    return render_template("error.html")


if __name__ == "__main__":
    app.run()
