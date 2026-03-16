# FastAPI Template

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.114-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Reusable starter repository for a FastAPI service with a clear application layout, async SQLAlchemy, Docker support, and a small sample CRUD resource you can replace with your own domain.

## Getting Started

These instructions will get you a copy of the project running on your local machine for development or as a starting point for a new FastAPI service.

### Prerequisites

- `python3`
- `pip`
- `docker` and `docker compose` for the container workflow

### Installation

1. Clone the repository.
2. Copy the environment variables file:

```bash
cp dot_env_example .env
```

> [!IMPORTANT]
> If you plan to run the service with [Docker Compose](#run-with-docker-compose) or inside the [`.devcontainer`](#devcontainer), steps 3 and 4 are not required. Those workflows install dependencies inside the container environment for you.

3. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install the application dependencies:

```bash
pip install -r fastapi_app/requirements.txt
```

### Usage

#### Run locally

```bash
set -a
source .env
set +a
cd fastapi_app
hypercorn app.main:app --reload --bind 0.0.0.0:8000
```

Open `http://localhost:8000/docs`.

#### Run with Docker Compose

```bash
docker compose up --build
```

Open `http://localhost:13000/docs`.

The local workflow uses `fastapi_app/app.db`. The Docker workflow persists SQLite under `db_volume/`.

#### Example endpoints

- `GET /`: basic health payload with app name and version.
- `GET /items`: list all items.
- `POST /items`: create an item.
- `GET /items/{item_id}`: retrieve one item.
- `PATCH /items/{item_id}`: partially update one item.
- `DELETE /items/{item_id}`: delete one item.

### Development

This template keeps the project split into API, dependency, business logic, and persistence layers:

- `fastapi_app/app/main.py`: application startup, OpenAPI metadata, lifespan hooks.
- `fastapi_app/app/routers/`: API layer.
- `fastapi_app/app/dependencies.py`: dependency injection for shared services and database sessions.
- `fastapi_app/app/business_logic/`: service layer where domain rules live.
- `fastapi_app/app/sql/`: database engine, models, schemas, and CRUD helpers.
- `compose.yml`: local container orchestration.
- `dot_env_example`: starter environment variables for local and Docker usage.
- `docs/`: Bruno requests and a simple PlantUML architecture diagram.

Recommended first changes after cloning:

1. Replace the sample `Item` model, schemas, CRUD helpers, and router endpoints with your own entities.
2. Split `routers/main_router.py` into multiple router modules once your API grows.
3. Adjust environment defaults in `dot_env_example` and `compose.yml` for your service name and database backend.
4. Add automated tests and CI checks for your project needs.

If you use PyCharm or another IDE, point the run configuration at `hypercorn` with `app.main:app --bind 0.0.0.0:8000` and use `fastapi_app` as the working directory or sources root.

#### [`.devcontainer`](./.devcontainer)
This repo ships with a VS Code devcontainer environment to make development simpler.

##### Configuring git
Follow the steps in the sections below to configure Git inside the container.

> [!WARNING]
> As stated in [Launching VS Code with Git config](#launching-vs-code-with-git-config), start VS Code (`code .`) from the same shell where you ran the configuration commands!

###### Setting up git `user.name` and `user.email`
Set the following environment variables; they are passed to the devcontainer automatically.

**Windows**
```powershell
$env:FASTAPI_TEMPLATE_DEV_GIT_NAME = "Your Name"
$env:FASTAPI_TEMPLATE_DEV_GIT_EMAIL = "your@email.com"
```

**Linux**
```bash
export FASTAPI_TEMPLATE_DEV_GIT_NAME="Your Name"
export FASTAPI_TEMPLATE_DEV_GIT_EMAIL="your@email.com"
```

> [!NOTE]
> You only need to perform these steps when you create (or rebuild) the devcontainer, not every time you start it.

###### Setting up git SSH keys
If you use Git with SSH keys, follow these steps (full info at [link](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials)).

> [!NOTE]
> You need to perform the actions below (SSH agent initialization and key loading) every time you **start** the container.

**1. Automatically initialize the SSH Agent**

**Windows**: Start a local Administrator PowerShell session and run the following commands:
```powershell
# Make sure you're running as an Administrator
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent
Get-Service ssh-agent
```

**Linux**: First, start the SSH Agent in the background by running the following in a terminal:

```bash
eval "$(ssh-agent -s)"
```

**2. Add your keys to the SSH Agent**

Both on Windows and Linux:
```bash
# Import default keys (~/.ssh/id_rsa, .ssh/id_dsa, ~/.ssh/id_ecdsa, ~/.ssh/id_ed25519, and ~/.ssh/identity)
ssh-add

# Import specific keys
ssh-add <path/to/your/key>
```

###### Launching VS Code with Git config
**Using the same shell** used to execute commands in the previous Git config sections, **move to the repo directory and launch VS Code**.

```bash
cd /path/to/fastapi-template

code .
```

##### Starting devcontainer
Once the [git configuration steps](#configuring-git) are completed, you can create the devcontainer. Follow this simple process:

1. Press `Ctrl + Shift + P` to open VS Code's command palette
2. Type `Dev Containers: Reopen in Container` and hit Enter
3. That's it! The environment is now ready to use :)

## Documentation

The repository includes starter documentation assets that should evolve with your project:

- Changelog: [`CHANGELOG.md`](./CHANGELOG.md)
- Bruno collection: `docs/bruno_collection`
- PlantUML architecture: `docs/uml/architecture.puml`
- Documentation notes: `docs/README.md`

## Versions

The template defaults to `APP_VERSION=0.1.0` in `dot_env_example`. Keep release history in [`CHANGELOG.md`](./CHANGELOG.md) and update the application version together with each release.

## Support

Use the issue tracker or the collaboration channel defined by the team adopting this template. If you turn this starter into a project template for others, replace this section with the correct support path.

## Authors

Update this section with the maintainers of the repository or the team that owns the template.

## License

This project is licensed under the [MIT License](./LICENSE).

## Roadmap

Tasks to improve this template.

- [ ] Add relevant agent skills.
- [ ] ...
