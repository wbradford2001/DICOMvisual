FROM python:latest


COPY . ./
RUN pip3 install numpy
RUN pip3 install pydicom
RUN pip3 install tk
RUN pip3 install mysql-connector-python
RUN pip3 install matplotlib
RUN pip3 install selenium
RUN pip3 install python-gdcm
RUN pip3 install pylibjpeg






CMD ["python", "master.py"]
