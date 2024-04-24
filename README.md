### MediCare-Rx
Project assignment for Programming


1. Unzip the .ZIP-archive to an empty directory

2. Go to the directory on the commandline (`cd <dir-name>`)

3. Install a Python Virtual Environment:  
   Windows: `py -m venv .venv`  
   Linux: `python3 -m venv .venv`

4. Activate the VEnv:  
   Windows: `.\.venv\Scripts\activate`  
   Linux: `source ./.venv/bin/activate`

5. Install requirements in the VEnv:  
   Windows: `py -m pip install -r requirements.txt`  
   Linux: `python3 -m pip install -r requirements.txt`

6. Run the create_db script:  
   Windows: `py .\Instance\create_db.py`  
   Linux: `python3 ./Instance/create_db.py`

7. Start the API server:  
   Windows: `py .\Server\api.py`  
   Linux: `python3 ./Server/api.py`

8. In order to work with CLI you have to write
   Windows: `py .\'Warehouse CLI'\stock_manager_cli.py`
   Linux: `python3 ./'Warehouse CLI'/stock_manager_cli.py`
