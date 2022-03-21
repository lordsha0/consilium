from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)

def getDataConnection():
    connect = sqlite3.connect("data/data.sqlite3") 
    return connect


def getProjects():
    sqlString = "SELECT id, name FROM projects"
    connect = getDataConnection()
    dbCursor = connect.cursor()
    results = dbCursor.execute(sqlString).fetchall()
        
    return results


@app.route("/")
def index():
    results = getProjects()
    return render_template("index.html", title="consilium", projects=results)


@app.route("/project")
def newProject():
    return render_template("newProject.html")


@app.route("/addProject", methods = ["POST", "GET"])
def addProject():
    # if the resquest is the correct method,
    # proceed with the insertion
    if request.method == "POST":
        try:
            projectName = request.form["name"]

            with getDataConnection() as connect:
                dbCursor = connect.cursor()
                dbCursor.execute("INSERT INTO projects (name) VALUES (?)", [projectName])

            connect.commit()
            message = "Project added successfully"
        except:
            connect.rollback()
            message = "Error errupted, creation unsuccessful"
        finally:
            connect.close()
            return render_template("feedback.html", message=message)
    # else, return an error
    else:
        return render_template("feedback.html", message="not a valid request")


@app.route("/deletProject", methods = [ "GET"] )
def removeProject():
    connect = getDataConnection()
    dbCursor = connect.cursor()
    projectId = request.args["project"]

    try:
        dbCursor.execute("DELETE FROM projects WHERE id=?", [projectId])   

        connect.commit()
        message = "Project deleted successfully"
    except:
        connect.rollback()
        message = "Error errupted, deletion unsuccessful"
    finally:
        connect.close()
        return render_template("feedback.html", message=message)


@app.route("/tasks", methods = ["GET"])
def showTasks():
    connect = getDataConnection()
    dbCursor = connect.cursor()

    projectId = request.args["project"]
    sqlString = "SELECT description, done, inProgress FROM tasks WHERE project_id = ?"

    results = dbCursor.execute(sqlString, [projectId]).fetchone()

    return render_template("tasks.html", tasks=results, project=projectId)


@app.route("/task")
def newTask():
    projectId = request.args["project"]
    return render_template("newTask.html", project=projectId)


@app.route("/addTask")
def addTask():
    # if the resquest is the correct method,
    # proceed with the insertion
    if request.method == "POST":
        try:
            projectName = request.form["name"]

            with getDataConnection() as connect:
                dbCursor = connect.cursor()
                dbCursor.execute("INSERT INTO tasks (description, project_id) VALUES (?, ?)", [projectName])

            connect.commit()
            message = "Project added successfully"
        except:
            connect.rollback()
            message = "Error errupted, creation unsuccessful"
        finally:
            connect.close()
            return render_template("feedback.html", message=message)
    # else, return an error
    else:
        return render_template("feedback.html", message="not a valid request")

@app.route("/deletTask")
def deletTask():
    connect = getDataConnection()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9993)