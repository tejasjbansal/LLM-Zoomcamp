# QueryGenie Bot

Welcome to the QueryGenie Bot project! This project utilizes a Large Language Model (LLM) to answer questions based on a provided question and answer document. Below, you'll find the requirements and steps needed to set up and run the project.

## Requirements

To run this project, you need the following:

- **Docker**
- **Python 3.10**
- **OpenAI account** (Optional, alternative models can be used)
- **GitHub account** (Optional, for version control and collaboration)

## Preparing the Environment

### 1. Install pipenv
To manage dependencies, install pipenv:
```bash
pip install pipenv
```

### 2. Install necessary packages
Use pipenv to install the required packages:
```bash
pipenv install tqdm notebook==7.1.2 openai elasticsearch
```

### 3. Manage API keys with direnv
To securely manage API keys, follow these steps to install and configure direnv:

1. **Update and install direnv**:
    ```bash
    sudo apt update
    sudo apt install direnv
    ```

2. **Configure direnv for your shell**:
    ```bash
    direnv hook bash >> ~/.bashrc
    ```

3. **Create or edit the .envrc file in your project directory**:
    ```bash
    export OPENAI_API_KEY='sk-proj-key'
    ```

4. **Allow direnv to run**:
    ```bash
    direnv allow
    ```

### 4. Run Jupyter Notebook
Start a new terminal and run Jupyter Notebook:
```bash
pipenv run jupyter notebook
```

### 5. Run Elasticsearch with Docker
In another terminal, start Elasticsearch using Docker:
```bash
docker run -it \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```

## Usage

Once your environment is set up and the necessary services are running, you can start using the QueryGenie bot by interacting with the Jupyter Notebook interface. The bot will utilize the LLM model to provide answers based on the provided document.

Feel free to modify the project to suit your needs and explore different configurations or alternative models as required.

## Contributing

If you have a GitHub account, you can clone the repository, make changes, and submit pull requests to contribute to the project. Collaboration and improvements are always welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
