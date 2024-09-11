import grpc
from concurrent import futures
import filetransfer_pb2
import filetransfer_pb2_grpc

class FileTransferServicer(filetransfer_pb2_grpc.FileTransferServicer):
    def SendFile(self, request_iterator, context):
        for file_chunk in request_iterator:
            # Process the file chunk (e.g., write it to disk, store in memory, etc.)
            print(f"Received chunk for file: {file_chunk.filename}, chunk size: {len(file_chunk.content)}")
        return filetransfer_pb2.FileResponse(message="File received successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    filetransfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
