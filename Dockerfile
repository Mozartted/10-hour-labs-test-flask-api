FROM python:3.6
ADD . /code
WORKDIR /code

# RUN pip install virtualenv

# RUN source venv/bin/activate
RUN pip install -r requirements.txt
RUN pip install gunicorn
# CMD python app.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:wsgi"]