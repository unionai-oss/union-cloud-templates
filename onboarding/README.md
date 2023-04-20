# Onboarding Project

This project contains a template Flyte project that can be used out-of-the-box
with a Flyte cluster hosted on [Union Cloud](https://www.union.ai/cloud).

This project template serves as a beginner-level entrypoint to learning how to:

1. Develop workflows in Flyte locally.
2. Deploy them to a Union-Cloud-hosted Flyte cluster.
3. Integrate the deployment process into your CI/CD via Github Actions

The high-level structure of this project is as follows:

```
.
├── Dockerfile               # Docker image for the project
├── LICENSE
├── README.md
├── docker_build_and_tag.sh  # convenience script to build docker image
├── requirements.txt         # project requirements
├── setup.py                 # project package spec
├── tutorial.ipynb           # hands-on tutorial
└── workflows                # workflow source code
```


## Setup

First clone the repo:

```bash
git clone https://github.com/unionai-oss/union-cloud-templates
cd union-cloud-templates/onboarding
```

Create a virtual environment:

```bash
python -m venv ~/venvs/ucloud-onboarding
source ~/venvs/ucloud-onboarding/bin/activate
pip install -e .
```

| ℹ️ **Note** |
|------|
| This project depends on `flytekit`, which supports Python 3.7 - 3.10 |


### Union Cloud Setup

First install the [`uctl` CLI tool](https://docs.union.ai/lPDZGfbii3Fs3osZsWrA/guides/set-up-uctl-to-interact-with-union-cloud).

These instructions are for setting up a project and registering workflows on
a playground cluster, which assumes that docker images are publis

Initialize the config file:

```bash
~/bin/uctl config init --host <host_url>
```

Create a new project:

```bash
~/bin/uctl create project \
    --id "onboarding" \
    --labels "my-label=onboarding" \
    --description "project for Union Cloud onboarding" \
    --name "onboarding"
```

Build and push docker:

```bash
./docker_build.sh
docker login ghcr.io
docker push <tag>
```

| ℹ️ **Note** |
|------|
| The default docker container in the [github repo packages](https://github.com/unionai-oss/union-cloud-templates/pkgs/container/union-cloud-templates) section is set to publicly visible. |


Fast register workflows for prototyping:

```
pyflyte --config ~/.uctl/config.yaml \
    register workflows \
    --project onboarding \
    --image ghcr.io/unionai-oss/union-cloud-templates:onboarding-latest
```

```bash
pyflyte --config ~/.uctl/config.yaml \
    register workflows \
    --project onboarding \
    --image ghcr.io/unionai-oss/union-cloud-templates:onboarding-latest
```

To register for production, first package your workflows with `pyflyte package`:

```bash
pyflyte \
    --pkgs workflows \
    package \
    --force \
    --image ghcr.io/unionai-oss/union-cloud-templates:onboarding-latest
```

Then register with `uctl`:

```bash
~/bin/uctl --config ~/.uctl/config.yaml \
    register files \
    --project onboarding \
    --domain development \
    --archive flyte-package.tgz \
    --version <version>
```


## Workflows

The `workflows` directory contains a suite of tasks and workflows that
demonstrates the core functionality of Flyte:

| Module | Description |
|--------|-------------|
| `example_00_intro.py` | a basic model training example. |
| `example_01_dynamic.py` | define execution graphs dynamically at runtime. |
| `example_02_map_task.py` | use map tasks to scale embarrassingly parallel tasks. |
| `example_03_plugins.py` | use plugins to leverage third-party integrations. |
| `example_04_type_system.py` | use type annotations for type-safety and to facilitate data passing. |
| `example_05_pandera_types.py` | validate tabular data at runtime. |
| `example_06_reproducibility.py` | code- and resource-level reproducibility. |
| `example_07_caching.py` | cache outputs of tasks to save compute resources. |
| `example_08_recover_executions.py` | pick up an execution where you left off. |
| `example_09_checkpointing.py` | checkpoint training progress within a task. |
| `example_10_flyte_decks.py` | create rich static reports associated with your tasks. |
| `example_11_extend_flyte_decks.py` | write your own visualizations/reports. |

## Tutorial

Follow the `tutorial.ipynb` notebook, which will take you through all the above
modules with explanations and examples of how to run each example directly from
a Jupyter runtime.

Create a jupyter kernel for your virtual environment:

```bash
pip install ipykernel
python -m ipykernel install --user --name ucloud-onboarding --display-name ucloud-onboarding
```

## Testing

### Running Unit Tests

Run the tests locally so that you can make sure 

```bash
pip install pytest pytest-xdist
pytest tests/unit
```


### Running End to End Tests

You can run end to end tests on the Union Cloud backend, assuming that you have
your `~/.uctl/config.yaml` file configured correctly.

The following will run all of the workflows in your backend to make sure they
work with the expected input.

```bash
pytest tests/end_to_end -n auto
```
