# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Reference

### Getting Started
- Base URL: For now this application can only be run using localhost and is not hosted as a base URL. The backend is hosted at the default, `http://127.0.0.1:5000/`, The frontend is React app which is hosted at the default, `http://127.0.0.1:3000/`.
- Authentication: The current version of this application does not need authentication or API keys.

### Error Handling
- Errors are returned as JSON in the following format:


    {
       "success": False,
       "error": 404,
       "message": "Resource Not Found!"
     }

The API will return three types of errors:

    400 – bad request
    404 – resource not found
    422 – unprocessable

### Endpoints
- GET/categories

    General:
    - request all categories
    - Returns a dictionary categories and success value.
    Sample: `curl http://127.0.0.1:5000/categories:`
    
    ```
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true 
    }
    ```

- GET/questions

    General:
    - Returns success value.
    - Returns a list of questions paginated in 10 questions per page.
    - Returns total number of questions, dictionary of all categories and list of current categories in the page.

    Sample: `curl http://127.0.0.1:5000/questions?page=1:`
    
    ```
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": [
        5,
        5,
        5,
        6,
        6,
        4,
        3,
        3,
        3,
        2
    ],
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        }
    ],
    "success": true,
    "total_questions": 20}
    ```

- DELETE//questions/`<int:question_id>`

    General:

    - Deletes a question which id is passed using url parameters.
    - Returns a JSON object contains id of the deleted question and success message.

    Sample: `curl http://127.0.0.1:5000/questions/2 -X DELETE`

        {
        "deleted": 2,
        "success": true }

- POST/questions

    ####1- In case no searchTerm is included in request:

    General:
    - Creates a new question using JSON data passed in the request.
    - Returns JSON object with success message and the created question id.

    Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Where do you live?", "answer": "Egypt", "category": "3", "difficulty": 1}'`

        {
        "created": 39,
        "success": true }'''

     ####2- In case searchTerm is included in request:
     General:

     - Search for all questions that contains the term passed in JSON object during the request.
     - Returns JSON object with success message and list of formatted
     questions, total resulted questions and current category of questions in the page.

     Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Where"}'`
     
     ```
     {
    "current_category": [
        3,
        3,
        3,
        3
    ],
    "questions": [
        {
            "answer": "Egypt",
            "category": 3,
            "difficulty": 1,
            "id": 36,
            "question": "where are you?"
        },
        {
            "answer": "in Africa",
            "category": 3,
            "difficulty": 1,
            "id": 37,
            "question": "where is Egypt?"
        },
        {
            "answer": "home",
            "category": 3,
            "difficulty": 1,
            "id": 38,
            "question": "where are you?"
        },
        {
            "answer": "Egypt",
            "category": 3,
            "difficulty": 1,
            "id": 39,
            "question": "Where do you live?"
        }
    ],
    "success": true,
    "total_questions": 4 
    }
    ```

- GET/categories/`<int:category_id>`/questions

    General:
     - Gets all questions related to specific category.
     - Returns JSON object contains success message, questions list, total questions, current category id.

    Sample: `curl http://127.0.0.1:5000/categories/1/questions`
    
    ```
    {
    "current_category": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "cells",
            "category": 1,
            "difficulty": 1,
            "id": 26,
            "question": "from what human organs is composed?"
        },
        {
            "answer": "organs",
            "category": 1,
            "difficulty": 1,
            "id": 34,
            "question": "from what human is composed?"
        },
        {
            "answer": "mammals",
            "category": 1,
            "difficulty": 1,
            "id": 35,
            "question": "to what species cat is grouped?"
        }
    ],
    "success": true,
    "total_questions": 6
    }
    ```
    
- POST/quizzes

    General:

    - Take category and previous question parameters and return a JSON object contains a random question within the given category,
    if provided, and that is not one of the previous questions ans also success message.

    Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"previous_questions": [22], "quiz_category": {"type": "Science", "id": "1"}}'`
    
    ```
    {
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
    }
    ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Deployment N/A

## Authors
some names

## Acknowledgements
The awesome team at Udacity and all of the students, soon to be full stack extraordinaries!
