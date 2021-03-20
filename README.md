# SchnelltestBot

A quick hack in python. Does 3 things: 
- Checks dm, rossmann, tedi and lidl for the availability of rapid antigen tests
- notifies a telegram group via bot if true
- main.py is a fastapi version of the same thing.

Todo: 
- add threema & signal
- add more sources
- Add Müller. Figure out how this works https://www.mueller.de/p/lyher-covid-19-antigen-nasal-schnelltest-2715778/?showpreview=true (no ID when you place in cart)
- add Müller https://www.mueller.de/p/boson-antigen-covid-19-schnelltest-nasal-2715995/
- Modify the code so that multiple URLs per shop are possible.
- Deploy the FastAPI part somewhere.
- Build frontend for the FastAPI part.
