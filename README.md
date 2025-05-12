# Alethic Instruction-Based State Machine (Gemini Processor)

Alethic ISM Gemini Processor is a component of the Alethic Instruction-Based State Machine ecosystem that integrates with Google's Gemini generative AI models to process natural language instructions and maintain state information.

## Features

- Seamless integration with Google's Gemini generative AI models
- Stateful processing through PostgreSQL storage
- Message routing through NATS messaging system
- Containerized deployment for easy scaling
- Kubernetes deployment support

## Prerequisites

- Python 3.12 or higher
- PostgreSQL database
- Google Cloud project with Generative AI API enabled and API key
- NATS server for messaging

## Installation

### Using Docker (Recommended)

Build the Docker image using the provided Makefile:

```shell
make build
```

Or build with custom image tag:

```shell
make build IMAGE=your-registry/alethic-ism-processor-gemini:tag
```

### Development Setup

1. Install uv (fast Python package installer):
```shell
pip install uv
```

2. Create and activate virtual environment:
```shell
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```shell
uv pip install -r requirements.txt
```

## Configuration

The following environment variables can be configured:

- `GEMINI_API_KEY`: Your Google Generative AI API key
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `ROUTING_FILE`: Path to the NATS routing configuration file
- `DATABASE_URL`: PostgreSQL connection string

## Running

### Docker

```shell
docker run -d \
  --name alethic-ism-processor-gemini \
  -e GEMINI_API_KEY="your_api_key_here" \
  -e LOG_LEVEL=DEBUG \
  -e ROUTING_FILE=/app/repo/.routing.yaml \
  -e DATABASE_URL="postgresql://postgres:postgres1@host.docker.internal:5432/postgres" \
  krasaee/alethic-ism-processor-gemini:latest
```

### Local Development

```shell
python main.py
```

## Kubernetes Deployment

A Kubernetes deployment configuration is provided in the `k8s/deployment.yaml` file. 
To deploy to a Kubernetes cluster:

1. Update the image reference in the deployment file
2. Create the required secrets:
   - `alethic-ism-routes-secret`: Contains the routing configuration
   - `alethic-ism-processor-gemini-secret`: Contains environment variables

```shell
kubectl apply -f k8s/deployment.yaml
```

## Development

### Versioning

The project uses semantic versioning. To bump the version:

```shell
make version
```

## License

Alethic ISM is under a DUAL licensing model, please refer to [LICENSE.md](LICENSE.md).

**AGPL v3**  
Intended for academic, research, and nonprofit institutional use. As long as all derivative works are also open-sourced under the same license, you are free to use, modify, and distribute the software.

**Commercial License**
Intended for commercial use, including production deployments and proprietary applications. This license allows for closed-source derivative works and commercial distribution. Please contact us for more information.

For details on third-party licenses, please see [OSS-LICENSE.md](OSS-LICENSE.md).