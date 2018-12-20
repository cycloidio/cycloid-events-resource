# Cycloid Events Resource

Send and receive events to/from [Cycloid DevOps platform](https://www.cycloid.io/devops-platform-with-ci-cd-container-pipeline)
Our platform has an Event endpoint in order to have a unique entrypoint to store and retrieve events in a centralized way.
By storing some events directly from the pipeline, you are able to give some visibility to important steps, but also store indefinitely an event like a production deployment.

## Deploying to Concourse

You can use the docker image by defining the [resource type](https://concourse-ci.org/resource-types.html) in your pipeline YAML.

For example:

```yaml

resource_types:
- name: cycloid-events
  type: docker-image
  source:
    repository: cycloid/cycloid-events-resource
    tag: latest
```

## Source Configuration

All optional values below, if specified in the source, will act as a default value until it's overrided by the params configuration.

* `api_url`: *Required.* The url of the Cycloid DevOps Platform API
    Example: `https://http-api.cycloid.io`

* `api_login`: *Required*. The login of the account you will use to store those events

* `api_password`: *Required*. The password of the account declared above

* `organization`: *Required*. The organization where you will store the events

* `type`: *Optional*. The type of the event. Currently, only `Cycloid`, `Custom`, `AWS` or `Monitoring` are allowed.

* `severity`: *Optional*. The severity of the event. Currently, only `info`, `warn`, `err` or `crit` are allowed.

* `icon`: *Optional*. Icon to display. The icons are the ones from Font Awesome.
    Example: `fa-cubes`

* `title`: *Optional*. The title of the event

* `message`: *Optional*. The message in the event body

* `fail_on_error`: *Optional*. If true, the resource will fail if the Cycloid event API return an error. Default false (True values are y, yes, t, true, on and 1; false values are n, no, f, false, off and 0).

* `tags`: *Optional*. The tags allow filtering
    Example:
    ```
    tags:
      - key: project
        value: myproject
      - key: env
        value: prod
    ```

## Behavior

### `check`: Check for new events

The check is currently not implemented but it will allow to trigger a job when new events are populated.

### `in`: Retrieve an event

Currently not implemented

### `out`: Send an event to Cycloid

Send the event to Cycloid API with the desired parameters.

#### Parameters

 ```
 /!\ Those parameters are *Required* if they aren't defined yet in the Source configuration /!\
 ```

* `type`: *Optional*. The type of the event. Currently, only `Cycloid`, `Custom`, `AWS` or `Monitoring` are allowed.

* `severity`: *Optional*. The severity of the event. Currently, only `info`, `warn`, `err` or `crit` are allowed.

* `icon`: *Optional*. Icon to display. The icons are the ones from Font Awesome.
    Example: `fa-cubes`

* `title`: *Optional*. The title of the event

* `message`: *Optional*. The message in the event body

* `fail_on_error`: *Optional*. If true, the resource will fail if the Cycloid event API return an error. Default false (True values are y, yes, t, true, on and 1; false values are n, no, f, false, off and 0).

* `tags`: *Optional*. The tags allow filtering
    Example:
    ```
    tags:
      - key: project
        value: myproject
      - key: env
        value: prod
    ```
