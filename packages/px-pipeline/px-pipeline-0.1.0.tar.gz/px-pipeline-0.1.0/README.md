# Pipeline runner

## Installation

```sh
pip install px-pipeline
```

## Usage

Simple usage:

```python
from px_pipeline import StraightPipeline, StopFlow


def second_pipeline_handler(context: dict) -> Optional[dict, None]:
  if 'nothing' in context:
    # You could return empty result so nothing would happen with context.
    return

  # You could mutate context with new data
  context['update'] = True

  # Or return a chunk of data, that will update context object.
  return {'update': False}


def flow_stopper(context):
  if context.get('update', False):
    return {'stopped': False}

  # Or you could raise an error that will stop pipeline from further execution.
  raise StopFlow({'stopped': True})


pipeline = StraightPipeline((
  # Callables can be used in form of import strings.
  'some.path.to.your.execution_function',
  second_pipeline_handler,
  flow_stopper,
))

result = pipeline({})
print(result['stopped']) # > True
print(result['update']) # > False


pipeline = StraightPipeline((
  flow_stopper,
  lambda context: {'called': True},
))

result = pipeline({'update': True})
print(result['stopped']) # > False
print(result['update']) # > True
print(result['called']) # > True

# Here flow stopped and lambda function were not executed.
result = pipeline({'update': True})
print(result['stopped']) # > True
print(result['update']) # > False
print('called' in result) # > False
```
