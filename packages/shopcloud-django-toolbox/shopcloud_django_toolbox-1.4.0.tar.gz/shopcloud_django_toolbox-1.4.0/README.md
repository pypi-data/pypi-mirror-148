# shopcloud-django-toolbox

## install

```sh
$ pip install shopcloud-django-toolbox
```

## Models

Add the GID as identifier to all django models

```python3
from shopcloud_django_toolbox import GID

class FooBarModel(models.Model, GID):
    pass
```

## Testing

### API standart tests

Standart template for the `tests.py` file in all modules with admin and REST API`s

```python3
from shopcloud_django_toolbox.tests import BaseTestAPIEndpointDoc
from shopcloud_django_toolbox import TestAdminTestCase
from shopcloud_django_toolbox.tests import BaseTestApiAuthorization
from shopcloud_django_toolbox import SetupClass


class TestDocEntpoint(BaseTestAPIEndpointDoc):
    pass
__

class TestAdminPages(TestAdminTestCase):
    MODULE = 'url-name'

    def test_admin_easylineitem(self):
        self.run_for_model(
            'url-model-name',
            is_check_add=False,  # deactivate when add function is deactivated
            is_check_template=False,  # deactivate generic template check
            is_check_search=True,  # activate searchbar check
        )


class TestApiAuthorization(BaseTestApiAuthorization):
    app_name = "url-module-name"

    def test_model_foo(self):
        self.run_test_endpoint("url-model-name")

    def test_model_bar(self):
        self.run_test_endpoint("url-model-name")


class YoutAPITest(SetupClass):
    def test_api_endpint(self):
        client = APIClient()
        client.login(username=self.username, password=self.pwd)
        
        r = client.get('/module/api/endpoint')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
```

## Event

To fire events and run tasks in prarallel, need [PROJECT] to receive and run the output from log and call the API.

```python3
from shopcloud_django_toolbox import Event


class FooBarModel(models.Model):
    ...

    def do_event(self):
        event = Event(
            name="de.talk-point.platform/module/model/sync",
            model=self,
        )
        event.add_task(
            queue="default",
            url=f"moduke/api/model/{self.id}/action/",
            json={}
        )
        event.fire()
```

## deploy

```sh
# change version Number in setup.py ändern und dann erst releasen
# delete build and dist-directory
$ rm -rf build
$ rm -rf dist
$ pip3 install wheel twine
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/* 
```