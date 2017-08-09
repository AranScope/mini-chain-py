FROM python:3-onbuild
COPY . /usr/src/app
EXPOSE 8000
CMD ["python", "run.py"]