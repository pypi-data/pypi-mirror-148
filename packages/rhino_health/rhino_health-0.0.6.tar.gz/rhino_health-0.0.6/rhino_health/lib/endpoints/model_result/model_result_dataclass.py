from typing import Annotated, Any, Optional

from pydantic import Field

from rhino_health.lib.dataclass import RhinoBaseModel


class ModelResult(RhinoBaseModel):
    uid: str
    """The unique ID of the ModelResult"""
    action_type: str
    """The type of action preformed"""
    status: str
    """The action status"""
    start_time: str
    """The action start time"""
    end_time: Any = None
    """The action end time"""
    _aimodel: Any = None
    input_cohorts: list[str]
    """The input cohort"""
    output_cohorts: list[str]
    """The output cohort"""
    aimodel_uid: Annotated[dict, Field(alias="aimodel")]
    """The relevant aimodel object"""
    result_info: Optional[str]
    """The run result info"""
    results_report: Optional[str]
    """The run result report"""
    report_images: list[Any]
    """The run result images"""
    model_params_external_storage_path: Optional[str]
    """The external storage path"""

    @property
    def aimodel(self):
        if self._aimodel:
            return self._aimodel
        if self.aimodel_uid:
            self._aimodel = self.session.aimodel.get_aimodel(self._aimodel)
            return self._aimodel
        else:
            return None
