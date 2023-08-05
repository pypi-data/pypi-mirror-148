# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ConnectivityCheckHost(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'host_id': 'str',
        'nics': 'list[ConnectivityCheckNic]'
    }

    attribute_map = {
        'host_id': 'host_id',
        'nics': 'nics'
    }

    def __init__(self, host_id=None, nics=None):  # noqa: E501
        """ConnectivityCheckHost - a model defined in Swagger"""  # noqa: E501

        self._host_id = None
        self._nics = None
        self.discriminator = None

        if host_id is not None:
            self.host_id = host_id
        if nics is not None:
            self.nics = nics

    @property
    def host_id(self):
        """Gets the host_id of this ConnectivityCheckHost.  # noqa: E501


        :return: The host_id of this ConnectivityCheckHost.  # noqa: E501
        :rtype: str
        """
        return self._host_id

    @host_id.setter
    def host_id(self, host_id):
        """Sets the host_id of this ConnectivityCheckHost.


        :param host_id: The host_id of this ConnectivityCheckHost.  # noqa: E501
        :type: str
        """

        self._host_id = host_id

    @property
    def nics(self):
        """Gets the nics of this ConnectivityCheckHost.  # noqa: E501


        :return: The nics of this ConnectivityCheckHost.  # noqa: E501
        :rtype: list[ConnectivityCheckNic]
        """
        return self._nics

    @nics.setter
    def nics(self, nics):
        """Sets the nics of this ConnectivityCheckHost.


        :param nics: The nics of this ConnectivityCheckHost.  # noqa: E501
        :type: list[ConnectivityCheckNic]
        """

        self._nics = nics

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ConnectivityCheckHost, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ConnectivityCheckHost):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
