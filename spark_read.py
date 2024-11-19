from pyspark import SparkContext, SparkConf, SQLContext
import random
import json
import os


CONFIG_FILE = "config.json"


def configure_spark(config_file):

    conf = SparkConf() \
    .setAppName(config_file['sparkapp']['name'] + " " + str(random.randint(1,5000))) \
    .setMaster(config_file['url']['master']) \
    .set("spark.driver.extraClassPath", config_file['environment']['connector_jar']) \
    .set("spark.driver.cores", config_file['cores']['driver']) \
    .set("spark.executor.memory", config_file['memory']['executor']) \
    .set("spark.executor.cores", config_file['cores']['executor'])

    sc = SparkContext(conf=conf)

    return sc


def mysql_query(user, password, server, database, query):

    with open(CONFIG_FILE, 'r') as infile:
        config_data = json.load(infile)

    if config_data['environment']['PYSPARK_PYTHON'] != "DEFAULT PATH":
        os.environ["PYSPARK_PYTHON"] = config_data['environment']['PYSPARK_PYTHON']

    url = "jdbc:mysql://" + server + "/" + database

    sc = configure_spark(config_data)
    sqlContext = SQLContext(sc)
    spark = sqlContext.sparkSession
    pd = []

    try:

        jdbcdf = spark.read.format("jdbc") \
            .option("url", url) \
            .option("query", query) \
            .option("user", user) \
            .option("password", password) \
            .option("driver", config_data['sparkapp']['driver']) \
            .load()

        pd = jdbcdf.toPandas()

    except Exception as e:
        print(e)

    finally:
        spark.stop()
        return pd