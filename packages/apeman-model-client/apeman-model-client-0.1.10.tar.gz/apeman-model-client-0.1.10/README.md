#### This library enables you to report the status of tasks in your model at runtime
#### publish:
```shell
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

```
#### install: `pip install apeman-model-client==0.1.8`


#### How to use
```shell
export apeman_meta_server_addr='localhost:9090'
```
```python
import os

from apeman.model.openapi import apemanOpenApi
from apeman.model.openapi.model_instance_task_status import TaskStatus

client = apemanOpenApi.ApemanModelServiceClient()
# get endpoint of other model
client.get_endpoint(model_instance_id='test')
# report status
client.report(task_id='', status=TaskStatus.RUNNING, progress=0.1, message='test', token='')


```
