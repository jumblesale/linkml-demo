# LinkML Demonstration

## Existing app

- [ ] [pyproject.toml](pyproject.toml)
- [ ] [schema/bookstore.md](schema/bookstore.md)
  - [ ] Show the natural language description of the schema
- [ ] [schema/bookstore.yaml](schema/bookstore.yaml)
  - [ ] Classes
  - [ ] Slots
  - [ ] Annotations
  - [ ] Enumerations
- [ ] Show the generated code
  - [ ] Templates
  - [ ] domain.py
  - [ ] dto.py
  - [ ] entity.py
  - [ ] constraints.py
  - [ ] schema.py
- [ ] Run the app
  - [ ] [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)
  - [ ] [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- [ ] Create a new author
  - [ ] Show the location header being set
  - [ ] Create a second author
  - [ ] GET the created authors
- [ ] Create a new book
  - [ ] Show validation on ISBN, genre
  - [ ] Add the author IDs to the payload
- [ ] Create a second book
  - [ ] Show the uniqueness constraint on ISBN, title


## Adding an entity

- [ ] Create a "Publisher" entity
- [ ] Add slots for:
  - [ ] publisher_name
  - [ ] books_published