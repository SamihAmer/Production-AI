Hello professors! In order to access my ACR deployment, firstly you will need to login to my ACR: 

az acr login --name acrjhusa1

Then you will need to pull the image: 
docker pull acrjhusa1.azurecr.io/python-flask-app:v1

Lastly, you will need to run the image: 
docker run -p 5000:5000 acrjhusa1.azurecr.io/python-flask-app:v1

In a seperate terminal, put in this command to access the python app locally: 
curl http://localhost:5000  

Please let me know if there is anything I can improve on. Thank you! 