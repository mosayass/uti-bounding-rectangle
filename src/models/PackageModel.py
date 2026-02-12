
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config, Detection, ROI, KeyPoints

class ConfigCustomColors(Config):
    """
    A comma-separated list of hex color codes (e.g., #FF0000, #00FF00) to customize the palette.
    """
    name: Literal["configCustomColors"] = "configCustomColors"
    value: str = Field(default="#000000")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    @validator('value')
    def validate_and_clean_hex_codes(cls, v):
        if not v or not v.strip():
            return v
        raw_parts = [part.strip() for part in v.split(',')]
        valid_colors = []
        hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

        for part in raw_parts:
            if not part or part == '#':
                continue
            if not part.startswith('#') and re.match(r'^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', part):
                part = '#' + part
            if re.match(hex_pattern, part):
                valid_colors.append(part)
            else:
                raise ValueError(f"Undefined hex color code: '{part}'. The format must be #RRGGBB.")
        if not valid_colors:
            return v

        return ", ".join(valid_colors)

    class Config:
        title = "Custom Colors"
        json_schema_extra = {
            "shortDescription": "Custom Hex Colors"
        }


class ColorPaletteCustom(Config):
    name: Literal["ColorPaletteCustom"] = "ColorPaletteCustom"
    configCustomColors: ConfigCustomColors
    value: Literal["custom"] = "custom"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Custom"


