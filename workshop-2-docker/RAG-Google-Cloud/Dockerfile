FROM python:3.10-slim

WORKDIR /AIForIndustry

COPY . .

RUN pip install -r requirements.txt

RUN python data_storage/db.py

# Run app.py when the container launches
CMD ["python", "app.py"]

# The devcontainer.json file will overwrite this CMD command by default with something like the following:
# ENTRYPOINT ["/bin/bash", "-c"]