+ **Step 1**: Copy this django_automater.py to the location of the app you want to automate.

For example:

+ <app_name>
    + migrations/
    + models.py
    + admin.py
    + apps.py
    + tests.py
    + urls.py (optional, this may not exist in a newly created app, our script will automatically generate it)
    + views.py
    + django_automater.py (our script file here)

+ **Step 2:** Write down the models in the models.py -> makemigrations -> migrate

+ **Step 3:** Now go to the location of this django_automater.py and run the following command:
    + python django_automater.py



<hr style="
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
">

Note: Make sure that this a new app if you do it on any app that is previously created then it will destory all the code you have done up until now. If your app is already created follow the instruction below.

+ If you app is already created:
    + copy the models.py to a seperate location. (it can be anywhere in the system)
    + copy the django_automater.py to the same folder
    + Note: good approach is create a folder and keep models.py and django_automater.py inside it and perform the actions.
    + delete the not required model class from the models.py (meaning that if those models have already been used and do not need to be automated)
    + run the python command to run django automater **(python django_automater.py)**
    + You will have views.py, urls.py, templates/ folder with all the required templates created and linked with each other.


