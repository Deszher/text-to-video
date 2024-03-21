# PyQt6 Video/Audio Player with Text to Speech conversion
На данный момент приложение принимет печатный текст, переводит его в речь.<br> В дальнейшем планируется, что можно будет не только озвучить текст, но и выбрать фотографию или картинку с лицом человека и получить "говорящую голову".

#### Сreate a virtual environment
```bash
  python -m venv .venv
```


#### Activate the virtual environment:
```bash
  source .venv/bin/activate
```

#### Upgrade pip
```bash
  python -m pip install --upgrade pip
```

#### Install all the dependencies listed in the `requirements.txt`
```
  pip install -r requirements.txt
```
____________
# Run Program

### PyQt6-based player
```
  python main.py
```

### Линтинг и форматирование кода

```
black *.py
flake8
```

# Идеи по улучшению проекта

1. Добавить линтер, к примеру flake8

2. Добавить форматтер, к примеру black

3. Создать CI-пайплайн с линтингом, используя github actions

4. Вынести UI в отдельный слой приложения, отделить от логики модели, в сторону Layered или Hexagonal архитектуры

5. Добавить тесты, запускать в github actions
