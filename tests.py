import requests

def test_create_task():
    # Set up
    url = "http://localhost:5000/tasks/1"
    headers = {'Content-Type': 'application/json'}
    data = {"title": "Task 1", "description": "This is the first task."}

    # Make the request
    response = requests.post(url, headers=headers, json=data)

    # Check the response
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["completed"] == False


def test_get_all_tasks():
    # Set up
    url = "http://localhost:5000/tasks/1"

    # Make the request
    response = requests.get(url)

    # Check the response
    assert response.status_code == 200
    assert len(response.json()["tasks"]) > 0


def test_get_task_by_id():
    # Set up
    url = "http://localhost:5000/tasks/1"

    # Make the request
    response = requests.get(url)

    # Check the response
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_update_task():
    # Set up
    url = "http://localhost:5000/tasks/1"
    headers = {'Content-Type': 'application/json'}
    data = {"title": "Task 1 updated", "description": "This is the first task updated.", "completed": True}

    # Make the request
    response = requests.put(url, headers=headers, json=data)

    # Check the response
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["description"] == data["description"]
    assert response.json()["completed"] == True


def test_delete_task():
    # Set up
    url = "http://localhost:5000/tasks/1"

    # Make the request
    response = requests.delete(url)

    # Check the response
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

