# Backend - Full Stack Trivia API 

## Introduction

- Full stack trivia api (backend) documentation
- List out getting started notes, errors, and endpoints

## Getting Started

- Below is a list of items needed to properly execute the api

### Installing dependencies

Install all of the required pacakages

- Navigate to the `/backend` folder directory
- Run install script

```shell
pip install -r requirements.txt
```

### Starting the server

Start the server

- Navigate to the `/flaskr` folder directory
- Run export script
- Run flask run script with reload to watch changes made to the file

```shell
export FLASK_APP
flask run --reload
```

## Errors

Errors are handled as json object messages

The api will return the following errors:

- 400: Return a bad request message
- 404: Return a not found message
- 415: Return an unsupported media type message
- 422: Return an unprocessable message

## Resource Endpoint Library

### GET /categories

#### General

- Return a list of all categories
- Categories must be returned as a dictionary with the id being the key, and the type being the value

#### Return sample

```shell
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### GET /questions

#### General

- Returns a list of questions, total quesstions, list of categories
- Results will be paginated in amounts of 10
- Results must be formated to display properly

#### Return sample

```shell
"questions": [
  {
    "id": 3,
    "question": "What color is the sky?",
    "answer": "Blue",
    "category": 3,
    "difficulty": 3
  }
]
```

### DELETE /questions/{id}

#### General

- Deletes the question with the id that is passed in via the url
- No data will be returned

### POST / questions

#### General

- When the add form is submitted with all of it"s fields filled out, a question will be successfully submitted
- No data will be returned
- The form will clear and the question will be added to the end of the last page

#### Return sample

```shell
{
  "success": True,
  "question": "Question entered",
  "answer": "Answer entered",
  "category": 3,
  "difficulty": 3
}
```

### POST /search

#### General

- The phrase or term that is entered via the search bar, will query the db and return all posts that are in relation to that term
- Will be compared by the question
- Term insensitive
- Results must be formated to display properly

#### Return sample

```shell
{
  "search_term": "Term/phrase passed in",
  "questions": List of questions returned based on term,
  "total_questions": Length of questions
}
```

### GET /categories/{id}/questions

#### General
- Return a list of questions based on the category id passed in
- Returned category will need to the type based on the id that has been passed through
- Results must be formated to display properly

#### Return sample

```shell
{
  "questions": list of questions,
  "total_questions": length of questions,
  "current_category": category type passed in,
}
```

### POST /quizzes

#### General

- The will retrieve all quesions
- Will either be all questions or filtered via the category that has been selected
- Questions will be randomized
- The current question displayed will not be one of the previous questions
- If there is no question, return an empty string to end the quiz

#### Return sample

```shell
{
  "question": question or ""
}
```
