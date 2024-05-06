import os
import re
import json

list_html = '''
    <h2>List of Items</h2>
    <a href="{{create_url}}">Create New</a>
    <table>
        <thead>
            <tr>
                {% for field_name in fields %}
                    <th>{{ field_name }}</th>
                {% endfor %}
                <th> Actions </th>
            </tr>
        </thead>
        <tbody>
            {% for item in data %}
            <tr>
                {% for field_name in fields %}
                {% for key,value in item.items %}
                {% if key == field_name %}
                <td>{{value}}</td>
                {% endif %}
                {% endfor %}
                {% endfor %}
                <td>
                    <a href="{% url detail_url pk=item.id %}">Detail</a>
                    <a href="{% url update_url pk=item.id %}">Update</a>
                    <a href="{% url confirm_delete_url pk=item.id %}">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
'''


detail_html = '''
    <h2>Item Detail</h2>
    <table>
        <tbody>
            {% for field, value in data.items %}
                <tr>
                    <th>{{ field }}</th>
                    <td>{{ value }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <a href="{% url update_url pk=object.id %}">Update</a>
    <a href="{% url confirm_delete_url pk=object.id %}">Delete</a>
'''

confirm_delete_html = '''
    <h2>Delete Item</h2>
    <p>Are you sure you want to delete "{{ object.name }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Delete</button>
    </form>
'''


form_html = '''
    <h2>Create Item</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>
'''

def generate_html_files(folder_location, model_and_template, fields):
    model_name, template_name = model_and_template
    file_path = os.path.join(folder_location, 'templates', pascal_to_snake_case(model_name) , template_name)

    view = ''
    if 'list.html' in file_path:
        view = 'list'    
    elif 'detail.html' in file_path:
        view = 'detail'
    elif 'update.html' or 'create.html' in file_path:
        view = 'form'
    elif 'confirm_delete.html' in file_path:
        view = 'confirm_delete'

    html_data = generate_html_content(model_name, view , fields)
    
    base_template = "dashboard-base.html"
    block_name = "main"

    with open(file_path, "w") as f:
        f.write(f"{{% extends '{base_template}' %}}\n")
        f.write(f"{{% block {block_name} %}}\n")
        
        f.write(html_data)
    
        f.write("{% endblock %}")


def generate_html_content(model_name, view, fields):
    title = model_name.title()
    if view == 'list':
        return list_html
    elif view == 'detail':
        return detail_html
    elif view in ['form']:
        return form_html
    elif view == 'confirm_delete':
        return confirm_delete_html
    

def fetch_template_names(folder_location, data):
    template_names = []
    for model_folder in data['model_folders']:
        current_model = model_folder['related_model']
        for url_info in model_folder['urls']['urls']:
            template_names.append([current_model,url_info['template_name']])
        
        for template in template_names:
            fields = fetch_fields(template[0], data)
            generate_html_files(folder_location, template, fields)

    # return template_names

def fetch_fields(model_name, data):
    fields_info = []
    for model_folder in data['model_folders']:
        if model_folder['related_model'] == model_name:
            fields_info = model_folder['fields']['fields']
            break
    return fields_info



