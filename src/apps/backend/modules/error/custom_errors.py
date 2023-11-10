from typing import Any


class AppError(Exception):
  def __init__(self, message: str, status_code: int) -> None:
    self.message = message
    self.code = status_code
    super().__init__(self.message)

  def to_str(self) -> str:
    return f"{self.code}: {self.message}"

  def to_dict(self) -> dict[str, Any]:
    error_dict = {
      'message': self.message,
      'code': self.code,
      'args': self.args,
      'with_traceback': self.with_traceback
    }
    return error_dict

class MissingKeyError(Exception):
  def __init__(self, *, missing_key: str, error_code: str) -> None:
    super().__init__(f"{missing_key} is not found")
    self.code = error_code


class ValueTypeMismatchError(Exception):
  def __init__(self, *, actual_value_type: str, error_code: str, expected_value_type: str, key: str):
    super().__init__(
      f"Value mismatch for key: {key}. Expected: {expected_value_type}, Actual: {actual_value_type}"
    )
    self.code = error_code
