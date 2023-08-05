"""Wrapper for the Profile API , version 12.0"""

import requests

class ProfileApi():
	def __init__(self , page_access_token):
		self.__graph_version = "12.0"
		self.__api_url = f"https://graph.facebook.com/v{self.__graph_version}/me/messenger_profile"
		self.__page_access_token = page_access_token

	def get_api_url(self):
		return self.__api_url

	def get_access_token(self):
		return self.__page_access_token

	def get_graph_version(self):
		return self.__graph_version

	def set_welcome_screen(self , get_started_button_payload , greetings=[{"locale":"default","text":"Welcome , {{user_full_name}} !"}]):
		"""
		Set the welcome screen of the page. #! <INSERT_DOC_URL>
		A welcome screen is the first screen a person sees when he clicks on the "Send message" button in the page.

		Args:
			get_started_payload (str) : The payload to be sent by the API when the user clicks on "Get started" button.
			greetings (list , optional) : The welcome message.
				Supports multiples locales by specifying the local and the corresponding message.
				Defaults to [{"locale":"default","text":"Welcome , {{user_full_name}} !"}]
		"""
		assert isinstance(greetings , list) and isinstance(greetings[0] , dict) , "param greetings must be a list of dicts"
		assert greetings[0]["locale"] == "default" , "first element of param greetings must be the default locale used"

		request_body = {
			"get_started" :
			{
				"payload" : get_started_button_payload
			},
			"greeting" : greetings
		}

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()

	def set_persistent_menu(self , persistent_menu):
		"""Set the persistent menu for the page.

		Args:
			persistent_menu (PersistentMenu object) : The content of the PersistentMenu object , obtained via the PersistentMenu().get_content() method.
		"""
		return requests.post(
			self.get_api_url() ,
			params={"access_token":self.get_access_token()} ,
			json=persistent_menu
		).json()