# Function to read JSON data from file
def read_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def create_view_file(folder_location, data):
    """
    Create a views file based on the provided JSON data.
    """
    views_file = os.path.join(folder_location, "views.py")

    with open(views_file, 'w') as f:
        f.write(f"from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView\n")
        f.write(f"from django.urls import reverse_lazy\n")
        f.write(f"from .models import *\n")

    with open(views_file, "a") as f:
        for model_folder in data["model_folders"]:

            for url_info in model_folder["urls"]["urls"]:
                
                current_success_url = ''
                current_create_url = ''
                current_update_url = ''
                current_delete_url = ''
                current_detail_url = ''

                for url_data in model_folder["urls"]["urls"]:                
                    for item, value in url_data.items():
                        if item == "name":
                            if "list" in value:
                                list_view_name = value
                                current_success_url = list_view_name
                                break

                            if "create" in value:
                                create_view_name = value
                                current_create_url = create_view_name
                                break

                            if "update" in value:
                                update_view_name = value
                                current_update_url = update_view_name
                                break

                            if "delete" in value:
                                delete_view_name = value
                                current_delete_url = delete_view_name
                                break

                            if "detail" in value:
                                detail_view_name = value
                                current_detail_url = detail_view_name
                                break
                            


                view_class_name = url_info["view"]
                view_name = view_class_name.replace("View", "").lower()
                model_name = model_folder["related_model"]
                template_name = f'{pascal_to_snake_case(model_name)}/{url_info["template_name"]}'
                success_url = current_success_url

                if "list" in view_name:
                    f.write(f"class {view_class_name}(ListView):\n")
                    f.write(f"    model = {model_name}\n")
                    f.write(f"    template_name = '{template_name}'\n\n")
                    f.write(f"    def get_context_data(self, **kwargs):\n")
                    f.write(f"        context = super().get_context_data(**kwargs)\n")
                    f.write(f"        fields = [field.name for field in {model_name}._meta.fields]\n")
                    f.write(f"        items = self.get_queryset()\n")
                    f.write(f"        data_list = []\n")
                    f.write(f"        for item in items:\n")
                    f.write(f"            data = {{field: getattr(item, field) for field in fields}}\n")
                    f.write(f"            data_list.append(data)\n")
                    f.write(f"        context['data'] = data_list\n")
                    f.write(f"        context['fields'] = fields\n")
                    f.write(f"        context['create_url'] = reverse_lazy('{current_create_url}')\n")
                    f.write(f"        context['update_url'] = '{current_update_url}'\n")
                    f.write(f"        context['detail_url'] = '{current_detail_url}'\n")
                    f.write(f"        context['confirm_delete_url'] = '{current_delete_url}'\n")
                    f.write(f"        return context\n\n")


                elif "detail" in view_name:
                    f.write(f"class {view_class_name}(DetailView):\n")
                    f.write(f"    model = {model_name}\n")
                    f.write(f"    template_name = '{template_name}'\n\n")
                    f.write(f"    def get_context_data(self, **kwargs):\n")
                    f.write(f"        context = super().get_context_data(**kwargs)\n")
                    f.write(f"        item = self.get_object()\n")
                    f.write(f"        fields = [field.name for field in {model_name}._meta.fields]\n")
                    f.write(f"        data = {{field: getattr(item, field) for field in fields}}\n")
                    f.write(f"        context['data'] = data\n")
                    f.write(f"        context['fields'] = fields\n")
                    f.write(f"        context['update_url'] = '{current_update_url}'\n")
                    f.write(f"        context['confirm_delete_url'] = '{current_delete_url}'\n")
                    f.write(f"        return context\n\n")

                elif "delete" in view_name:
                    f.write(f"class {view_class_name}(DeleteView):\n")
                    f.write(f"    template_name = '{template_name}'\n")
                    f.write(f"    model = {model_name}\n")
                    f.write(f"    success_url = reverse_lazy('{success_url}')\n\n")

                elif "update" in view_name:
                    f.write(f"class {view_class_name}(UpdateView):\n")
                    f.write(f"    model = {model_name}\n")
                    f.write(f"    fields = '__all__'\n")
                    f.write(f"    template_name = '{template_name}'\n")
                    f.write(f"    success_url = reverse_lazy('{success_url}')\n\n")

                elif "create" in view_name:
                    f.write(f"class {view_class_name}(CreateView):\n")
                    f.write(f"    model = {model_name}\n")
                    f.write(f"    fields = '__all__'\n")
                    f.write(f"    template_name = '{template_name}'\n")
                    f.write(f"    success_url = reverse_lazy('{success_url}')\n\n")



