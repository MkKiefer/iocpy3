# Simple Python IoC Framework

## Usage

Examples how to use this library.

### Singleton with no dependency's

Registering a singleton means we will return the same instance
for every `ioc.get` request.

```PYTHON
class MyInterface(ABC):
    @abstractmethod
    def do_it(self):
        ...

class MyClass(MyInterface):

    def __init__(self, name):
        self.name = name

    def do_it(self):
        print(f"{self.name} I did it")

ioc = IOCContainer()
ioc.register_singleton(MyInterface, MyClass("Manuel"))
ioc.get(MyInterface).do_it()
```

### Singleton with dependency's

Creating a singleton with dependency enables us to reuse already registered configurations.

⚠️ A singleton should only have singletons as dependency's if we use a transient, the transient will become a singleton.

```PYTHON

class AppConfig(BaseModel):
    user_name: str

ioc = IOCContainer()
ioc.register_singleton(AppConfig, AppConfig(user_name="Manuel"))
ioc.register_singleton(MyInterface, lambda x: MyClass(
    name=x.get(AppConfig).user_name)
    )
ioc.get(MyInterface).do_it()

```

### Transient

Registering a transient means we will generate the instance
for every `ioc.get` request.

```Python

class LoveCalculator():
    def __init__(self, name: str):
        self.name = name
        self.in_love_percent = random.randint(0, 100)

    def print(self):
        print(f"[{self.name}] -> {self.in_love_percent}%")

ioc = IOCContainer()
ioc.register_singleton(AppConfig, AppConfig(user_name="Manuel"))
ioc.register_transient(LoveCalculator, lambda x: LoveCalculator(
    name=x.get(AppConfig).username)
    )

ioc.get(LoveCalculator).print()
# output: Manuel -> 20%

ioc.get(LoveCalculator).print()
# output: Manuel -> 53%


```

### Scoped

Register a scoped resource this can be used to get the same instance every time as long as you are in the scope.
Another usage could be session aware stuff like opening and closing a db session within that scope.

```Python

class Database():
    def __init__(self, connection_string: str):
        self._cs = connection_string
        self._session_factory = SessionFactory()

    def get_session(self) -> Generator[Session, None, None]
        session = self._session_factory()
        try:
            yield session
        except:
            session.rollback()
        finally:
            session.close()


ioc = IOCContainer()
ioc.register_singleton(AppConfig, AppConfig(connection_string="Secret123"))
ioc.register_singleton(Database, lambda x: Database(
    connection_string=x.get(AppConfig).connection_string
    )
)
ioc.register_scoped(Session, lambda: x.get(Database).get_session)
ioc.register_transient(LoveCalculator, lambda x: LoveCalculator(
    db_session = x.get(Session)
))

#DB Session gets automatically closed when leaving the scope 
with ioc.create_scope() as scope:
    scope.get(LoveCalculator).print()



```

## Development

Run basic tests

```BASH

# Option 1
# Install package local to prevent module not found errors
python -m pip install -e .
pytest tests/

#option 2
# By using this approach the sys part gets automatically added
python -m pytest tests/

```

Run coverage check

```powershell
python -m coverage run -m unittest discover -s tests -p test*.py; python -m coverage report; python -m coverage html
```

Build and deploy

```BASH

python -m build
python -m twine upload dist/*

```