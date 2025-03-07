1. Erstatt secret key i routes.py med egen key som man får tak i på openai sin nettside
2. Kjør ```python run.py```
3. Kjør curls:
```curl "http://127.0.0.1:5000/jobs"```
```curl "http://127.0.0.1:5000/jobs/{id}"```
```curl "http://127.0.0.1:5000/extract?url=https://www.capgemini.com"``` (urferdig)
