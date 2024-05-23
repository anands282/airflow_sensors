# airflow_sensors
## What are Sensors in Airflow?
Sensors in Airflow are operators that keep running until a certain condition is met. They are typically used for monitoring external systems or conditions, such as the arrival of a file in a directory, the completion of a task in another system, or the availability of a specific resource.

Sensors work by periodically checking if a condition is satisfied. Once the condition is met, the sensor task is marked as successful and the downstream tasks can proceed. If the condition is not met within a specified timeout period, the sensor task fails.

## Types of Sensors
Airflow provides a variety of built-in sensors, including:

* FileSensor: Waits for a file or directory to land in a filesystem.
* S3KeySensor: Waits for a key (file or folder) to be present in an S3 bucket.
* ExternalTaskSensor: Waits for a task in a different DAG or a different execution to complete.
* HttpSensor: Waits for an HTTP response to be successful.
* SqlSensor: Waits for a SQL query to return a desired result.

In this project, we will focus on the FileSensor, because this is a very common usecase. The files can be FTP or SFTPed into your S3 bucket from source systems and it can be data dumps from nosql databases or logs files. The FileSensor provides an automation possibility which makes the whole process event driven. The file being present in the S3 path is the event and it can trigger the downstream processing of the files or data thats received.

## FileSensor
The FileSensor is used to monitor the existence of a file or directory. It is useful in scenarios where downstream tasks depend on data files being available in a specified location before they can proceed. For instance, you might use a FileSensor to wait for a data file to be uploaded to an FTP server or a local directory.

## Key Parameters
* filepath: The path of the file or directory to wait for.
* fs_conn_id: The connection ID for the file system (e.g., S3, HDFS, etc.). By default, it uses the local file system.
* poke_interval: The time in seconds that the sensor waits before checking the condition again.
* timeout: The maximum amount of time in seconds the sensor waits for the file to be available before failing.
