# Research Portal Client

Library to interact with Minder Research APIs.

## Example

```python
import logging
import asyncio
import datetime
from minder.research_portal_client import Configuration, JobManager
from minder.research_portal_client.models import ExportJobRequest, ExportJobRequestDataset


logging.basicConfig(level="INFO")

Configuration.set_default(
    Configuration(
        access_token="---REDACTED---",
    )
)


async def example1():
    async with JobManager() as job_manager:
        now = datetime.datetime.today()
        since = now - datetime.timedelta(days=7)
        datasets: dict(str, ExportJobRequestDataset) = {
            "patients": ExportJobRequestDataset(),
            "observation_notes": ExportJobRequestDataset(),
        }

        export_job = ExportJobRequest(since, datasets=datasets)
        job_id = await job_manager.submit(export_job)
        job = await job_manager.wait(job_id)
        await job_manager.download(job)


async def example2():
    job_id = "c25249e0-82ff-43d1-9676-f3cead0228b9"
    async with JobManager() as job_manager:
        await job_manager.download(job_id)


async def main():
    await example1()
    await example2()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```



# Development

## Useful commands

### Run tests
  
```bash
poetry run pytest
```

### Code Coverage

This command consists of 2 parts:
- running tests with coverage collection
- formatting the report: `report` (text to stdout), `xml` (GitLab compatible: cobertura), `html` (visual)

```bash
poetry run coverage run -m pytest && poetry run coverage report -m
```

### Linting

```bash
poetry run flake8
```

### Formatting

```bash
poetry run black .
```

### Type Checking

```bash
poetry run mypy .
```
