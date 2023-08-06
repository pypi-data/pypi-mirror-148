# std
from __future__ import annotations
import logging
import traceback
from typing import Generic, Optional as Opt, TypeVar, Union

# internal
from rustlike.base_exception import RustLikeException

##########
# Option #
##########

# https://doc.rust-lang.org/std/option/#extracting-the-contained-value

# types
SomeType = TypeVar('SomeType')
NoneType = type(None)
OkType = TypeVar('OkType')
ErrType = TypeVar('ErrType', Exception, ValueError, TypeError)


class Option(Generic[SomeType]):

    def __init__(self, value: Union[SomeType, NoneType] = None):
        self._value: Union[SomeType, NoneType] = value

    @classmethod
    def new(cls, value: Opt[SomeType] = None) -> Option[SomeType]:
        """Create the correct variant of Option depending on the input value"""
        if value is None:
            return NONE_OPT
        else:
            return Some(value)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._value)})'

    def __str__(self):
        return f'{self.__class__.__name__}({str(self._value)})'

    def __bool__(self):
        raise NotImplementedError

    # Querying the variant

    def is_some(self) -> bool:
        """Returns True if the Option is Some, otherwise False"""
        return isinstance(self, Some)

    def is_none(self) -> bool:
        """Returns True if the Option contains None, otherwise False"""
        return self._value is None

    # Extracting the contained value

    def expect(self, msg_or_error: Union[str, Exception]) -> SomeType:
        """Return contained value if Some, otherwise raise OptionException with given message

        Optionally provide custom exception to raise.
        """
        if self.is_some():
            return self._value
        else:
            if isinstance(msg_or_error, str):
                raise OptionException(msg_or_error)
            else:
                raise msg_or_error

    def unwrap(self) -> SomeType:
        """Return contained value if Some, otherwise raise generic OptionException"""
        if self.is_some():
            return self._value
        else:
            raise OptionException('Tried to unwrap None variant of Option')

    def unwrap_or(self, default: SomeType) -> SomeType:
        """Return contained value if Some, otherwise return given default value"""
        if self.is_some():
            return self._value
        else:
            return default

    # Transforming contained values

    def ok_or(self, err: ErrType) -> Result[SomeType, ErrType]:
        """Transform Some to Ok and None to Err"""
        if self.is_some():
            return Ok(self._value)
        else:
            return Err(err)


class Some(Option[SomeType]):
    _value: SomeType

    def __init__(self, value: SomeType):
        super().__init__(value)

    def __bool__(self):
        return True


class NoneOpt(Option[SomeType]):
    _value: NoneType

    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return 'Option(None)'

    def __str__(self):
        return 'None'

    def __bool__(self):
        return False


NONE_OPT = NoneOpt()  # NoneOpt singleton


def option(value: Union[SomeType, NoneType] = None) -> Option[SomeType]:
    """Short-hand for Option.new"""
    return Option.new(value)


class OptionException(RustLikeException):
    pass


##########
# Result #
##########

# https://doc.rust-lang.org/std/result/


class Result(Generic[OkType, ErrType]):

    def __init__(self, value: Union[OkType, ErrType]):
        self._value: Union[OkType, ErrType] = value

    @classmethod
    def new(cls, value: Union[OkType, ErrType, Result[OkType, ErrType]]) -> Result[OkType, ErrType]:
        if isinstance(value, Result):
            return value
        elif isinstance(value, Exception):
            return Err(value)
        else:
            return Ok(value)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._value)})'

    def __str__(self):
        return f'{self.__class__.__name__}({str(self._value)})'

    # Querying the variant

    def is_ok(self) -> bool:
        """Return True if Ok, otherwise False"""
        return isinstance(self, Ok)

    def is_err(self) -> bool:
        """Return True if Err, otherwise False"""
        return isinstance(self, Err)

    # Extracting contained values

    def expect(self, msg: Union[str, Exception]) -> OkType:
        """Return contained value if Ok, otherwise raise ResultException with given message

        Optionally provide custom exception to raise.
        """
        if self.is_ok():
            return self._value
        else:
            if isinstance(msg, str):
                raise ResultException(msg, self._value)
            else:
                raise msg

    def unwrap(self) -> OkType:
        """Return contained value if Ok, otherwise raise generic ResultException"""
        if self.is_ok():
            return self._value
        else:
            raise ResultException('Tried to unwrap Err variant of Result')

    def unwrap_or(self, default: OkType) -> OkType:
        """Return contained value if Ok, otherwise return given default value"""
        if self.is_ok():
            return self._value
        else:
            return default

    # Transforming contained values

    def err(self) -> Option[ErrType]:
        """Transforms Result to Option

        Err(e) -> Some(e)
        Ok(x) -> None()
        """
        if self.is_err():
            return option(self._value)
        else:
            return option()

    def ok(self) -> Option[OkType]:
        """Transforms Result to Option

        Ok(x) -> Some(x)
        Err(e) -> None()
        """
        if self.is_ok():
            return option(self._value)
        else:
            return option()


class Ok(Result[OkType, ErrType]):
    _value: OkType

    def __init__(self, value: OkType):
        super().__init__(value)

    def __bool__(self):
        return True


class Err(Result[OkType, ErrType]):
    _value: ErrType

    def __init__(self, value: ErrType):
        super().__init__(value)
        self.traceback = traceback.format_exc()

    def __bool__(self):
        return False

    def __repr__(self):
        return self.traceback


def result(value: Union[OkType, ErrType, Result[OkType, ErrType]]) -> Result[OkType, ErrType]:
    return Result.new(value)


def resultify(
        exception_type: ErrType = Exception,
        logger: Opt[logging.Logger] = None,
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return Ok.new(func(*args, **kwargs))
            except exception_type as error:
                if logger is not None:
                    logger.error(f'{str(error)}\n{repr(error)}\n{traceback.format_exc()}')
                return Err.new(error)
        return wrapper
    return decorator


class ResultException(RustLikeException):
    pass
