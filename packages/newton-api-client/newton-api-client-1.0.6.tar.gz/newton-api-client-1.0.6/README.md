# Newton API client

This is python package to call all API from (https://api.objectways.com/docs)

## Import package and create a `client`
## "api_url" is and optional parameter for private installs
```python
from pprint import pprint
from objectways import newton

client = newton.Newton(api_url="YOUR_API_URL",api_key="YOUR_API_KEY")
```

## 1. Task
### 1.1. Add new task

```python
body = {
  "project_id": "449354de1168469a8229f605",
  "file_name": "document.pdf",
  "file_type": "application/pdf",
  "source": "s3://examples/pdfs/document.pdf"
}

pprint(client.add_task(body))
```

### 1.2. Add task file

```python
data = client.add_task_file(
    project_id="449354de1168469a8229f605", 
    file_path="examples/pdfs/document.pdf",
    mime_type="application/pdf",
    annotations=None
)

pprint(data)
```

### 1.3. Find task by Filters

- Find all the tasks by `task_id`, `file_name`, `file_type` and `trail`
- If all of `task_id`, `file_name`, `file_type` are `None`, it will return all possible tasks

```python
tasks = client.find_task(
    project_id="449354de1168469a8229f605", 
    task_id="449354de1168469a8229f605-0",
    file_name=None,
    file_type=None,
    trail = False
)

pprint(tasks)
```
### 1.4. Add bulk tasks
- 
```python
body = {
  "project_id": "cd1a965e334a9a63e2f17932",
  "task_list": [
    {
      "source": "s3://examples/pdfs/document.pdf",
      "annotations": "s3://examples/pdfs/annotation.json"
    },
    {
      "source": "s3://examples/pdfs/document2.pdf"
    },
    {
      "source": "s3://examples/pdfs/document3.pdf",
      "annotations": {
        "tags": [
          {
            "page": 1,
            "range": [
              192,
              198
            ],
            "text": "Oxford",
            "id": 1,
            "type": "NAME"
          }
        ]
      }
    }
  ]
}

pprint(client.add_bulk_tasks(body))
```
### 1.5 Add labels to task
-
```python
body = {
  "project_id": "179cd15e334f9a63e2a9632a",
  "task_id": "e51d511da586d5cf622acbdd",
  "annotations": "s3://examples/pdfs/annotation.json"
}


pprint(client.add_labels_to_task(body))
```

## 2. Project

### 2.1. Add a new project

```python
body = {
  "project_name": "TestProject",
  "project_type": "NER",
  "enable_text_mode_option": true,
  "disable_quality_audit": true,
  ...
}
# check API docs for the full body: https://api.objectways.com/docs/#/projects/upload_project

pprint(client.add_project(body))
```

### 2.2. Find projects by Filters

- Find all the projects by `project_id`, `project_name` or `active`
- If all of `project_id`, `project_name`, `active` are `None`, it will return all possible projects 


```python
projects = client.find_project(
    project_id="449354de1168469a8229f605", 
    project_name=None, 
    active: bool=None
)

```