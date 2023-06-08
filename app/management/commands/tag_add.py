from django.core.management.base import BaseCommand
from file_tools import traverse_dir
from django.conf import settings



class Command(BaseCommand):
    help = """
    arguments:
        1) -fp  : Folder path (required)
        2) -fn  : Folder name (required)
        3) -ex  : extensions of file
        4) -script : the script which will be replaced
    Example:
        python manage.py tag_add -fp "D:\github_projects\ga_vy\ga\app\templates" -fn "demo_files"
    -script "tag_demo.txt" -ex ".html"
    """
    def add_arguments(self, parser):
        parser.add_argument('-fp', nargs='+', type=str)
        parser.add_argument('-fn', nargs='+', type=str)
        parser.add_argument('-ex', nargs='+', type=str)
        parser.add_argument('-scripts', nargs='+', type=str)

    def handle(self, *args, **options):
        folder_path = options["fp"]
        folder_name = options["fn"]
        scripts = options["scripts"]
        extensions = options["ex"]
        files = traverse_dir(folder_name[0], folder_path[0], extensions=tuple(extensions))

        search_text= ""
        replace_text = ""

        for script in scripts:
            with open(script, "r") as sf:
                search_text = sf.readline()

            with open (script,'r') as sf:
                replace_text = sf.read()

            for file in files:
                print(file)
                with open(file, 'r', encoding="utf-8") as fp:
                    data = fp.read()
                if 'finalytics.js' not in data:
                    data = data.replace(search_text, replace_text)
                    with open(file, 'w') as fp:
                        fp.write(data)
        

