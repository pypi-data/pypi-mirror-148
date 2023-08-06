class Payloads:
    '''
    Specifies all the payloads available in the system.
    This is a low level class for :class:`~winerp.lib.payload.PayloadTypes`.
    '''
    success = 0
    verification = 1
    request = 2
    response = 3
    error = 4
    ping = 5
    information = 6

class PayloadTypes:
    '''
    Specifies the type of message. Available Types:
        | ``success``: Successful authorization.
        | ``verification``: Verification request.
        | ``request``: Request for a route.
        | ``response``: Response to a request.
        | ``error``: Error response.
        | ``ping``: Ping message.
    '''
    def __init__(self, type: int) -> None:
        self._type = type
    
    def __repr__(self) -> str:
        return '<PayloadTypes: {}>'.format(self._type)
    
    @property
    def success(self) -> bool:
        '''
        :class:`bool`: Returns ``True`` if the message is a success message.
        '''
        return self._type == Payloads.success

    @property
    def verification(self) -> bool:
        '''
        :class:`bool`: Returns ``True`` if the message is a verification message.
        '''
        return self._type == Payloads.verification
    
    @property
    def request(self) -> bool:
        '''
        :class:`bool`: Returns ``True`` if the message is a request message.
        '''
        return self._type == Payloads.request
    
    @property
    def response(self) -> bool:
        '''
        :class:`bool`: Returns ``True`` if the message is a response message.
        '''
        return self._type == Payloads.response
    
    @property
    def error(self) -> bool:
        '''
        :class:`bool`: Returns ``True`` if the message is an error message.
        '''
        return self._type == Payloads.error

    @property
    def ping(self) -> bool:
        '''
        :class:`bool`: Returns ``True`` if the message is a ping message.
        '''
        return self._type == Payloads.ping

    @property
    def information(self) -> bool:
        '''
        :class:`bool`: Returns ``True`` if the message is an information message.
        '''
        return self._type == Payloads.information



class MessagePayload:
    '''
    Represent IPC payload class.
    '''
    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)
        self.type = kwargs.pop('type', None)
        self.route = kwargs.pop('route', None)
        self.traceback = kwargs.pop('traceback', None)
        self.data = kwargs.pop('data', {})
        self.uuid = kwargs.pop('uuid', None)
        self.destination = kwargs.pop('destination', None)
        self.pseudo_object = kwargs.pop('pseudo_object', None)
    

    def from_message(self, msg):
        '''
        Makes a payload from message. This is similar to cloning a message's ``dict`` to a new ``dict`` with same values.

        Parameters
        ----------
        msg: :class:`~winerp.lib.message.WsMessage`
            The message to clone
        
        Return Type
        -----------
        :class:`~winerp.lib.payload.MessagePayload`
        '''
        self.id = msg.id
        self.type = msg.type
        self.route = msg.route
        self.data = msg.data
        self.traceback = msg.traceback
        self.uuid = msg.uuid
        self.destination = msg.destination
        self.pseudo_object = msg.pseudo_object
        return self

    def to_dict(self) -> dict:
        '''
        Returns a ``dict`` representing the message.

        Return Type
        -----------
        :class:`dict`
        '''
        return {
            'id': self.id,
            'type': self.type,
            'route': self.route,
            'data': self.data,
            'traceback': self.traceback,
            'uuid': self.uuid,
            'destination': self.destination,
            'pseudo_object': self.pseudo_object
        }


class responseObject:
    def __init__(self, data):
        self.__name__ = data["__name__"]
        for each_attribute, attribute_value in data["__attr__"].items():
            self.__setattr__(each_attribute, attribute_value)


class winerpObject:
    def __init__(self, object, required_functions = [], required_iterables = []):
        self.object = object
        self.required_functions = required_functions
        self.required_iterables = required_iterables

    def serialize_attributes(self):
        self.serialized = {}
        for each_attribute in self.object.__dir__():
            if each_attribute.startswith("_"):
                continue
            
            try:
                attribute_value = getattr(self.object, each_attribute)
            except:
                continue
            
            if isinstance(attribute_value, (int, float, str, bool, type(None))):
                self.serialized[each_attribute] = attribute_value
            elif callable(attribute_value) and each_attribute in self.required_functions:
                ...
            elif isinstance(attribute_value, (list, tuple)) and each_attribute in self.required_iterables:
                ...
                
        return self.serialized

    def serialize(self):
        return {
            "__name__": self.object.__class__.__name__,
            "__attr__": self.serialize_attributes(),
        }
