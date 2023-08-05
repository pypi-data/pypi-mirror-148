from typing import Any
from typing import Dict
from typing import Type

from enot_lite.backend import BackendFactory
from enot_lite.benchmark.backend_runner import BackendRunner
from enot_lite.benchmark.backend_runner import EnotBackendRunner
from enot_lite.benchmark.backend_runner import TorchCpuRunner
from enot_lite.benchmark.backend_runner import TorchCudaRunner
from enot_lite.type import BackendType
from enot_lite.type import ModelType

__all__ = [
    'OrtCpuBackendRunnerBuilder',
    'OrtOpenvinoBackendRunnerBuilder',
    'OpenvinoBackendRunnerBuilder',
    'OrtCudaBackendRunnerBuilder',
    'OrtTensorrtBackendRunnerBuilder',
    'OrtTensorrtFp16BackendRunnerBuilder',
    'TorchCpuBackendRunnerBuilder',
    'TorchCudaBackendRunnerBuilder',
]


class OrtCpuBackendRunnerBuilder:  # pylint: disable=missing-class-docstring
    def __call__(
            self,
            onnx_model,
            onnx_input: Dict[str, Any],
            model_type: ModelType,
            inter_op_num_threads,
            intra_op_num_threads,
            enot_backend_runner: Type[EnotBackendRunner],
            **_ignored,
    ) -> BackendRunner:
        backend = BackendFactory().create(
            model=onnx_model,
            backend_type=BackendType.ORT_CPU,
            model_type=model_type,
            input_example=onnx_input,
            inter_op_num_threads=inter_op_num_threads,
            intra_op_num_threads=intra_op_num_threads,
        )
        return enot_backend_runner(backend, onnx_input)


class OrtOpenvinoBackendRunnerBuilder:  # pylint: disable=missing-class-docstring
    def __call__(
            self,
            onnx_model,
            onnx_input: Dict[str, Any],
            model_type: ModelType,
            inter_op_num_threads,
            intra_op_num_threads,
            openvino_num_threads,
            enot_backend_runner: Type[EnotBackendRunner],
            **_ignored,
    ) -> BackendRunner:
        backend = BackendFactory().create(
            model=onnx_model,
            backend_type=BackendType.ORT_OPENVINO,
            model_type=model_type,
            input_example=onnx_input,
            inter_op_num_threads=inter_op_num_threads,
            intra_op_num_threads=intra_op_num_threads,
            openvino_num_threads=openvino_num_threads,
        )
        return enot_backend_runner(backend, onnx_input)


class OpenvinoBackendRunnerBuilder:  # pylint: disable=missing-class-docstring
    def __call__(
            self,
            onnx_model,
            onnx_input: Dict[str, Any],
            model_type: ModelType,
            enot_backend_runner: Type[EnotBackendRunner],
            **_ignored,
    ) -> BackendRunner:
        backend = BackendFactory().create(
            model=onnx_model,
            backend_type=BackendType.OPENVINO,
            model_type=model_type,
            input_example=onnx_input,
        )
        return enot_backend_runner(backend, onnx_input)


class OrtCudaBackendRunnerBuilder:  # pylint: disable=missing-class-docstring
    def __call__(
            self,
            onnx_model,
            onnx_input: Dict[str, Any],
            model_type: ModelType,
            enot_backend_runner: Type[EnotBackendRunner],
            **_ignored,
    ) -> BackendRunner:
        backend = BackendFactory().create(
            model=onnx_model,
            backend_type=BackendType.ORT_CUDA,
            model_type=model_type,
            input_example=onnx_input,
        )
        return enot_backend_runner(backend, onnx_input)


class OrtTensorrtBackendRunnerBuilder:  # pylint: disable=missing-class-docstring
    def __call__(
            self,
            onnx_model,
            onnx_input: Dict[str, Any],
            model_type: ModelType,
            enot_backend_runner: Type[EnotBackendRunner],
            **_ignored,
    ) -> BackendRunner:
        backend_instance = BackendFactory().create(
            model=onnx_model,
            backend_type=BackendType.ORT_TENSORRT,
            model_type=model_type,
            input_example=onnx_input,
        )
        return enot_backend_runner(backend_instance, onnx_input)


class OrtTensorrtFp16BackendRunnerBuilder:  # pylint: disable=missing-class-docstring
    def __call__(
            self,
            onnx_model,
            onnx_input: Dict[str, Any],
            model_type: ModelType,
            enot_backend_runner: Type[EnotBackendRunner],
            **_ignored,
    ) -> BackendRunner:
        backend_instance = BackendFactory().create(
            model=onnx_model,
            backend_type=BackendType.ORT_TENSORRT_FP16,
            model_type=model_type,
            input_example=onnx_input,
        )
        return enot_backend_runner(backend_instance, onnx_input)


class TorchCpuBackendRunnerBuilder:  # pylint: disable=missing-class-docstring
    def __call__(
            self,
            torch_model,
            torch_input,
            torch_cpu_runner: Type[TorchCpuRunner],
            **_ignored,
    ) -> BackendRunner:
        return torch_cpu_runner(torch_model=torch_model, torch_input=torch_input)


class TorchCudaBackendRunnerBuilder:  # pylint: disable=missing-class-docstring
    def __call__(
            self,
            torch_model,
            torch_input,
            torch_cuda_runner: Type[TorchCudaRunner],
            **_ignored,
    ) -> BackendRunner:
        return torch_cuda_runner(torch_model=torch_model, torch_input=torch_input)
