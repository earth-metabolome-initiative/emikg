# Use an official Miniconda runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory to /app
WORKDIR /app

# We clone the dirty-pipeline repository
RUN git clone https://github.com/enpkg/enpkg_full.git

# We need to checkout the correct branch of the dirty-pipeline repository
# to make sure that the enricher works as expected, namely the branch
# called "emikg-adapt".
RUN cd enpkg_full && git checkout emikg-adapt

# We install all requirements specified in the dirty-pipeline repository
# environment.yml file.
RUN conda env create -f enpkg_full/environment.yml

# We run the conda init command
RUN conda init bash

# We activate the enpkg_full environment
RUN echo "source activate enpkg_full" > ~/.bashrc

# We install jq
RUN apt-get update && apt-get install -y jq unzip curl

# We install Sirius using the bash script provided by the dirty-pipeline repository
RUN bash enpkg_full/src/install_sirius.sh v5.8.6

# Set the permission to allow the execution of the files under
# the /app/sirius/bin directory
RUN chmod +x /app/sirius/bin

# We copy the content of the dirty-pipeline repository into the container
COPY enrichers/enricher-dirty-pipeline /app

# We copy the enrichers folder into the container at /app
COPY enrichers/enrichers /app/enrichers

# Similarly, we copy the alchemy wrapper directory from the database.
COPY postgres-configuration/alchemy_wrapper /app/alchemy_wrapper

# And then we copy the emikg interfaces
COPY emikg_interfaces /app/emikg_interfaces

# We make sure that the pip version is up to date
RUN pip install --upgrade pip

# We install the emikg interfaces
RUN pip install -e ./emikg_interfaces

# We install the alchemy wrapper package so to make it available to the run.py script
RUN pip install -e ./alchemy_wrapper

# We install the enrichers package so to make it available to the run.py script
RUN pip install -e ./enrichers

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run run.py when the container launches
CMD ["python", "run.py"]
