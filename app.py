from flask import Flask, render_template, reques, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key"

@app.rout("/")

def home():
    features = [
        "3 working routes",
        "Shared layout with templates",
        "Basic stlying",
        "Contact form + flash message!" 
    ]
    return render_template("home.html", features=features)

@app.rout("/about")

def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])

def contact():
    if request.method == "POST":
        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        message = request.form.get("message").strip()

        if not name or not email or not message:
            flash("", "error")
            return redirect(url_for("contact"))
        
        flash(f"Thanks, {name}! Your message has been submitted :) ", "success")
        return redirect(url_for("contact"))
    
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)