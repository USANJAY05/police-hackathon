FROM python

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
RUN pip install flask numpy pandas scipy scikit-learn matplotlib seaborn statsmodels
# Set the working directory inside the container

# Copy the entire application directory into the container
COPY . .
# Expose port 8080
EXPOSE 8080


CMD ["nohup", "python", "app.py", "&"]
