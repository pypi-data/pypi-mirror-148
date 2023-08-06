How to Grid
===

Example dashboard

```python
GritDash(
    uid="human-id",
    version=8,
    title="your dashboard title",
    description="your dashboards description",
    tags=[
        'tag1',
        'tag2'
    ],
    timezone="browser",
    dataSource="Prometheus",
    stack=Stack(
        row6(panel1),
        row6(panel1, panel2),
        row6(panel1, panel2, panel3),
        row6(panel1, panel2, panel3, panel4),
        row6(panel1, panel2, panel3, panel4, panel5),
    )
)
```

# Variations

Variations allow to create a different collection of dashboards from same code base, for example per-environment variation can be achieved with Environment variation.

You can create multiple variations, and quickly generate hundreds of dashboards

```python
# Variation is just subclass of Variation
class Environment(Variation):
  color: str = "green"

Environment(name="dev", color="blue")
Environment(name="qa")
Environment(name="test")
Environment(name="prod", color="red")
```

When writing dashboard you can access specific variation values by calling `<VariationClass>.resolve()`

```python
environment = Environment.resolve()
print(environment.color)
print(environment.name)
```

You create as many variatoins as you want and combine them
```python
class Environment(Variation):
  color: str = "green"

Environment(name="dev", color="blue")
Environment(name="qa")
Environment(name="test")
Environment(name="prod", color="red")

class Turn(Variation):
  pass

class Taste(Variation):
  pass

class Animal(Variation):
  pass

Turn(name="first")
Turn(name="second")
Turn(name="third")

Taste(name="sweet")
Taste(name="sour")

Animal(name="rabbit")
Animal(name="donkey")
Animal(name="turtle")
Animal(name="rat")
```

And use all of them during generation
```bash
❯❯❯ python -m grit generate --module grafana.dashboards --out 'out/{turn}-{taste}-{animal}-company/{environment}' --var environment=qa environment=prod animal=* turn=first taste=sweet
Generating out/first-sweet-donkey-company/qa
Generating out/first-sweet-donkey-company/prod
Generating out/first-sweet-rabbit-company/qa
Generating out/first-sweet-rabbit-company/prod
Generating out/first-sweet-rat-company/qa
Generating out/first-sweet-rat-company/prod
Generating out/first-sweet-turtle-company/qa
Generating out/first-sweet-turtle-company/prod
```


# Command-Line

## Inspect dashboards

```yaml
❯❯❯ python -m grit inspect --module dashboards
---
name: dashboards
folders:
- jmeter
- mongodb
variations:
  environment:
  - dev
  - nab-dev
  - nab-prod
  - prod
  - qa
  - test
```

## Publish to Grafana

```
❯❯❯ python -m grit publish --module grafana.dashboards --var environment=dev
```

## Generate to output directory

```shell
❯❯❯ python -m grit generate --module grafana.dashboards --out 'out/{environment}' --var environment=*
Generating out/dev
Generating out/nab-dev
Generating out/nab-prod
Generating out/prod
Generating out/qa
Generating out/test
```

# Utilities

## Rows
You have some handy utilities

### Predefined row heights

Each creating row of respective height
  *  `row3`
  *  `row4`
  *  `row5`
  *  `row6`
  *  `row7`
  *  `row8`
