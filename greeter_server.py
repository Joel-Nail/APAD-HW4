# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
from email.message import Message
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

from datetime import date
from datetime import datetime
import random


class Greeter(helloworld_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

  def SayHelloAgain(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)


# creates a list of random numbers and creates a data_id_string using the provided project_id and datetime
# these variables are then returned to the client 
class dataProvider(helloworld_pb2_grpc.dataProviderServicer):

    def sendData(self, request, context):
        intList = []
        for i in range(0, 10):
            x = random.randint(0, 1000)
            intList.append(str(x))
        
        data_id_string = request.project_id + "_" + str(datetime.now())
        
        return helloworld_pb2.Data(data_id=data_id_string, data_elements=intList)
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    helloworld_pb2_grpc.add_dataProviderServicer_to_server(dataProvider(), server) # DON'T FORGET THIS!!
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
