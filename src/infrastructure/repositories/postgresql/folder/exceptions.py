class FolderNotFound(Exception):
    def __init__(self):
        super().__init__('Folder not found.')


