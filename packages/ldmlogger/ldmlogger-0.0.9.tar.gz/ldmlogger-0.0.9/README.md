# LDMLogger

Class LDMLogger contains methods for working with LDM framework. Basically it is python wrapper around LDM framework REST API.

By using this class provided methods users can:
 - [start/finish](#Creating-runs) runs
 - [log message](#Logging-messages) to a current run 
 - [upload file](#Uploading-files) to a current run
 - [upload sources](#Uploading-sources) (directory of files, excluding files matched by ldmignore file) to a current run
 - [upload silver data](#Uploading-silver-data) for a given run

 Detailed description of these methods (in a form of pydoc documentation is given [here](#Pydoc-documentation)).

 Tutorial:

 To start using functionality provided by ldmlogger you need to install package ldmlogger. It can be done by in a following way:
 ```bash
  pip install ldmlogger
 ```
 Also you need to have:
  - an IP adress of a running instance of LDM framework (TODO: Vai dot seit linku uz local host vai uz palaisto platformu uz 185...)
  - a permission to create a user or credentials of already created user (to login to LDM framework)
  - id of a project in LDM framework, that you want to work with
  - user token that is issued by the LDM platform for the specific user.

  After all aforementioned things have been acquired the first thing that we can do is create a run.

## Creating runs

```python
from logger import LDMLogger

user_token_loc = "<InsertYourTokenHere>"
project_id_loc = "<InsertYourProjectID>"
ldm_server_address = "<InsertServerAddress>"

#create instance of LDMLogger
lgr = LDMLogger(user_token_loc, 
                project_id_loc, 
                ldm_server_address
)

lgr.start_run("my first run")

lgr.finish_run()
```

Code seen in a listing above connects to LDM framework instance located at the address ```ldm_server_address```, "logins" to this framework with token ```user_token_loc```, and creates (starts and finishes) a run for project ```project_id_loc```.

## Logging messages

```python
from logger import LDMLogger

user_token_loc = "<InsertYourTokenHere>"
project_id_loc = "<InsertYourProjectID>"
ldm_server_address = "<InsertServerAddress>"

#create instance of LDMLogger
lgr = LDMLogger(user_token_loc, 
                project_id_loc, 
                ldm_server_address
)

lgr.start_run("my first run")

lgr.log({"msg": "first message"})

lgr.finish_run()
```
Code seen in a listing above is appended with just one additional line compared to previous example. Line ```lgr.log({"msg": "first message"})``` creates a log message inside a current run. Method ```log``` gets a free form JSON object as a parameter.

## Uploading files

```python
from logger import LDMLogger

user_token_loc = "<InsertYourTokenHere>"
project_id_loc = "<InsertYourProjectID>"
ldm_server_address = "<InsertServerAddress>"

#create instance of LDMLogger
lgr = LDMLogger(user_token_loc, 
                project_id_loc, 
                ldm_server_address
)

lgr.start_run("my first run")

lgr.upload_file("./abc.txt")

lgr.finish_run()
```
Line ```lgr.upload_file("./abc.txt")``` takes file from path passed as a parameter ("./abc.txt" in this case) and uploads this file to LDM server (Uploaded file will be attached to a current run). Path is resolved against current directory.

## Uploading sources
```python

TODO: update this when LDMLogger has new version of upload sources

from logger import LDMLogger

user_token_loc = "<InsertYourTokenHere>"
project_id_loc = "<InsertYourProjectID>"
ldm_server_address = "<InsertServerAddress>"

#create instance of LDMLogger
lgr = LDMLogger(user_token_loc, 
                project_id_loc, 
                ldm_server_address
)

lgr.start_run("my first run")

lgr.upload_sources()

lgr.finish_run()
```
Code seen in a listing above is appended with just one additional line compared to previous example. Line ```lgr.upload_file("./abc.txt")``` takes file from path passed as a parameter ("./abc.txt" in this case) and uploads this file to LDM server (within a current run). Path is resolved against current directory.

## Uploading silver data

```python
from logger import LDMLogger

user_token_loc = "<InsertYourTokenHere>"
project_id_loc = "<InsertYourProjectID>"
ldm_server_address = "<InsertServerAddress>"

#create instance of LDMLogger
lgr = LDMLogger(user_token_loc, 
                project_id_loc, 
                ldm_server_address
)

lgr.start_run("my first run")

results_on_test_data_set = [
    {
        'file': 'file1.jpeg',
        'silver': 'A'
    },
    {
        'file': 'file2.jpeg',
        'silver': 'B'
    },
]

lgr.validate(results_on_test_data_set, 'Test')

lgr.finish_run()
```

TODO: vai LDMLogger.validate ir labs metodes vards  ? Vai nebut labak to aaukt par upload_silver_data ? Reali jau nekada validaciju tas neveic.

Code seen in a listing above uploads silver data for Test dataset in a specific run of a specific project to LDM server. Method validate takes 2 parameters. The second tells for what kind of data set we upload silver data (Test in our case). The first one specifies silver data to be uploaded. This silver data is in fact a list of objects, where each object has 2 fields: 'file' - specifing name of the file for which we provide silver label and 'silver', specifiying the value of the silver label for this file. Variable ```results_on_test_data_set``` contains an example of this kind of list. There are 2 objects. The first one saying that for file 'file1.jpeg', value of silver label is 'A'. The second one saying that for file 'file2.jpeg' value of silver label is 'B'.


# Pydoc documentation
Detailed python method description (pydocs).

Class LDMLogger contains methods for working with LDM framework.

## Methods:

- ```python 
  def __init__(self, 
               user_token, project_id=None, 
               server_url="http://localhost:5000",
               root_dir=Path(os.getcwd()).parent,
               should_upload_sources = False)
   ```
    Creates new instance of class LDMLogger. 
    
    **Parameters**:
    - user_token:str - user token. Can be obtained insede LDM framework.
    - project_id:str - ID of the project for which we are creating run. This ID can be obtained in LDM. 
    - server_url:str - IP address of LDM server instance.
    - root_dir:str - path to root_dir. Is used only in upload sources.
    - should_upload_sources:boolean. Set to True if sources shoud be uploaded when run is started.

    **Returns**: None


- ```Python 
  def start_run(self, 
                comment = "", git_commit_url = "")
  ```
    Starts a new run.
    
    **Parameters**: 

    - comment (string): Comment for a run.  This parameter is optional and can be ommited.

    - git_commit_url (string): URL of a git commit representing the state of a code base used in this run. This parameter is optional and can be ommited.
    
    **Returns**: None  

- ```Python
    def log(self, log_msg_obj):
  ```
  Logs object, representing log message to server.
    
    **Parameters**: 

    - log_msg_obj: Object representing message to log 

    **Returns**: None
- ```Python
  def finish_run(self):
  ```

    Finish the current run.
    
    **Returns**: None

- ```Python
  def validate(self, results, dataset_type="Train"):
  ```
    Uploads silver data for (Train/Test/Validate) dataset  to server.
      
    **Parameters**: 
    
    - silver_data: list. List of objects representing silver data. Each object must have fields 'file', representing file name and 'silver', representing silver label for this file.
    
    - dataset_type: str . One of Train, Validation, Test.
    
    **Returns**: 

    None

- ```Python
  def upload_file(self, file_name, comment = ""):
  ```

    Uploads file (file_name) to the logging server and attaches it to the current run.
    
    **Parameters**: 

    - file_name (string): File path (on a local machine) of file to be uploaded.

    - comment (string): Comment for a file to be uploaded.  This prm is optional and can be ommited.
    
    **Returns**: 

    None

- ```Python
  def add_project(self, name, project_type, description=""):
  ```
    Creates project on LDM server.
    
    **Parameters**: 
    
    - name:str  - name of a project to be created 
    - project_type:str - one of  "ImageClassification", "ImageCaptioning", "VideoTranscription", "AudioTranscription"
    - description:str - project description. This prm is optional. 
    
    **Returns**: 

    project_id in case of successfull project creation or None in case of errors

- ```Python
  def upload_dataset(self, path_to_dataset,dataset_type_in="Train"):
  ```
    Creates .zip file of path_to_dataset dir and its subdirs and uploads this .zip as a dataset_type_in dataset.
      
    **Parameters**: 
    - path_to_dataset - path to dir to be zipped.
    - dataset_type_in - one of Train, Test, Validation

    **Returns**: 

    None

- ```Python
  def upload_sources(self, ldmignore_path = "ldmignore.txt"):
  ```
    Creates a .zip of root_dir (passed in constructor) and uploads this .zip to the LDM server. 
    In case if root_dir is None no action is performed (method exits immediately).
  
    **Parameters**: 

    - ldmignore_path - path to .gitignore style file, containing dirs and files to be ignored when uploading sources to LDM. 
  
    **Returns**: 

    None
- ```Python
  def download_dataset(self, path="", dataset_type_in="Train"):
  ```
    Downloads dataset from server.
        
    **Parameters**: 
    - path - path to dir, where to put downloaded .zip file
    - dataset_type_in - one of Train, Test, Validation
    
    **Returns**: 

    None

- ```Python
  def save_colab_notebook_history_to_file(self, file_name):
  ```
    Use this function to save the history of executed cells in IPython notebook to a new notebook (file_name).
      
    **Parameters**: 

    - file_name (string): Path to file were notebook will be stored.
    
    **Returns**: 

    None



