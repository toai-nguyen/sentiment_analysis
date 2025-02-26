# Dockerfile
FROM python:3.9-slim

# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    default-jre \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Java (yêu cầu cho Spark)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
RUN ln -s /usr/lib/jvm/default-java $JAVA_HOME

# Tải và cài đặt Apache Spark
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
RUN curl -L "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" | tar -xz -C /usr/local/ \
    && ln -s /usr/local/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /usr/local/spark

# Thiết lập biến môi trường cho Spark
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYSPARK_PYTHON=python3

# Cài đặt thư viện Python cần thiết
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt Jupyter Notebook
RUN pip install jupyter

# Tạo thư mục cho notebook
WORKDIR /notebooks
COPY notebooks/ .

# Thiết lập thư mục làm việc chính
WORKDIR /app

#Expose port cho Flask và Jupyter
EXPOSE 5000 8888

# Lệnh khởi động mặc định (có thể override trong docker-compose)
CMD ["bash"]