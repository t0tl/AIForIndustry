# Workshop 2 - AI for Industry - Docker and Google Cloud

This project is part of a series of workshops aimed at teaching students how to work with data at scale. In this workshop, we focus on Docker via a RAG (Retrieval Augmented Generation) pipeline using OpenAIs API and hosting on Google Cloud.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes or directly on Google Cloud.

### Prerequisites

What things you need to install the software and how to install them.

* Docker Engine
* Google Cloud SDK
* Google Cloud account
* OpenAI API keys

Regardless of deployment mode you need to keep your API keys safe. For this repo, I am storing the OpenAI API keys inside Google Clouds Secretmanger service.

### Local development / testing
To test locally, you can use the devcontainer extension for Visual Studio Code or you can manually build and run the docker image/container using (assuming you are inside the `RAG-Google-Cloud` directory)

When using the devcontainer, I am assuming you have your Google Cloud credentials in the default location in Ubuntu based systems. If you are not using the devcontainer, you can run the following commands to build and run the docker container with Google Cloud credentials mounted:
```bash
docker build -t <tag> .
docker run -it -p 8989:8989 --entrypoint /bin/bash <tag> -v ~/.config/gcloud:/root/.config/gcloud
```
Skip the `--entrypoint /bin/bash` if you want to just run the server directly. If you do run the container with the entrypoint as `/bin/bash` you can then run the server by running
```bash
python app.py
```
Now navigate to `http://localhost:8989` and you can now prompt ChatGPT.


### Google Cloud deployment

To deploy on Google Cloud, you need to have a Google Cloud account and have the Google Cloud SDK installed. You can then run the following commands to deploy the container to Google Cloud Run:

```bash
gcloud builds submit --tag gcr.io/<project-id>/<tag>
gcloud run deploy --image gcr.io/<project-id>/<tag> --platform managed
```

Note that you will also need to do additional set up to access your web app. You can find more information on how to do this [here](https://cloud.google.com/run/docs/quickstarts/build-and-deploy).