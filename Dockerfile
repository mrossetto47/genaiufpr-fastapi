FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

COPY . .

CMD ["conda", "run", "--no-capture-output", "-n", "travel_api", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]