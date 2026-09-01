# DEMO

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
  - [ ] Jinja templates
  - [ ] domain.py
  - [ ] dto.py
  - [ ] entity.py
  - [ ] constraints.py
  - [ ] schema.py
- [ ] Run the app
  - [ ] [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)
  - [ ] [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- [ ] Create a book

## Adding a slot
- [ ] `git checkout 646a11c -- schema/bookstore.yaml`
- [ ] Introduces ISBN slot with validation
- [ ] Show the diff of the schema YAML
- [ ] `just generate`
- [ ] Show the diff of the generated files
- [ ] `just run`
- [ ] Create a book with an invalid ISBN

## Uniqueness constraints
- [ ] `git checkout 9284a5c -- schema/bookstore.yaml ; just rerun`
- [ ] Introduces book unique keys
- [ ] Create a book with conflicting title / ISBN

## Adding a new entity
- [ ] `git checkout 9a9e549 -- schema/bookstore.yaml ; just rerun`
- [ ] Introduces Author entity
- [ ] Create an author
- [ ] Use the author ID to create a book
- [ ] Create a second book
