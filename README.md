# Streamlit Portfolio
Welcome to my github repo! You can access the webpage via my website: itsmejoeyong.com

This is the main branch of my streamlit portfolio, all other branches (except dev) have been structured to more easily convey the logic & codebase.

The main branch essentially integrates all the other branches & features into a sidebar on the top left, with dynamic link generation for each project. For more information press the provided link in the main webpage.

```
root/
│
├── .streamlit/
│   └── config.toml   
│       # contains streamlit configurations
│
├── src/
│   ├──pages/
│   │   # contains streamlit page integrations from other branches/projects
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