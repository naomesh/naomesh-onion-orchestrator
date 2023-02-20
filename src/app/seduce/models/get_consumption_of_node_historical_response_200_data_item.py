from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetConsumptionOfNodeHistoricalResponse200DataItem")


@attr.s(auto_attribs=True)
class GetConsumptionOfNodeHistoricalResponse200DataItem:
    """
    Attributes:
        start (Union[Unset, int]):  Example: 1675782804000.
        end (Union[Unset, int]):  Example: 1675782805000.
        data (Union[Unset, List[List[float]]]): array of tuples, first is timestamp and secone is value in watt Example:
            [[1675782805000, 113.4]].
    """

    start: Union[Unset, int] = UNSET
    end: Union[Unset, int] = UNSET
    data: Union[Unset, List[List[float]]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start = self.start
        end = self.end
        data: Union[Unset, List[List[float]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data

                data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = cast(List[float], data_item_data)

            data.append(data_item)

        get_consumption_of_node_historical_response_200_data_item = cls(
            start=start,
            end=end,
            data=data,
        )

        get_consumption_of_node_historical_response_200_data_item.additional_properties = d
        return get_consumption_of_node_historical_response_200_data_item

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
