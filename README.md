# Mastermind api
## Run wit docker-compose
`make run`
The server would run on 0.0.0.0:8000/search.


## Codebase
This repo uses [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)

This repo follows [githubflow](https://docs.github.com/en/get-started/quickstart/github-flow).

This service follows the [twelve-factors methodology](https://12factor.net/). A .env file containing enviroment variables could be provided.

This projects is structured following [Domain Driven Design](https://www.amazon.es/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215) guidelines. The src folder contains all the app code. You can find inside three folders:
- Domain, where the business rules and important logic is contained.
- Application, where all the use cases of the app are listed.
- Infrastructure, where all the entrypoints and communications of the app are implemented.


## Assumptions
Maybe there should be nice to have some kind of authentication and authorization, but since is not specified on the requirements and for the sake of time, I assume these not to be required.


## Architecture
The proposed architecture is based on three critical components:
- A database to store all games.
- The api server, responsable for reading games from the db.


## Packege manager pdm
This project is handled with [pdm](https://pdm.fming.dev/latest/#installation)

You can run the following scripts:
```
pdm run server
pdm run cli
pdm run make_migration
pdm run migrate
pdm run test
pdm run test_coverage
pdm run test_coverage_html
```

## Code quality
Install pre-commit with `pdm run pre-commit install` to lint, format code and order imports on every commit.
