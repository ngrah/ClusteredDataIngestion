import ipyparallel as ipp
import json
import pandas

# from fhir.resources.patient import Patient
def list_files_in_path(path):
    import os
    file_paths = []
    for root, dirs, files in os.walk(path):
            for file in files:
                print(os.path.join(root, file))
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
        print(file_data)
        # pandas.read_json()

#todo json to df

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # cluster = ipp.Cluster()
    # resource_path = '/home/nick/PycharmProjects/pythonProject/venv/resources'
    # todo parameterize resource path,
    resource_path = '/home/nick/PycharmProjects/ClusteredDataIngestion/venv/resources/synthea_sample_data_fhir_r4_nov2021/'
    path_list = list_files_in_path(resource_path)

    # todo parameterize num executors
    num_executors = 4
    executor_path_lists = path_split(path_list,num_executors)
    # print(executor_path_lists)

    path_to_json(path_list.pop())