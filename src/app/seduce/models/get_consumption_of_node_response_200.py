from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetConsumptionOfNodeResponse200")


@attr.s(auto_attribs=True)
class GetConsumptionOfNodeResponse200:
    """
    Attributes:
        name (Union[Unset, str]):  Example: Consumption of node {{nodeID}} from last {{from}} hours.
        unit (Union[Unset, str]):  Example: watt.
        sum_ (Union[Unset, float]): Total consumption in kWh Example: 1100.
        data (Union[Unset, List[List[float]]]): array of tuples, first is timestamp and secone is value in watt Example:
            [[1675782805000, 113.4]].
    """

    name: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    sum_: Union[Unset, float] = UNSET
    data: Union[Unset, List[List[float]]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        unit = self.unit
        sum_ = self.sum_
        data: Union[Unset, List[List[float]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data

                data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if unit is not UNSET:
            field_dict["unit"] = unit
        if sum_ is not UNSET:
            field_dict["sum"] = sum_
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        unit = d.pop("unit", UNSET)

        sum_ = d.pop("sum", UNSET)

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = cast(List[float], data_item_data)

            data.append(data_item)

        get_consumption_of_node_response_200 = cls(
            name=name,
            unit=unit,
            sum_=sum_,
            data=data,
        )

        get_consumption_of_node_response_200.additional_properties = d
        return get_consumption_of_node_response_200

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
