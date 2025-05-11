# Alethic Instruction-Based State Machine (Gemini Processor)

### Docker Build
```shell
  sh docker_build.sh -t krasaee/alethic-ism-processor-gemini:local`
```

### Required Packages
```shell
  pip install uv
```

```shell
  pip venv
  source .venv/bin/activate
```

```shell
  uv pip install -r requirements.txt
```

## Run
Create a Google Cloud project and enable the `Generative AI API`. Obtain your API key from the Google Cloud Console associated to the `Generative AI API` service, specifically!

 * Alternately, one can try to enable the `Vertix AI`

```shell
docker run -d \
  --name alethic-ism-processor-gemini \
  -e Gemini_API_KEY="your_api_key_here" \
  -e LOG_LEVEL=DEBUG \
  -e ROUTING_FILE=/app/routing-nats.yaml \
  -e DATABASE_URL="postgresql://postgres:postgres1@host.docker.internal:5432/postgres" \
  krasaee/alethic-ism-processor-gemini:latest
```

## License
Alethic ISM is under a DUAL licensing model, please refer to [LICENSE.md](LICENSE.md).

**AGPL v3**  
Intended for academic, research, and nonprofit institutional use. As long as all derivative works are also open-sourced under the same license, you are free to use, modify, and distribute the software.

**Commercial License**
Intended for commercial use, including production deployments and proprietary applications. This license allows for closed-source derivative works and commercial distribution. Please contact us for more information.