def initialize_urls(urls_location):
    with open(urls_location, "w") as f:
        f.write("from django.urls import path\n")
        f.write("from .views import *\n\n")
        f.write("urlpatterns = [\n")
        f.write("    # Auto-generated URLs\n")
        f.write("]\n")
        


def create_django_urls(class_name, urls_location):
    """
    Create Django URL patterns for the given folder name and insert them into the urlpatterns list
    in the specified URLs file. If the URLs file exists, insert the URL patterns into the urlpatterns list.
    If it doesn't exist, create the file and write the urlpatterns list along with the URL patterns.
    """
    urls = [
        f"    path('{class_name.lower()}/', {class_name}ListView.as_view(), name='{pascal_to_snake_case(class_name)}-list'),",
        f"    path('{class_name.lower()}/create/', {class_name}CreateView.as_view(), name='{pascal_to_snake_case(class_name)}-create'),",
        f"    path('{class_name.lower()}/<int:pk>/update/', {class_name}UpdateView.as_view(), name='{pascal_to_snake_case(class_name)}-update'),",
        f"    path('{class_name.lower()}/<int:pk>/', {class_name}DetailView.as_view(), name='{pascal_to_snake_case(class_name)}-detail'),",
        f"    path('{class_name.lower()}/<int:pk>/delete/', {class_name}DeleteView.as_view(), name='{pascal_to_snake_case(class_name)}-delete'),\n\n",
    ]

    urls_content = "\n".join(urls)
    created_urls = []

    # # Check if the URLs file exists
    if os.path.exists(urls_location):
        # Read the contents of the URLs file
        with open(urls_location, "r") as f:
            lines = f.readlines()

        # Find the urlpatterns list and insert the URL patterns
        with open(urls_location, "w") as f:
            for line in lines:
                if "urlpatterns" in line:
                    f.write(line)
                    f.write(urls_content)
                else:
                    f.write(line)
        
        # Collect the created URLs
        for url in urls:
            name = url.split("name='")[1].split("'")[0]
            template_name = ''

            if name.__contains__('list'):
                template_name = f'{pascal_to_snake_case(class_name)}_list.html'
            elif name.__contains__('create'):
                template_name = f'{pascal_to_snake_case(class_name)}_form.html'
            elif name.__contains__('update'):
                template_name = f'{pascal_to_snake_case(class_name)}_form.html'
            elif name.__contains__('delete'):
                template_name = f'{pascal_to_snake_case(class_name)}_confirm_delete.html'
            elif name.__contains__('detail'):
                template_name = f'{pascal_to_snake_case(class_name)}_detail.html'

            created_urls.append({
                "name": name,
                "url":  url.split("path('")[1].split("'")[0],
                "view": url.split(".as_view()")[0].split(',')[1].strip(),
                "template_name": template_name
            })

            view_name = url.split(".as_view()")[0].split(',')[1].strip()
    
    return {"urls": created_urls}



def create_django_template(folder_location, folder_name, base_template="base.html", block_name="main"):
    """
    Create Django template files in the specified folder location with the given folder name.
    """
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_location):
        os.makedirs(folder_location)

    # Define template file names
    template_files = [
        f"{folder_name}_form.html",
        f"{folder_name}_list.html",
        f"{folder_name}_detail.html",
        f"{folder_name}_confirm_delete.html"
    ]

    # Iterate through template files and create them with content
    for file_name in template_files:
        file_path = os.path.join(folder_location, file_name)
        file_type = file_name.split('_')[1] 

        try:
            with open(file_path, "w") as f:
                f.write(f"{{% extends '{base_template}' %}}\n")
                f.write(f"{{% block {block_name} %}}\n")
                
                if file_name.__contains__('form'):
                    f.write('form')
                elif file_name.__contains__('list'):
                    f.write("    <!-- Add your list content here -->\n")
                elif file_name.__contains__('detail'):
                    f.write("    <!-- Add your detail content here -->\n")
                elif file_name.__contains__('delete'):
                    f.write("confirm_delete_content")
            
                f.write("{% endblock %}")
            print("File created successfully.")  # Debug print
        except Exception as e:
            print("Error creating file:", e)


