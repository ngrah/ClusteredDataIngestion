import ipyparallel as ipp
import json
import jsonschema
import pandas as pd
import time


# from fhir.resources.patient import Patient
def list_files_in_path(path):
    import os
    file_paths = []
    for root, dirs, files in os.walk(path):
            for file in files:
                # print(os.path.join(root, file))
                file_paths.append(os.path.join(root, file))
    return file_paths

def path_split(path_list,num_exc):
    list_of_path_lists = []
    exc_list_size = len(path_list) // num_exc
    remainder = len(path_list) % num_exc
    start_index = 0
    for i in range(num_exc):
        exc_list_end = start_index + exc_list_size + (1 if i < remainder else 0)
        list_of_path_lists.append(path_list[start_index:exc_list_end])
        start_index = exc_list_end
    return list_of_path_lists

def path_to_json(path):
    with open(path) as json_file:
        file_data = json.load(json_file)
        return file_data
def path_to_validated_json(path,schema):
    from jsonschema import validate
    with open(path) as json_file:
        file_data = json.load(json_file)
        file_data
        try:
            validate(file_data, schema)
            return file_data
        except jsonschema.exceptions.ValidationError as ex:
            print(ex)
            return ""
        return file_data
def schema_type_match(entity_name, schema_path):
    if entity_name == "patient":
        return path_to_json(schema_path + "/patient.schema.json")
    if entity_name == "fhir":
        return path_to_json(schema_path + "/fhir.schema.json")
    if entity_name == "bundle":
        return path_to_json(schema_path + "/bundle.schema.json")

    def par_file_read(list_of_paths):
        task_durations = [4] * 25
        with ipp.Cluster("mpi", 4) as cluster:
            cluster.start_cluster()
            client = cluster.start_and_connect_sync()
            rc = cluster.connect_client_sync()
            view = rc[:]
            view.activate()
            json_list = map(path_to_json, list_of_paths)



if __name__ == '__main__':
    resource_path = '/home/nick/PycharmProjects/ClusteredDataIngestion/venv/resources'
    # todo parameterize resource path,
    synthea_path = resource_path + "/synthea_sample_data_fhir_r4_nov2021/"
    path_list = list_files_in_path(synthea_path)

    # todo parameterize num executors
    num_executors = 4
    executor_path_lists = path_split(path_list, num_executors)


    json_record = path_to_json(path_list.pop())
    schema_path = resource_path+"/schema"
    json_schema = schema_type_match("bundle", schema_path)

    # json_record = path_to_validated_json(path_list.pop(), json_schema)
    print(json_record)