class ConfigPaletteSize(Config):
    """
    Determines the total number of distinct colors to generate from the selected palette.
    """
    name: Literal["ConfigPaletteSize"] = "ConfigPaletteSize"
    value: int = Field(default=10, ge=1, le=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Color Palette Size"
        json_schema_extra = {
            "shortDescription": "Palette Color Count"
        }


class ColorPaletteTab20c(Config):
    name: Literal["ColorPaletteTab20c"] = "ColorPaletteTab20c"
    configPaletteSize: ConfigPaletteSize
    value: Literal["tab20c"] = "tab20c"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Tab20c"


class ColorPaletteTab20b(Config):
    name: Literal["ColorPaletteTab20b"] = "ColorPaletteTab20b"
    configPaletteSize: ConfigPaletteSize
    value: Literal["tab20b"] = "tab20b"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Tab20b"


class ColorPaletteTab20(Config):
    name: Literal["ColorPaletteTab20"] = "ColorPaletteTab20"
    configPaletteSize: ConfigPaletteSize
    value: Literal["tab20"] = "tab20"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Tab20"


class ColorPaletteTab10(Config):
    name: Literal["ColorPaletteTab10"] = "ColorPaletteTab10"
    configPaletteSize: ConfigPaletteSize
    value: Literal["tab10"] = "tab10"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Tab10"


class ColorPaletteSet3(Config):
    name: Literal["ColorPaletteSet3"] = "ColorPaletteSet3"
    configPaletteSize: ConfigPaletteSize
    value: Literal["Set3"] = "Set3"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Set3"


class ColorPaletteSet2(Config):
    name: Literal["ColorPaletteSet2"] = "ColorPaletteSet2"
    configPaletteSize: ConfigPaletteSize
    value: Literal["Set2"] = "Set2"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Set2"


class ColorPaletteSet1(Config):
    name: Literal["ColorPaletteSet1"] = "ColorPaletteSet1"
    configPaletteSize: ConfigPaletteSize
    value: Literal["Set1"] = "Set1"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Set1"


class ColorPaletteDark2(Config):
    name: Literal["ColorPaletteDark2"] = "ColorPaletteDark2"
    configPaletteSize: ConfigPaletteSize
    value: Literal["Dark2"] = "Dark2"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Dark2"


class ColorPaletteAccent(Config):
    name: Literal["ColorPaletteAccent"] = "ColorPaletteAccent"
    configPaletteSize: ConfigPaletteSize
    value: Literal["Accent"] = "Accent"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Accent"


class ColorPalettePaired(Config):
    name: Literal["ColorPalettePaired"] = "ColorPalettePaired"
    configPaletteSize: ConfigPaletteSize
    value: Literal["Paired"] = "Paired"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Paired"


class ColorPalettePastel2(Config):
    name: Literal["ColorPalettePastel2"] = "ColorPalettePastel2"
    configPaletteSize: ConfigPaletteSize
    value: Literal["Pastel2"] = "Pastel2"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Pastel2"


class ColorPalettePastel1(Config):
    name: Literal["ColorPalettePastel1"] = "ColorPalettePastel1"
    configPaletteSize: ConfigPaletteSize
    value: Literal["Pastel1"] = "Pastel1"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Pastel1"


class ConfigColorPalette(Config):
    """
    Selects the color palette used for drawing bounding boxes.
    Includes standard matplotlib maps and custom options.
    """
    name: Literal["ConfigColorPalette"] = "ConfigColorPalette"
    value: Union[
        ColorPalettePastel1,
        ColorPalettePastel2,
        ColorPalettePaired,
        ColorPaletteAccent,
        ColorPaletteDark2,
        ColorPaletteSet1,
        ColorPaletteSet2,
        ColorPaletteSet3,
        ColorPaletteTab10,
        ColorPaletteTab20,
        ColorPaletteTab20b,
        ColorPaletteTab20c,
        ColorPaletteCustom
    ]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Color Palette"
        json_schema_extra = {
            "shortDescription": "Color Scheme"
        }


class ColorAxisClass(Config):
    name: Literal["Class"] = "Class"
    value: Literal["Class"] = "Class"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Class"


class ColorAxisIndex(Config):
    name: Literal["Index"] = "Index"
    value: Literal["Index"] = "Index"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Index (ROI)"


class ColorAxisTrack(Config):
    name: Literal["Track"] = "Track"
    value: Literal["Track"] = "Track"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Track"


class ConfigColorAxis(Config):
    """
    Determines how colors are assigned to bounding boxes.
    'Class' colors by object type, 'Index' by sequence, 'Track' by tracking ID.
    """
    name: Literal["ConfigColorAxis"] = "ConfigColorAxis"
    value: Union[ColorAxisClass, ColorAxisIndex, ColorAxisTrack]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Color Axis"
        json_schema_extra = {
            "shortDescription": "Color Assignment Logic"
        }


class ConfigRadius(Config):
    """
    Sets the radius of the bounding box corners in pixels.
    Use 0 for sharp corners, or higher values for rounded corners.
    """
    name: Literal["ConfigRadius"] = "ConfigRadius"
    value: int = Field(default=0, ge=0, le=50)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Radius"
        json_schema_extra = {
            "shortDescription": "Corner Radius (px)"
        }


class ConfigThickness(Config):
    """
    Sets the thickness of the bounding box lines in pixels.
    """
    name: Literal["ConfigThickness"] = "ConfigThickness"
    value: int = Field(default=2,ge=1, le=10)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Thickness"
        json_schema_extra = {
            "shortDescription": "Line Thickness (px)"
        }


class BoundingRectangleConfigs(Configs):
    """
    Aggregates all visualization settings for drawing bounding rectangles.
    Controls color assignment logic, color palettes, line thickness, and corner radius.
    """
    configColorAxis: ConfigColorAxis
    configColorPalette: ConfigColorPalette
    configThickness: ConfigThickness
    configRadius: ConfigRadius

    class Config:
        title = "Bounding Rectangle Configurations"
        json_schema_extra = {
            "shortDescription": "Bounding Rectangle Visual Settings"
        }

class Detection(Detection):
    """
    Extends the base Detection to ensure we accept the keyPoints
    generated by the YOLO Segmentation model.
    """
    keyPoints: Optional[List[KeyPoints]] = None
    # We also accept 'angle' if OBB mode was used, though unlikely for segmentation
    angle: Optional[float] = None

class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: Union[List[Detection], List[ROI]]
    type: str = "list"

    class Config:
        title = "Detections/ROI"

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class BoundingRectangleInputs(Inputs):
    inputImage: InputImage
    inputDetections: InputDetections

    class Config:
        title = "Bounding Rectangle Inputs"


class BoundingRectangleOutputs(Outputs):
    outputImage: OutputImage

    class Config:
        title = "Bounding Rectangle Outputs"

class BoundingRectangleRequest(Request):
    inputs: Union[BoundingRectangleInputs]
    configs: BoundingRectangleConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class BoundingRectangleResponse(Response):
    outputs: BoundingRectangleOutputs

    class Config:
        title = "Bounding Rectangle Response"


class BoundingRectangleExecutor(Config):
    name: Literal["BoundingRectangle"] = "BoundingRectangle"
    value: Union[BoundingRectangleRequest, BoundingRectangleResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Bounding Rectangle Executor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[BoundingRectangleExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }

class PackageConfigs(Configs):
    executor: ConfigExecutor

    class Config:
        title = "Package Configurations"

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["BoundingRectangle"] = "BoundingRectangle"

    class Config:
        title = "Package Model"