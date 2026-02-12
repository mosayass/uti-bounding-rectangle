
from sdks.novavision.src.helper.package import PackageHelper
from components.DrawBoundingRectangle.src.models.PackageModel import PackageConfigs, ConfigExecutor,PackageModel,OutputDetections,BoundingRectangleOutputs,BoundingRectangleExecutor,BoundingRectangleResponse


def build_response(context):
    output_detections = OutputDetections(value=context.detections)
    detect_outputs = BoundingRectangleOutputs(outputDetections=output_detections)
    bounding_rectangle_response = BoundingRectangleResponse(outputs=detect_outputs)
    bounding_rectangle_executor = BoundingRectangleExecutor(value=bounding_rectangle_response)
    executor = ConfigExecutor(value=bounding_rectangle_executor)
    package_configs = PackageConfigs(executor=executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    packageModel = package.build_model(context)
    return packageModel