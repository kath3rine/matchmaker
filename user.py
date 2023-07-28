from helpers import get_image, get_data

class User:

    def __init__(self, uid):
        self.uid = uid
        self.data = get_data(self.uid, 'users')
        self.name = self.data['display_name']
        self.pfp = get_image(self.data)
        self.url = self.data['external_urls']['spotify']