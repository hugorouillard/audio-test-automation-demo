# Audio Test Automation Demo

![Tests](https://github.com/hugorouillard/audio-test-automation-demo/actions/workflows/tests.yml/badge.svg)

Minimal test automation pipeline simulating audio QA workflows.

## Features
- Audio processing (normalize → amplify → convert)
- Automated tests (pytest + coverage)
- CI pipeline (GitHub Actions)
- Logs + coverage reports uploaded on each run

## Try locally

```bash
poetry install
poetry run pytest
```

## CI Artifacts
- Test logs
- HTML coverage report
