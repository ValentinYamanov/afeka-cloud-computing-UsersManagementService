# afeka-cloud-computing-UsersManagementService
UsersManagementService  for Afeka Cloud Tech Class

# Software Requirements:
	The app use Port: 5000
	Check if you have python version 3.9 on the pc by typing the command "python --version" from cmd or terminal,
	if the output is "Python 3.9" you can start from step 2.
	
	 1. Install Python 3.9 (Link For Win64: https://www.python.org/ftp/python/3.9.7/python-3.9.7-embed-amd64.zip,
						  linux: https://docs.python-guide.org/starting/install3/linux)
		   a. Run the installation with default configuration.
		   b. Check the check box for "Add Pythone 3.9 to PATH"
		
	 2. Navigate to the project folder on your PC with CMD or therminal.
		   and type "python --version", make shore that the response is: "Python 3.9.7".
		   after that from the project folder type the command "pip install -r requirements.txt" to let python install packages
		   that the project uses.
			    List of packages:
				     a. Flask~=2.0.2
				     b. requests~=2.26.0
				
	 3. To deploy the service navigate to the "src" folder then type the command "flask run"
	    the server shuld start and the text will be: "Running on http://127.0.0.1:5000/"
	

# How to use the API:
	1. if you have a postman on your pc, you can import our collection from "\tests\postman"
		  Filename "User Management Local.postman_collection"
	2. after adding the collection to postman you can use the queries from the collection.
	
	
	postman Link:https://www.postman.com/downloads/
