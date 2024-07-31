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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import time
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import threading

#def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
#     print("Will try to greet world ...")

#     while True:
#         with grpc.insecure_channel("localhost:50051") as channel:
#             stub = helloworld_pb2_grpc.GreeterStub(channel)
#             response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
#         print("Greeter client received: " + response.message)

# --------------------------------- multiple messages --------------------------------
# def run():
#    print("Will try to greet world 100 times...")
#    with grpc.insecure_channel("localhost:50051") as channel:
#        stub = helloworld_pb2_grpc.GreeterStub(channel)

#        # Prepare messages
#        messages = []
#        total_message_bits = 0
#        for _ in range(10):
#            message = helloworld_pb2.HelloRequest(name="you")
#            serialized_message = message.SerializeToString()
#            print("Greeter client received: " + message)
#            message_size_bits = len(serialized_message) * 8  # Convert bytes to bits
#            print(f"message_size_bits: {message_size_bits}")
#            total_message_bits += message_size_bits
#            print(f"total_message_bits: {total_message_bits}")
#            messages.append(message)

#        # Start timer before sending messages
#        start_time = time.time()

#        # Send all messages
#        for message in messages:
#            response = stub.SayHello(message)

#        # Stop timer after sending all messages
#        elapsed_time = time.time() - start_time

#        # Calculate throughput in bits/second
#        throughput_bits_per_second = total_message_bits / elapsed_time
#        print(f"Greeter client received: {response.message}")
#        print(f"Sent 100 messages of total size {total_message_bits} bits in {elapsed_time:.2f} seconds.")
#        print(f"Throughput: {throughput_bits_per_second:.2f} bits/second")

# -------------------------------------- multiple channel 
  
def run():
    print("Will try to greet world in parallel on 5 channels...")

    # Define channel addresses (replace with your actual addresses)
    channel_addresses = ["localhost:50051", "localhost:50052", "localhost:50053", "localhost:50054", "localhost:50055"]

    total_messages_bits = 0
    total_elapsed_time = 0

    for address in channel_addresses:
        with grpc.insecure_channel(address) as channel:
            print("Channel address: " + address)
            stub = helloworld_pb2_grpc.GreeterStub(channel)

            # Prepare messages
            messages = []
            total_message_bits = 0
            for _ in range(10000):
                message = helloworld_pb2.HelloRequest(name="you")
                serialized_message = message.SerializeToString()
                #print("Greeter client received: " + message)
                message_size_bits = len(serialized_message) * 8  # Convert bytes to bits
                #print(f"message_size_bits: {message_size_bits}")
                total_message_bits += message_size_bits
                #print(f"total_message_bits: {total_message_bits}")
                total_messages_bits += message_size_bits
                messages.append(message)

            # Start timer before sending messages
            start_time = time.time()

            # Send all messages
            for message in messages:
                response = stub.SayHello(message)

            # Stop timer after sending all messages
            elapsed_time = time.time() - start_time
            total_elapsed_time += elapsed_time

            # Calculate throughput in bits/second
            throughput_bits_per_second = (total_message_bits / elapsed_time)/1000
            print(f"Greeter client received: {response.message}")
            print(f"Sent 1000 messages of total size {total_message_bits} bits in {elapsed_time:.2f} seconds.")
            print(f"Throughput: {throughput_bits_per_second:.2f} kb/second")

    # Calculate total throughput
    total_throughput_bits_per_second = (total_messages_bits / total_elapsed_time)/1000
    print(f"Total Throughput: {total_throughput_bits_per_second:.2f} kb/second")

if __name__ == "__main__":
    logging.basicConfig()
    run()
