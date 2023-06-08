from django.core.management.base import BaseCommand
from file_tools import traverse_dir
from django.conf import settings

class Command(BaseCommand):
    help = """
    arguments:
        1) -fp  : Folder path (required)
        2) -fn  : Folder name (required)
        3) -ex  : extensions of file
        4) -st  : search text
        5) -rt  : replace text

    Example:
        1) for script file
        python manage.py tag_path_replace -fp "D:\github_projects\ga_vy\ga\app\templates" -fn "demo_files_replace_path" -ex ".html" -st "https://finpixel.s3.us-east-2.amazonaws.com" -rt "https://finalytics.blackstone.studio/ga/"
    """
    def add_arguments(self, parser):
        parser.add_argument('-fp', type=str)
        parser.add_argument('-fn', type=str)
        parser.add_argument('-ex', type=str)
        parser.add_argument('-st', type=str)
        parser.add_argument('-rt', type=str)

    def handle(self, *args, **options):
        folder_path=options["fp"]
        folder_name=options["fn"]
        extensions = options["ex"]
        search_text=options["st"]
        replace_text=options["rt"]

        files = traverse_dir(folder_name, folder_path, extensions=tuple(extensions))
        print(files)
        for file in files:
            with open(file, 'r') as fp:
                data_original = fp.read()
                data = data_original.replace(search_text, replace_text)
            if data != data_original:
                with open(file, 'w') as fp:
                    fp.write(data)
        
