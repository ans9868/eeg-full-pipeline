FROM bitnamilegacy/spark:4.0.0

WORKDIR /app

COPY shared/app.py /app/app.py
COPY shared/jobs.py /app/jobs.py
COPY standard/session_builder.py /app/session_builder.py
COPY --chmod=755 standard/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["spark-submit", "--conf", "spark.jars.ivy=/tmp/.ivy2", "/app/app.py", "--job", "all"]
