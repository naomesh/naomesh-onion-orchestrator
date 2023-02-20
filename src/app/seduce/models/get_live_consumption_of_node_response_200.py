from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetLiveConsumptionOfNodeResponse200")


@attr.s(auto_attribs=True)
class GetLiveConsumptionOfNodeResponse200:
    """
    Attributes:
        name (Union[Unset, str]):  Example: Live consumption of node {{nodeID}}.
        unit (Union[Unset, str]):  Example: watt.
        data (Union[Unset, float]):  Example: 114.4.
    """

    name: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    data: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        unit = self.unit
        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if unit is not UNSET:
            field_dict["unit"] = unit
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        unit = d.pop("unit", UNSET)

        data = d.pop("data", UNSET)

        get_live_consumption_of_node_response_200 = cls(
            name=name,
            unit=unit,
            data=data,
        )

        get_live_consumption_of_node_response_200.additional_properties = d
        return get_live_consumption_of_node_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
