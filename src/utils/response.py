
from sdks.novavision.src.helper.package import PackageHelper
from components.DrawBoundingRectangle.src.models.PackageModel import PackageConfigs, ConfigExecutor,PackageModel,OutputImage,BoundingRectangleOutputs,BoundingRectangleExecutor,BoundingRectangleResponse


def build_response(context):
    output_image = OutputImage(value=context.image)
    detect_outputs = BoundingRectangleOutputs(outputImage=output_image)
    bounding_rectangle_response = BoundingRectangleResponse(outputs=detect_outputs)
    bounding_rectangle_executor = BoundingRectangleExecutor(value=bounding_rectangle_response)
    executor = ConfigExecutor(value=bounding_rectangle_executor)
    package_configs = PackageConfigs(executor=executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    packageModel = package.build_model(context)
    return packageModel