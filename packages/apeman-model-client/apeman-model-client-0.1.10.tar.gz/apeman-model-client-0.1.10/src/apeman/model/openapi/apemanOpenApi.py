import logging
import os

import grpc

from apeman.model.modelInstanceTaskStatus_pb2 import ModelInstanceTaskStatus
from apeman.model.openapi import apemanOpenApi_pb2
from apeman.model.openapi import apemanOpenApi_pb2_grpc
from apeman.model.openapi.model_instance_task_status import TaskStatus

logging.basicConfig(level=logging.DEBUG)


class ApemanModelServiceClient(object):

    def __init__(self):
        apeman_meta_server_addr = os.getenv("apeman_meta_server_addr")
        if apeman_meta_server_addr is None:
            raise RuntimeError('Invalid value of apeman_meta_server_addr')

        logging.debug('Connect to APEMAN meta server %s', apeman_meta_server_addr)
        channel = grpc.insecure_channel(apeman_meta_server_addr)
        self.__stub = apemanOpenApi_pb2_grpc.ApemanModelOpenApiStub(channel)

    def report(self, task_id='', status=TaskStatus.NONE, progress=0.0, message='', token=''):
        print('report....')
        model_instance_task_status = ModelInstanceTaskStatus.Value(status.value)
        request = apemanOpenApi_pb2.TaskStatusReportRequest(modelInstanceTaskId=task_id,
                                                            status=model_instance_task_status,
                                                            progress=progress,
                                                            token=token,
                                                            message=message)
        self.__stub.Report(request)

    def get_endpoint(self, model_instance_id=''):
        request = apemanOpenApi_pb2.GetModelEndpointRequest(modelInstanceId=model_instance_id)
        response = self.__stub.GetModelEndpoint(request)
        return response.endpoint
