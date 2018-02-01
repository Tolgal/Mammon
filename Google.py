
def get_credentials(file_Name):
	"""Gets valid user credentials from storage.

	Returns: Credentials, the obtained credential.
	"""
	credential_dir = 'Credentials'
	credential_path = os.path.join(credential_dir,file_Name)

	store = Storage(credential_path)
	credentials = store.get()
	return credentials
