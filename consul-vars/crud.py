#! /usr/bin/python

import consul
import json
import sys, getopt

class crud():

    def update(self, client, kvp):
        for i in range(len(kvp)):
            consul_path = kvp[i]['path']+"/"+kvp[i]['key']
            value = kvp[i]['value']
            client.kv.put(consul_path, value)
        print 'Success: All Key Values got Updated and Stored in Consul'

    def delete(self, client, key):
        key = key.split(",")
        for k in key:
            consul_path = k
            print consul_path[-1]
            if consul_path[-1] == "/":
                client.kv.delete(consul_path, recurse=True)
                print 'Success: All Key Values got deleted recursively under the path: ',consul_path
            else:
                client.kv.delete(consul_path, recurse=False)
                print 'Success: provided Key Value: ',consul_path,' got deleted'

    def read(self, client, key):
        key = key.split(",")
        for k in key:
            consul_path = k
            if consul_path[-1] == "/":
                value = client.kv.get(consul_path, recurse=True)
                for i in range(len(value[1])):
                    print value[1][i]['Key'].split("/")[-1], value[1][i]['Value']
                    #value[1][0]['Key'].split("/")[-1], value[1][0]['Value']
                    # print 'Success: Key Values which got read recursively under the path are: \n',value
            else:
                value = client.kv.get(consul_path, recurse=False)
                print consul_path, value[1]['Value']
                # print 'Success: Value for the Key provided is: \n',value

    def config(self, client, inputfile):
        key_value_dict = list()
        with open(inputfile) as var_file:
            data = json.load(var_file)

        for comp in data.keys():
            for key_dir in data[comp].keys():
                for i in range(len(data[comp][key_dir]['KeyValues'])):
                    key_value = dict(
                        path = comp+"/"+key_dir+"/KeyValues",
                        key = data[comp][key_dir]['KeyValues'][i]['key'],
                        value = data[comp][key_dir]['KeyValues'][i]['value']
                    )
                    key_value_dict.append(key_value)
                for j in range(len(data[comp][key_dir]['Secrets'])):
                    key_value = dict(
                        path = comp+"/"+key_dir+"/Secrets",
                        key = data[comp][key_dir]['Secrets'][j]['key'],
                        value = data[comp][key_dir]['Secrets'][j]['value']
                    )
                    key_value_dict.append(key_value)

        self.update(client, key_value_dict)


def main(argv):

    c = consul.Consul(host='127.0.0.1', port=8500, token=None, scheme='http', consistency='default', verify=True)
    crudclass = crud()

    try:
        opts, args = getopt.getopt(argv,"hi:d:r:",["input=","delete=","read="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile to push keyvalues> -d <consul keypath to delete keys> -r <consul keypath to get values>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: test.py -i <inputfile> -d <consul keypath> -r <consul keypath>\n'
            print 'where options include:'
            print '\t -i \t --input \t Your input file which has key values in json format'
            print '\t -d \t --delete \t Your KeyPath in cosul to delete the values (Note: use / at the end of the path for recursive delete)'
            print '\t -r \t --read \t Your KeyPath in cosul to read the values (Note: use / at the end of the path for recursive search)\n'
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
            crudclass.config(c, inputfile)
        elif opt in ("-d", "--delete"):
            del_key = arg
            crudclass.delete(c, del_key)
        elif opt in ("-r", "--read"):
            read_key = arg
            crudclass.read(c, read_key)


if __name__ == '__main__':
    main(sys.argv[1:])

