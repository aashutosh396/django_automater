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

    ``` python
    python manage.py makemigrations <app_name>
    ```
    ``` python
    python manage.py migrate <app_name>
    ```

+ **Step 3:** Now go to the location of this django_automater.py and run the following command:
    ``` python
    python django_automater.py
    ```


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



## Additional Steps to make asethetic UI

+ Copy the following code to the end of the dashboard-base.html

    ```html
    <!-- MDB -->
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/3.10.1/mdb.min.js"></script>

    <!-- Jquery -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"
        integrity="sha512-894YE6QWD5I59HgZOGReFYm4dnWc1Qt5NtvYSaNcOP+u1T9qYdvdihz0PPSiiqn/+/3e7Jo4EaG7TubfWGUrMQ=="
        crossorigin="anonymous" referrerpolicy="no-referrer"></script>

    <!-- Data Tables Jquery-->
    <script type="text/javascript" charset="utf8"
        src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.js"></script>

    <script>
    $(document).ready(function () {
        $('#create_table').DataTable();
    });
    </script>
    ```

+ Copy the following code to the head section of the dashboard-base.html

    ```html

    <!-- Bootstrap -->
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

    <!-- MDBootstrap -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css" rel="stylesheet" />
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet" />
    
    <!-- MDB -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/3.10.1/mdb.min.css" rel="stylesheet" />

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"
        integrity="sha512-KfkfwYDsLkIlwQp6LFnl8zNdLGxu9YAA1QvwINks4PhcElQSvqcyVLLD9aMhXd13uQjoXtEKNosOWaZqXgel0g=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />

    <!-- Data Tables CSS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.12.1/css/jquery.dataTables.css">
    ```
