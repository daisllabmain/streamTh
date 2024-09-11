# file_client_utils.py
import csv
import grpc
import filetransfer_pb2
import filetransfer_pb2_grpc
import os
import time
from threading import Lock
import sys

class ChannelStatus:
    def __init__(self):
        self.current_file = "Waiting..."
        self.files_sent = 0
        self.total_size = 0
        self.active_start_time = None
        self.total_active_time = 0
        self.errors = []

    def update(self, filename, size):
        # If the channel was waiting, start timing when transmission begins
        if self.current_file == "Waiting...":
            self.active_start_time = time.time()
        self.current_file = filename
        self.files_sent += 1
        self.total_size += size

    def add_error(self, error):
        self.errors.append(error)

    def pause(self):
        # Stop the timer when the channel goes idle
        if self.active_start_time is not None:
            self.total_active_time += time.time() - self.active_start_time
            self.active_start_time = None
        self.current_file = "Waiting..."

    def get_stats(self):
        # Calculate the final elapsed time
        if self.active_start_time is not None:
            self.total_active_time += time.time() - self.active_start_time
            self.active_start_time = None
        bandwidth = self.total_size / self.total_active_time if self.total_active_time > 0 else 0
        return (self.files_sent, self.total_size, self.total_active_time, bandwidth)

def print_status(channel_statuses, lock):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Channel Status:")
    for name, status in channel_statuses.items():
        print(f"{name}: {status.current_file}")
    print("\nErrors:")
    for name, status in channel_statuses.items():
        for error in status.errors:
            print(f"{name}: {error}")
    sys.stdout.flush()

def send_files_to_channel(channel_name, channel, files, channel_statuses, lock, chunk_size=1 * 1024 * 1024):  # Default 1 MB chunks
    stub = filetransfer_pb2_grpc.FileTransferStub(channel)
    for filename in files:
        if not os.path.exists(filename):
            error = f"Error: File {filename} does not exist."
            with lock:
                channel_statuses[channel_name].add_error(error)
                print_status(channel_statuses, lock)
            continue
        
        try:
            file_size = os.path.getsize(filename)
            with lock:
                channel_statuses[channel_name].update(os.path.basename(filename), file_size)
                print_status(channel_statuses, lock)
                
            def file_chunks_generator():
                with open(filename, 'rb') as f:
                    while chunk := f.read(chunk_size):
                        yield filetransfer_pb2.FileChunk(filename=os.path.basename(filename), content=chunk)
            
            response = stub.SendFile(file_chunks_generator())
        except grpc.RpcError as e:
            error = f"RPC error while sending {filename}: {e}"
            with lock:
                channel_statuses[channel_name].add_error(error)
                print_status(channel_statuses, lock)
        except Exception as e:
            error = f"Unexpected error while sending {filename}: {e}"
            with lock:
                channel_statuses[channel_name].add_error(error)
                print_status(channel_statuses, lock)
    
    # Pause the timer when done
    with lock:
        channel_statuses[channel_name].pause()
        print_status(channel_statuses, lock)


def log_to_csv(log_data, filename="throughput_log.csv"):
    # Save log data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["Iteration", "File Group", "Num Channels", "Channel", "Files Sent", "Total Size (MB)", "Time Taken (s)", "Bandwidth (MB/s)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in log_data:
            writer.writerow(data)