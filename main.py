from flask import Flask, render_template, redirect, request, url_for
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


def getTasks(projectId):
    sqlString =  "SELECT id, description, done, inProgress FROM tasks WHERE project_id = ?"
    connect = getDataConnection()
    dbCursor = connect.cursor()

    results = dbCursor.execute(sqlString, [projectId]).fetchall()

    return results


def getProjectName(projectId):
    sqlString = "SELECT name FROM projects WHERE id = ?"
    connect = getDataConnection()
    dbCursor = connect.cursor()

    results = dbCursor.execute(sqlString, [projectId]).fetchone()

    return results[0]
    

@app.route("/")
def index():
    results = getProjects()
    return render_template("index.html", title="projects | consilium", projects=results)


@app.route("/project")
def newProject():
    return render_template("newProject.html", title="create a new project | consilium")


@app.route("/addProject", methods = ["POST", "GET"])
def addProject():
    title = "feedback | consilium"

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
            return render_template("feedback.html", title=title, url="/", message=message)
    # else, return an error
    else:
        return render_template("feedback.html", title=title, url="/", message="not a valid request")


@app.route("/deletProject", methods = [ "GET"] )
def removeProject():
    title = "feedback | consilium"

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
        return render_template("feedback.html", title=title, url="/", message=message)


@app.route("/tasks", methods = ["GET"])
def showTasks():
    connect = getDataConnection()
    dbCursor = connect.cursor()

    projectId = request.args["project"]
    results = getTasks(projectId)
    projectName = getProjectName(projectId)

    return render_template("tasks.html", title="tasks | consilium", tasks=results, project=projectId[0], name=projectName)


@app.route("/task")
def newTask():
    projectId = request.args["project"]

    return render_template("newTask.html", title="create a new task | consilium", project=projectId)


@app.route("/addTask", methods = ["POST", "GET"])
def addTask():
    title = "feedback | consilium"
    # if the resquest is the correct method,
    # proceed with the insertion
    if request.method == "POST":
        try:
            taskDescription = request.form["description"]
            projectId = request.form["project"]

            with getDataConnection() as connect:
                dbCursor = connect.cursor()
                dbCursor.execute("INSERT INTO tasks (description, done, inProgress, project_id) VALUES (?, ?, ?, ?)", (taskDescription, 0, 0, projectId,))

            connect.commit()
            message = "Task added successfully"
        except:
            connect.rollback()
            message = "Error errupted, creation unsuccessful"
        finally:
            connect.close()

            return redirect(url_for("showTasks", project=projectId))
    # else, return an error
    else:
        return render_template("feedback.html", title=title, url="/", message="not a valid request")


@app.route("/deletTask")
def deletTask():
    title = "feedback | consilium"

    connect = getDataConnection()
    dbCursor = connect.cursor()
    taskId = request.args["task"]
    projectId = request.args["project"]

    try:
        dbCursor.execute("DELETE FROM tasks WHERE id=?", [taskId])   

        connect.commit()
        message = "Task deleted successfully"
    except:
        connect.rollback()
        message = "Error errupted, deletion unsuccessful"
    finally:
        connect.close()

        return redirect(url_for("showTasks", project=projectId))


@app.route("/updateTask")
def updateTask():
    title = "feedback | consilium"

    connect = getDataConnection()
    dbCursor = connect.cursor()
    taskId = request.args["task"]
    updatedField = request.args["field"]
    projectId = request.args["project"]

    try:
        if (updatedField == "progress"):
            dbCursor.execute("UPDATE tasks SET done=0, inProgress=1 WHERE id= ? ", [taskId])
        elif (updatedField == "done"):
            dbCursor.execute("UPDATE tasks SET done=1, inProgress=0 WHERE id = ?", [taskId])
            
        connect.commit()
        message = "Task updated successfully"
    except:
        connect.rollback()
        message = "Error errupted, update unsuccessful"
    finally:
        connect.close()

        return redirect(url_for("showTasks", project=projectId))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9993)