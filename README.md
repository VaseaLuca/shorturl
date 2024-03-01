
### Webservice for shortening urls using python



## Steps to setup and run the project

To run this project, you will need to follow these steps:


 - `git clone <repository_url>`
 ---

 - `cd <project_directory>`

 ---

 - Create virtual env:
     `python3 -m venv env`

 ---

 - Activate virtual env (Linux/Mac):
     `source env/bin/activate`

---

- Install the required deps using pip:
    `pip install -r requirements.txt` 

---
- Set Up the Database: Ensure that you have PostgreSQL installed and running. Then, create the database specified in your URL_DATABASE configuration. You may need to adjust the database connection URL in your code if necessary. (search in project for URL_DATABASE)

--- 


- To start the project:

   `uvicorn app.main:app --reload`

  and access the application on http://127.0.0.1:8000
    
# Running Tests

To run tests, run the following command

```bash
  pytest tes
```