def fetch_class_names(models_file):
    class_names = []
    
    # Check if the models file exists
    if not os.path.exists(models_file):
        return {"error": "Models file not found."}

    # Extract class names from the file
    with open(models_file, "r") as file:
        content = file.read()
        matches = re.findall(r'class\s+(\w+)\s*\(', content)
        class_names.extend(matches)

    return class_names



def fetch_fields_and_types(models_file, model_name):
    fields_info = {"fields": []}
    
    # Check if the models file exists
    if not os.path.exists(models_file):
        return {"error": "Models file not found."}
    
    # Read the content of the models file
    with open(models_file, "r") as file:
        content = file.read()
        
        # Find the model class definition
        pattern = r'class\s+' + model_name + r'\(models.Model\):(.+?)(?=class\s+|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        # If the model class is found
        if match:
            # Extract fields and their types
            fields_text = match.group(1)
            fields_matches = re.findall(r'\s+(\w+)\s*=\s*models\.(\w+)\(', fields_text)
            
            # Populate the fields_info dictionary
            for field_name, field_type in fields_matches:
                fields_info["fields"].append({"name": field_name, "type": field_type})
        else:
            return {"error": "Model not found."}

    return fields_info


def pascal_to_snake_case(name):
    # Convert PascalCase to snake_case
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def create_model_folders(folder_location):
    # Check if the given folder location exists
    if not os.path.exists(folder_location):
        return {"error": "Folder location does not exist."}

    # Look for a models file inside the given location
    models_file = os.path.join(folder_location, "models.py")
    if not os.path.exists(models_file):
        return {"error": "Models file not found."}

    # Get class names from the models file
    class_names = fetch_class_names(models_file)
    if not class_names:
        return {"error": "No classes found in the models file."}




    # Create a templates folder in the initial folder
    templates_folder = os.path.join(folder_location, "templates")
    os.makedirs(templates_folder, exist_ok=True)

    base_template = "dashboard-base.html"
    block_name = "main"
    # Get user input for extending file and block name
    extend_file = input("Enter file to extend with (default is dashboard-base.html): ")
    if extend_file:
        base_template = extend_file.strip()

    extend_block = input("Enter block name to extend with (default is main): ")
    if extend_block:
        block_name = extend_block.strip()

    # Create a folder for each class inside the templates folder
    urls_location = os.path.join(folder_location, "urls.py")
    model_folders = []

    initialize_urls(urls_location)

    for class_name in class_names:
        field_names = fetch_fields_and_types(models_file, class_name)
        model_folder_name = os.path.join(templates_folder, pascal_to_snake_case(class_name))
        os.makedirs(model_folder_name, exist_ok=True)
        model_info = {"folder": pascal_to_snake_case(class_name), "location": model_folder_name, "related_model": class_name, "fields": field_names}
        
        create_django_template(model_folder_name, pascal_to_snake_case(class_name), base_template, block_name)
        current_urls = create_django_urls(class_name, urls_location)

        model_info['urls'] = current_urls
        model_folders.append(model_info)

    # Store the model_folders dictionary as a JSON file
    json_file_path = os.path.join(folder_location, "model_folders.json")
    with open(json_file_path, "w") as json_file:
        json.dump({"model_folders": model_folders}, json_file, indent=4)

    json_file_path = os.path.join(folder_location, "model_folders.json") 
    data = read_json(json_file_path)
    
    create_view_file(folder_location, data)
    fetch_template_names(folder_location, data)


    return {"model_folders": model_folders, "json_file_path": json_file_path}



if __name__ == "__main__":
    current_folder_location = os.path.dirname(os.path.abspath(__file__))
    folder_location = current_folder_location
    result = create_model_folders(folder_location)
