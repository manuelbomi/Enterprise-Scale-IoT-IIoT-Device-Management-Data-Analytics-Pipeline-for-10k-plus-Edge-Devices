from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.processing import ScriptProcessor
from sagemaker.estimator import Estimator
from sagemaker.workflow.parameters import ParameterString
from sagemaker.workflow.pipeline_context import PipelineSession

pipeline_session = PipelineSession()

bucket = "your-cleaned-bucket"
role = "arn:aws:iam::123456789012:role/SageMakerExecutionRole"

input_data_uri = f"s3://{bucket}/cleaned/"

# Training parameters
train_image = "382416733822.dkr.ecr.us-west-2.amazonaws.com/linear-learner:latest"

estimator = Estimator(
    image_uri=train_image,
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    output_path=f"s3://{bucket}/models/",
)

step_train = TrainingStep(
    name="TrainTempModel",
    estimator=estimator,
    inputs={
        "train": f"{input_data_uri}"
    }
)

pipeline = Pipeline(
    name="TemperaturePredictionPipeline",
    steps=[step_train],
    sagemaker_session=pipeline_session
)
