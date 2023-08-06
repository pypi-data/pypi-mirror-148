from logger import LDMLogger
import os, json
import requests

def main():
    print("Starting main ... ")

    # specific to the user
    user_token = "pbkdf2:sha256:260000$CpJyGMH69vOQsMpp$0aeab9b4cb502c9305fb0806d50fd86927fe628cabb46501b5ecf0b17421b272"
    
    # specific to the project
    project_id = "6266737da114437f6ced64ef"

    logger = LDMLogger(user_token, project_id, "http://185.23.162.188:3000")
    logger.start_run("Experiment 1")

    learning_rate = 0.02
    epochs = 200
    hidden_nodes = 11
    output_nodes = 1

    logger.log({"learning_rate": learning_rate,
                "epochs": epochs,
                "hidden_nodes": hidden_nodes,
                "output_nodes": output_nodes,
            })


    logger.upload_file('./captioning.py', "captioning.py")

    results = [
                {"file": "image_0242.jpg", "silver": "buttercup",},
            ]

    logger.validate(results, "Train")
    # logger.validate(results, "Validate")
    # logger.validate(results, "Test")


    logger.finish_run()


    
main()



