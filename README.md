# Streamlit Portfolio
Welcome to my github repo! You can access the webpage via my website: itsmejoeyong.com

This is the main branch of my streamlit portfolio, all other branches (except dev) have been structured to more easily convey the logic & codebase.

The main branch essentially integrates all the other branches & features into a sidebar on the top left, with dynamic link generation for each project. For more information press the provided link in the main webpage.

New data will be fetched for any data-related projects on a daily basis.

```
root/
│
├── .streamlit/
│   └── config.toml   
│       # contains streamlit configurations
│
├── src/
│   ├── pages/
│   │   ├── projects/
│   │   │   ├── src/
│   │   │   │   # contains project src code, mainly abstracts logic away from each projects app.py
│   │   │   │   
│   │   │   └── app.py
│   │   │       # each projects main entrypoint
│   │   │
│   │   └── homepage.py
│   │       # homepage project main entrypoint
│   │
│   └── streamlit_text_functions.py 
│       # contains functions to manipulate streamlit text more easily
│
├── app.py
│   # main logic & entrypoint
│
├── requirements.txt  
│   # Python requirements file
...
```

# NOTES
> pipeline.py is used to refresh the data from any project that requires fresh data to be fetched, further efforts will be put into abstracting multiple project's pipeline.py into a single entrypoint.